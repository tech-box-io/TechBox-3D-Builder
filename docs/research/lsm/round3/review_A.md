# LSM Full Build, round 3: independent review, group A (Steps 6, 7, 10 - 12, 14, the LED under the header)

Reviewer: independent agent, 19 Oct 2026. I ran nothing heavy and used no browser. I read `steps.json` (now) against the round-2
file (`scratchpad/steps_r3_before.json`), plus the guide and tool diffs, the player code and the renders in
`LSM Build Instructions/thumbs/`. I also made crops of the renders (in the session scratchpad, not in the repository).
Step numbers are the same in both files for this group.

**Timing of the renders matters.** `player/js/player.js` was last changed at 22:24:33. The `v_*`, `sheet_*` (22:15) and `f_*` (22:22)
renders were all made before that change. Only `p_Step6.png` and `p_Step14.png` (22:25:20/21, after a page reload) show the
final rule for placing close-ups. `ledcorner.png` (22:32) and `parts/LED-Matrix.png` (22:31) show the final model.

## Verdicts

| Note | Verdict |
|---|---|
| Step 6: Lee's Capacitor picture as the close-up | done |
| Step 7: lead lines at [652.5, 863.6, 1170.6] and [652.5, 863.6, 1173.1] | done |
| Step 11: white and grey wires ribbon-like, not fully separated | partial |
| Steps 11 and 12: camera like image 2 | done |
| Step 14: BTE / Better Than Expected / Only ONE Pin / WS2812B-64 removed, the rest moved, white label kept | done |
| Step 14: leaders no longer overlapping or confusing | done at the one size checked; other sizes not verified |
| The LED under the header to match the others | partial |

### Step 6: done
- `steps.json` view "Step 6" has `inset.image = "capacitor-card.webp"` and `image_aspect 1.0942`. The file is byte for byte
  Lee's `1.webp` (sha1 880e8252...), 1199 x 1312 px, and it is staged in git.
- `publish.py needed_files()` and `bundle.py` now carry the picture along, and `.webp` is a type `check_site.py` allows.
- `p_Step6.png`: the picture shows in the box at the right, with the caption "The grey strip marks the GND (-) leg". The box covers
  neither the eye nor the GND (-) and + labels.
- Small points Lee may notice (low):
  - The picture is a mirror image of the 3D view. In the picture the strip and the GND leg are on the left; in the 3D view the
    stripe and the "GND (-)" leg are on the right.
  - The close-up caption says "strip", where the step's caption and Step 7's caution say "stripe".
  - Already so in round 2 (not changed): the GND (-) leader runs just under the "+" ring on the other leg (`p_Step6.png`,
    about x 540, y 440-450).

### Step 7: done
- Both lead lines are exactly Lee's points: `guides = [{tip: [652.5, 863.6, 1170.6], mouth: same}, {tip: [652.5, 863.6, 1173.1], mouth: same}]`.
  In round 2 they were [652.6, 871.9, 1170.4/1173.0], at the tops of the holes.
- In the hover view the tips are drawn 29 mm up, at [652.5, 892.6, ...], which is the legs' ends. In a 3x crop of `v_Step7.png` the
  red lines start right at the leg ends and run straight down into j2 and j3. The labels, eye and camera are unchanged.

### Steps 10 - 12: ribbon partial, camera done
**Camera (done).** Steps 11, 11c, 12 and 12c all use `dir [-0.3282, 0.6298, -0.704]`, `target [644.3, 895.7, 1180.6]`, `r 38.3`, the
camera solved from image 2. `cmp-2.png` (Lee's screenshot beside the render) matches in viewpoint and framing. No other camera in
this group changed: Steps 6, 7, 10, 13 and 14 are the same as in round 2 (`review_camdiff.txt`).

**Ribbon (partial).** I measured how close each point of the grey wire comes to the white wire, centre line to centre line:

| View | Round 2 | Now |
|---|---|---|
| Step 11 (opening) | 6 mm of 53 within 3.5 mm; 5 - 9 mm apart along most of it | 63 of 72 mm within 3.5 mm: a ribbon all the way (2.5 mm pitch) |
| Step 11c and Step 12 (opening) | 0 mm within 3.5 mm | 13 of 72 mm within 3.5 mm; 23 - 27 mm apart over the first half (from the grey pin) |
| Step 12c, 13, 13c | partly together | a ribbon all the way |

- So the opening of Step 11 and every view from 12c on now meet the note.
- Step 11c and the opening of Step 12 do not. With the white pin in and the grey pin still held 30 mm up, the grey wire takes the
  high `HOVER_MIDS` path. That path joins the white's low path only over its last two points (`guide.py:401`, `_hi` against `_lo`).
- In `v_Step11c.png` the grey wire arches from its held-up pin on the left of the picture over to the sockets, while the white one
  runs low and diagonal across the breadboard. They read as two separate wires for half their length, the "fully separated"
  look Lee objected to, in the very step he named.
- A fix: give the held-up grey wire a path that runs down beside the white ribbon and leaves it only near its own pin.

### Step 14: done (text); done at one size (leaders)
**Text.** In `decals.json` the silkscreen keeps only "24 bit color" at [31.9, 26.0] and "64 RGB LEDs" at [31.9, 30.5], centred on
the board. WS2812B-64, Better Than Expected, the BTE block (its fill too) and Only ONE Pin are gone. The "label V- IN V+" entry is
unchanged (origin [619.96, 895.563, 1193.5], same items: `git diff` shows only the back print lines). `p_Step14.png` and
`f_Step14.png` agree.

**Leaders.**
- The eye is gone (`eye: []`). The three labels are anchored at different places along their pins: V- at z 1183.4 by the header,
  IN at 1186.2, V+ at 1189.4 at the tip (`guide.py:435-439`).
- In `p_Step14.png` (1152 x 720, final player) V-, IN and V+ are stacked top to bottom, their leaders fan out to left pin / middle
  pin / right pin without crossing, and the close-up box sits below them at the right.
- Not verified at any other window size. `f_Step14.png` (1440 wide) and `v_Step14.png` (768 wide) were made before the player
  change. In both, the close-up's leader runs level through the V+ pin's ring and past the IN pin to the V- pin's tip: with
  the V+ leader beside it, V+ appears to point at two pins (3x crops).
- My reading of `player.js:432-460` with the 768 x 428 geometry: the box now drops to (521, 217), just under the labels. Its
  leader from there to the target [612.5, 894.5, 1191.0] passes about 8 px under the V+ ring. That would still be confusing on a
  narrow embed (iPad portrait).
- The root cause is the close-up's target. It sits just past the V- pin's tip, next to the V+ ring, so the step shows four rings
  on three pins. Putting it on the header or on the white label would keep its ring and leader away from the pin labels.

### LED under the header: partial
- `materials.json:45` adds a region (a box 3.7 mm square, no `"cut"`) coloured `#a6a9aa` on the corner LED.
- The colour matches: the disc in `ledcorner.png` is (192, 195, 196), the same pixel value as its neighbours.
- But the LED now has an outline the other 63 lack: an inner square frame with four diagonal ticks in its corners. This is the
  square region's edge running across the white body round the circular window.
- It shows in the parts-list picture (`parts/LED-Matrix.png`, top-left LED; the HEAD copy had a white disc and no frame) and in
  `ledcorner.png`.
- At the guide's own zoom (`f_Step31.png`, the LED nearest the wires) it is not noticeable. In the Parts List's large view it is.
- A fix: a round region, or `"cut": true` with a box no larger than the window.

## Regressions and risks next to these steps

1. **Step 11c and the opening of Step 12, wires apart** (medium). See above. This is the unmet half of Lee's note.
2. **Steps 11c - 17, the ribbon now lies over the 12 kΩ resistor and kinks at the pins** (low).
   - The new low ribbon (`_lo`, about y 885 - 905) runs along columns g/h over rows 2 - 19. It crosses and partly hides the 12 kΩ
     resistor (h3 - h16), which stood clear in Lee's own image 2 (crop of `f_Step12c.png`).
   - Each wire also bends about 90 degrees with a bend radius of about 1.4 mm right on top of the pin's housing (Step 12c route:
     white 1.45 mm at [649.9, 883.6, 1170.4]; wire radius 0.62). It reads as a sharp kink.
   - No wire passes into a part or another wire: my check at rest and `review_wire.txt` both find 0.
3. **Step 14, close-up leader at other window sizes** (low; not verified). See above. Re-render Step 14 with the final player at
   768 and 1440 wide before showing Lee.
4. **Player: the extra placement tries do not re-check the caption box** (low, possible).
   - `player.js:456` adds tries at `[12, sy]` and `[W - boxW - 12, sy]` for the top and bottom sides. `sy` came from `placeAt()`
     for a different x, so the try at the left edge is not tested against the instructions box (top left).
   - At some window sizes a close-up (Step 6 or 14, or a single-view close-up in another kit) could land on the caption.
5. **Steps 11 - 12, sockets close to the top edge** (low). In `f_Step12c.png` the held-up sockets' tops are about 20 px from the
   top (2.5 %), against about 6 % in Lee's image 2: the new upright-matrix socket pose holds them higher.
6. Checked with no problem found:
   - Steps 1 - 10, 7c and 13 views: no change other than those named (key diff against round 2).
   - The Start view: wire flags changed, points the same.
   - Wire against wire at rest in Steps 11 - 17: no pair closer than their radii added.
