# Review v7: Lee's comprehensive feedback of 14 Oct 2026 (second round)

Three independent reviewers (the player; the generator, guide and silkscreen; coverage of Lee's 31 requests and the docs),
then an adversarial verifier for each medium or high finding. Workflow run `wf_a207fce6-387`. What was found and what was done:

| Finding | Severity | Outcome |
|---|---|---|
| A resize (full screen, turning a tablet) stopped the reading and scrolled the parts page back to the top | medium, verified | Fixed: a redraw of the same view keeps both. Checked: no cancel on resize, the speaker stays pressed. |
| The Parts List left out the 8 breadboard wires (F-F) | medium, verified | Fixed: `Guide.list_part()` lists a kit part whose CAD pieces are hover-only; pictured as one wire (its two caps and the CAD's route). parts.json / parts.csv now have 53 entries. |
| The Step 76 jiggle pulled A11 3.5 mm off its screw on A10 | medium, verified | Fixed: A11 rocks 1.5 degrees and takes that screw with it (A11 lies over the joint, so A10's hole stays hidden). The linkage itself is still not modelled. |
| Decal print darker in snapshots (thumbnails, part pictures) | low | Fixed: decals use a shader that writes the canvas's sRGB values as they are, like the toon material. Part pictures re-rendered. |
| Home / End on the focused step list did nothing or opened the grid | low | Fixed: the page's key handler takes them there too. Checked. |
| Keyboard focus lost when the focused speaker button's box was hidden | low | Fixed: focus moves to the visible speaker or to Next / Previous. Checked (Step 16c to the checklist card). |
| A cancelled utterance's end event could clear the next one's state | low | Fixed: only the utterance being read clears it. |
| The wiggle played only when stepping forward | low | Fixed: it plays however its step is reached (forward, back, jump). |
| `_dev.show(name, k)` mis-timed wiggle and per-part paths | low | Fixed in runthrough.js. |
| The Parts List page could not be scrolled from the keyboard in Safari | low | Fixed: the page takes focus (tabindex 0). |
| `buildInset` cleared lead lines and arrows (latent: hover views) | low | Fixed: restored after the snapshot. |
| The inset's red box was 14% larger than `mark` | low | Fixed: sized from the picture's real half-height at the detail. |
| Caption only 3% bigger on narrow windows | low | Changed: 18.4 px down to 420 px wide, 17.2 px on a phone (documented). |
| Steps 18 and 76 had no cue (rulebook: every Step N has one) | low | Fixed: an eye on the plugs (Step 18) and on A12 (Step 76). |
| Parts List page names fixed per group (a split guide would get "Parts List" then "(Cont. 2)") | low | Fixed: pages are named in order; "Other parts" goes on the last page. |
| `put_away` left riders in place; `cut` not handled by rest steps; docstring still asked for a card | low (latent) | Fixed in stepgen.py. |
| The sagging shoulder lead had corners where the sag began and ended | low | Fixed: eased in and out over 18 mm; ray-tested clear of every part again. |
| silkscreen.py wrote commas for exactly four decals | low | Fixed. |
| Docs: "the player draws the silkscreen from decals.json" (it reads the copy in model.glb); the USB step's number; the dot-label convention missing from the rulebook; the label boxes recorded as wider than asked | low | Fixed in the notes, rulebook, README and materials notes. |
| Step 100's label on the extension's plug reads "Claw Motor (Blue Dot)" | low | Kept: the label names the motor the plug carries, as on Steps 98 and 99; reported to Lee. |
| The close-up is a framed box, not a cloud shape | low | Kept: the house style for a picture with a lead line; reported to Lee. |
| White boxes are drawn behind every label, not only on Steps 98 - 100 | low | Kept (invisible in white space; shows only where a label lies over the model); reported to Lee. |

After the fixes: `_runthrough()` 212 views, 0 problems; every camera diffed against steps.json from before the round
(only Steps 18, 39, 52, 56, 57, 66, 67 and 76 changed, as asked); the single-file checkpoint loads with nothing else requested.
