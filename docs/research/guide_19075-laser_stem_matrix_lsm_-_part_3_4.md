# Guide report: Laser Stem Matrix (LSM) - Part 3 + 4

- Guide id: `19075-laser_stem_matrix_lsm_-_part_3_4` (kit LSM, role: combined)
- Sources read: digest `.md`/`.json` for this guide, Part 3 and Part 4; all 6 contact sheets and ~25 individual frames (plus 2559 px crops from `thumbs_raw`); targeted queries on `cadasio_raw` for the three guides and the Full Build.
- Working files (scripts, tracker output, crops) are in `reports/_work/`.

## 1. Summary

This guide takes the finished electronics tray from Parts 1-2 (base D1 with breadboard, Nano, LED matrix on a 3-wire lead, USB cable) and builds the wooden enclosure and light-guide stack around it: four housing walls (D2, D4, D3, D5), two wide LED supports (D9), the clip-on LED support (D10), seating of the 8x8 LED matrix, three perforated shelves (D6, D7, D8) on four corner posts (D11), and finally 64 white stems. It is 43 viewer steps: a title page, 18 numbered steps each authored as a strict `Step N` (hover + annotations) / `Step Nc` (seated, annotations gone) pair, 4 auto-advancing `Transition` steps, one section card (`LED Stems`, "64X"), and a final view (misspelt `Copmleted View`). There is no instruction text anywhere (all step descriptions empty, no popups); the whole guide communicates through part motion, red lead lines (43 shown), 2 red arrows, 5 eye icons, 3 picture insets, the engraved part IDs modelled on the wood (D1...D11) and hover tooltips. No wires, screws or boards are added in this guide - only laser-cut wood and stems; the only "electronics" actions are re-posing the already wired LED matrix (3 times) which is done by cross-fading between pre-modelled poses rather than by tweening.

## 2. Data caveat that matters for this guide (digest under-reports)

The per-step digest for this guide is unreliable for the wooden parts, so the step table below is built from the thumbnails plus my own pass over the raw step deltas (`reports/_work/track2.py`).

- 96 depth-1 components carry `hidden: true` in the assembly tree (all four walls `LSM_Side1..4`, `LSM_Lens_Bottom/Middle/Top`, the four `LSM_LensSupport`, five of the `8x8 LED` pose variants, the 64 stems). Their leaf solids are switched on by step properties, but `digest.py` requires every ancestor to be visible, so the digest never reports these parts appearing or moving. Example: digest [003] Step 2 says "0 appear, parts still displaced: none" while the thumbnail shows wall D4 hovering 69 mm away with 4 lead lines; the raw data has `position z=33.2 units` (= 69.4 mm) on the D4 solids at Step 2 and `0` at Step 2c. The digest's "on screen now: 23 parts" stays flat for the same reason (true count rises from 25 to 40 top-level parts, then 103-105 with stems).
- Offsets in the digest are in the parent component's local frame, not world. Example: digest [015] says the D9 supports appear displaced `[0,0,-65.3] (-Z)`; in world axes that is `+Y (up) 65.3 mm`, which is what the thumbnail and the `-Y (down)` lead lines show. All offsets below are converted to world axes (Y up).
- The 64 stems (and nothing else) have a CAD "seated" pose ~1.6 m from where they are used, so the digest's "still displaced: LSM_Stem 64" is an artefact, not a hover.
- Lead-line lengths are computed from the stored end points and are good to a few mm.

## 3. Step table (every viewer step)

Index = digest/thumbnail index. Camera column: `d` = distance mm, `el` = elevation, `az` = azimuth; "static" = identical to previous step. All steps are 800 ms.

| idx | name | kind | what is added or done | annotations | camera |
|---|---|---|---|---|---|
| [000] | Start | title page, pause | Finished model (box, 3 shelves, 64 stems, USB cable) as hero on the right half. Step description still holds Cadasio's placeholder text. | TechBox logo SVG at (2,5)% w 37.6%; title PNG "Laser Stem Matrix (LSM) / Part 3 + 4 / (c) 2025 TechBox..." at (2,61)% w 42.9%. No leaders. | d321 el27 az57 |
| [001] | Step 1 | hover, pause (page transition = fade) | Model cuts back to the electronics tray (base D1 with breadboard, Nano, loose LED matrix, USB cable). Housing Left Side D2 with the pre-fitted black push button and its red + black wires is shown detached about 45 mm from base D1 (a separate "detached" model variant; it fades in). | 1 red 3D arrow, 45 mm, pointing from the panel toward the base edge. | rot 102 deg; d300 el51 az-133 |
| [002] | Step 1c | completed | D2 variant cross-fades to the seated variant (tabs in base slots, button wires re-routed). No tween. | none (arrow removed) | static |
| [003] | Step 2 | hover | Housing Rear Side D4 fades in 69 mm out along -X. | 4 solid red lead lines, 64-68 mm: 2 from base D1 edge tabs to D4 slots, 2 from D2 edge tabs to D4 slots. | rot 57 deg, zoom out; d350 el43 az-45 |
| [004] | Step 2c | completed | D4 tweens 69 mm onto the tabs. | none | static |
| [005] | Step 3 | hover, no new part | Nothing changes in the model: instruction is "carry the LED matrix over wall D4". | Red arrow 103 mm pointing -X, drawn above the model; eye icon at (77,32)% with cyan leader to the matrix centre. | top-down: rot 43 deg; d300 el85 az-18; up-axis -z |
| [006] | Step 3c | completed | Matrix and its 3 wires cross-fade to a pose outside D4, wires lying in the notch in D4's top edge. | Eye icon at (30,26)% with leader to the wires at the notch (the only eye icon on a "c" step outside an inset). | static |
| [007] | Transition | auto (play) | No part change. View flips so the box reads as standing on wall D4, base D1 vertical. | none | rot 143 deg; d300 el-48 az146; up-axis +x |
| [008] | Step 4 | hover | Housing Right Side D3 fades in tilted about 22 deg and 64 mm away. | 2 lead lines (40.5, 40.6 mm) from D3's two end tabs to two slots in D4. | static |
| [009] | Step 4c | completed (stage 1) | D3 translates 46 mm so its tabs sit in D4's slots; stays tilted 22 deg. | none | static |
| [010] | Step 5 | hover, same part | Nothing moves. | 2 short lead lines (12.5, 15.6 mm) from base D1 edge tabs to slots in D3: shows the swing-closed. | static |
| [011] | Step 5c | completed (stage 2) | D3 rotates 22 deg to upright and closes the last 32 mm. | none | static |
| [012] | Step 6 | hover | Housing Front Side D5 fades in 42 mm off (reads as a lid above the tipped box). | 6 lead lines, 38-43 mm: one per tab, 2 from D3, 2 from D2, 2 from D1, each into its D5 slot. | rot 90 deg; d300 el41 az129 |
| [013] | Step 6c | completed | D5 tweens 42 mm onto the six tabs. Walls complete. | none | static |
| [014] | Transition | auto (play) | No part change. Back to an upright three-quarter view. This is the Part 3 / Part 4 seam. | none | rot 53 deg; d300 el31 az-165; up-axis +y |
| [015] | Step 7 | hover | 2x Wide LED Supports D9 fade in 65 mm above the box. | 4 lead lines, 64-66 mm, vertical: each end notch of each D9 to its slot in the top edge of walls D3 / D2. | static |
| [016] | Step 7c | completed | Both D9 drop 65 mm together. | none | static |
| [017] | Step 8 | hover, no new part | Nothing changes: "pick up the matrix". | Eye icon at (50,18)% with leader to the matrix centre. | rot 35 deg; d300 el24 az-126 |
| [018] | Step 8c | completed | Matrix and wires cross-fade to a pose lifted above the open box. (A 0.2 mm "Paper" sheet also becomes visible silently.) | none | static |
| [019] | Step 9 | hover | LED Support D10 fades in beside/below the lifted matrix edge (19 mm below and 43 mm out from where it clips on). | 2 red elbow lead lines (3 points each): straight up from each D10 hook, then horizontally onto the matrix edge. They trace the two-leg path. | rot 3 deg; d300 el21 az-126 |
| [020] | Transition | auto (play) | Leg 1: D10 rises 19 mm. | lead lines removed | static |
| [021] | Step 9c | completed | Leg 2: D10 slides 43 mm horizontally onto the matrix edge. | none | static |
| [022] | Step 10 | hover, no new part | Nothing moves (matrix + D10 still lifted). | 2 vertical lead lines, 57 mm, between D10's end tabs and the notches in the top edges of walls D4 and D5. | rot 84 deg; d300 el33 az-30 |
| [023] | Step 10c | completed | Lifted matrix + D10 cross-fade to the seated matrix inside the box, wires re-routed. | Picture inset at (14,11)% w 16.8%, cyan rounded border, eye icon drawn inside the picture: x-ray close-up of the wires passing the notch. Cyan leader + ring to the matrix corner. | static |
| [024] | Step 11 | hover | Bottom Shelf D6 fades in 64 mm above. | 4 vertical lead lines, 59-68 mm, D6 slots to wall-top tabs (D2, D4 x2, D5). Picture inset at (68,14)% w 19.6%: top view of the seated matrix with 4 red rectangles at its corners; cyan leader to matrix centre. | rot 63 deg, zoom in; d258 el31 az47 |
| [025] | Step 11c | completed | D6 drops 64 mm. | none | static |
| [026] | Step 12 | hover | 2x Shelf Supports D11 fade in 89 mm above two corners. | 2 vertical lead lines (54 mm and 99 mm) from each post's bottom tip down to its corner slot. | rot 14 deg, zoom out; d300 el21 az36 |
| [027] | Step 12c | completed | Both posts drop 82 mm and stop 7 mm proud. | none | static |
| [028] | Step 13 | hover | The other 2x D11 fade in 84 / 90 mm above the other two corners. | 2 vertical lead lines (37, 43 mm). | rot 82 deg; d300 el23 az-55 |
| [029] | Step 13c | completed | Both drop 77 / 83 mm, also 7 mm proud. | none | static |
| [030] | Step 14 | hover, no new part | Underside view; base D1 and wall D5 go to 50% opacity so the post tips can be seen. | 4 short lead lines (about 17 mm) at the four corner slots of the base; eye icon at (20,25)% with leader to one corner. | rot 117 deg, zoom in; d258 el-57 az49; up-axis -y |
| [031] | Step 14c | completed | All four D11 move the last 7 mm through the base slots; base opaque again. | Picture inset (close-up of post tips protruding through the base, eye icon inside the picture), cyan border, leader to the corner. Thumbnail shows it lower-left; stored position is (93,48)%. | static |
| [032] | Transition | auto (play) | No part move; remaining opacity restored. Back to top three-quarter view. | none | rot 110 deg, zoom out; d300 el34 az123; up-axis +y |
| [033] | Step 15 | hover | Middle Shelf D7 fades in 68 mm above. | 4 vertical lead lines, 49 mm, from the top tip of each D11 post to the matching slot in D7 (style stored as "dashed"; rendered thumbnail looks solid). | static |
| [034] | Step 15c | completed | D7 drops 68 mm. | none | static |
| [035] | Step 16 | hover | Top Shelf D8 fades in 54 mm above. | 4 vertical lead lines, 59-63 mm, posts to D8 slots (stored "dashed"). | static |
| [036] | Step 16c | completed | D8 drops 54 mm. | none | static |
| [037] | LED Stems | section card, pause (page transition = fade) | Everything hidden except one stem. | Text "64X": Arial bold 6em, light blue #7fdbff, no box, no leader, at (53,21)% just right of the stem. | rot 75 deg, zoom in x1.73; d173 el31 az32 |
| [038] | Step 17 | hover | Assembly fades back in; the single stem hovers 55 mm above a corner hole of D8. | 1 vertical lead line, 49 mm, from the stem's bottom face into the corner hole. | no rotation, zoom out x0.46; d374 el31 az32 |
| [039] | Step 17c | completed | Stem drops 55 mm through D8/D7/D6 onto its LED. | none | static |
| [040] | Step 18 | hover, repeat | Nothing changes: "do the same for the rest". | Eye icon at (55,14)% with leader to the seated stem. | static |
| [041] | Step 18c | completed | The other 63 stems fade in already inserted (no per-stem motion). All 64 sit 9.7 mm higher than the stem did in 17c. | none | static |
| [042] | Copmleted View | final, pause | Stems settle 9.7 mm; small orbit and zoom to a beauty view. | none | rot 13 deg, zoom in; d321 el39 az44 |

## 4. Conventions found

### 4.1 Structure

- **Fixed skeleton**: `Start` -> numbered pairs -> final view. 43 viewer steps = 1 Start + 36 (18 x `Step N`/`Step Nc`) + 4 `Transition` + 1 section card + 1 final. Always true: every numbered step has both halves, in order, numbered consecutively 1-18 with no gaps.
- **`Step N` = hover/explain, `Step Nc` = result.** Always true (18/18): all red lines and arrows shown on `Step N` are gone on `Step Nc`; every annotation object is used on exactly one viewer step (0 of the 56 shown annotations persists to a second step).
- **Title page**: logo top-left, title/subtitle/copyright as one image lower-left, finished product on the right, no leaders.
- **Section card** (1 here: `LED Stems` [037]): isolates one part on an empty stage and gives a quantity ("64X") immediately before the repeated operation. Named by the part, not numbered.
- **`Transition` steps** are `play` (auto-advance), 800 ms, hidden from the step picker and with the navigation overlay hidden (4/4). Three reposition the camera and switch the scene up-axis ([007], [014], [032]); one is the middle leg of a two-leg part move ([020]).
- **No text**: 0 step descriptions (other than leftover placeholder on Start), 0 popups, 1 text label in the whole guide.
- **Page transitions**: stored `transition` is `none` (animated tween) for all steps except `fade` on Step 1 (leaving the title page) and on the `LED Stems` card - i.e. a cross-fade is used where the whole stage content is replaced.
- **Hidden authoring leftovers** are kept, not deleted: 5 hidden steps (a base-state step "Step 51" at position 0 and hidden duplicates named "Step 2", "Step 2c", "Step 8", "Step 8c").

### 4.2 Granularity

- 13 steps introduce parts: 9 introduce exactly one part (Steps 1, 2, 4, 6, 9, 11, 15, 16, 17); 3 introduce two identical parts together (Step 7: 2x D9; Steps 12 and 13: 2x D11 each); 1 introduces 63 identical parts at once without motion (Step 18c).
- **Identical parts are grouped only as far as one camera view can show them clearly**: the four D11 posts are split 2 + 2 with an 82 deg camera turn between them, not shown as 4.
- **"Do one, then repeat"** for high-count parts: one stem is animated (Step 17), then an eye icon on that stem (Step 18) and the remaining 63 simply appear (18c).
- **Awkward insertions are split over two numbered steps**: wall D3 is "tabs into D4, tilted" (Step 4) then "swing upright" (Step 5); the D11 posts are "drop in from above" (12, 13) then "push through the base, seen from below" (14).
- **Handling steps with no new part get their own number** (4 of 18: Steps 3, 8, 10, 14) - moving the matrix, lifting it, lowering it, pushing the posts home.
- A sub-assembly with wires already attached (D2 with push button) is added as one unit.

### 4.3 Ordering

- Outside-in then bottom-up: walls (D2, D4, D3, D5 = left, rear, right, front) -> internal supports (D9) -> matrix with its clip (D10) seated -> shelves bottom (D6), posts (D11), middle (D7), top (D8) -> 64 stems last.
- The loose, wired LED matrix is deliberately parked outside the box (Step 3) before the walls close, then brought back in (Steps 8-10).
- Electronics are complete before this guide starts; nothing is wired here.

### 4.4 Motion

- **New rigid part**: fades in at its hover pose on `Step N` (never flies in), then tweens in a straight line to its seat on `Step Nc` in 800 ms. True for all 11 rigid-part steps (2, 4, 6, 7, 9, 11, 12, 13, 15, 16, 17).
- **Hover offset is along the real insertion axis and axis-aligned**: of the 11 rigid-part steps, 7 are vertical (part straight above its seat: Steps 7, 11, 12, 13, 15, 16, 17), 2 horizontal (Step 2: 69 mm; Step 6: 42 mm), 1 tilted (Step 4), 1 two-leg (Step 9). The 7 mm push at Step 14 is vertical too.
- **Hover distances**: 42, 54, 55, 64, 64, 65, 68, 69, 84-90 mm (the D10 clip travels 19 mm + 43 mm in its two legs). Parts are 50-110 mm in size, so the hover gap is roughly half to one part length - always clear of the assembly.
- **Two-leg move** (Step 9): hover -> auto `Transition` (rise 19 mm) -> `Step 9c` (slide 43 mm). The one place a part needs an L-shaped path.
- **Rotation** appears once: D3 is shown tilted 22 deg, translated in tilted, then rotated upright.
- **Not-quite-seated poses** are used to carry state between steps: D11 posts rest 7 mm proud from 12c/13c until 14c.
- **Flexible/wired things are never tweened; they cross-fade between pre-modelled poses** (D2 + button wires at 1c; matrix + 3 wires at 3c, 8c, 10c). The LED matrix exists as four pose variants (beside the base, outside wall D4, lifted above the box, seated), each with its own set of three routed wires.
- **Temporary transparency** is used once (Step 14: base and front wall at 50%) and removed on the next step.
- **The model is never rotated to re-orient it**; the camera moves and the scene up-axis is switched (-z top-down at Step 3, +x at [007], +y at [014], -y at Step 14, +y at [032]).

### 4.5 Red lead lines and arrows

- **Lead lines are the default hover annotation**: on 14 of 18 hover steps (2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17), 43 lines in total, 1-6 per step (counts: 4, 2, 2, 6, 4, 2, 2, 4, 2, 2, 4, 4, 4, 1).
- **One line per mating feature pair, tab/tenon to slot**: each line starts on a tab, notch or tip of one part and ends in the slot/hole that receives it (small red dot visible inside the slot). Step 6 has 6 lines for 6 tabs; Steps 11, 15, 16 have 4 lines for 4 corner slots; the stem has 1.
- **Lines are parallel to the travel direction** and, when they join features that end up coincident, their length equals the hover offset within a few mm: Step 2 (64-68 vs 69), Step 6 (38-43 vs 42), Step 7 (64-66 vs 65), Step 11 (59-68 vs 64), Step 10 (57 vs the 57 mm lift). Where a part passes through the target the line is shorter or longer than the travel (posts: 37-54 mm vs 77-83 mm travel; D7: 49 vs 68; stem: 49 vs 55).
- **Path-shaped lines**: the two Step 9 lines have 3 points and trace the up-then-across path.
- **Lead lines are also used with no motion pending in that step**, to show what goes where: Step 5 (swing), Step 10 (lower the matrix), Step 14 (push posts through).
- Style: `#ff0000`, constant screen width (`scale 5`, not world units), 35 solid + 8 stored as dashed (Steps 15, 16 only; dash 10 / gap 5 - not distinguishable from solid in the saved renders).
- **Arrows (2 shown) are used only where a wired assembly is moved by hand and shown as a pose swap**: Step 1 (bring the button panel to the base, 45 mm, fat arrow) and Step 3 (carry the matrix across, 103 mm, drawn floating above the model in the top view). Exceptions: the other two pose-swap steps do not use an arrow (Step 8 has only an eye icon, Step 10 uses lead lines).
- Every hover step carries at least one annotation (18/18): arrow only (Step 1), lead lines only (12 steps, including the single-line stem step), arrow + eye (Step 3), eye only (Steps 8, 18), lines + eye (Step 14), lines + inset (Step 11).

### 4.6 Labels, eye icon, insets, tooltips

- **Text labels**: exactly one ("64X"), on the section card: Arial bold 6em, `#7fdbff`, no container, no leader, placed just right of the part.
- **Part identity comes from the engraved IDs modelled on the parts** (black "D1"..."D11" decals on the wood) and from hover tooltips, not from callouts.
- **Tooltips** are enabled for every part and show its `Description`: "Housing Base - Part D1", "Housing Left Side - Part D2", "Housing Right Side - Part D3", "Housing Rear Side - Part D4", "Housing Front Side - Part D5", "Bottom Shelf - Part D6", "Middle Shelf - Part D7", "Top Shelf - Part D8", "Wide LED Supports - Part D9", "LED Support - Part D10", "Shelf Supports - Parts D11", "LED Stems", "LED Matrix", "Nano Board", "Breadboard", "Mini USB Cable", "Black Push Button", "Breadboard Wires (M-F)", "12 kOhm Resistor", "330 Ohm Resistor", "Capacitor".
- **Eye icon** (black eye PNG, 7.8% of viewport width, no box) with a thin cyan `#7fdbff` leader ending in a "life-saver" ring on the feature. 5 standalone uses: Step 3 (matrix), 3c (wires in notch), Step 8 (matrix), Step 14 (corner slot), Step 18 (stem). It means "look at / act on this" when nothing is flying in (3 of the 4 no-new-part hover steps plus the repeat step), or "check this" on a result (3c).
- **Picture insets** (3: 10c, 11, 14c): a rendered close-up or alternate view in a white rectangle with a 5 px cyan `#7fdbff` rounded border, 14-20% of viewport width, cyan leader + ring to the feature it explains; two of the three have the eye icon baked into the picture. Used on a `c` step to show a result that is hidden in the main view (wire path under the matrix; post tips through the base) and once on a hover step as an orientation aid (top view with red rectangles).
- Placement: icons and insets sit in empty white space 10-25% of the viewport away from the model, positioned in screen space; only the leader tip tracks the 3D feature.

### 4.7 Camera

- **Never moves between `Step N` and `Step Nc`** (18/18).
- Moves on entering 12 of 18 hover steps. The 6 that do not: 3 follow a camera `Transition` (Steps 4, 7, 15) and 3 continue work in the same place (Steps 5, 16, 18).
- Rotations on entering a hover step range from 0 to 117 deg; large turns happen both directly (Step 1: 102, Step 6: 90, Step 10: 84, Step 13: 82, Step 14: 117) and via `Transition` (143, 53, 110), so "big turn = Transition" is not a rule. What the three camera Transitions share is that they follow a `c` step and switch the up-axis to set up a new working orientation.
- **Working distance is quantised**: d300 on 30 of 43 steps; otherwise one wheel-click steps of x1.17 (258 on 4, 350 on 2), 321 for Start/final, 374 for the tall stem steps (4), 173 for the section card.
- **Framing**: a three-quarter view from above (elevation 21-51 deg on 14 of the 18 hover views) chosen so the mating slots face the camera; the model plus hovering part occupy roughly the middle third of a wide frame with white margin for icons. Special views: top-down el85 (Step 3), from below el-48 (Steps 4-5) and el-57 (Step 14).
- Zoom follows the size of what is happening: in for small details (d258 for Step 11 and the underside check), out when a tall part hovers (d350 for D4 at 69 mm; d374 for the stem).
- Project settings: perspective camera FOV 45, camera tween (speed 2, no orbit animation), view cube shown, bottom horizontal navigation overlay, auto-start, previous-step animation on.

### 4.8 Look

- White background `#ffffff`; every part rendered "toon" (flat two-tone shading) with normal black edge lines; scene-level edges/silhouettes off; ambient light 2.

## 5. Part looks (from the renders)

| part | look |
|---|---|
| Plywood parts (base D1, walls D3/D4/D5, shelves D6-D8, supports D9/D10/D11) | Flat tan `#deb887`, lighter on lit faces and a darker tan on shaded faces (toon), thin black outlines; slots and tabs drawn crisply; 3 mm thick. |
| Wall D2 (button panel) | Same tan, but its outer face is a distinctly darker brown `#855e42` - the one wall you can always recognise as the front. |
| Engraved part IDs | Black `#1e1616` bold sans decals ("D1"..."D11") on the wood face; they move with the part. |
| Shelves D6/D7/D8 | Tan plates with an 8x8 grid of small square holes and 4 rectangular corner slots. |
| LED stems (x64) | Pure white `#ffffff` 3.2 mm square rods, 67 mm long, thin black outline, almost paper-white against the background. |
| 8x8 LED matrix | Black PCB with 64 light grey/silver square LED packages; black 3-pin connector on one edge. |
| Matrix wires | Three jumper wires: white, light grey/silver, and purple (`#4e008e`), black Dupont housings at the ends. |
| Push button and its wires | Black round button with a silver hex nut on the inside; one red and one black wire. |
| Breadboard | White with printed rows/letters and red/blue rail lines. |
| Arduino Nano | Dark blue board, silver/black pin headers, white mini-USB socket. |
| Resistors, capacitor | Blue resistor bodies with coloured bands; silver capacitor. |
| USB cable | Black cable and overmould, silver plug with white insert. |
| Annotations | Lead lines and arrows pure red `#ff0000`; eye icon black; leaders, rings, inset borders and the "64X" text light blue `#7fdbff`. |

## 6. Combined guide vs Part 3 + Part 4 played back to back

Part 3 has 13 viewer steps (Start, Steps 1-5 with one Transition, Completed View); Part 4 has 29 (Start, 12 step pairs labelled up to 13, two Transitions, LED Stems, Completed View). Back to back = 42. The combined guide has 43.

### 6.1 Renumbering

| combined | source |
|---|---|
| Start [000] | Part 4 Start (same camera d321 el27 az57, same finished model); only the title image differs ("Part 3 + 4") |
| Step 1 / 1c [001-002] | **not in Part 3 or Part 4.** It is the "attach button panel D2" step: Part 2 Step 12, Part 1+2 Step 20, Full Build Step 21 |
| Steps 2-6 [003-013] | Part 3 Steps 1-5 (N = n + 1), including Part 3's Transition before its Step 3 |
| Transition [014] | replaces Part 3 "Completed View" + Part 4 "Start" |
| Steps 7-13 [015-029] | Part 4 Steps 1-7 (N = n + 6), including Part 4's Transition inside Step 3 |
| Step 14 / 14c [030-031] | Part 4 "Step 8" / "Step 9c" (Part 4 mislabels this pair) |
| Transition [032], Steps 15-16 [033-036] | Part 4 Transition, Steps 10-11 (N = n + 5) |
| LED Stems [037], Steps 17-18 [038-041] | Part 4 LED Stems, Steps 12-13 (N = n + 5) |
| Copmleted View [042] | Part 4 Completed View (same camera d321 el39 az44) |

The combined guide is a clean 1-18; Part 4's numbering gap (no "Step 8c", no "Step 9") is not carried over. Step count check: 5 (Part 3) + 12 (Part 4) + 1 (extra D2 step) = 18.

### 6.2 Start / Completed views kept and dropped

- Kept: one Start (Part 4's, i.e. the fully finished product) and one final view (Part 4's).
- Dropped: Part 3's Start (which showed the Part-3 end state, the open box, subtitled "Part 3"), Part 3's Completed View (d221 el42 az35), and Part 4's Start.
- No "Part 4" divider card or recap is inserted.

### 6.3 Seam

- Part 3 ends on Step 5c in the tipped view (d300 el41 az129), then cuts to its Completed View.
- The combined guide goes Step 6c [013] -> one auto-advancing `Transition` [014] (800 ms, rotates 53 deg, up-axis back to +y) that lands exactly on Part 4 Step 1's camera (d300 el31 az-165) -> Step 7 [015] with the camera static. The student never stops at the seam.
- In Part 4 the two D9 supports are visible in the Start hero and animate upward out of it into their hover pose; in the combined guide they simply fade in at hover.

### 6.4 Content that differs

- **Extra first step** (Step 1/1c, the D2 button panel) overlaps the end of Part 2 / Part 1+2, where the same action carries an eye icon as well as the arrow.
- **Extra inset** on combined Step 11 (top view with red corner rectangles); Part 4 Step 5 has none.
- **Cameras**: identical (distance, elevation, azimuth to the degree) on 31 of the 40 matched steps; different on 9: combined Step 3/3c (d300 vs Part 3's d350), Step 8/8c (el24 az-126 vs el25 az-128), Step 9 / Transition / 9c (d300 el21 az-126 vs Part 4's d258 el20 az-128) and Step 10/10c (d300 el33 az-30 vs d258 el22 az-35). Against the Full Build 12 of 42 steps differ (the same Steps 8-10 plus the tipped view of Steps 4-5: el-48 az146 here vs el-35 az141).
- **Hover distances / lead lines**: D9 supports hover 65.3 mm (Part 4: 68.0); stem drops 55 mm (Part 4: 50 mm); Step 12 lead lines are 54 and 99 mm with one free end (Part 4: 43 and 44 mm, both anchored); one Step 11 line is 59 mm (Part 4: 103 mm).
- **D10 clip**: a different instance and start pose is used (measured from its final seat in the box: combined 14 mm up / 29 mm out, Part 4 10 mm up / 38 mm out; the two legs are 19 + 43 mm here and 19 + 41 mm in Part 4), and the seated D10 is not switched on at Step 10c in the combined guide (it is in Part 4 Step 4c); it only returns at Step 17. Hidden under the matrix, so barely visible.
- **Stems**: Part 4 keeps all stems at one height; the combined guide shows the 64 stems 9.7 mm high at 18c and drops them at the final view.
- **Annotation placement** shifts by a few percent (eye at Step 3: (77,32) vs (72,34); Step 8: (50,18) vs (57,18); Step 18: (55,14) vs (56,12)); the 14c inset is stored at (93,48)% vs Part 4's (19,47)%.
- **Names**: final step is "Copmleted View" (Part 4: "Completed View").
- **Housekeeping**: 5 hidden authoring steps (Part 3: 1; Part 4: 8). Placeholder Start description present here and in Part 4, absent in Part 3.
- Everything else matches: same step order, same parts per step, same annotation types and counts on every other step, same 800 ms timing, same section card.

### 6.5 Lineage note

Project creation dates in the raw payloads: combined 2025-08-04, Part 3 and Part 4 both 2025-08-22, Full Build 2025-08-28. All three of combined/Part 3/Part 4 carry the same annotation inventory (Part 3 still contains the never-shown "64X" label and the 8 dashed lines), so the parts look like cut-down copies of one master rather than the combined guide being stitched from the parts. The copies have since drifted independently (cameras, offsets, insets), which is where the differences in 6.4 come from. The combined guide is step-for-step Full Build Steps 21-38.

## 7. Anomalies

1. Final step name typo: "Copmleted View" [042].
2. Start step [000] still has Cadasio's default description "A Start point for your project - feel free to rename, reorder or delete".
3. Step 1/1c duplicates the last-but-one action of Part 2 / Part 1+2 (attach D2). A student following 1+2 then 3+4 sees it twice.
4. Step 14c inset [031]: stored position (93.1, 48.4)% with width 14.2% would overflow the right edge; the saved thumbnail shows it lower-left (about 19%, 47%), which is Part 4's value. Either the thumbnail is stale or the inset is clipped in the live viewer.
5. Stems: at 18c all 64 stems are 9.7 mm higher than the stem seated in 17c; they drop 9.7 mm on the final view. No annotation explains it.
6. Step 12 [026]: the two lead lines are inconsistent (54 mm anchored to the shelf slot; 99 mm with a free far end).
7. Steps 15-16: lines stored as `dashed` but indistinguishable from solid in the saved renders; unclear if the dash is intended.
8. Seated D10 clip is invisible from Step 10c until Step 17 (data only).
9. A "Paper" component (55 x 82 x 0.2 mm sheet) appears silently at 8c; no step introduces it.
10. One eye-icon ring is a different cyan (`#39cccc` at Step 14; all others `#7fdbff`); ring size 1.3 at Step 8 vs 1.2 elsewhere.
11. Arrow styling is not uniform: Step 1 arrow body 5 / head 20 x 15 with head at "start"; Step 3 arrow body 3 / head 9 x 10 with head at "end".
12. Tooltip description typo on several parts: "Laster Stem Matrix (LSM) - Part 1" (also applied to parts that are not Part 1).
13. The Start/final state is not identical to the state after 18c: two wire caps reappear and the top shelf sits 1 mm off its seated pose on the Start page and final view (data only, not noticeable).
14. 20 of 76 annotation objects are never shown (leftovers), and 5 hidden duplicate steps remain in the project.
15. Digest issue (not an authoring issue): see section 2.

## 8. Relation to the other LSM guides

- LSM has 8 guides. This one is the second half of the build and equals Full Build Steps 21-38 renumbered 1-18.
- Part 3 = its Steps 2-6; Part 4 = its Steps 7-18; its Step 1 belongs to Part 2 (Step 12) / Part 1+2 (Step 20).
- The same patterns appear across the set: `Step N`/`Step Nc` pairs, auto `Transition` steps, part-named section cards ("Capacitor", "LED Matrix Diagram", "Mini USB Cable", "LED Stems").
- Naming of the final step is not uniform across the kit: "Completed View" (Part 1, Part 3, Part 4, Full Build, Deconstruction), "Completed Build" (Part 2, Part 1+2), "Copmleted View" (here).
- The quantity label is "64X" here and in Part 4, "64x" in the Full Build.
- Part 1+2 uses "Step 20C" (capital C) once; the Deconstruction guide has a "Transiton" typo.
