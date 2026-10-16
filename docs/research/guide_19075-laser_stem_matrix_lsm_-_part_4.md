# Guide report: 19075-laser_stem_matrix_lsm_-_part_4

"Laser Stem Matrix (LSM) - Part 4" (kit LSM, role: part). 37 authored steps, 29 shown in the viewer (27 pause, 2 auto-advance, 8 hidden).

Sources: `digest/19075-laser_stem_matrix_lsm_-_part_4.md`, all 4 contact sheets, individual thumbs, and targeted queries on `cadasio_raw/…part_4.json` (helper script kept at `reports/_work_p4/track.py`).

## Summary

Part 4 is the purely mechanical close-up of the LSM box: no wire is connected and no screw is used. Starting from the end state of Part 3 (open plywood box with the electronics inside and the 8x8 LED matrix lying outside on its 3-wire ribbon), the student drops in two long matrix supports (D9), picks up the LED matrix, clips a small support (D10) onto it, lowers that sub-assembly into the box, closes the box with the lens bottom plate (D6), inserts four lens-support posts (D11) two at a time, flips the box to push the posts home through the bottom, stacks the middle (D7) and top (D8) lens plates on the posts, and finally pushes 64 white LED stems through the plates. The guide is authored as 12 hover/completed pairs ("Step N" / "Step Nc") between a title page and a "Completed View", with two auto-advancing "Transition" steps and one section card ("LED Stems", quantity label "64X"). There is no instructional text at all: the only words on screen are the title block, the part IDs engraved on the wood (D2 to D11) and "64X". Guidance is carried by red lead lines (29 over 10 steps), a black eye icon (3 uses), two inset detail pictures, part motion and camera moves.

## Data caveat that affects how the digest reads for this guide

Two things in the digest are wrong for this guide and were corrected from the raw payload:

1. Top-level components flagged `hidden` in the assembly tree (all lens plates, all four lens-support posts, the four side walls, 6 of the 7 LED-matrix pose copies, 63 of 64 stems) are still rendered whenever their solids are switched visible. The digest treats that flag as a gate, so it reports nothing appearing or moving in [010] to [022] and under-counts "parts on screen". The thumbnails show those parts clearly.
2. `position` on a single-solid top-level part (stems, wires) is an absolute position, not an offset. The digest's "displaced by [607, 947, 1175] mm" for stems is an artefact; the real stem hover is 50.2 mm. Offsets on multi-solid parts are in the part's local axes, so the digest's "-Z" for the D9 supports is world "up".

All offsets below are world-space millimetres, Y up, recomputed with these corrections.

## Step table (every viewer step)

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title, pause | Finished model (box, 3 lens plates, 64 stems, USB cable) shown complete, placed right of centre | 2 unanchored images: TechBox logo SVG top-left (x 1.8%, y 5.1%, width 37.6%); title block PNG "Laser Stem Matrix (LSM) / Part 4 / copyright line" lower-left (x 1.8%, y 61.5%, width 42.9%) | dist 321 mm, elev 27, azim 57 |
| 001 | Step 1 | hover | State jumps to the Part 3 end state: open box with electronics, LED matrix lying outside on its ribbon. 2 long matrix supports "D9" shown 68.0 mm straight above their slots | 4 red solid lead lines, each 68.0 mm, vertical: each D9 end tab to its notch in the wall top (2 into Side1, 2 into Side3) | MOVES 109.5 deg, 321 to 300; elev 31, azim -165 |
| 002 | Step 1c | completed | Both D9 tween down 68.0 mm to seat | none (4 lines removed) | unchanged |
| 003 | Step 2 | hover, no new part | Nothing moves | Eye icon (width 7.8%) at (57,18)% with light-blue leader and ring on the centre of the LED matrix | MOVES 32.5 deg, dist 300; elev 25, azim -128 |
| 004 | Step 2c | completed, pose swap | Cross-fade: the flat-lying matrix copy (matrix + 3 wires + 3 housings) fades out; a copy held 56.6 mm above its seat over the box, turned 180 deg, with re-routed wires fades in | none | unchanged |
| 005 | Step 3 | hover | Small matrix support "D10" fades in 19.3 mm below and 41.2 mm sideways of where it clips onto the lifted matrix | 2 red solid L-shaped lead lines (3 points: up 19.6 to 20.6 mm, then across 41.4 to 41.9 mm) from the top of each D10 hook to the matrix PCB edge | MOVES 5.2 deg, 300 to 258 (x1.17); elev 20, azim -128 |
| 006 | Transition | auto-advance | D10 rises 19.3 mm (first leg of the L path) | lines removed | unchanged; nav overlay hidden |
| 007 | Step 3c | completed | D10 slides 41.1 mm horizontally onto the matrix edge (second leg) | none | unchanged |
| 008 | Step 4 | hover, no new part | Nothing moves; lifted matrix + D10 sub-assembly sits above the box | 2 red solid vertical lead lines, 56.9 and 57.0 mm: slot in the top of the Side2 and Side4 walls to the D10 end ears | MOVES 85.5 deg, dist 258; elev 22, azim -35 |
| 009 | Step 4c | completed, pose swap | Cross-fade: lifted matrix + D10 + wires out; seated matrix, seated D10 and tucked ribbon in | Inset image (width 16.8%, rounded rectangle, 5 px light-blue border, eye glyph inside) at (14,9)% with leader and ring to the box corner: close-up of the ribbon connector and wire routing inside | unchanged |
| 010 | Step 5 | hover | Lens bottom plate "D6" (8x8 holes) fades in 64.3 mm above | 4 red solid vertical lead lines from the plate's 4 edge slots down to the wall tabs: 63.1, 62.3, 67.8 and 102.8 mm (the last is mis-anchored, see anomalies) | MOVES 72.1 deg, dist 258; elev 31, azim 47 |
| 011 | Step 5c | completed | D6 tweens down 64.3 mm, closing the box | none | unchanged |
| 012 | Step 6 | hover | 2 lens-support posts "D11" (near pair) fade in 88.6 mm above | 2 red solid vertical lines, 43.8 and 43.4 mm: bottom tip of each post to its corner slot in D6 | MOVES 14.1 deg, 258 to 300 (x0.86); elev 21, azim 36 |
| 013 | Step 6c | completed | Both posts drop 81.7 mm and stop 7.0 mm short of fully seated | none | unchanged |
| 014 | Step 7 | hover | The other 2 D11 posts fade in 90.1 and 84.4 mm above | 2 red solid vertical lines, 44.1 and 37.4 mm: tip to slot | MOVES 82.2 deg, dist 300; elev 23, azim -55 |
| 015 | Step 7c | completed | Posts drop 83.1 and 77.4 mm, again to 7.0 mm short | none | unchanged |
| 016 | Step 8 | hover, no new part | Model viewed from underneath; bottom plate and one side wall ghosted to 50% opacity; nothing moves | Eye icon at (20,25)% with leader to a ring on one post end; 4 short red solid lines, 16.5 to 17.5 mm, one at each post end to the bottom-plate slot | MOVES 116.9 deg, 300 to 258; elev -57, azim 49; scene up-axis flipped to -y |
| 017 | Step 9c (sic) | completed | The 4 posts travel the final 7.0 mm into the bottom plate; bottom plate opaque again | Inset image (width 14.2%, light-blue rounded border, eye inside) at (19,47)% with leader and ring to the same corner: close-up of a tab through its slot | unchanged |
| 018 | Transition | auto-advance | Nothing moves; remaining ghosting restored | inset removed | MOVES 110.2 deg, 258 to 300; elev 34, azim 123; up-axis back to +y; nav overlay hidden |
| 019 | Step 10 | hover | Lens middle plate "D7" fades in 67.8 mm above | 4 red vertical lead lines (stored as dashed, render as solid), 48.9 to 49.3 mm: top tip of each post up to the 4 slots of D7 | unchanged |
| 020 | Step 10c | completed | D7 drops 67.8 mm onto the posts | none | unchanged |
| 021 | Step 11 | hover | Lens top plate "D8" fades in 54.1 mm above | 4 red vertical lead lines (stored as dashed), 59.1 to 63.2 mm: posts up to the D8 slots | unchanged |
| 022 | Step 11c | completed | D8 drops 54.1 mm | none | unchanged |
| 023 | LED Stems | section card | Everything hidden except one white stem | Label "64X" (Arial bold 6em, light blue #7fdbff, no box, no leader) at (53,21)%, right of the stem | MOVES 74.6 deg, target shift 95 mm, 300 to 173 (x1.73); elev 31, azim 32 |
| 024 | Step 12 | hover | Whole model fades back in; the one stem is 50.2 mm above its hole (corner cell) | 1 red solid vertical line, 48.1 mm: stem bottom face to the hole / LED cell | MOVES 0.0 deg rotation, target shift 87 mm, 173 to 374 (x0.46) |
| 025 | Step 12c | completed | Stem drops 50.2 mm | none | unchanged |
| 026 | Step 13 | hover, no new part | Nothing moves | Eye icon at (56,12)% with leader to a ring on the installed stem | unchanged |
| 027 | Step 13c | completed | The remaining 63 stems fade in already seated | none | unchanged |
| 028 | Completed View | final | Nothing built | none | MOVES 12.9 deg, 374 to 321 (x1.17); elev 39, azim 44 |

Counts: 1 title, 12 hover steps (1 to 8, 10 to 13), 12 completed steps (1c to 7c, 9c, 10c to 13c), 2 Transitions, 1 section card, 1 Completed View.

## Conventions

### Structure

- **Skeleton.** Start (title) then repeated [Step N hover, Step Nc completed] pairs, then Completed View. Always true for the 12 pairs. Every step except the two Transitions waits for the student.
- **Hover step vs completed step.** The hover step introduces what is about to happen (new part at its hover pose, or an eye icon, plus red lead lines) and is where the camera moves. The completed step shows the result with the lead lines gone. True for 12 of 12 pairs.
- **Title page.** Finished model on the right, logo top-left, title/part/copyright block lower-left, both as unanchored images with no container.
- **Section card.** One card, [023] "LED Stems": the part is shown alone (everything else hidden) with a quantity label. It sits immediately before the first step that uses the part. The wood parts D6 to D11 get no card.
- **No text.** No step has a description or popup (27 of 27 build steps empty). The only label object in the guide is "64X". Parts are identified by the IDs engraved on the wood, which are part of the 3D model.
- **Transition steps.** Auto-advance, 800 ms, navigation overlay hidden (`overlayVisible` false on both, true on every other step). Two different uses: [006] is the intermediate waypoint of a two-leg part move with no camera change; [018] is a pure camera move that flips the model upright again after the underside view.
- **Uniform timing.** All 37 authored steps are 800 ms, parts tween, show/hide fade, camera tween speed 2 with no orbit animation.

### Granularity

- **One kind of part per step.** 8 of 12 hover steps introduce a new part: 5 introduce exactly one (Steps 3, 5, 10, 11, 12) and 3 introduce two identical parts (Steps 1, 6, 7). Different kinds of part are never combined.
- **Pairs only when both are visible from one view.** The four identical D11 posts are split 2 + 2 across Steps 6 and 7 with an 82.2 deg camera rotation between them, rather than added as four.
- **Bulk repeat.** For 64 identical stems: one exemplar is animated in full (Step 12), then Step 13 shows an eye icon on that exemplar and Step 13c fades the other 63 in already seated. No per-stem lines or motion.
- **Steps with no new part.** 4 of 12: Step 2 (pick up and turn the LED matrix), Step 4 (lower the sub-assembly), Step 8 (push posts home, inspect from below), Step 13 (repeat for the rest).

### Ordering

- **Bottom-up, inside-out.** Internal supports, then LED matrix, then lid plate, then posts, then middle plate, then top plate, then stems.
- **Sub-assemble in the air.** D10 is clipped onto the LED matrix while the matrix is held above the box (Step 3), then both go in together (Step 4).
- **Check before covering.** The wire-routing inset [009] comes on the last step before the lid plate hides the inside.

### Motion

- **Hover pose.** A new rigid part fades in already at its hover pose; it never flies in from off-screen. In 6 of 7 animated cases the hover is straight above the seat: 68.0 (D9), 64.3 (D6), 88.6 / 88.6 / 90.1 / 84.4 (D11 posts), 67.8 (D7), 54.1 (D8), 50.2 mm (stem). There is no fixed hover distance; the range is 50 to 90 mm and the long posts sit highest.
- **Seat.** The completed step tweens the part along a straight line back to the seat. No rotation is animated anywhere in the guide.
- **Two-leg insertion.** The one non-vertical case (D10, Step 3) starts 19.3 mm below and 41.2 mm sideways, and is played as hover, auto Transition (up 19.3), completed (across 41.1).
- **Wired assemblies are swapped, not moved.** The LED matrix exists as 3 pre-posed copies, each with its own 3 routed wires and 3 connector housings (lying beside the box, held 56.6 mm above the seat, seated). Steps 2c and 4c cross-fade between copies; nothing with a wire attached is ever tweened (2 of 2 cases).
- **Deliberate partial seating.** The posts stop 7.0 mm short in 6c and 7c and are pushed home in a separate step shown from underneath.

### Red lead lines

- **Style.** 3D lines, colour #ff0000, thickness scale 5. 29 line objects are shown, each for exactly one viewer step.
- **Where.** On hover steps only (10 of 12; Steps 2 and 13 have only an eye icon). Never on a completed step.
- **How many.** One per mating feature pair, 1 to 4 per step: 4, 2, 2, 4, 2, 2, 4, 4, 4, 1.
- **Geometry.** 27 of 29 are single straight segments exactly parallel to the insertion axis (vertical). The other 2 are 3-point L-shaped polylines that trace the two-leg path of D10.
- **End points.** One end on the leading mating feature of the moving part (underside of a tab, bottom tip of a post, a slot in a plate, bottom face of a stem), the other on the receiving feature of the fixed part (notch in a wall top, wall tab, slot in a plate, hole).
- **Length vs hover offset.** Equal when the two features end up face to face: Step 1 68.0 / 68.0, Step 4 57 / 56.6, Step 5 62 to 68 / 64.3, Step 12 48.1 / 50.2. Shorter when the part passes through the feature: Steps 6 and 7 about 44 / 88 (ratio 0.44 to 0.50), Step 10 49 / 67.8 (0.72). Step 11 is the exception at 59 to 63 / 54.1.
- **Also used without a new part.** Step 4 (lowering) and Step 8 (final push) carry lead lines although nothing appears.

### Eye icon and inset images

- **Eye icon.** A black eye glyph image (width 7.8% of the viewport) with a 5 px light-blue (#7fdbff) straight leader ending in a dashed "life saver" ring on the target. Used 3 times, always on a hover step with no new part: "handle this existing part" (Step 2), "look here" (Step 8), "do the same for the rest" (Step 13). Step 4 is the one no-new-part step without it.
- **Inset detail image.** A pre-rendered close-up in a rounded rectangle with a 5 px light-blue border and an eye glyph inside the picture, connected by the same leader and ring. Used twice, both on completed steps, to show a result that is hard to see: wire routing inside the box (4c) and a tab through the bottom plate (9c).
- **Placement.** Callouts sit in white space 10 to 35% of the viewport away from their target, mostly above or left of the model, never over it. Each lives for exactly one step.

### Labels

- **Quantity label.** "64X": Arial bold, 6em on a base font size of 20, colour #7fdbff, no container, no leader, placed just right of the isolated part. It is the only text label.

### Camera

- **Moves only on hover steps.** The camera moves on entering 9 of 12 hover steps and on 0 of 12 completed steps; the completed step always keeps the hover framing exactly. Steps 10, 11 and 13 reuse the previous view because the action is on the same side.
- **Re-aim to the working side.** Rotations between views range from 5 to 117 deg. Build-step elevation stays between 20 and 34 deg; the orbit target stays within about 25 mm of the model centre.
- **Few zoom levels.** Only five distances occur: 173 (card), 258, 300, 321 (title and completed), 374 mm. 258 is used for small or close work, 300 when tall parts hover, 374 for the stems.
- **Framing.** The view is sized so the hovering part and its target both fit; the posts in Steps 6 and 7 touch the top edge of the saved render. The model occupies roughly a third of the frame width.
- **Underside view.** Step 8 goes to elevation -57 deg, flips the scene up-axis to -y and ghosts the covering parts to 50% opacity; an auto Transition then flips back before the next part.
- **Section card to next step.** The card and Step 12 share the same view direction (rotation 0.0 deg); only the target and distance change (x0.46 zoom out).
- **Lens.** Perspective, 45 deg field of view.

### Look

- **Scene.** Pure white background, no ground or shadows, view cube on, navigation overlay along the bottom.
- **Rendering.** Flat toon shading with thin black outlines on every part.
- **Colour roles.** Red is reserved for insertion lines; light blue for attention callouts and the quantity label; black for the eye glyph.

## Part looks

| part | look |
|---|---|
| Plywood parts (walls, bottom, D6/D7/D8 plates, D9/D10 supports, D11 posts) | Burlywood tan #deb887, slightly darker on shaded faces, black outlines; engraved ID text (D2 to D11) in near-black #1e1616 |
| Front panel D2 | Same tan body but the outer face is brown #855e42; carries the round black push button |
| LED matrix | Black PCB #1e1616 with an 8x8 grid of white/silver LED packages (#fbfbfb, #a6a9aa, #b1b3b3); black right-angle header underneath |
| Ribbon to the matrix | Three wires: white #ffffff, light grey #b1b3b3, purple #4e008e; black connector housings #1e1616 at each end |
| Wires inside the box | Red #ef3340 and black #2d2926 |
| LED stems | White #ffffff square rods with black outlines (read as very light grey in shade) |
| USB cable | Black cable and moulded plug (#1e1616 / #2d2926), silver shell #a6a9aa with white insert |
| Breadboard / Nano / resistors | White breadboard with black holes and red/blue rails; silver and white Nano; resistor bodies blue #0074d9 with coloured bands. Only glimpsed through the open box in [001] to [008] |
| Ghosted parts (Step 8 only) | Same colours at 50% opacity |
| Lead lines | Red #ff0000, thickness 5 |
| Callouts | Black eye glyph; leader, ring and inset border light blue #7fdbff; "64X" in the same light blue |

## Anomalies

1. **Step numbering.** [016] "Step 8" is completed by [017] "Step 9c". There is no "Step 8c" and no "Step 9", so the guide's numbers run 1 to 13 for 12 actual steps. The same pair is correctly "Step 14 / 14c" in Part 3+4.
2. **Mis-anchored lead line.** In Step 5 [010] one of the four lines is anchored to the bottom plate instead of a wall tab: 102.8 mm against 62.3 to 67.8 mm for the others. It visibly overshoots the wall top and runs down in front of the LED matrix.
3. **Dashed vs solid.** The 8 lines in Steps 10 and 11 are stored as `dashed`; the other 21 are `solid`. In the saved renders all look solid. The same split exists in Part 3+4 and the Full Build, so it is consistent but not visibly meaningful.
4. **Uneven hover heights for identical parts.** The four posts hover at 88.6, 88.6, 90.1 and 84.4 mm, with lead lines of 43.8, 43.4, 44.1 and 37.4 mm.
5. **Inconsistent line length rule.** Step 11's lines (59.1 to 63.2 mm, all four different) are longer than the plate's 54.1 mm travel, while Step 10's (49 mm) are shorter than its 67.8 mm travel.
6. **Anchor ring colour.** The eye-icon ring in Step 8 is teal #39cccc; the other four callouts use #7fdbff.
7. **Boilerplate left in.** The Start step still carries Cadasio's default description "A Start point for your project - feel free to rename, reorder or delete".
8. **Hidden leftovers.** 8 hidden authoring steps: "Step 60" at index 0 (also the project's start step id) and seven duplicates named Step 4, Step 2, Step 2c, Step 4c, Step 5, Step 5c, Step 6 between Step 4c and Step 5. 52 of 89 annotation objects (36 lines, 12 images, 4 arrows) are never shown.
9. **Silent part toggles.** "Paper-1" switches on at Step 2c with no introduction and is not noticeable in the renders; two light-grey wire-cap solids are visible only on Start and Completed View.
10. **Ghosting restored in two stages.** The bottom plate and one of three ghosted wall solids return to opaque at "9c"; the other two solids return at the Transition.
11. **Seated poses are not exactly the CAD pose.** Stems end 5.4 mm below their CAD position (pushed deeper), the top plate 0.5 mm off, the seated matrix 0.2 mm off.
12. **Label case.** "64X" here and in Part 3+4, "64x" in the Full Build.

## Relation to the other LSM guides

Checked against Part 3, Part 3+4 and the Full Build (step lists, digests, two Part 3+4 contact sheets).

- **Same content, renumbered.** Part 4 Steps 1 to 13 are Part 3+4 Steps 7 to 18 and Full Build Steps 27 to 38, cut from one master project. The camera moves match to the decimal for most steps (82.2, 116.9, 110.2, 74.6, 0.0, 12.9 deg).
- **Start state.** Part 4's Step 1 state is Part 3's Completed View (open box, LED matrix lying outside).
- **Entry differs.** In the combined guides an auto Transition (53.1 deg, up-axis back to +y) precedes the D9 step; Part 4 instead moves the camera 109.5 deg from its title page.
- **Hand-tweaked copies.** Lead-line lengths differ slightly per copy (D9 lines 68.0 here, 63.6 to 65.7 in Part 3+4, 64.6 in the Full Build). The mis-anchored line moves around: Step 5 here, the post step in Part 3+4 (98.6 mm).
- **Missing inset.** The lid-plate step has an extra top-view inset of the LED matrix in Part 3+4 and the Full Build that Part 4 lacks.
- **Zoom.** Part 4 and the Full Build zoom to 258 mm for the D10 step; Part 3+4 stays at 300 mm.
- **Typos elsewhere.** Part 3+4 ends on "Copmleted View"; Part 4 spells it correctly but has the 8 / 9c numbering slip that Part 3+4 does not.
- **Section cards.** "LED Stems" appears in all three. Part 4 has only this one card; the Full Build also has "Capacitor", "LED Matrix Diagram" and "Mini USB Cable".
