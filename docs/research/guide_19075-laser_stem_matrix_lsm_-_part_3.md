# Guide report: `19075-laser_stem_matrix_lsm_-_part_3`

Title as published: **"Laser Stem Matrix (LSM) - Part 3."** (kit LSM, role: part). 14 authored steps, 13 shown in the viewer.

Sources read: the full digest (`digest/19075-laser_stem_matrix_lsm_-_part_3.md` + `.json`), both contact sheets, all 13 thumbnails (plus enlarged crops of 001, 003, 004, 006, 008, 010), and targeted queries of `cadasio_raw/19075-laser_stem_matrix_lsm_-_part_3.json`.

> **Data caveat (important for anyone reusing the digest of this guide).** The digest under-reports this guide. It shows no MOVE for Steps 1c, 3c and 4c and no APPEAR for the D3 panel, although the thumbnails clearly show panels moving. Two causes, both verified in the raw payload:
> 1. *Visibility.* The digest treats a solid as visible only if every ancestor is visible. Here the top-level CAD nodes of `LSM_Side1_r8-1`, `LSM_Side2_r2-1`, `LSM_Side3_r2-1` and `8x8 LED-1` carry `hidden: true` while their child solids are individually switched on, and the thumbnails show them. Using each solid's own flag reproduces every thumbnail (26-28 top-level components / 684-690 solids on screen, not the digest's 23-24 / 353-356).
> 2. *Position.* `position` is the node's local translation (it replaces the translation in the node's CAD transform), not always an offset. The digest's "Resistor 1 still displaced 1680 mm" is this artefact; the real value is a 1.3 mm nudge.
>
> Everything below about what is visible and how far things move was recomputed from the raw payload with those two corrections (scripts in `reports/_work_19075_lsm3/`), and cross-checked against the thumbnails. Annotation data (lead lines, arrow, images, camera) in the digest is correct and was used as is.

## Summary

Part 3 closes the wooden housing around the electronics built in Parts 1-2. The student starts with the base D1 (breadboard, Nano, resistors, capacitor), the button panel D2, the USB cable and the LED matrix hanging on its three jumper wires, and adds three laser-cut plywood walls by tab-and-slot press fit: D4 (rear), D3 (right) and D5 (front). In between, one handling step moves the LED matrix to the outside of D4 with its wires passing through a notch in that panel. No wires, screws or electronics are added. The guide is 13 viewer steps: a branded title page, five numbered steps each authored as a `Step N` / `Step Nc` pair, one auto-advancing `Transition`, and a `Completed View`. It contains no text at all: no labels, no step descriptions, no popups. Instruction is carried by 14 red lead lines (one per tab-slot joint), one red arrow, two eye icons, the D-codes engraved on the wood, and camera choice.

## Step table (every viewer step)

Part codes: D1 = `LSM_Bottom_r1` "Housing Base", D2 = `LSM_Side3_r2` "Housing Left Side" (button panel), D3 = `LSM_Side1_r8` "Housing Right Side", D4 = `LSM_Side2_r2` "Housing Rear Side", D5 = `LSM_Side4_r2` "Housing Front Side" (names from the hover-tooltip metadata).

| idx | name | kind | what is added or done | annotations on screen | camera |
|---|---|---|---|---|---|
| 000 | Start | title page (pause) | Shows the **finished state of this part**: five-sided open box D1-D5, electronics inside, LED matrix outside on its wires, USB cable. 28 components / 690 solids, identical content to [012]. | 2 images, no leader: TechBox logo (SVG) top-left at (1.8 %, 5.1 %), width 37.6 % of viewport; title block (PNG: "Laser Stem Matrix (LSM)", "Part 3", copyright line) at (1.8 %, 61.7 %), width 42.9 %. Model sits in the right half. | Set: dist 258 mm, elevation 41°, azimuth 51°, Y-up. |
| 001 | Step 1 | hover | D4 is shown 69.3 mm off its seat along its own normal (it was seated on the title page, so it slides out). D3 and D5 fade out. LED matrix + 3 wires swap to their "before" pose (matrix on the open side). Logo and title removed. | 4 solid red lead lines, 64.9 / 65.3 / 68.1 / 67.8 mm: two from D2's edge tabs, two from D1's edge tabs, each to its slot in D4. | Moves: rotates 67.1°, zoom ×0.74 to 350 mm; elevation 43°, azimuth -45°. |
| 002 | Step 1c | completed | D4 tweens 69.4 mm straight onto the four tabs. USB cable now sits in D4's U-notch. | none (4 lines removed) | unchanged |
| 003 | Step 2 | hover (cue only, nothing moves) | Tells the student to carry the LED matrix across to the D4 side. | 1 red straight arrow, 102.9 mm, pointing screen-left, parked above the model; 1 eye icon at (72 %, 34 %) with cyan leader to the centre of the LED matrix. | Moves: rotates 42.9°, same distance 350 mm; top-down (elevation 85°); scene up-axis set to -z. |
| 004 | Step 2c | completed | Matrix and its 3 wires cross-fade to the "after" pose: matrix outside D4, wires passing through the notch in D4's edge. No tween. | Arrow removed. Eye icon replaced by a second one at (30 %, 26 %) whose leader ends on the wires where they cross the D4 notch. | unchanged |
| 005 | Transition | transition (play, auto-advance, 800 ms) | Nothing changes on the model. | Eye icon removed. Navigation overlay hidden for this step only. | Moves: rotates 142.8°, target shifts 62 mm, zoom ×1.17 to 300 mm; now looking at the underside of D1 with D4 at the bottom; up-axis +x. |
| 006 | Step 3 | hover | D3 fades in tilted 21.6° and about 46 mm away from where its tabs will go. | 2 lead lines, 42.7 / 42.4 mm, from D3's two bottom-edge tabs to the two rectangular slots in D4. | unchanged |
| 007 | Step 3c | completed (stage 1 of D3) | D3 translates 45.8 mm so its tabs sit in D4's slots; it stays leaning out at 21.6°. | none | unchanged |
| 008 | Step 4 | hover (cue only, nothing moves) | Announces the swing-shut of D3. | 2 short lead lines, 16.0 / 12.6 mm, from D1's two edge tabs to the long slot in D3. | unchanged |
| 009 | Step 4c | completed | D3 rotates 21.6° about the hinge line to upright and seated. | none | unchanged |
| 010 | Step 5 | hover | D5 fades in 42.0 mm off its seat along its normal, which is straight up on screen. | 6 lead lines, 38.3 / 39.4 / 39.3 / 42.8 / 42.0 / 42.0 mm: D3 tabs ×2, D2 tabs ×2, D1 tabs ×2, each to one of D5's six slots. | Moves: rotates 89.8°, same distance 300 mm; from above (elevation 41°, azimuth 129°); up-axis still +x. |
| 011 | Step 5c | completed | D5 tweens 42.0 mm straight down onto the six tabs. | none | unchanged |
| 012 | Completed View | completed view (pause) | Nothing changes. | none | Moves: rotates 66.4°, zoom ×1.36 to 221 mm; elevation 42°, azimuth 35°; up-axis back to +y. Same hero angle family as Start, closer. |

Authored but never shown: index 0 is a hidden step named `Step 50` that holds the base state (render style, colours, tooltips).

## Conventions found

### Structure
- **Fixed skeleton.** `Start`, then numbered steps, then `Completed View`. 13 viewer steps = 1 title + 5 hover + 5 completed + 1 transition + 1 completed view. No section cards in this guide.
- **Every numbered step is a pair** `Step N` then `Step Nc` (5 of 5). `Step N` shows what is about to happen with its annotations; `Step Nc` shows the result. Numbering restarts at 1 for this part.
- **Title page shows the end state of this guide**, not the starting state: [000] and [012] have identical part visibility (28 components / 690 solids). Only the camera and the two branding images differ.
- **No text anywhere.** 0 labels visible, every step `description` is empty, `popupType` is `none` on all 14 steps. The one label in the toolbox ("64X") is never shown here.
- **Uniform timing.** Every step is 800 ms; parts move by tween, show/hide by fade, camera by tween (speed 2). 12 steps pause, 1 (the Transition) plays through.
- **Part identity comes from the model and tooltips.** D1-D5 are engraved on the wood; hovering a part shows its "Description" (for example "Housing Rear Side - Part D4"). Tooltips are enabled project-wide.

### Granularity
- **One part or one action per numbered step, always** (5 of 5). Three panels are added over four steps; the fifth step is a handling action. Nothing is ever added in a group.
- **A compound motion is split into two numbered steps** rather than animated as a two-stage move: D3 is "insert tabs at an angle" (Step 3 / 3c) then "swing shut" (Step 4 / 4c). Each half gets its own lead lines and its own completed view.
- **A step can be a pure cue.** In 2 of 5 hover frames (Step 2, Step 4) no geometry changes from the previous completed frame; only annotations appear.

### Ordering
- Start state already has D1 + electronics + D2 + USB cable (the end of Part 2).
- Order is D4 (rear) → re-route matrix through D4 → D3 (right) → D5 (front). The wall with the cable notches goes on first, the cable handling follows immediately while the box is still open, and the panel that locks onto the most neighbours (D5, 6 joints across three parts) goes last.

### Motion
- **Rigid parts hover along their insertion axis and travel in one straight tween.** D4: 69.3 mm along its normal. D5: 42.0 mm along its normal. D3: 45.8 mm oblique plus a 21.6° tilt, then a 21.6° rotation in the next step.
- **New parts fade in already at the hover pose** (D3 at [006], D5 at [010]). The hover pose is pre-staged in earlier steps while the part is hidden (D5's -42 mm offset is written at Step 1; D3's tilt and pivot at Step 2c). Exception: D4 is visible on the title page, so it slides out to hover at [001].
- **Hover direction is the joint's axis, not "up".** On screen D4 comes in from the lower-left, D3 from the upper-right, D5 from straight above.
- **Flexible items are not tweened; two pre-posed copies are cross-faded.** The "before" set (`8x8 LED-1` + wires `Part5/6/7` + `Wire Cap-8/9/10`) is shown in [001]-[003]; the "after" set (`8x8 LED-6` + `Part31/32/33` + `Wire Cap-17/18/19`) from [004] on, and on the title page. 329 solids each.

### Red lead lines
- **Style:** colour `#ff0000`, solid, line scale 5, straight two-point 3D segments. 14 shown in total (4, 2, 2, 6). Dashed and dotted lines exist in the project toolbox but never appear in this guide.
- **One line per tab-slot pair engaged in that step, and all of them.** Step 1: 4 joints, 4 lines. Step 3: 2 and 2. Step 4: 2 and 2. Step 5: 6 and 6.
- **Endpoints are the mating features:** the tip of a tab on one part and the matching slot on the other. In Steps 1, 4 and 5 the tabs are on already-placed parts and the slots on the incoming panel; in Step 3 the tabs are on the incoming D3 and the slots on seated D4.
- **Length is about the feature's travel.** Step 1: 0.94-0.98 of the 69.3 mm hover. Step 5: 0.91-1.02 of the 42.0 mm hover. Step 3: 0.93 of the 45.8 mm travel. Step 4: 12.6-16.0 mm, the chord the slot sweeps during the 21.6° swing.
- **Lines are parallel to the travel direction and to each other.** Exactly axis-aligned in Step 1; within about 2° in Step 5; within about 4° in Step 3.
- **Lines are real 3D geometry.** They are occluded by parts ([001]: three of the four vanish behind D4's edge) and are visible through slots ([010]: red dots inside D5's slots). Both ends are bound to their parts.
- **Lines live only on the hover frame**; all are removed on the `c` frame (4 of 4 steps that have them).
- The same line objects are reused across steps (`Line 3D_basic_52/53` serve Steps 1, 3 and 4 with new endpoints).

### Arrow
- Used once ([003]), for a free-hand move with no mating features. Red `#ff0000` straight 3D arrow, body width 3, head 9 × 10, 102.9 mm long, parked clear of the model and parallel to the motion; anchored to D1 at both ends so it does not move. Removed on the `c` frame.

### Eye icon
- Used twice ([003], [004]). Black eye glyph PNG, 7.81 % of viewport width, placed in white space above and outboard of its target (16-22 % of viewport height above it). Leader is a straight cyan `#7fdbff` line, thickness 5, ending in a cyan broken-ring anchor ("Life Saver Circle") on the target.
- Meaning here is "look at this". On the hover frame it marks the thing to handle (centre of the LED matrix); on the completed frame a second icon marks the result to check (wires in the D4 notch).
- **Unlike lead lines, the eye persists on the `c` frame** and is cleared by the following Transition.

### Images
- Only on the title page: logo top-left and title block lower-left, both left-aligned at x = 1.8 %, together occupying roughly the left 45 % of the frame; the model is pushed into the right half. Positions and widths are in percent of the viewport, measured from the image's top-left corner.

### Camera
- **Never moves inside a `Step N` / `Step Nc` pair** (5 of 5).
- **Moves on 6 of 13 steps:** Start, Step 1, Step 2, Transition, Step 5, Completed View. Steps 3 and 4 inherit the view set by the Transition.
- **Each new view puts the joint on the visible side with the travel axis well off the view axis** (51° to 88° between travel direction and view direction across Steps 1, 2, 3, 5), so the part never moves toward or away from the viewer.
- **Whole model always in frame; no close-ups.** Content spans 23-45 % of frame width and 59-77 % of frame height in the working steps, even when the lead lines are only 13-16 mm long (Step 4). Working distances are 350 mm ([001]-[004]) and 300 mm ([005]-[011]); hero views are 258 mm (Start) and 221 mm (Completed View). Perspective, 45° field of view.
- **Framing is set for the exploded arrangement and held.** In [005]-[009] the assembly sits left of centre (x 25-55 %) leaving room for D3 to hover on the right (to 67 %); in [010] the hovering D5 reaches 4 % from the top edge.
- **The on-screen "up" is re-declared to show the model resting on a different face.** Up-axis goes +y → -z at Step 2 (top-down) → +x at the Transition (box standing on D4, used for Steps 3-5) → +y at Completed View.
- **Transition:** exactly one, auto-advancing, 800 ms, camera only, used for the largest re-orientation (142.8°, flipping to the underside). It also clears the leftover eye icon, and it is the only step with the navigation overlay hidden. The 67° (Step 1), 43° (Step 2), 90° (Step 5) and 66° (Completed View) moves happen on entering the step with no Transition, so a Transition is not used for every camera move.
- **Completed View returns to the title-page angle family** (elevation 42° vs 41°, azimuth 35° vs 51°) and moves in closer (×1.36).

## Part looks (from the renders)

| part | look |
|---|---|
| Background | Pure white `#ffffff`, flat, no floor or shadow. |
| Render style | Every solid is toon-shaded (two flat tones per colour) with thin black outline and feature edges. |
| Plywood panels D1, D3, D4, D5 | Tan. Base colour `#deb887`; renders `#ffdda2` on lit faces and `#d5b282` on shaded faces. Tabs, slots, notches and L-shaped corner cuts are all modelled. |
| Engraved part codes | "D1".."D5" as near-black `#1e1616` inlaid glyphs on the outer face of each panel. |
| Button panel D2 | Same tan body and edges, but its outer face is overlaid in brown `#855e42` (renders `#a0714f`). The inner face is tan. It is the only two-colour panel. |
| Breadboard | White body, black tie-point holes and row/column legend, thin red and blue rail lines. |
| Arduino Nano | Dark navy PCB `#000f41`, silver header pins and USB socket, black IC, white silkscreen. |
| Resistors | Blue body `#0074d9` with colour bands (brown/red on one, orange/black on the other), silver leads. |
| Capacitor | Black can with silver-grey top. |
| Push button | Black cap and body, light-grey hex nut; its two leads are red `#ef3340` and black `#2d2926`. |
| Matrix jumper wires | Three smooth round tubes: white `#ffffff`, light grey `#b1b3b3`, purple `#4e008e`, each outlined in black. |
| Dupont housings | Black `#1e1616` blocks with a light-grey `#cccccc` pin. |
| LED matrix | Black PCB `#1e1616`; 64 square light-grey `#b1b3b3` LED packages with white `#fbfbfb` round lenses; black 3-pin connector on one edge. |
| USB cable | Black cable and over-moulds, silver USB-A shell `#a6a9aa` with white insert, black right-angle mini-USB plug. |
| Lead lines and arrow | Pure red `#ff0000`. |
| Eye icon | Solid black glyph; cyan `#7fdbff` leader and ring. |
| Title page branding | Cyan rounded-rectangle logo with white "TECHBOX" and a bulb-and-gear mark; title in dark-grey condensed bold; copyright in small serif. |

## Anomalies

1. **Title has a trailing period:** "Laser Stem Matrix (LSM) - Part 3." No other LSM guide title ends in a period. "Stem" is also not capitalised as "STEM".
2. **Hidden first authored step is named `Step 50`**, a leftover from the master project (the project's step counter is at 51).
3. **Toolbox leftovers.** 50 of the 69 annotation objects are never shown in this guide: 30 solid, 8 dashed and 1 dotted lead lines, 7 images, 3 arrows and the "64X" label.
4. **Lead-line anchor order is inconsistent.** Steps 1, 4 and 5 list the already-placed part first; Step 3 lists the moving part first. A player cannot infer "which end moves" from the order.
5. **Step 5 lead lines are uneven** for a uniform 42.0 mm hover: 38.3, 39.4, 39.3, 42.8, 42.0, 42.0 mm, two of them slightly out of parallel. The two exact ones are anchored to the whole `LSM_Bottom_r1-1` part, the other twelve lines in the guide to a `Cut-Extrude1` body.
6. **D4's rest pose drifts by about 1.2 mm** between the title page and its seated pose after Step 1c (local offset (0.0, -0.6, 0.6) mm vs (1.0, -0.5, -0.1) mm). Not visible, but it shows poses were placed by hand.
7. **USB cable through D4 is implied, not called out.** In [001] the rigid cable model crosses D4's path; in [002] it sits in D4's U-notch. The matrix wires get a whole step and two eye icons for the equivalent notch; the USB cable gets nothing.
8. **Camera animation options are stored as strings** (`"false"`, `"2"`) on the 13 shown steps and as proper types on the hidden step.
9. **Three solids keep the CAD default colour `#cad1ee`** (two on the push button, one on the right-angle USB plug) instead of an assigned colour.
10. **Digest under-reporting** for this guide, as described in the caveat at the top.

## Relation to the other LSM guides (checked)

- **Part 2 → Part 3.** Part 2's last frame ("Completed Build") is D1 + electronics + D2 + USB cable with the matrix loose, which is exactly the starting assembly in [001] here. Part 2 names its last step "Completed Build"; this guide names it "Completed View".
- **Part 3 → Part 4.** Part 4's first step starts from this guide's end state (five-sided box, matrix outside D4).
- **Same content in the combined guides.** Steps 1-5 here are Steps 2-6 of "Part 3 + 4" and Steps 22-26 of "Full Build": same parts, same lead-line anchors with near-identical lengths, the same 102.9 mm arrow and eye icons, and the same Transition before the D3 step (143° in Part 3 + 4, 130° in Full Build). Those two guides prepend the D2-panel step (their Step 1 / Step 21), which the split series places in Part 2.
- **Differences between the copies.** The matrix-move step is viewed from 350 mm here and 300 mm in the other two. The D5 step has 6 lead lines here and in Part 3 + 4 but only 4 in Full Build, two of which are about 133 mm long. Full Build anchors the second eye icon to the D4 panel rather than to the wire.
- **Step-name typos seen in siblings, not here:** "Copmleted View" (Part 3 + 4), "Transiton" (Deconstruction), "Step 20C" (Part 1 + 2), "Step 9c" following "Step 8" (Part 4).
