LAC round 2 (Lee, 21 Oct 2026): the research agents' working scripts, kept as they ran (they read the session scratchpad and the kit's
steps.json of that day; paths may need changing to run again). The reports they back are in docs/research/lac/round2/.

  labels_sim.py, labels_search.py, labels_render.py   where the player puts each label and eye (player.js layoutCallouts copied into
                                                      Python, Arial widths, the caption box), a search over 'near-*' places and reaches
                                                      at eight window shapes, and a drawing of each view: labels.md
  bend.py                                             a route's turning per mm over a 3 mm window (the "crazy, bent" measure):
                                                      wire_clipping.md
  lcd_checker.py                                      the LCD's vertices along each move (mixed as the player does) against F8, F9, F3,
                                                      F4, the F7s and F1, plates as prisms of a 0.1 mm raster: lcd_slide.md
  buzzer_field.py, buzzer_planner.py,                 the buzzer's seated leads over the jumpers: clearance at rest in every view from
  buzzer_astar_over.py                                Step 43c, and an A* search with the jumpers' columns closed: buzzer_leads.md

The camera fits from Lee's screenshots were done in the player (cameras.md: Nelder-Mead on the reprojection of known points, with
core.js cameraPose), and the hole sight-line tests are scripts/routing/sight.py.
  step43_low/                                         Step 43's carry beat, design "low, round the holes" (step43_low.md): common.py
                                                      (guide.py's buzzer helpers copied), linking.py (Gauss linking numbers: which
                                                      crossings are forced), field.py + blend.py + episodes.py (motioncheck's blending
                                                      over a precomputed clearance field, fast), guide_patch.py (the paste-ready code),
                                                      build_final.py (the steps copy), rest.py (clearances at rest); paths point at the
                                                      session scratch of 21 Oct 2026
  step43_high/                                        Step 43's carry, design "carry high, keep the over/under order" (step43_high.md):
                                                      common.py (guide.py's buzzer helpers copied, write_steps: a steps copy as stepgen
                                                      writes a step with stops), design4.py + cand13.json (the shapes), make_patch.py ->
                                                      guide_patch.txt / guide_patch_step43.txt (the paste-ready code), build_final.py (runs
                                                      the patch with guide.py's helpers, writes the steps copy), static.py (clearances at
                                                      rest, view by view), stops.py (the in-between shapes at their stops), partpath.py (the
                                                      buzzer against the other parts along its way), cross.py (plan crossings, over/under);
                                                      mc*.txt / static_final*.txt: the outputs quoted in the report. Paths point at the
                                                      session scratch of 21 Oct 2026
  step43_judge/                                       the judge of the two Step 43 designs (step43_judge.md): paste_check.py (pastes
                                                      each design's code into a copy of guide.py, runs the buzzer section with guide.py's
                                                      own setup lines and compares with the design's steps copy), mc_bends.py +
                                                      run_bends.py (motioncheck's blending, the buzzer leads' sharpest bend at each
                                                      moment), player_tools.js (a steps copy played in the real player from thumbs/:
                                                      the buzzer against the caption box, pictures of moments); *.txt: the outputs quoted
  f9/                                                 F9 hooked in and swung upright as published (Lee, 21 Oct 2026): f9check.py (F9 at
                                                      11 moments of each stretch of the published poses against every part on screen at
                                                      Step 45: clean, but for the back foot's barb in F3's edge, 1.3 mm, as it is swung
                                                      upright), f9pivot.py (other turning points: none below 1.2 mm), feet.py (the outline
                                                      of F9's feet and F3's slots); *_out.txt: their outputs
