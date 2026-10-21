# LSM deconstruction draft: conventions and code review (21 Oct 2026)

Angle: the draft (`LSM Build Instructions/deconstruction.py` -> `steps-deconstruction.json`) against Lee's and TechBox's take-apart
conventions (rulebook `docs/cadasio-patterns.md` section 11 and its dated paragraphs, section 13, CLAUDE.md "A deconstruction guide",
the MRA, RCC and PMG scripts), then the script's helpers and the two shared code changes. Wording is in `review_wording.md` and is
not repeated here. Nothing was run except small Python reads of the JSON. Picture numbers are
`LSM Build Instructions/pages/steps-deconstruction/NNN.png`.

State of the tree when read: the PMG session committed its staged-arrow work (f6c9063, 17:58) after the draft was generated (17:50).
The only uncommitted changes in `player/js/player.js` and `tools/stepgen.py` are now the LSM's own hunks (player.js:539-542,
stepgen.py:915 and 1827-1829). `code_changes.diff` in this folder is out of date: it still carries the PMG's hunks.

## 1. Steps 13, 11 and 7: a removal in two stages shows one arrow (high)

- **Wrong:** Lee ruled on the PMG the same day (rulebook docs/cadasio-patterns.md:292-299, "there's a motion toward H1 required first
  before the lift ... Examine the Cadasio") that a part coming off in stages shows an arrow for each stage, in turn (Step N the
  first stage's; the next appears as the stage before it plays). The draft shows one arrow, on the longest stage:
  - Step 13 (deconstruction.py:148): D4's way is `[[-8, 0, 0], [-8, 65, 0]]` (slide off the tabs of D1 and D2, then lift). The only
    arrow points up (steps-deconstruction.json Step 13: tail [595.91, 909.04, 1204.25], head +Y 40; picture 025.png). This is exactly
    Lee's H11/H12 complaint: the arrow goes up, the slide that must come first is not shown, though the caption names it.
  - Step 11 (deconstruction.py:141): D3 swings 22 degrees about its hinge at D4, then slides 40 mm (Step 11c paths). The arrow is on
    the slide only, and it floats off the part (item 3).
  - Step 7 (deconstruction.py:130-134): D10 slides 40 mm to unhook, then drops 22 mm from under the matrix. Arrow on the slide only.
  - Optional, same pattern: Step 19 (the matrix pulled 15 mm off the pins, then lifted 30; arrow on the pull, `stage=0`) and Step 8
    (over D4, then set down).
- **Fix:** the committed `arrow_style ... then=` (stepgen.py, f6c9063). Each of these steps moves one part, so the "as many stages"
  check holds: Step 13 `arrow_style={D4: dict(stage=0, then=[dict(stage=1)])}`; Step 11 `{D3: dict(stage=0, at=<D3's free end>,
  then=[dict(stage=1)])}`; Step 7 `{D10: dict(stage=0, at=at_now(D10, [599.5, 880.0, 1207.0]), then=[dict(stage=1)])}`. Re-run
  motioncheck is not needed (no motion changes); runthrough checks staged arrows.

## 2. Arrow sizes and group arrows: the PMG ruling of the same day not applied or put to Lee (medium)

- **Wrong:** the draft uses the MRA's in-house 15 - 40 mm long, 1.6 - 3.2 mm thick (CLAUDE.md "A deconstruction guide"), but Lee's
  PMG ruling (docs/cadasio-patterns.md:296-299) moved the PMG, also asked for with "same principles as the MRA", to the published
  take-apart's sizes "not the in-house 15 - 40 mm set for the MRA", and groups to one arrow "as published". TechBox's published LSM
  take-apart has measured arrows (docs/research/guide_19075-...deconstruction.md, step table): stems 69 mm, D8 66, D7 59, D5 63,
  D4 80, D11 posts 42 - 47 each (two per pair), D6 71, D9 61 - 69 (one each), D10 51, D3 51, D2 86.5, nut 56, button 38, USB 63,
  resistors 32 / 31.5, capacitor 21, Nano 40.5. The draft's: 15 - 40 mm, except two off the in-house band that Lee did not ask for:
  Step 1's stems at `arrow_scale=2.0`, 48.7 x 4.87 mm (deconstruction.py:114; its comment "(in one step: Lee; ... twice the size")
  reads as if Lee asked for the size; Lee asked for the group), and Step 12's 105 x 5 mm (the Full Build's own Step 26 arrow, reused).
  Step 4 has four arrows (generator NOTE: "published take-aparts show 2 at most"); the rulebook now holds both "each with its own
  arrow" (line 287) and "groups have one arrow" (line 298).
- **Fix:** put it to Lee with the numbers above: the LSM's arrows as the published LSM take-apart's (`dims=` per step, as the PMG's),
  or the MRA's band. Until then, take `arrow_scale=2.0` off Step 1 (or say in the comment it is the draft's choice), and ask whether the
  four posts take four arrows or one.

## 3. Step 11: D3's arrow floats 16 mm off the plate (medium; a generator weakness behind it)

- **Wrong:** Step 11's arrow tail is [681.58, 881.63, 1137.67]; D3 is z 1153.68 - 1156.68 (assembly-report.json), so the tail is 16 mm
  out from D3's outer face, in empty space beyond its end (picture 021.png). Rulebook docs/cadasio-patterns.md:109: "Tail on the
  part". Cause: `_arrow_out` (stepgen.py:1422-1445) draws the longest stage's arrow (the slide, tilted 22 degrees by the swing before
  it) from the part's centre *as it is now*, so a stage that follows a turn starts off the part.
- **Fix:** item 1's `stage=0` + `then=` (the committed `then=` draws a later stage's arrow where the part is as that stage begins,
  stepgen.py around 1806-1815), with `at=` on D3's free end for the swing. In the generator, a later note: a default arrow along a
  stage after a turn could be drawn from the part as that stage begins, as `then=` already does.

## 4. The order rests on b19 being blocked by the USB plug; TechBox's own take-apart unplugs it first (medium, for Lee)

- **Wrong:** the script's docstring (deconstruction.py:17-20) and plan_final.md fact 4 keep the LED matrix wired until Step 19
  because "b19 is under the USB plug's leg, so they come after it", and that is what forces the matrix's round trip (lifted over the
  box, carried over D4, turned over with the box hanging by its wires in Steps 10 - 11, carried back in Step 12: three lift steps and
  two Full Build wire shapes walked back). The overlap is a CAD placement ("it passes 0.3 mm into the plug, as the CAD places the
  two", guide.py:644). TechBox's published LSM take-apart unplugs the three matrix wires from the breadboard at its Steps 11 - 13,
  with the USB cable still plugged in until its Step 20 (guide_19075-...deconstruction.md step table, rows 031 - 036 and 054), then
  takes the matrix and D10 apart in an isolated view (its Step 14) and lays the matrix aside once.
- **Fix:** make sure plan question 1 reaches Lee with this evidence (in README.txt's questions): if the purple wire comes out of b19
  with the USB plug in, as TechBox's own guide shows, the matrix can be unplugged once it is out of the box and set aside, removing
  Steps 8 and 12 and the turned-over box with a dangling matrix (review_wording.md item 7). That needs new loose-wire shapes (the
  reason the draft avoided it), so it is Lee's call, not a fix to make unasked.

## 5. 2D PDF: pages.js puts Step 4's close-up over one of the four arrows (medium)

- **Wrong:** `player/js/pages.js:20-35` frames every close-up in the corner farthest from its spot and checks nothing else; the player
  change in this draft keeps the on-screen close-up clear of arrows, the PDF's does not. Picture 007.png (Step 4, drawn by pages.js):
  the close-up in the top-right corner covers the arrow on the D11 post at the D4 / D2 corner (only its tip shows at its left edge).
  Lee asked for the deconstruction's PDF with the Full Build's (rulebook section 13, "2D instructions", 21 Oct 2026). Labels and eyes
  are not avoided there either.
- **Fix:** in pages.js, place the close-up where the player placed it (read `#inset`'s box after `_dev.show(view.name)` and scale it
  to the page), or test the four corners against the projected arrows, labels and eyes as buildInset does. Then draw Step 4 again
  before any PDF is made.

## 6. Step 4: the tabs are pushed up from under D1 with the box standing upright (medium; same point as review_wording.md item 2)

- **Wrong:** the Full Build pushed the posts home with the box turned over (FB Step 36, `flip`, camera dir [0.4109, -0.8401, 0.3541]);
  the rulebook says work on the underside is shown with the kit turned over (docs/cadasio-patterns.md:155; section 13, "A part that
  goes on underneath"). Step 4 keeps D7's upright camera for both stages; only the close-up, from below, shows where the push is
  done (picture 007.png). The plan's reason (FB 36's camera would make the upward arrows eyes) is about the second stage only.
- **Fix:** either split it: "Turn the box over. Push the tabs of the four D11 posts up out of the slots in D1." by FB 36's camera
  (`flip`), with its close-up, then "Turn the box the right way up. Remove the four D11 posts from D6." by D7's camera; or keep one step
  and caption the lift of the box (the wording review's fix). Lee's choice; the split costs one step (25 for 40, still 0.63).

## 7. Step 7: a sub-assembly that came off is taken apart in place, not on its own (low, for Lee)

- **Wrong:** the matrix with D10 is lifted off the box (Step 6) and D10 is removed from it by the Full Build's camera with the box in
  view (Step 7). Lee's RCC rule (docs/cadasio-patterns.md:277-283): "a sub-assembly that comes off is taken apart on its own, the rest
  hidden, close in, then the guide returns to the main model"; TechBox's published LSM take-apart takes D10 off in an isolated view
  (its Step 14). The draft follows the MRA's other rule (seen the way the build showed it; FB 31 was in context), and the matrix is
  still wired to the breadboard, which an `alone=` view would cut.
- **Fix:** name the choice in README.txt's questions for Lee; no change unless Lee asks (it falls away if item 4 goes Lee's way).

## 8. Hand-placed arrows off their parts (low)

- **Step 18** (deconstruction.py:168-170): the button's arrow tail is at seated z 1219.0, 14.65 mm *behind* the button's back
  (BUTTON z 1233.65 - 1258.55, assembly-report.json), beside its wires, not "beside the button's body" as the comment says; its head
  stops 1 mm short of D2's inner face (head z 1307.99, D2's inner face 1309.03 after the 57.1 mm slide), so it points into the wood
  (picture 035.png), not into free space (docs/cadasio-patterns.md:109). TechBox's published take-apart turns to the cap side for this
  step (its Step 19, "moves 56 deg to the other face").
- **Step 14** (deconstruction.py:154): D2's arrow tail is 5 mm above D2's top edge (y 912.0 against 907.03), so it floats over the
  panel (picture 027.png).
- **Fix:** Step 18: tail on the button body (seated z about 1236) so the arrow runs along the body and ends at the hole, or ask Lee
  whether this step may turn to the cap side as the published guide does (against "two steps on one sub-assembly keep one camera");
  Step 14: y 907.5, on the edge. Correct the two comments.

## 9. Code: values copied from the Full Build by hand, and helpers that assume a pure shift (low)

- **Copies:** the script says it must be re-run after any Full Build change (deconstruction.py:1-3), but several Full Build values are
  typed in, so they will not follow a change: the D11 posts' way `[0, 6.38, 0]`, `[0, 85, 0]` (:121; guide.py:802's D11_SHORT /
  D11_UP); FB 36c's close-up target, dir and radius (:122; steps.json Step 36c `inset`); FB 26's arrow tail and head, swapped (:146;
  steps.json Step 26 `arrows[0]`). Read them from `VIEW` as the MRA's script reads its Row labels (`row_labels('Step 100')`).
- **Assumptions:** `camera_of(..., moved=)` (:51-56) and `slid()` (:74-78) zip with `by` as a plain [x, y, z]; given a pose dict they
  fail with a TypeError (the MRA's `camera_of` takes `moved.get('t')`), and given a turn they would be wrong without a word. `carried_back()`
  (:81-90) does not check that the walk-back starts where the part is now (its last stop against `where(part)`); a Full Build change
  that moved the matrix between FB 30 and 32 would make it jump. Add `assert` lines (D2_AT a list, `np.allclose` on the start).
- **Comment:** :163 "(a stop after one whole turn: two beats, as the Full Build's)": the Full Build's nut turned through both beats
  without stopping (FB Step 20: NUT `path_stops` [0, 8], the two beats came from BUTTON's still way); the draft's slows to rest after
  one turn (Step 17c `path_stops` [0, 4, 8]). Harmless; say so, or drop "as the Full Build's".
- **Workaround:** `g.put_away([BACKING])` (:96) is needed because `take_apart()` places every part any Full Build view showed
  (stepgen.py:874-880), including one the Full Build itself put away after Step 1c; the cost is a cut, not a glide, from the title page
  to Step 1. A later generator fix: skip a part that no view after its last appearance shows and that the Completed View does not
  `hide`.

## 10. player.js: a close-up keeps clear of the step's arrows (low; otherwise correct)

- **Correct:** buildInset (player.js:539-542) adds the projected tail-to-head line of each `arrowsOf(view)` arrow to the marks. It runs
  once as a view opens or the layout changes (no per-frame work); `project()` goes through `stage.world.matrixWorld`, so turned-over
  views are right; `arrowsOf` is empty except on Step N. Across every steps file in the repository (Full Builds, Parts, deconstructions)
  only three views have both a close-up and arrows: the LSM's Steps 4 and 19 and the MRA deconstruction's Step 64, so no build or Part
  guide moves. Side effect worth knowing: with arrows present, the instructions box is now also counted (the `marks.length && clear`
  line), as it already was for labels. The published MRA deconstruction (r3) keeps its old player until it is published again.
- **Weakness:** the band is a fixed 20 px wide (`qx - 10 ... qx + 10`), but an arrow's head is four times its body width
  (core.js setArrows: `hw = width * 2` each side). At Step 4's camera (radius 90) a 3.2 mm arrow's head is about 50 px across in an
  800 px tall view, so a close-up can cover a head's wings while counted clear.
- **Fix:** pad each square by the arrow's projected half head width (project `tail` and `tail + 2 * width` across the arrow, or take
  `2 * width` mm at the view's scale) instead of 10 px.
- **stepgen.py:1827-1829** (take-apart close-ups take `side`, `marks`, `ghost`): the same keys and formats as a build's (stepgen.py:1975-1977),
  except `image`, which the docstring (:915) rightly does not claim. It must be committed with the LSM files: without it the next run
  of deconstruction.py silently drops Step 19's `ghost` (the matrix drawn solid over the connectors in the close-up).

## Before this ships

1. Lee's round: items 1, 2, 4, 6 and 7, the plan's questions (plan_final.md section 7) and the wording review, on the test site
   (`publish.py laser-stem-matrix-deconstruction --to "share/Test guides preview"`, `check_site.py` on that folder, Lee on 8799).
   Nothing to `site/` or `live` without Lee's word.
2. Commit together, once checked: deconstruction.py, steps-deconstruction.json, `cards/steps-deconstruction.webp` and `.json` (the Full
   Build's card, byte for byte, model 0a7267f2bc49 = steps.json's: valid), the guides.json line **with** render.yaml (check_site.py
   requires a framing rule for every guides.json guide, so neither goes alone), the stepgen.py hunk (above) and the player.js hunk
   (a player change for every kit: the PMG session's run-through of every guide at 17:58 was made with this hunk in the tree, by its
   commit message; make the Website Preview again for every guide), docs/research/lsm/decon/. Refresh `code_changes.diff` or drop it.
3. Delete `LSM Build Instructions/thumbs/` (six cam19_*.png from 16:43, this work's camera trials; CLAUDE.md: "Delete thumbs/ afterwards").
4. Docs: `LSM Build Instructions/README.txt`, a deconstruction section with the open questions (it has none: README.txt:103 only says
   one may come); CLAUDE.md: an LSM paragraph under "A deconstruction guide" (as the MRA's, RCC's and PMG's), the command line beside
   CLAUDE.md:156-157, the LSM entry under Layout (CLAUDE.md:491: deconstruction.py), "inset= ... mark=, marks=, ghost=, side=" in the
   remove() options, and "and arrows" where a close-up keeps clear of labels and eyes (CLAUDE.md:100); the rulebook: arrows added to
   "A close-up never covers the step's labels or eyes" (docs/cadasio-patterns.md:139), and a "Lee, 2026-10-2x (the LSM's
   deconstruction)" paragraph once Lee rules, recording the exception to "the power cable first" (the USB cable at Step 15, as
   TechBox's own LSM take-apart, with Step 1's caution) and whatever Lee decides on items 1, 2 and 4.
5. The 2D PDF only after item 5 is fixed in pages.js.
