# LAC round 2: the six reports checked against Lee's notes (critic, 21 Oct 2026)

Read-only. Nothing in the project was edited, regenerated or committed except this file. The cameras for Steps 16 - 18, 30 - 32,
33 - 34 and 49 are skipped (they are being solved in the player). Numbers are assembly mm, seated, Y up.

## 0. Already in the working tree (not regenerated)

Nothing has been regenerated: the LAC's `steps.json` and `model.glb` are still those of 1b1bc68.

- **`guide.py`:** the four cameras; Step 49's `side='up-right'`; the USB fix from usb_ends.md (all three edits); and the Step 53
  lead line (`F1_LINES`, guide.py:1075 - 1077). No report covers the Step 53 line; it is checked in section 1.
- **`colour-atlas-lac.json` and `docs/research/lac/scripts/lac_atlas.py`:** the buzzer stub swap (buzzer_leads.md section 1).
  `build_model.py` has to run before the swap shows.

## 1. Lee's notes, one by one

| Lee's note | Report | Covered? | Remarks |
|---|---|---|---|
| 1. Breadboard tabs as on the LSM's | breadboard_tabs.md | **Yes**, checked; not applied | I confirmed it is the same mesh: `Breadboard` in lac-guide.glb and in lsm-electronics.glb, 66,284 vertices each, box (-69.29, -5.25, -42.17) .. (-13.21, 4.27, 40.84). The revised lsm.glb has body 66,219 vertices and tabs 100, with the boxes the report gives. Step 1 conflicts with labels.md: see 2.1. |
| 2 - 7. Labels at the screen edges (Steps 3, 5 - 7, 9 - 18, 20, 21, 30 - 34, 36, and the general review) | labels.md | **Yes**, every labelled step | The patch still applies to the current guide.py: `git apply --check` passes. It conflicts with three other reports (2.1 - 2.4). Step 49: `'up-right'` lands on F8 in windows under ~880 px wide, and an iPad in the LMS is 768 px. The report's way out is a player change, which Lee ruled out ("ONLY for this kit"); use `'up-left'` 0.05 instead if narrow frames matter. Step 43, "above the buzzer": the report uses `'up-left'` (above and to the left, off the buzzer's way up). That is a reading of Lee's word, not literally above. |
| Step 13, white through blue and purple | wire_clipping.md | **Yes**, 0 problems at 37 moments | The fix makes the white a low arch and brings the caps in from the front (`FRONT_LOW`). It conflicts with labels.md in text (2.2), and on screen in Step 14 (2.3). |
| Step 14, dark red through blue and purple | wire_clipping.md | **Yes**, 0 problems | See 2.3: the labels proposed for Step 14 sit over the a12 cap's new starting place. |
| Step 32, black through brown (tan) | wire_clipping.md | **Yes**, 0 problems | Together with labels.md, the eye and the label overlap (2.4). |
| Steps 33 - 34, buzzer colours | buzzer_leads.md section 1 | **Yes**, applied in the atlas | I checked the matcher (build_model.py:490 - 527). It scores box geometry only and keeps the first best mapping, so swapping the colours does not change the mapping it picks. The red stub will be at x 673.79 - 675.21, where the red lead leaves (674.5). Still to do: run `build_model`, then `guide.py`, then re-render `parts/Alarm-Buzzer.png` and the card. |
| Step 35, move the ribbon | none | **No** | Nobody proposes a new place. wire_clipping.md ("What is left", item 1) gives only constraints and two untested options. The ribbon lies at x 733 - 754, z 1287 - 1353; the pot leads cross it at z 1328 - 1341. The eyes of Steps 35 - 39 and the beat-1 clipping of Steps 36 - 39 both wait on this. |
| Step 36, through green and black; path bent randomly | wire_clipping.md (a), (c) | **Partly** | (a) clears the jumpers only by moving the LCD's GND and VCC caps from rail k = -2 to k = +2 / +4 (z 1290.00 / 1295.08). That is a departure from the CAD and the published holes, so Lee decides. I listed every cap in the rails, and both new holes are free: (+) red is used at z 1269.67, 1279.85, 1284.90, 1310.36, 1330.62; (-) blue at 1279.84, 1284.92, 1310.35, 1330.65, 1340.86. (c) smooths the lying lanes. Not measured after (c): the beat-1 blend from the 66 mm table line, which was 586 deg of turning in 117 mm half way and is the part that looks crumpled. That beat still passes through the pot leads (0.14 - 0.90 mm), pending Step 35. |
| Step 37, as 36 | same | **Partly** | As Step 36. |
| Step 38, teal through purple and yellow | wire_clipping.md (b) | **Mostly** | The touches with the LCD purple and yellow in the push are gone. Left in beat 1: the purple jumper brushes the teal's cap (0.36 - 0.90 mm, 3 frames), and the teal passes the pot tan. |
| Step 39, as 36 - 38 | wire_clipping.md (b), (c) | **Mostly** | As Step 38, and the blue brushes the teal by 0.27 mm at the end of beat 1. |
| Step 40, USB cable off-centre at both plugs | usb_ends.md | **Yes**, applied | I measured the Mini-B stub's end face from the mesh: x 658.34, centre (y 903.33, z 1354.39), radius 2.25. That is the report's `USB_EXIT`. Taking the breadboard's +Z tabs away (note 1) can only add to the cable's clearance at the board's corner. |
| Step 43, eye above the buzzer | labels.md | Yes (as `'up-left'`) | |
| Step 43, red and black over the jumpers | buzzer_leads.md section 3 | **Partly** | The seated shape is fixed. During the carry beat (0.45 - 0.59 of the move) both leads still sweep through the jumpers, the switch's tan lead and the LCD wires for about 1/3 s, as now. The report says so itself. That sweep is likely the "clipping through" Lee saw, so tell him. |
| Step 43, discontinuity (lee_7) | buzzer_leads.md sections 2 - 3 | **Yes** | The leads now start at the stubs' ends: gap 0 mm, angle 0 deg. The atlas swap also fixes the crossed colours visible in lee_7. |
| Step 49, F8 label up and to the right | labels.md; applied | Yes | See the narrow-window caveat in the labels row above. |
| Step 50, slide into F8's slots, turn up and over, closer view | lcd_slide.md | **Yes**, not applied | Checked against the CAD: F8's slot is x 712.22 - 714.00, at y 889.55 - 895.90 and 943.07 - 949.90; the board is x 712.16 - 713.76. Checked by hand: `LCD_IN` puts the board's end at z 1276.5, 9.0 mm short of F8's inner face at 1267.47. Checked by hand: `LCD_ON_END`, 90 deg about +x, stands the F8 end straight up. Seen from `LCD_IN_DIR`, +z is on the left of the screen, so the F8 end starts on the left and comes down on the right of the header end. That is the "up and over" Lee asked for. The old camera is ([755.5, 919.5, 1375.9], 130.6) and the new one has radius 100. Step 51's camera is unchanged. It needs merging with wire_clipping (2.5). |
| Step 53, red line through F1's slot | none (edit already in guide.py:1076 - 1077) | **Yes**, not regenerated | I measured F4's front tab: it reaches x 727.21 over z 1315.3 - 1329.2. F1 is x 720.83 - 723.83, its slot there z 1315.27 - 1327.97, y 951.46 - 954.46. `FRONT_OUT` = [76.659, 0, 1.081]. The pair's first point moves with F1 (stepgen `hand_lines`: [[tip], [mouth]]), so with F1 out the line runs from x ~797.7 to the tab tip at 727.2 and never passes through F1. The first point lies in F1's slot, as the other three do. Check it in the player after regenerating. |

## 2. Conflicts between the proposals (merge by hand; each is a g.place two reports rewrite)

### 2.1 Step 1 (guide.py:253 - 255): labels.md and breadboard_tabs.md rewrite the same line

Merged:

```python
        labels=[dict(id=BREADBOARD, text='Breadboard', anchor=[663.9, 897.1, 1302.6], **near('near-right'))],   # (beside it, clear of the arrow)
        view_dir=BENCH_DIAG, frame=([674.5, 914.3, 1305.8], 58.4))   # (Step 1's camera and the label's spot as they were before the
                                                                     # breadboard's tabs moved: Lee, 21 Oct 2026)
```

Today's steps.json has Step 1's camera at dir [0.5792, 0.5736, -0.5792], target [674.5, 914.3, 1305.8], radius 58.4, and its anchor
at [663.9, 897.1, 1302.6], so these pins change nothing. Step 2 frames F3 and the hovering board; F3's box (x 641 - 727, z 1207 - 1372)
holds the board's moved box, so its camera should not move either. The camera diff will confirm it.

### 2.2 jumper_run (guide.py:401 - 406): labels.md's new line puts back `paths={ca: [UP, ZERO], cb: [UP, ZERO]}`

That would undo wire_clipping's `paths=ways`. Merged:

```python
    for k, (colour, (ca, la), (cb, lb), key) in enumerate(jumpers):
        done = jumper_done(colour, ca, cb, key)
        ways = JUMPER_WAYS.get(colour, {ca: [UP, ZERO], cb: [UP, ZERO]})
        for c in (ca, cb):
            g.rest_at([c], ways[c][0])
        g.place(wire_caption.format(colour=colour.replace('_', ' '), a=la, b=lb), move=[ca, cb], appear=[ca, cb], paths=ways, lines=False,
                labels=sides([hole_label(la, ca), hole_label(lb, cb)], view_dirs[colour], JUMPER_PLACES.get(colour)),
                wires={f'jumper {colour}': done}, wires_done={f'jumper {colour}': done}, **hole_camera([ca, cb], view_dirs[colour]))
```

`hole_camera` frames `held_over()` (the caps at UP), so the cameras of Steps 9 - 14 and 20 - 21 do not move.

### 2.3 Step 14: labels.md's places cover the a12 cap where it now starts

wire_clipping starts the a12 cap (NAUO30) at `FRONT_LOW` = [14, 5, 0]. From Step 14's camera (dir [0.3691, 0.8191, -0.4391]) +x is to
the left on screen, so the cap starts towards the two `'near-left'` labels that labels.md proposes. In my projection (the player's
`cameraPose` and NEAR rules; text widths estimated):

| window | a12 label over the cap's start | (+) red label over the cap's start |
|---|---|---|
| 2000 px | 11 % | 15 % |
| 1000 px | 26 % | 42 % |

Step 13 is clear. Re-score Step 14's places with labels.md's scorer once the caps' ways are in; `'up-left'` or `'down-left'` for (+) red
is the obvious thing to try.

### 2.4 Step 32: the eye and the hole label overlap once the cap is held 5 mm up (not 18)

Both are `'near-right'` 0.05 in labels.md. The camera is `POT_CAMERA`; the hole spot is [699.2, 897.1, 1330.6] and the eye on NAUO14 is
at [699.5, 899.8, 1331.5] plus the hold.

| window | eye with an 18 mm hold | eye with a 5 mm hold |
|---|---|---|
| 2000 x 1016 | y 398 - 476, clear of the label (y 541 - 581) | y 483 - 561: **overlaps** |
| 1000 x 634 | clear | **overlaps** |
| 700 x 634 | clear | **overlaps** |

With the eye `'up-right'` 0.05 instead, the eye box is at y 344 - 422 at 2000 px and y 237 - 276 at 1000 px, and the leaders do not
cross. Merged loop (guide.py:622 - 628):

```python
POT_EYE = {'black': ('up-right', 0.05)}                             # (Step 32: the cap held only 5 mm up, its eye clear of the hole's label)
for colour, cap, label, exit_, _ in POT_LEADS:
    done = pot_plugged(colour, cap, exit_, F1_DOWN, POT_WAY[colour], above=POT_ABOVE.get(colour, 10.0))
    g.place(f"Connect the potentiometer's {colour} wire to {label}.", move=[cap], path=[POT_HOLD.get(colour, UP), ZERO], lines=False,
            labels=[dict(hole_label(label, cap), **near('near-right'))], eye=[dict(id=cap, **near(*POT_EYE.get(colour, ('near-right', 0.05))))],
            wires={f'pot {colour}': done}, wires_done={f'pot {colour}': done}, **POT_CAMERA)
```

I worked this out from the projection only; run it through labels.md's scorer, which checks the caption and the leads.

### 2.5 Step 50: wire_clipping (b) changes the shape the LCD's new motion starts from

**The problem.** From Step 37 on, (b) leaves each LCD wire on `LCD_PLAIN`, a route with no `tail_from`.

- lcd_slide.md checked its first beat from `LCD_LYING_LEAD` to `on_end`. Both routes have `tail_from`, so the player pairs head with
  head and tail with tail (player.js:178 - 186).
- From `LCD_PLAIN` the player instead pairs the points by distance from the first end (player.js:187). That gives a different
  in-between shape, which nobody has checked.

**The fix.** Give Step 50 an unseen swap as it opens (the same points, measured by wire_clipping as 0.5 mm):

```python
        wires={f'lcd {c}': LCD_LYING_LEAD[c] for c, *_ in LCD_WIRES},
```

Add it to lcd_slide.md's Step 50 call, with labels.md's `eye=[dict(id=LCD, **near('up-left'))]` in place of `eye=[LCD]`. Choose that
eye's place again for the new motion: the lying LCD's left end rises through the region above and to the left of it.

**Still to re-check.** (a) and (c) change `LCD_HEAD` and the lying shapes, and every `LCD_LEADS` shape is built on them. Run motioncheck
on Steps 50c and 51c again after the merge.

**A tool limit.** lcd_slide.md's optional Step 51 `via()` poses are turns about a point 1.4 m from the origin. motioncheck spaces such
poses by their matrix translation: about 89 mm per 3.5 deg here, against the player's few mm (wire_clipping.md, "Notes on the checking
tools"). Its "0 problems" for Step 51c therefore sampled other moments than the player plays. Run it again with the player's spacing,
or leave Step 51's path as it is. Lee did not ask for a change to Step 51.

### 2.6 Other same-call edits, merge by hand

- **LCD loop** (guide.py:892 - 909): labels.md writes the labels and eye; wire_clipping (b) writes `wires=prev`. The hole labels of
  Steps 36 and 37 move 10.16 and 15.23 mm in z with (a), so re-score them.
- **Buzzer loop** (guide.py:746 - 757): touched by labels.md only.
- **Step 43** (guide.py:984 - 987): labels.md writes the eye; buzzer_leads.md writes `wires_done`.

### 2.7 Checked compatible

- **Buzzer leads (buzzer_leads.md section 3) against the moved GND/VCC wires (wire_clipping (a)).** I smoothed `BUZZER_SEAT_WAY['black']`
  with `W.smooth`, rebuilt the rerouted LCD purple and yellow from steps.json's routes 94 and 95 with `LCD_RISE`, and measured at rest:

  | pair | surface gap after both fixes | gap today |
  |---|---|---|
  | buzzer black to LCD purple | 4.94 mm, at [694.4, 926.7, 1291.8] | 9.62 mm |
  | buzzer black to LCD yellow | 1.47 mm, at z 1312.8 | 1.47 mm (past the rerouted run) |

  The motion of the two together is not checked.
- **USB against the breadboard.** The fix kept its clearances, and removing the +Z tabs only adds room.
- **Breadboard tabs against the new LCD motion.** `LCD_IN` and `LCD_OUT` lie further out along +x and +z than `LCD_ANGLED`, which the
  breadboard report already cleared by 8.28 mm.

## 3. Smaller points

- **`materials.json` has no `"adjust_mm"` key yet.** wire_clipping (a) writes it as if it existed (`{ ..., "NAUO82": ...}`). Add the
  key, and say why under `_notes.adjusted` (CLAUDE.md's convention).
- **I spot-checked wire_clipping's cause for Steps 36 - 37.** From route 22 and route 21 in steps.json, the green jumper passes 1.21 mm
  from the GND hole's axis at [700.4, 925.3, 1279.6]. The black jumper passes 0.25 mm from the VCC hole's axis, at y 923.2. The report
  says 1.24 and 0.55 mm; the cause holds.
- **lcd_slide.md rewrites Step 50's caption** ("slots"); Step 51 still says "notch". The LAC has no `step-text.json`, so no outside edit
  is lost.
- **One `build_model.py` run covers both model changes** (the atlas and the breadboard). The order is:
  1. Save a copy of steps.json.
  2. Run `build_model`.
  3. Run `guide.py`.
  4. Diff every view's camera against the saved copy.
  5. Re-render `parts.html`: the Breadboard and Alarm Buzzer pictures change.
  6. Take `_dev.card()` again: the buzzer, the A end and the tabs show in it.
  7. Run motioncheck on 13c, 14c, 32c, 36c - 40c, 43c - 56c with `--moments 37` (the scratch copy); 19 moments miss beat edges.
  8. Run `_runthrough()`.

  Swap was 9.6 of 11.3 GB used when I wrote this: run one heavy job at a time.
- **The numbers I did not re-derive.** These rest on the agents' own harnesses: the 1.48 mm cut through F8's front, the 0.33 / 0.41 mm
  gaps of the buzzer leads, and the leader lengths in labels.md.

## 4. Still uncovered after all six reports

1. **Step 35's new ribbon place**, and with it the beat-1 clipping in Steps 36 - 39 and the eye places for Steps 35 - 39.
2. **Step 43's carry beat:** the leads still sweep through the jumpers and the switch's tan lead.
3. **Steps 36 - 37:** the jumper clip is cleared only by moving the GND and VCC holes, which is Lee's call. The crumpled beat-1 blend has
   not been measured after the fix.
4. **Step 49 in windows under 880 px:** the label sits on F8 (Lee's call; no player change, as he asked).

## How I checked

- **Spot measurements.** I read meshes one at a time with tools/glbio.py: lac-guide.glb NAUO122, NAUO44, NAUO94, NAUO1, NAUO62, NAUO10,
  NAUO2, and f4.glb with its `extra_parts` pose. I also read lsm-electronics.glb and lsm.glb accessor counts and boxes.
- **Data files.** I read steps.json (views, cameras, routes) and wire-paths.json (caps, poses).
- **Code.** I read player.js `layoutCallouts` (:371 - 415), the wire pairing in player.js (:162 - 186), core.js `cameraPose`,
  stepgen `hand_lines` / `_hand_lines`, and build_model `colour_from_atlas`.
- **Projections.** I projected labels with the player's own camera and NEAR rules.
- **Patch.** `git apply --check` on labels.patch.
- **Memory.** Peak Python well under 300 MB. Scratch scripts are in
  `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad/critic/`.
