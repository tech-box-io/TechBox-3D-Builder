# Research reports behind the rulebook

Working material from the study of TechBox's 20 published Cadasio guides (2026-10-13). The rules themselves are in
`../cadasio-patterns.md`; every rule with its numbers and verdict is in `../cadasio-patterns-evidence.md`.

- `guide_<guide id>.md` (20): one reader's report per published guide: a table of every step, the conventions seen, how each kind of part looks, and slips.
- `dim_<topic>.md` (9): one analyst's cross-guide report per topic, with the tables behind its numbers.
- `verify_<topic>.md` (9): the second analyst's notes from re-deriving each of that topic's rules from the data.
- `gap_check.md`: the final pass that looked for what an author would still have to guess at.

The deconstruction topic's analyst and verifier returned their rules and verdicts but did not write report files; their results are in
the evidence document under "Deconstruction (take-apart) guides".

Step references such as `[057]` are the index of a step view within its guide. The readers worked from per-step digests that mis-read
visibility and position in some guides (see Appendix A of the rulebook); each report says where it re-derived things from the raw data
instead. `tools/cadasio/digest.py` now reads both correctly.

`nano-colour-atlas-published.json`: the colour of every solid of the Arduino Nano as the published guides show it (taken from the PMG
full build with `tools/cadasio/atlas.py`). The MRA guide used it until 2026-10-13 and now takes its colours from TechBox's own MRA
Cadasio project instead; it is kept for kits whose Cadasio project is not available.

## `mra/`: the Mini Robot Arm (2026-10-13)

What the MRA guide is built on. Engraved codes and CAD ids are tied together in `cad_codes_base.md`.

- `lee_notes_2026-10-13.md`: Lee's notes on the guide, word for word, with the step list they refer to.
- `lee_notes_2026-10-14.md`: Lee's notes on v201, word for word (step numbers are v201's; the electronics test added since moves the mechanical steps on by 18).
- `review_v3_code.md`: the independent code review of the 14 Oct changes (turned-over views, faded wires, highlight, per-part paths, put_away, stickers) and what was fixed.
- `review_v4_usb.md`: the review of the USB cable (from Lee's STEP files) and the title-page camera taken from Lee's screenshot, and what was fixed.
- `review_v5.md`: the review of the changes for Lee's notes of 14 Oct (afternoon) and what was fixed.
- `review_v6.md`: the review of the evening's changes and the first shareable checkpoint (share/), and what was fixed.
- `lee_notes_2026-10-14b.md`: Lee's "first comprehensive review" (31 requests), what was done for each, and the old-to-new step numbers; Lee's pictures for it are in `lee_images_2026-10-14b/`.
- `review_v7.md`: the review of that round's changes, and what was fixed.
- `lee_notes_2026-10-14c.md`: Lee's third round that day (parts-list picture and zoom, board colour, dot colour, the arm check on A13 / A12 in one view, the extension wire's clipping in Step 100, copyright, review notes off) and what was done.
- `review_v8.md`: the review of the third round, and what was fixed.
- `lee_notes_2026-10-15.md`: Lee's notes of 15 Oct (parts-list pictures of the breadboard wire and T2, the voice, "Row" in Steps 12 - 15, Step 26's wording, the extension wire's resting route from Step 97c to 100) and what was done; `round9_extension_rest/`: the three independent designs for that route.
- `review_v9.md`: the review of that round, and what was fixed.
- `lee_notes_2026-10-15b.md`: Lee's second note of 15 Oct ("Row" in Steps 40, 98 - 100, Step 26's wording again, the elbow motor's lead clipping the base motor's in Step 98, the shoulder motor's lead flipping in Step 99) and what was done.
- `review_v10.md`: the review of that round, and what was fixed.
- `lee_notes_2026-10-15c.md`: Lee's third note of 15 Oct (the elbow motor's lead over the base motor's lead, not under it as the CAD has it; Step 98) and what was done.
- `review_v11.md`: the review of that change, and what was fixed.
- `lee_notes_2026-10-16.md`: Lee's notes of 16 Oct (the step list's pictures of the Parts List pages, the wood bands' colour, a view reset button, the joysticks' hover names, the step text in a CSV for the curriculum director) and what was done.
- `review_v12.md`: the review of that round, and what was fixed.
- `video_base.md`, `video_controller.md`, `video_arm.md`, `video_claw.md`: what the builder does in each of the four build videos, action
  by action with times; the `_seg` files are the stretch-by-stretch reports they were merged from; `stills/` the frames they cite.
- `cad_codes_base.md` (+ `.json`): the code engraved on every wood part, and the base joints measured (R1's cut-out against the horn,
  B2's keyhole, B1's pocket, tabs and slots of R2 to R6).
- `cad_arm_claw.md` (+ `.json`): servos, horns, every screw and what it passes through, how the arm and claw go together, a tested order.
- `cad_wire_paths.md`, `cad_wires.json`: the centre line of every wire in the CAD, each servo's lead as a chain, the slots leads pass through.
- `cad_pins.md` (+ `.json`): every pin a wire plugs into, with the names printed on the boards (read from the Controller video).
- `cadasio_mra_project.md`, `cadasio_mra_colours.json`: TechBox's own Cadasio project for the kit: colours solid by solid, tooltips, look settings.
- `review_*.md`: independent checks of the finished steps. `authoring/`: the brief and working logs of the arm and claw sections.

## `rcc/`: the Radio Controlled Car (2026-10-15)

What the RCC guide's first draft is built on.

- `cadasio_study.md`: TechBox's published Cadasio guide for the kit (19075), step by step: the wiring, its errors and colour slips, a
  proposed step list and the decisions for Lee. Its data and step pictures are in `cadasio/`.
- `cad_study.md` (+ `.json`), `cad_tree.md`: Lee's STEP: the 42 parts, how the wood joins, which way each part can go in, the
  engraved codes, the connector geometry, and what looks wrong in the CAD.
- `reuse_and_colours.md`: what carries over from the MRA (Nano, I/O module, joysticks, USB) and the colour plan.
- `materials_notes.md`, `cad_wire_paths.md`, `silkscreen.md`: how materials.json, wire-paths.json and decals.json were made and checked.
- `lee_images_2026-10-15/`: Lee's photos of the adapter and controller boards and the L1 etching drawing.
- `review_v1.md`: the independent review of the first draft.
