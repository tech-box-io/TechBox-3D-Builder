# LSM round 4 (Lee's notes of 20 Oct 2026): independent review, group B

Scope: the new D3 from `LSM_D3.STEP`, Step 28's four added lead lines, and D8's seat height (Step 38 onward).
Method: read `steps.json` against the round before (`scratchpad/steps_before_r4.json`), `assembly-report.json` and `git diff HEAD`;
loaded the exact parts from `lsm.glb` (new) and from `HEAD:lsm.glb` (old) through `tools/stepgen.py`'s `Model`, with trimesh, and
measured overlaps by sampling 40 000 - 60 000 surface points per part and testing them inside the other part (depth = distance to
its surface); looked at the pictures in `LSM Build Instructions/thumbs/` and `cards/steps.webp` (old and new). No guide.py,
build_model.py, assemble.py or browser runs. Scripts: `scratchpad/rb/` (dump.py, pen.py, swing.py, holes.py, chk1.py, chk2.py).

## Verdicts

### 1. D3 replaced by Lee's STEP, and where it is placed: done (two sub-pixel notes below)
- `assemble.py` takes D3 from `lsm-d3.glb` `LSM_D3` with the old instance's placement (`at('LSM_Side1_r8-1')`); the old wood entry is
  gone from the loop. `assembly-report.json`: D3 x 590.32 - 685.64, z 1153.68 - 1156.68 (was 590.78 - 685.18, 1153.50 - 1156.68).
- The inner face stays at z 1156.68, where D6, D7 and D8 butt against it (their lo z 1156.68). D4's slots for D3's tabs are
  z 1153.61 - 1156.61 and D5's 1153.59 - 1156.59, so the 3.0 mm D3 is 0.07 / 0.09 mm off centre in them (the old 3.175 mm D3
  overlapped both sides). Invisible.
- The engraving is in the same place: pocket floor at x 664.69 - 674.22, y 867.95 - 873.89 on the outer face (normal -z), 0.254 mm
  deep, in both the old and the new part. The LSM kit has no `engraved-codes.json`, so no camera data went stale.
- `model.report.json`: `LSM_D3`, 2808 triangles, colours ink + wood, "edges roughened by up to 0.1 mm" (publish's roughening check
  will pass).
- Seated overlaps, new against old D3: D4 0.71 (old 0.71: the latch hooks over D4's outer face), D5 0.26 (old 0.27), D9_A 0.175 and
  D9_B 0.237 (old the same), D2 / D6 / D7 / D8 / D10 / D11_B / D11_D none. New: **D1 0.26 (old 0)**, see regression 1.
- The new D3 has exactly D2's outline (949 outline points at mid-thickness, 95.31 mm long, as D2's 590.58 - 685.89), but sits
  0.255 mm towards D4 of where D2 sits. See regression 1.

### 2. Steps 27 and 28 with the new D3: done
- Step 27's path, hinge and camera are unchanged (`HINGE` = [597.41, 881.63, 1156.68]: D4's inner face, D3's mid height and inner
  face, all unchanged). Swing simulated as the player plays it (`mixPose`: a pure turn about the hinge, 22 to 0 degrees): D3 into D4
  at most 1.50 mm while tilted (old 1.50: a 3 mm plate turned in a 3 mm slot), D3 into D1 1.06 - 1.30 mm in the last 5 degrees
  (old 0.98 - 1.19), 0.25 at rest (old 0). Brief and inside the slot; Lee would not see it.
- Step 27's label moved with the face: [640.1, 882.0, 1153.5] -> [635.9, 882.0, 1153.7]. Its two hand-set lead lines start at
  x 590.9, now 0.58 mm in from the longer tab's end (590.32; was 0.12 mm in); the lower one is in the hook's spring cut, 0.22 mm off
  D3, as before. Same look (`thumbs/n_Step27.png`: two lines, D3's hooked end to D4's slots).
- Tabs in the slots: the D3 material inside D5's thickness spans y 859.47 - 867.40 (D5's slot 859.34 - 867.15) and the same at D4;
  as the old part. The new tabs stand 3.13 mm proud of D5's outer face (old 0.04), 4.09 mm proud of D4's (old 3.63), as D2's do
  (3.38 and 3.83): that is Lee's part.
- `thumbs/q_sheet.png` (Step 27c at 0.3, 0.6, 0.85 of the swing) and `nsheet_1.png` (Steps 27, 27c, 28) show the new D3 hooked into
  D4 and swinging shut, nothing out of place.

### 3. D3 in the later steps, the Completed View, the card, the part picture: done
- D3 is seated (offset zero) in all 30 views that show it; its only change on screen is the longer tabs and the 0.18 mm thinner
  outer face.
- `parts/D3.png` (and `thumbs/parts_r4.png`) is the new part: the long end tabs, the curved spring cuts, the D1 slot, "D3" readable.
  `parts/parts.json` model stamp 20146e2708d1 = the sha256 of `model.glb` = `steps.json`'s `model.glb?v=` = `cards/steps.json`.
- `cards/steps.webp` against `HEAD`'s: only D8's height differs visibly; D3's tabs at the far corner a little longer.

### 4. Step 28: Lee's four added lead lines: done
`steps.json` Step 28 `guides` now holds six (the two of 19 Oct and Lee's four). The player draws each from `tip` moved by D5's hover
(+42 mm x) to `mouth`, so each runs from D5 to the point:

| Line | tip (on D5, seated) | mouth | where the mouth is (new lsm.glb) |
|---|---|---|---|
| D1 (19 Oct) | 682.6, 861.3, 1176.1 | same | on D1's tab end (0.08 mm) |
| D1 (Lee, 20 Oct) | 682.8, 861.1, 1233.2 | same | on D1's tab end (0.12 mm; the tab ends at x 682.68) |
| D2 (19 Oct) | 682.5, 864.8, 1254.2 | 685.9, 864.8, 1254.2 | on D2's tab end (0.01 mm) |
| D2 (Lee, 20 Oct) | 682.5, 899.0, 1253.4 | 685.9, 899.0, 1253.4 | on D2's tab end (0.01 mm) |
| D3 (Lee, 20 Oct) | 682.6, 865.4, 1155.5 | same | 1.18 mm inside the new D3; the line meets D3 at its new tab end, x 685.64 |
| D3 (Lee, 20 Oct) | 682.6, 899.5, 1155.2 | same | 0.80 mm inside the new D3; the line meets D3 at its new tab end, x 685.64 |

- Every line starts in one of D5's slots: tested along D5's thickness (x 679.6 - 682.4) at each line's y and z, none passes through
  D5's solid; each tip is 0.0 - 0.3 mm beyond D5's outer face, in the slot's mouth. Lee's D2 point is made a pair from D5's face, as
  the 19 Oct D2 line was (a single point would have started 3.4 mm out in the air past D5).
- Lee picked the two D3 points on the old D3, on the end faces of the tabs that sat flush in D5 (x 682.55). The new tabs reach
  x 685.64, so the points are now inside them, and each line visibly ends where it meets the tab's new end face, 3 mm short of the
  picked spot. That is still tab-to-slot, which is what the points meant.
- `thumbs/n_Step28.png`: six red lines, each with red showing in its D5 slot; the two to D3 end on D3's two tabs.
- Six lines exceed the rulebook's 1, 2 or 4. Lee's decision of 14 Oct ("as many as the joint needs when Lee asks") covers it, and
  README question 14 records it.

### 5. D8 in Step 38 and after: done
- `assemble.py` raises D8 2.09 mm: y 929.19 - 932.36 (was 927.10 - 930.27). The D11 posts' latch bottom face is at y 932.38 and the
  ledge under the neck at 929.38 (read from D11_A's and D11_C's outlines), so D8's top is 0.02 mm under the latch and its bottom
  0.19 mm into the ledges. The ledges (z 1237.24 - 1238.43 and 1246.37 - 1247.56 on D11_A, likewise on the others) lie wholly
  under D8, so the 0.19 mm is out of sight.
- All views that show D8 have it seated (Start, 38c, 39, 39c, 40, 40c, Completed View) or hovering 55 mm above its seat (Step 38).
  Step 38's lines and label were worked out again by the generator (mouths at y 932.3, label at y 932.4). Cameras unchanged.
- `thumbs/d8_corner_A.png`, `d8_corner_zoom.png`, `n_Step38c.png`: the latch heads sit on D8's top face. The card shows the same.
- Anything D8 now passes into: D7 nothing (12.69 mm gap); the stems 0.19 mm in D8's holes, the same as before; D2 / D3 / D6 none.
  The posts' necks are 7.94 mm wide (z 1238.43 - 1246.37 on D11_A) where D8's slots are 5.56 mm (1239.62 - 1245.18), so each
  post passes 1.19 mm into D8 on both sides of its slot. That is in the CAD as given and was worse before (1.49 - 1.59 mm, part
  of it into the wider ledge); it lies inside D8's thickness and cannot be seen.

## Regressions and points next to these steps

1. **D1's middle tab passes 0.26 mm into the new D3 (low).** The new slot is the tab's width exactly (x 631.88 - 644.07, 12.19 mm;
   the old was 631.63 - 644.33, 12.70 mm), and D1's tab is at 632.14 - 644.33, so its +x end is 0.26 mm into D3 from Step 27c to the
   end (seated depth 0.255, old 0). The new D3 is D2's outline; D2 sits at x 590.58 - 685.89 and D1's same tab fits D2's slot (0.002).
   Moved +0.255 mm in x, D3 lies exactly where D2 does: D1 0.002, D4 0.45, D5 0.26 (D2's own figures), though D9_A's slot overlap
   would rise from 0.175 to 0.32 mm. About 1 px at Lee's window size; Lee would not see it. The README's "placed where the first D3 was
   (the same part frame)" is true, but the first D3 was itself 0.255 mm off D1's and D2's centre, which its wider slot hid.
2. **D9's ends stand proud of D3's new outer face (low).** D9_A ends at z 1153.50 and D9_B at 1153.44, flush with the old D3's
   outer face; the new face is at 1153.68, so they stick out 0.18 and 0.24 mm. D9 is 101.25 mm long, exactly D2's outer face to the
   new D3's (1254.93 - 1153.68). Moved +0.18 / +0.24 mm in z, both ends would be flush and D9's shoulders would stop overlapping D3's
   inner face (now 0.175 / 0.237 mm, the same as before). The D3 wall faces the camera in Steps 29 - 40 (the D4 / D3 corner), but
   0.2 mm is about 1 px.
3. Not on screen, for the record: the evidence file says the new D3's slots are "a little wider". They are narrower: the D9 slots
   3.18 -> 3.0 mm (617.02 - 620.20 -> 617.20 - 620.20, 655.75 - 658.93 -> 655.76 - 658.76), the D1 slot 12.70 x 3.18 -> 12.19 x 3.0.
   That is what makes regression 1 new. `assemble.py` and the README say "reshaped", which is accurate.
4. Step 39 (the first stem): its lead line moved up 1 mm with D8 (tip y 914.7 -> 915.8, mouth 917.1 -> 918.1). The mouth is in the
   gap under D8, 1.6 mm above D7, not at D8's hole; it was 0.6 mm above D7 before. D8 hides that part of the line, so on screen
   (`thumbs/q_Step39_1.png`) it still runs from the stem's foot into D8's corner hole. This was already so before the change.

Nothing else found in these steps: no camera changed (all 82 views compared by name), Step 28's caption already names D1, D2 and D3,
and no other view has a label, eye, arrow or close-up anchored on D3 or D8 besides Steps 27 and 38.
