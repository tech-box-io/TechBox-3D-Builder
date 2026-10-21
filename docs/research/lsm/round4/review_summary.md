# LSM, Lee's notes of 20 Oct 2026: combined review summary

Sources: `review_A.md` (Steps 3 and 6, the yellow wire, Step 32c), `review_B.md` (the new D3, Step 28, D8), the skeptics' checks of
the problems those two raised, and a completeness check against Lee's notes word for word (`../lee_notes_2026-10-20.md`). Nothing was
regenerated and no browser was used. The evidence is the working tree against the last commit (05ae94b) and
`scratchpad/steps_before_r4.json`, the author's pictures in `LSM Build Instructions/thumbs/`, and re-runs of the player's layout in
Python.

Changes found by comparing every view key by key: 82 views before and after, the same names, and no camera changed in any of them.
The views that changed are Step 3 (labels), Step 6 (labels), Steps 11, 11c, 14, 15 and 15c (caption and text_key), Step 27 (label),
Steps 28 and 29 (lead lines), Step 32c (close-up), Step 38 (lead lines and label) and Step 39 (lead line). No other view changed.

## Per note: final status

| # | Lee's note | Status |
|---|---|---|
| 1 | Step 3: c16 label covers a red lead line, move it right | Done |
| 2 | Step 6: GND (-) to the right of its lead; + becomes VCC (+) | Done (one new visible side effect, C1) |
| 3 | The white wire yellow in every relevant step | Done (the tube's hover name has no colour, C2) |
| 4 | Step 28: add four lead lines | Done (six lines in all) |
| 5 | D3 replaced by LSM_D3.STEP | Done (the change is described wrongly in the evidence; two changes too small to see, C4) |
| 6 | Step 32: the breadboard wire ends missing in the close-up | Done |
| 7 | Step 38: D8 too low; its top just under the D11 latch's bottom face | Done (README question 17 on D8's thickness) |

1. **Step 3, c16.**
   - `guide.py:294` anchors c16 at the hole + [-1.06, 0, 1.06] mm. That is exactly screen-right for Step 3's view_dir, and the label
     has `ring=False`. In steps.json the anchor went from [629.58, 871.92, 1206.01] to [628.52, 871.92, 1207.07].
   - In `q_Step3_c16.png`, compared with `s3_c16.png`, the leader ends just right of the end of the red line instead of on it.
     Clearance edge to edge is 5.1 px at 1280, 3.7 px at 1000 and 2.8 px at 768. The leader crosses no other red line.
   - The skeptic refuted A's R1 (that the label now reads as c17 or b16). At full resolution the leader's tip touches c16's corner.
     The red line ending in c16 is always shown with the label (Step 3 only).

2. **Step 6.**
   - `guide.py:313`: GND (-) has `side='right'`, and + is now VCC (+). In `n_Step6.png`, VCC (+) is on the left with its leader to
     the left leg, and GND (-) is on the right with its leader to the striped right leg. The leaders no longer cross. In `s6_now.png`
     both labels were on the left and the GND leader crossed the + leg.
   - The capacitor picture is clear of every label, eye and leader at 1280, 1000 (85% size) and 768 (72%), and at five more sizes.
     The alt text names VCC (+).
   - The side effects (the picture now on the left, its leader across the can, the picture mirrored) are under C1.

3. **The yellow wire.**
   - `materials.json`: `wire_white #f2f2f2` is now `wire_yellow #ffdc00` (the MRA's house yellow), with a decided note.
     steps.json "wire white" has colour #ffdc00. No view sets its own colour, and #f2f2f2 appears nowhere. The routes are unchanged.
   - Captions: Steps 11/11c, 14 and 15/15c now say yellow, and no caption says white.
   - The caps' hover names (J_WHITE_M/F) are now "Yellow Breadboard Wire". The caps themselves are black and grey in the model
     ("Wire Cap", "Wire Cap V2" in model.report.json), so nothing white on them was missed.
   - The parts-list picture uses a purple wire. `nsheet_0/1.png` show the wire yellow in Steps 10c, 12c, 15, 22, 26c, 27 and 32c.

4. **Step 28.** steps.json Step 28 has six lines: Lee's two of 19 Oct and his four of 20 Oct.
   - The D1 points are on D1's tab ends (0.08 and 0.12 mm).
   - The D2 point is made a pair from D5's face, like the 19 Oct D2 line, and ends on D2's tab end.
   - Lee picked the two D3 points on the old D3's tab ends (x 682.55). The new tabs reach x 685.64, so the points are now 3 mm inside
     the tabs. Lead lines are depth-tested (core.js:289), so each line is seen to end at the new tab end, which is still tab to slot.
   - Every line starts in a D5 slot. `n_Step28.png` shows the six. Six lines is more than the rulebook's 1/2/4, but Lee's 14 Oct
     decision covers it, and README question 14 is answered.

5. **The new D3.**
   - `assemble.py` takes D3 from `lsm-d3.glb` LSM_D3 at the old instance's placement. `lsm-d3.glb` is git-ignored like the other
     source GLBs. `cad-sources.sha256` has the STEP's checksum, which matches the file.
   - Its inner face is still at z 1156.68 (D6, D7 and D8 butt against it). It is 3.0 mm thick and 0.07 to 0.09 mm off centre in
     D4's and D5's slots.
   - The engraving pocket is in the same place. model.report.json shows LSM_D3 as ink + wood, roughened. `parts/D3.png` is the new
     part. The parts.json, steps.json and card stamps are all 20146e2708d1 (the sha256 of model.glb).
   - Step 27's swing is unchanged: same path, same hinge, D3 into D4 at most 1.50 mm as before. Step 27's D3 label moved 4.2 mm along
     the face (auto-placed). Step 29's D9 lines moved 0.1 to 0.2 mm. Both are too small to notice.
   - **Correction for the reply to Lee.** The evidence file says the end tabs are "0.46 mm longer" and the slots "a little wider".
     Measured on `scratchpad/d3_compare.png` at 20 px per mm:
     - Only the corner hooks grew 0.46 mm.
     - The two middle tabs at each end grew about 3.1 mm (old ends 62 and 61 px short of the new ones). They now stand out of D4 by
       4.09 mm (about 1.0 before) and out of D5 by 3.13 mm (0.04 before), as D2's do (3.83 and 3.38 mm).
     - The slots are narrower: the D9 slots 3.18 to 3.0 mm, and the D1 slot 12.70 x 3.18 to 12.19 x 3.0 mm.
     - Lee will see D3's tabs standing out of the end walls from Step 28c to the end. It is his part (exactly D2's outline), but do
       not describe it as 0.46 mm. The README and assemble.py ("longer end tabs ... slots reshaped") are accurate.

6. **Step 32c close-up.**
   - `guide.py:777`: the ghost is now {MATRIX: 0.12, D4: 0.25}, so the three J_*_F sockets are solid.
   - `inset32_r4.png`, compared with Lee's `lee_images_2026-10-20/1.webp`: three black sockets now end the grey, purple and yellow
     wires below their S-bends. The S-bends and the engraved "D10" still show.
   - The sockets' boxes (z up to 1191.26) do not reach D10 (z from 1202.97).
   - Only Step 32c has this close-up. It has no labels, so the player's new close-up shrinking does not apply to it.

7. **D8.**
   - `assemble.py` raises D8 2.09 mm to y 929.19 to 932.36. The D11 latches' bottom face is at 932.38 (D11 top 935.76), so D8's top
     is 0.02 mm under the latch.
   - D8's bottom is 0.19 mm into the ledges, wholly under D8 and out of sight. D8 is 3.17 mm thick in the CAD, and the posts leave
     3.0 mm: README question 17.
   - Every view after Step 38 has D8 seated. The Step 38 lines and label were regenerated 2.1 mm higher. Their z moved ±0.5 mm, so the
     four are no longer at the same z; about 2 px, not noticeable.
   - Step 39's stem line moved up 1 mm. `d8_corner_zoom.png`, `n_Step38c.png` and the card show the latch heads resting on D8.

## Confirmed problems, with fix hints

**C1 (low, visible; new this round, not raised by either reviewer). Step 6: the capacitor picture's leader now crosses the capacitor's can.**
- Because GND (-) took the right side, the player placed the picture on the left at every window size (A's re-run at 1280: x 12-358).
- The STRIPE target is on the right of the can as seen, so the picture's leader now runs from the left across the black body to the
  stripe. In `n_Step6.png` (768 px wide) the line runs from (213, 178) to the ring at (403, 150). About 55 px of it lies over the
  black can (x of about 345 to 400).
- Before (`s6_now.png`) the picture was on the right and its leader came straight to the stripe, clear of the can.
- The picture is also a mirror of the model: in Lee's photo the stripe and GND are on the left; in the model, GND (-) is on the
  right. This was noted in round 3 (item 18) and is not a regression.

Fix options, Lee's call:
- (a) Leave it.
- (b) Let a close-up ask for a side (`inset=dict(..., side='right')`, which the player does not have yet) and place it on the right,
  below GND (-), where it fits at 1280. At 1000 px the player may still need the left side.
- (c) Turn Step 6's view so that the stripe faces left as in his photo. The photo, the labels and the leader would then agree, but
  that is a camera change, which needs Lee's word.

**C2 (low). The yellow wire's tube says "Breadboard Wire (M-F)" on hover; only its pin and socket say "Yellow Breadboard Wire".**
- player.js:985 names a hovered tube from `wireDefs[id].name`, and steps.json "wire white".name is "Breadboard Wire (M-F)" (from
  `guide.py:203`). This was the same before, for all three wires.
- The new rulebook entry (`docs/cadasio-patterns.md:188`) says the colour changes "in its name on hover too".
- Fix (hover-only; the name is used nowhere else): in `guide.py:203` use `name=f'{SHOWN[w].capitalize()} Breadboard Wire'`, then
  regenerate. Or drop "and its name on hover" from the rulebook entry.

**C3 (docs only). The new rulebook entry `docs/cadasio-patterns.md:191-192` ("a label's leader never lies over a red lead line ...") is broader than Lee's note, and the guide does not keep it.**
- In the same Step 3, g2 still has its ring on the end of its red line. So do h3 and h16 (Step 5), j2 and j3 (Step 7), and a11 and
  a19 (Step 9). All are unchanged since Lee's review.
- The skeptic showed g2 is not the covering Lee described: its line runs unbroken into the ring. But by the ring's fixed dash angles,
  a dash crosses the line just above its end at h3, a19 and j2/j3, as it did at c16.
- Fix: reword the entry to the c16 case ("where a label's ring would cut across a red lead line's end, its leader stops beside the
  hole, without a ring: the LSM's c16, Step 3"). Also ask Lee whether h3, a19 and j2/j3 should get the same treatment (below).

**C4 (not visible, about 1 px or less; optional). Two small fit changes from the new D3, confirmed from `assembly-report.json` part boxes.**
- D3 has exactly D2's outline but sits 0.255 mm towards D4 of D2's x (D2 590.58-685.89, D3 590.32-685.64). Its narrower D1 slot
  therefore leaves D1's middle tab 0.26 mm into D3 at the slot's +x end, from Step 27c on. It was 0 with the old, wider slot.
- D9_A (z 1153.50-1254.75) and D9_B (1153.44-1254.69) stand 0.18 and 0.24 mm proud of the new D3's outer face (1153.68). They are
  short by the same amounts at D2's face (1254.93). D9 is exactly 101.25 mm, D2's outer face to D3's.
- Fix if wanted: in `assemble.py`, move D9_A +0.18 and D9_B +0.24 mm in z (both ends flush; the 0.175 / 0.237 mm shoulder overlaps
  with D3 go away). Moving D3 +0.255 mm in x would fit D1's tab but push D9_A's slot overlap from 0.175 to 0.32 mm, so leave D3
  where it is. Neither is worth a regeneration on its own.

## Raised by the reviewers and refuted by the skeptics

- A-R1 (c16 reads as c17 or b16): refuted. The leader tip ends at c16's corner, and c16's red line is always shown with it.
- A-R2 (the same overlap at g2, h3, h16, j2, j3, a11, a19): not a regression. They are unchanged and were seen by Lee, who named only
  c16. It remains as the docs point C3 and a question for Lee.
- A-R3 (Step 6 picture mirrored against the model): not a regression (round 3, item 18). It is part of C1 as a question for Lee.
- A-R4 (Step 6's shrunk close-up caption wraps to two lines, so the box reaches the step bar at 1000 and 768 px): real, but it covers
  0.1 to 0.4 px of the bar's white background and no control. Optional tidy-up: in `buildInset`, place the box by its real
  `offsetHeight` instead of a fixed `capH = 24`.

## Not verified

- No one looked at the pages themselves in a browser. Everything above comes from the author's thumbnails, steps.json, the part boxes
  and Python re-runs of the player's layout. In particular, nobody saw C1 in the page at Lee's window size (about 1000 px). It follows
  from the 3D render and from where the box is placed.
- C4's depths were not re-measured on the meshes in this check (swap was 7.2 of 8 GB used). They come from B's mesh sampling and agree
  with the part boxes.
- motioncheck's three brief wire-to-wire touches (Step 26c twice, Step 32c) are the same as last round and were not looked at again.
- Whether the kit's real ribbon has a white wire (A-R6): the captions now say "yellow". Lee asked for it, but it should be confirmed.

## For the reply to Lee (easy to miss)

- **Not on Lee's review site yet.** `share/Test guides preview/site/laser-stem-matrix-full-build/steps.json` is still release r6 (no
  "Yellow" in it).
  - Publish with `--to "share/Test guides preview"`, run `_runthrough()` on http://localhost:8799/laser-stem-matrix-full-build/, and
    give Lee that address.
  - Per CLAUDE.md, every guide's preview copy should be redone after a player change. Only the LSM's Steps 6 and 14 have a close-up
    with labels, so no other kit behaves differently.
  - Nothing is committed yet.
- Step 28 now has six lines, two each to D1, D2 and D3. His D3 points were picked on the old D3, so those lines end at the new,
  longer tab ends.
- The new D3's middle tabs stand about 3 to 4 mm out of D4 and D5, like D2's (not "0.46 mm longer"), and its slots are narrower.
- D8 is 3.17 mm thick in the CAD and the posts leave 3.0 mm (README question 17): is there a 3.0 mm D8?
- Step 6: the picture now sits on the left and its leader crosses the can, and the photo is mirrored against the model (C1). Ask
  whether to turn the view so the stripe faces left as in his photo.
- Step 3: c16 now has no ring; its leader stops just right of the hole. h3 (Step 5), a19 (Step 9) and j2/j3 (Step 7) have a ring
  dash across their red line's end as c16 had. Offer the same fix.
- The captions now say "yellow wire". Confirm that this is fine for the kit's real ribbon.
- Step 6's caption still says "a positive (+) leg" (the label says VCC (+)). Leave it, or add "VCC" if he wants the wording to
  match.
- The player change applies to every kit: a close-up that has no clear place at full size is drawn at 85%, 72% or 60%. Step 6 is
  drawn at 85% at 1000 px and 72% at 768.
