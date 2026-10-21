# LSM, Lee's notes of 20 Oct 2026: independent review, group A

Group A: Step 3 (c16 label), Step 6 (GND (-) / VCC (+) labels and the capacitor picture), the white wire drawn yellow, Step 32c's
close-up (the wire ends). Reviewed from the working tree against the round before (`scratchpad/steps_before_r4.json`), with no
browser and nothing regenerated. Where a window size matters, I re-ran the player's own label layout and close-up placement in
Python for that view (`scratchpad/revA/sim6.py`, `sim3.py`, `sim3b.py`). The model's corners came from `assembly-report.json`, the
text widths from Arial Bold. The re-run agrees with the evidence: Step 6's close-up comes out at 100% at 1280 x 800, 85% at
1000 x 680 and 72% at 768 x 560. Its label boxes match `thumbs/n_Step6.png` to within about 3 px.

## Verdicts

| Note | Verdict |
|---|---|
| Step 3: c16 no longer covers a red lead line, moved right | done (but see R1, R2) |
| Step 6: GND (-) to the right of its leg, + becomes VCC (+), picture clear of labels | done (small points R3, R4) |
| The white wire yellow everywhere | done (small point R5) |
| Step 32c: the wire ends (sockets) shown in the close-up | done |

### Step 3, c16: done
- The fix is in `guide.py:294`. The anchor is hole c16 + [-1.06, 0, 1.06] mm, which is exactly the camera's screen-right
  direction for `view_dir=[-0.5792, 0.5736, -0.5792]` (right = (-0.707, 0, 0.707)), so the leader moved right as Lee asked. It has
  `ring=False`. In steps.json (Step 3): c16 moved from [629.58, 871.92, 1206.01] to [628.52, 871.92, 1207.07] with `"ring": false`.
- `thumbs/q_Step3_c16.png` against `s3_c16.png`: the ring and the leader's end no longer sit on the end of the red line in c16.
  There is now a visible gap.
- Measured on screen (re-run), from the c16 leader's end to the red line: 8.5 px centre to centre (5.1 px edge to edge) at
  1280 x 800, 7.1 px (3.7) at 1000 x 680, 5.7 px (2.8) at 768 x 560. The leader crosses no other red line (it stays at least 7.1 px
  from every red line at 1000 px). So the end of the line is no longer covered, but the gap is only a few pixels.

### Step 6: done
- `guide.py:313`: `GND (-)` with `side='right'`, `+` renamed `VCC (+)`. steps.json Step 6 labels: GND (-) on the j3 leg (z 1172.97,
  the striped leg), VCC (+) on the j2 leg.
- `thumbs/n_Step6.png` against `s6_now.png`. Before, both labels were on the left and the GND leader ran across the + leg. Now
  VCC (+) is on the left with its leader to the left leg, GND (-) is on the right with its leader to the right (striped) leg, and
  the two leaders do not cross. Re-run at 1280 x 800: VCC (+) box x 398 - 520, leg at (601, 483); GND (-) box x 768 - 886, leg at
  (638, 501). The rings are 41 px apart (ring radius 10 px).
- Capacitor picture against the labels, eye and leaders (re-run, with the leader actually drawn from the end of the underline, and
  the box at its real height with a wrapped caption):

  | Window | Size | Box (x, y) | Over a label, the eye or a leader? | Picture's own leader over a label? |
  |---|---|---|---|---|
  | 1280 x 800 | 100% | 12 - 358, 297 - 696 | no | no |
  | 1000 x 680 | 85% | 12 - 262, 282 - ~594 | no | no |
  | 768 x 560 | 72% | 12 - 187, 245 - ~474 | no | no |

  Also clear at 1440 x 900, 1180 x 820, 1100 x 700, 900 x 620 and 820 x 1180 (portrait). See R4 for the bottom edge.
- The `inset` alt text names VCC (+). The caption is unchanged: "The grey stripe marks the GND (-) leg".

### The yellow wire: done
- `materials.json`: `wire_white #f2f2f2` is now `wire_yellow #ffdc00`, with a decided note. steps.json `"wire white"` (line 133) has
  colour `#ffdc00`. No view carries its own wire colour, and `#f2f2f2` appears nowhere in steps.json. So every view that draws the
  wire (Start, Steps 10 - 40, Completed View) draws it yellow. The routes are unchanged, so the shapes are the same as checked before.
- Captions: Steps 11/11c, 14, 15/15c now say "yellow" (`guide.py:443, 459, 474` via `SHOWN`). A search of every caption in steps.json
  finds no "white". The hover names of J_WHITE_M and J_WHITE_F are now "Yellow Breadboard Wire" (`guide.py:52`; steps.json lines
  19 - 20).
- The parts list picture of the Breadboard Wire (M-F) is drawn with a purple wire (`guide.py:367-368`), so it needed no change.
  Nothing else in the model is yellowish (none of the 21 colours in model.report.json is).
- Yellow and the light grey (#cad1ee) now differ clearly in hue. Their brightness is close (luminance ratio 1.12), so a greyscale
  print would not separate them, but on screen they are plainly different.
- The text_key of Steps 11, 14 and 15 changed with the wording. The LSM has no step-text.json and share/ has no LSM sheet, so no
  outside edit is lost.

### Step 32c close-up: done
- `guide.py:777`: `ghost={MATRIX: 0.12, D4: 0.25}`; the three sockets (J_*_F) are no longer faint. steps.json Step 32c `inset.ghost`
  went from five parts to these two.
- `thumbs/inset32_r4.png` against Lee's `lee_images_2026-10-20/1.webp`. The three black sockets now show at the ends of the grey,
  purple and yellow wires, below their S-bends. The S-bends in the slot and the engraved "D10" are still fully visible.
- The sockets' boxes (assembly-report.json) do not reach D10 (socket z ≤ 1191.26, D10 z ≥ 1202.97). Drawing them solid therefore
  shows no part passing into another.
- Step 32c has no labels or eyes, so the player change (smaller close-ups) does not apply to it. Its placement is as before.

## Regressions and points next to these notes

**R1 (medium): Step 3, without its ring the c16 leader now points nearer c17 and b16 than c16.** On screen the end of the leader
is closer to the neighbouring holes than to c16: 5.3 px to c17, 5.8 px to b16 and 7.0 px to c16 at 1000 x 680 (6.4 / 7.0 / 8.4 px at
1280, 4.2 / 4.6 / 5.6 px at 768; `sim3b.py`). In 3D the end is 1.5 mm from c16 and 1.8 mm from c17, but the angled view brings the
neighbours closer on screen. The crop `scratchpad/revA/c16_zoom.png` (from q_Step3_full.png) shows the end of the leader against
the outline of the next hole along the row. Only the red line ending in c16 shows which hole is meant. A student who reads the label
on its own could put the Nano Board one column off. The ring-less label is for "an exact spot, such as a pin" (player.js:350), and
this spot is now no hole at all.

**R2 (medium): the overlap Lee pointed out at c16 is still at g2 in the same step, and at five more hole labels.** The rulebook
entry added this round (`docs/cadasio-patterns.md:191`) says a label's leader *never* lies over a red lead line, and where both end on
one hole the leader stops beside the hole without its ring. Only c16 was changed. The label anchor sits on the end of a red lead line,
ring and all, at:
- Step 3: g2. The anchor is 0.05 mm from the line's end; on screen 0.2 px at 1000 x 680, with a 9.7 px ring over the line. See
  `scratchpad/revA/g2_zoom.png`: the ring is centred on the end of the leftmost red line. This is in the picture Lee just looked at.
- Step 5: h3 and h16 (0.05 mm, 0.2 - 0.3 px).
- Step 7: j2 and j3. The lines run down into the board and pass through the label points at the board's surface (1.3 - 1.7 px).
  The j3 leader also crosses the other red line (0.0 px).
- Step 9: a11 and a19 (0.02 - 0.04 mm, 0.1 px).

(guide.py:294, 302, 319, 326; distances from `sim3.py`.) Lee will probably see g2 the next time he opens Step 3.

**R3 (low): Step 6, Lee's picture beside the model is a mirror image of it.** In capacitor-card.webp the stripe and GND are on the
left and VCC on the right. In the 3D view (camera unchanged) the stripe and GND (-) are on the right and VCC (+) on the left. With
GND (-) moved to the right, the picture now sits on the left beside VCC (+). The reader sees the picture's GND at one side of the
screen and the model's GND (-) at the other. Lee called the labels "somewhat confusing"; this mirroring may keep some of that. It
can't be fixed without changing Step 6's camera, which Lee would have to ask for.

**R4 (low): Step 6 in a narrow window, the smaller picture's caption wraps and the box reaches the step bar.** player.js:430/459
always allows a one-line caption (`capH = 24`). "The grey stripe marks the GND (-) leg" is about 248 px wide at 14 px bold. That
fits at full size from 1100 px up, but not in the 230 px picture at 1000 x 680 (85%) or the 155 px one at 768 x 560 (72%). There it
takes two lines, about 16 px more than the placement allowed. The box was placed 12 px above the bottom of the 3D area, so its real
bottom is at about 594 of 594 px (1000 x 680) and 474 of 474 px (768 x 560), touching the step bar. #inset has z-index 2 and #bar
none, so it would sit over the bar rather than under it. At 1000 px the second line is the word "leg" alone. It covers no label or
leader.

**R5 (low): the wire itself is named without its colour on hover.** The three wire tubes keep `name='Breadboard Wire (M-F)'`
(`guide.py:203`; steps.json `"wire white".name`), and player.js:985 names a hovered tube from that. Hovering the yellow wire's body,
which is most of what shows, says "Breadboard Wire (M-F)". Hovering its pin or socket says "Yellow Breadboard Wire". This was the
same before for all three wires. The new rulebook entry (`cadasio-patterns.md:188`), though, says the colour is changed "in its
name on hover too".

**R6 (question, cannot tell): the captions now call the wire yellow.** The published guide, and the photographs it was taken from,
show this jumper as white. If the kit's real ribbon has a white wire, a student holding it will read "Push the yellow wire's pin
into i2". Lee's "make the white wire Yellow instead, across all of the relevant steps" reads as including the wording, so this is
probably intended. Worth one line to Lee confirming that the kit's wire colours do not matter here (or that the kit ships yellow).

Not regressions, checked:
- Cameras: no view's `camera` changed (diff of every view's keys: only labels, captions/text_key, guides and the 32c inset changed).
- The player change can only affect hover views that have both a close-up and labels or eyes: the LSM's Steps 6 and 14 in every kit's
  steps files. No MRA, RCC, LAC or PMG view has both, so no other kit's close-up can shrink.
- Step 32c's alt text now says the wires "go down through its slot" while the caption says they "lie in the slot". This is
  screen-reader text only.
- The review preview (`share/Test guides preview`, Lee's 8799) still holds the 19 Oct steps (no "Yellow Breadboard" in it): Lee
  will see none of this until it is published there again.
