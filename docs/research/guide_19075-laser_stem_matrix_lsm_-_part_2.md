# Guide report: `19075-laser_stem_matrix_lsm_-_part_2` — Laser Stem Matrix (LSM) - Part 2

Kit: LSM. Role: part (2 of 4). 31 viewer steps (31 authored, none hidden): 30 `pause`, 1 `play`.
Sources read: `digest/19075-laser_stem_matrix_lsm_-_part_2.md` + `.json` (all of it), all 4 contact sheets, all 31 thumbs, targeted queries on `cadasio_raw/…part_2.json`.
Enlarged crops used as evidence are in `reports/_crops_19075_lsm_p2/` (009_bl, 009_tr, 019, 021, 025, 028, 010, 023, 001, fullbuild_041).

## 1. Summary

Part 2 starts from the finished Part 1 board (base plate "D1" + breadboard + Arduino Nano + two resistors + capacitor) and adds the wiring and the first housing panel. The student (1) takes a 3-wire male-to-female ribbon jumper and peels its ends apart, (2) plugs the three male ends into breadboard holes i2, i3, b19, (3) plugs the three female ends onto the V+, In, V- header pins of the 8x8 LED matrix, (4) takes the nut off the push button, pushes the button through side panel "D2" and refits the nut, (5) plugs the button's two leads into j16 / j5, (6) slots the D2 panel onto the base, and (7) plugs in the mini-USB cable. It is authored as 13 `Step N` / `Step Nc` pairs plus a title page, two un-numbered section cards ("LED Matrix Diagram", "Mini USB Cable"), one auto-advancing "Transition" and a "Completed Build" page. The guide is almost entirely a **wiring** guide, and its most distinctive trait is that wiring is shown **without any red lead lines and without any part travel**: the hover view names the destination with a small text label or a matched pair of pin discs, and the completed view cross-fades the straight wire for a routed one. Real tweened motion and red lead lines appear only for the three push-button/nut moves.

## 2. Step table (every viewer step)

Camera column = distance mm / elevation / azimuth after entering the step; "same" = camera did not move.

| idx | name | kind | what is added or done | annotations on screen | camera |
|---|---|---|---|---|---|
| 000 | Start | title page | Finished Part 2 assembly (25 parts) shown at right, 3/4 view | 2 unanchored images: TechBox logo SVG top-left (w 33 %, at 2,4 %), title block PNG bottom-left (w 48 %, at 2,62 %: "Laser Stem Matrix (LSM) / Part 2 / (c) 2025 TechBox…") | 351 / 37 / 50 |
| 001 | Step 1 | hover (part intro) | Everything hidden; the 3-wire ribbon jumper (white / purple / grey, joined black 3-way housings) alone, straight | 2 eye icons: one leader to the male 3-pin block, one to the female 3-pin block | moves: 103 / 46 / -55 (rot 74, zoom x3.4) |
| 002 | Step 1c | completed | Ribbon model swapped (step transition `fade`) for the "split" ribbon: both ends peeled into 3 separate connectors, middle still joined | none | same |
| 003 | Step 2 | hover | Part 1 assembly fades in (base D1, breadboard, Nano, 2 resistors, capacitor); split ribbon hovers ~27 mm above the breadboard | label "i2" -> male connector housing of the white wire | moves: 163 / 27 / -138 |
| 004 | Step 2c | completed | White conductor's straight model fades out; routed white wire + male connector seated in i2 fade in. Other two wires stay straight/hovering | none | same |
| 005 | Step 3 | hover | nothing changes in 3D | label "i3" -> male connector of the grey wire | same |
| 006 | Step 3c | completed | Grey wire swapped for routed wire seated in i3 | none | same |
| 007 | Step 4 | hover | nothing changes in 3D | label "b19" -> male connector of the purple wire | same |
| 008 | Step 4c | completed | Purple wire swapped for routed wire seated in b19. The three female ends remain as a hovering bunch | none | same |
| 009 | LED Matrix Diagram | section card (2D) | All 3D parts hidden. One flat raster image (w 62.8 %, at 18,5 %): back of the matrix PCB, In header (top-right) and "V- Out V+" pads (bottom-left) boxed in red, each with an eye icon baked into the picture | 1 image (no anchor) | same |
| 010 | Step 5 | hover | Scene returns (step transition `fade`) and the LED matrix appears hovering ~41 mm above the breadboard | label "i2" -> the already-seated male connector at i2; blue disc "V+" -> matrix V+ pin; white disc "V+" -> white wire's loose female connector | moves: 190 / 27 / 129 (rot 81) |
| 011 | Step 5c | completed | White wire swapped for a wire routed from i2 up to the matrix V+ pin (female housing now on the pin) | none | same |
| 012 | Step 6 | hover | nothing changes in 3D | label "b19" -> seated male connector at b19; blue disc "V-In" -> matrix middle pin; white disc "V-In" -> purple wire's female connector | moves: 190 / 20 / -32 (rot 130) |
| 013 | Step 6c | completed | Purple wire swapped for wire routed b19 -> matrix In pin | none | same |
| 014 | Step 7 | hover | nothing changes in 3D | label "i3" -> seated male connector at i3; blue disc "V-" -> matrix V- pin; white disc "V-" -> grey wire's female connector | moves: 163 / 19 / -147 (rot 105) |
| 015 | Step 7c | completed | Grey wire swapped for wire routed i3 -> matrix V- pin | none | same |
| 016 | Step 8 | hover (part intro + removal) | Scene swap (step transition `fade`): only the push button with its red and black leads and its hex nut | 1 fat red arrow (63 mm) beside the body, pointing from the nut toward the lead tips = slide the nut off | moves: 163 / 39 / -52 |
| 017 | Transition | auto-advance, 1600 ms | Nut spins and travels 99 mm along the button axis to beyond the lead tips. Hidden in step picker, nav overlay off | arrow removed | same |
| 018 | Step 8c | completed | Nut fades out (set aside) | none | same |
| 019 | Step 9 | hover | Side panel D2 fades in; button is 103 mm away on the outside, leads pointing at the hole | 1 solid red lead line (107 mm) from the back of the button body, on its axis, to the centre of the panel hole | moves: 221 / 36 / -53 (rot 3, pull back x0.74) |
| 020 | Step 9c | completed | Button + its two lead connectors tween 103 mm along the axis through the hole and seat | none | same |
| 021 | Step 10 | hover | Nut fades in 83 mm away on the inside, beyond the lead tips | 1 red lead line (93 mm, stored as `dashed`, renders as a thin solid line) from nut centre to the back of the button body | moves: 163 / 26 / 134 (rot 118, to the inside face) |
| 022 | Step 10c | completed, 1600 ms | Nut travels 80 mm along the axis while rotating, seats against the panel | none | same |
| 023 | Step 11 | hover | Rest of the build fades back in (16 parts): Part 1 assembly plus the LED matrix now lying flat in front with its 3 wires in a long final routing. Button leads still straight | 2 labels: "j16" -> black lead's male connector, "j5" -> red lead's male connector | moves: 221 / 27 / 135 (rot 1, pull back) |
| 024 | Step 11c | completed | Button model swapped; routed red wire seated at j5 and routed black wire at j16 fade in | none | same |
| 025 | Step 12 | hover | Nothing new; panel sub-assembly (with button and plugged leads) stands ~22 mm off its seat (19 mm out, 9 mm sideways, 6 mm up) | 1 fat red arrow (50 mm) floating beside the panel, pointing from the panel toward the base; 1 eye icon -> slot on the panel's lower edge | moves: 258 / 48 / -123 (rot 78) |
| 026 | Step 12c | completed | Panel + button + 2 wires cross-faded to seated duplicates (no tween) | none | same |
| 027 | Mini USB Cable | section card (3D part) | Step transition `fade`; only the loose straight USB-A to right-angle mini-USB cable | 1 eye icon -> middle of the cable | moves: 190 / 46 / 51 |
| 028 | Step 13 | hover | Assembly returns, cable hidden again | 1 eye icon -> the Nano's mini-USB socket | moves: 258 / 36 / -53 |
| 029 | Step 13c | completed | Installed (curved) cable with right-angle plug fades in, already seated | none | same |
| 030 | Completed Build | final view | nothing added; all 25 parts | none | moves: 221 / 39 / 40 |

## 3. Conventions found (evidence and exceptions)

### Structure
1. **Title page "Start"** [000]: logo top-left, title/part/copyright block bottom-left, finished assembly on the right half, no 3D annotation. Always (1/1).
2. **Every action is a `Step N` then `Step Nc` pair**: N = instruction view with annotations, Nc = result view with zero annotations and the identical camera. 13/13 pairs; numbers run 1-13 with no gaps and restart at 1 for this Part. Exception: Step 8 is a triplet (Step 8, Transition, Step 8c).
3. **Annotations live only on the instruction view.** All 13 `Step N` views carry 1-3 annotations (1 on seven steps, 2 on three, 3 on three); 0 of 13 `Nc` views and 0 on Completed Build. Every annotation is removed on the very next step.
4. **Un-numbered named section cards introduce something new before it is used**: "LED Matrix Diagram" [009] (pure 2D picture, all 3D hidden) before the matrix connections; "Mini USB Cable" [027] (the part alone) before plugging it in. Cards have no "c" twin. Step 1 [001] does the same job for the ribbon but is numbered.
5. **Closing page** named "Completed Build" [030]: clean, new camera.
6. **Pacing**: 30/31 steps wait for the student; 29 steps are 800 ms, 2 are 1600 ms ([017], [022] - both nut spins). No popups, checklists or on-screen sentences anywhere.
7. **The single "Transition" [017] is a part-motion transition, not a camera move**: camera unchanged, nut travels + rotates for 1600 ms, auto-advances, hidden from the step picker (`hideInStepPicker` true, `overlayVisible` false).

### Granularity
8. **One wire END per step pair.** The 3-wire ribbon takes 6 pairs ([003]-[008] male ends, [010]-[015] female ends). Exception: Step 11 [023] connects both push-button leads in one pair (2 labels) - they belong to one component and are the same kind of connection.
9. **Fastener work is split out**: remove nut (Step 8), insert button (Step 9), refit nut (Step 10) are three pairs although the stale description text bundles insert + nut.
10. **A new loose component is first shown alone on white**: ribbon [001], push button [016], USB cable [027] (3/3). Exceptions: the LED matrix and side panel D2 first appear in context ([010], [019]).
11. **Preparation of a part is its own pair** (Step 1/1c: peel the ribbon ends apart; Step 8/8c: remove the nut).

### Ordering
12. Starts from the Part 1 result; no Part 1 action is repeated.
13. **All near (breadboard, male) ends first, then all far (matrix, female) ends.** Breadboard order i2, i3, b19 = V+, V-, then data (power before signal). Matrix order V+, In, V- (i2, b19, i3) - follows the pin row, so "power before signal" does not hold at the far end.
14. **Electronics before housing; sub-assemble before joining; power last**: button fitted to the loose D2 panel (Steps 8-10), then its leads (11), then panel onto base (12), USB cable last (13).

### Motion
15. **Wiring is a model swap by cross-fade, never a travel.** 8/8 wire-end connections: the straight conductor (or previous routed wire) fades out and a routed wire fades in "already in seated pose". No wire ever tweens.
16. **Tweened travel is reserved for rigid mechanical parts, along their own axis**: button in, 103 mm [020]; nut off, 99 mm [017]; nut on, 80 mm [022]. Only 3 tweened moves in 31 steps.
17. **Threaded parts spin while travelling and get double duration** (1600 ms): 2/2 nut moves.
18. **Hover offset is long enough to clear the part completely**: button hovers 103 mm (button + leads is 75 mm long); nut hovers 83 mm (just beyond the lead tips). Both offsets are purely axial.
19. **Loose wire ends and their target hover above the board**: ribbon ~27 mm above the breadboard top; LED matrix ~41 mm above the breadboard for Steps 5-7.
20. **Isolation**: parts irrelevant to the action are hidden (Steps 8-10 show only button, nut and panel; the board returns in Step 11). Whole-scene swaps carry step transition `fade` on 4 steps ([002], [010], [016], [027]); other scene changes ([001], [003], [009], [019], [023], [028]) rely on per-part fades only.
21. **Sub-assembly join is shown displaced (~22 mm) with an arrow, then swapped to the seated duplicate by fade** [025]->[026] - no tween.
22. **Final plug-in with no hover**: the USB cable is never shown hovering; the socket is marked [028], then the installed cable fades in [029].

### Red lead lines
23. **Lead lines are used only for axial mechanical insertion; exactly one per step.** 2 shown in the whole guide: [019] button axis -> hole centre in panel; [021] nut centre -> back of button body. Colour #ff0000, thin, constant screen width.
24. **Line length is roughly the hover offset** (107 vs 103 mm; 93 vs 83 mm) and both ends are anchored to parts, so the line collapses (2-8 mm) as the part seats; it is hidden on the Nc step.
25. **No lead lines for wires** (0 of 8 wire ends). Exception to note for the kit: this differs from guides where wires get pin-to-hole lines.

### Arrows
26. **Fat flat red 3D arrow (#ff0000, body 5, head 20x15) = direction of a push or removal that is not shown as a guided line**: [016] nut removal direction, [025] panel push direction. 2 shown. Each arrow has both ends anchored to one part. Removed on the next step.

### Labels and callouts
27. **Breadboard holes are named by lower-case coordinate labels** ("i2", "i3", "b19", "j5", "j16"): bold black Arial 2.5 em, sitting on a light-blue (#7fdbff) underline, thickness 5, with a same-colour leader ending in a dashed "life-saver" ring (30 px). 8 showings on 7 steps.
28. **The label leader ends on the wire's connector housing, not on the breadboard hole** (8/8). On male-end steps it is the hovering connector to be plugged in; on far-end steps it is the already-seated connector, re-identifying which wire to pick up (3/3: [010], [012], [014]).
29. **Labels sit above their target**, 9-15 % of viewport height higher and 6-29 % sideways (6 to the upper-left, 2 to the upper-right); the leader leaves the underline end nearest the target.
30. **Pin connections use a matched pair of discs with the same text**: filled light-blue disc on the target pin, white disc with thin outline on the loose wire end (3/3 matrix connections: "V+", "V-In", "V-"). Discs are raster images 5.9-7.8 % of viewport width with a light-blue leader and ring.
31. **No sentences on screen**: the longest on-screen text is 4 characters.

### Eye icon
32. **Black eye icon = "look at this feature", no text**, ~7.8 % of viewport width, light-blue leader + ring. 5 live uses on 4 steps: both connector blocks of the ribbon [001], slot on panel D2 [025], USB cable [027], Nano USB socket [028]; plus 2 baked into the diagram picture [009].
33. The eye marks either a part being introduced ([001], [027]) or the mating feature when there is no lead line ([025], [028]).

### Images
34. The diagram card is one flat picture with its own red boxes and eye callouts baked in; it replaces the 3D scene completely [009].

### Camera
35. **Camera never moves between `Step N` and `Step Nc`** (13/13) nor during the Transition.
36. **Camera moves only when the work location or viewing side changes**: on entering 11 of 13 `Step N` views; it stays put for consecutive actions at the same place (Steps 3 and 4). 14 of 31 steps move the camera.
37. **Always a 3/4 view from above**: elevation 19-48 deg (never top-down, never level). Azimuth is free - 11 of 14 moves rotate more than 60 deg to face the feature being connected (three matrix pins = three different sides). The 3 small rotations are the title page [000] and two straight pull-backs that make room for newly appearing parts ([019], [023]).
38. **Framing keeps the whole working assembly in view, not a close-up of the hole**: subject spans roughly 35-50 % of viewport width; the hole is identified by the label, not by zoom. Parts introduced alone get the closest view (103-190 mm).
39. Distances fall on a ladder 103 / 163 / 190 / 221 / 258 / 351 mm (whole multiples of an about x1.17 zoom notch). Camera tween, 800 ms, no orbit animation.

### Style / colour
40. **White background, toon shading with thin black outline edges on every part** (1092 style overrides), no ground, no shadows.
41. **Annotation palette**: red #ff0000 = motion (lines, arrows); light blue #7fdbff = identification (underlines, leaders, rings, target discs); black = text and eye.

### Wiring specifics
42. Wires are identified by breadboard coordinate and pin name, never by a colour legend. Mapping here: white = i2 -> V+, grey = i3 -> V-, purple = b19 -> In; button red -> j5, black -> j16.
43. A ribbon is modelled as joined (Step 1), split-ended (1c) and then per-conductor routed models; connector housings are separate black parts that swap with the wire.

### Mechanical specifics
44. Button is inserted from the outside of the panel, leads first; nut goes on from the inside after the camera flips to the inside face ([021], 118 deg rotation).

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Background | plain white #ffffff |
| Base plate "D1" (laser-cut ply) | light peach-tan (model #deb887, renders ~#fdd7a1), black engraved "D1", black outline edges |
| Side panel "D2" | outer face mid brown (model #855e42, renders ~#9e6d4d) with black engraved "D2"; inner face and edges tan (~#cfad7f / #deb887) |
| Breadboard | white/very light grey body (~#efefef), black hole squares and printed row/column legend, thin red and blue rail lines |
| Arduino Nano | dark navy PCB, mid-grey USB shell, black IC, gold/tan ICSP pins, silver pins |
| Resistors | blue body with colour bands, silver bent leads |
| Capacitor | black cylinder, silver legs |
| 8x8 LED matrix | black PCB, 64 white/silver square packages with light-grey lens; plain black back; silver right-angle header pins |
| Ribbon jumper wires | white, light grey (#b1b3b3), purple (#4e008e) |
| Dupont connector housings | near-black (#1e1616), silver pin tips |
| Push button | near-black body, silver/light-grey hex nut, red (#ef3340) and black leads with black housings |
| USB cable | near-black cable and mouldings, silver USB-A shell with white insert, right-angle mini-USB plug |
| Text labels | bold black Arial on light-blue underline, light-blue leader and dashed ring |
| Pin discs | target: filled light blue (~#82cdee) with black bold text; source: white with thin grey outline |
| Eye icon | solid black glyph, light-blue leader and ring |
| Lead lines / arrows | pure red #ff0000; lines hair-thin, arrows broad and flat |
| Title images | cyan TechBox logo; grey condensed title text |

## 5. Anomalies and inconsistencies

- **Stale step descriptions.** 18 steps carry a description numbered for an older script, offset +5 from the viewer names (viewer Step 2 = "Step 7 - …", Step 10 = "Step 15"). Step 3's text has no number; Step 10 and Step 11 both say 15; Step 11c says "Step 16c". 13 steps have none (Start, Steps 1/1c, 8c, 10c, 12/12c, 13/13c, both cards, Transition, Completed Build). Only 9 of the 18 contain an instruction sentence (Steps 2-9, plus Step 7c which repeats Step 7's sentence); the other 9 are bare "Step 7c"-style stubs.
- **Typos in descriptions**: "srew", "Push Buttoim" [016]; "Ste[ 15" [023]; "Step 10C" (capital C) [011]; "Step 12c 0 Connect…" ("0" for "-") [015]. [016] says "screw" for what is a nut.
- **Pin naming**: discs say "V-In" [012], the description says "IN pin", the diagram card shows "V- Out V+" on the output pads. "V-In" is not a pin name.
- **Case**: on-screen labels are lower case (i2, b19); descriptions use upper case (I2, B19).
- **Lead line style**: [019] solid, [021] dashed in the data; they render alike. The Full Build uses solid for both.
- **Label data**: 3 of 8 label showings have leader colour unset ([003], [010], [014]) vs #7fdbff on the rest; no visible difference.
- **Disc size**: V+ and V-In discs are 7.81 % wide, V- discs 5.94 / 6.06 %. The V-In discs are the V+ objects with their picture swapped.
- **Unused leftovers**: 40 of 61 annotation objects are never shown (labels "Pin d12", "c16", "h3", "h16", "a11", "a19", "j2", "j3", "I3", "In", "V-", "V+"; 18 lead lines; 1 arrow; 7 images). They belong to Part 1 content of the shared project.
- **LED matrix is never "placed"**: it appears hovering in Step 5 with no instruction, and from Step 11 it lies flat beside the base with re-routed wires, with no step for the change. It is a duplicate staging instance in Steps 5-7.
- **Digest gap**: that staging instance (`8x8 LED-2`) is flagged hidden at assembly level, so the digest never lists it; thumbs [010]-[015] show it. Per-leaf visibility is on from Step 5 [010] to Step 8 [016].
- **Step 1 / 1c have no text of any kind**: "peel the ends apart" must be inferred from two pictures and two eye icons.
- **Later insertion**: Step 12 / 12c have newer record ids than every other step and no description; Completed Build carries raw index 44 at position 30.
- **Model fudges**: USB cable parts scaled 0.93-0.95 and one push-button instance scaled 1.05; Nano, Resistor 1 and Push button stay 1-3 mm "displaced" at the end. Not hover states.
- **Tooltips** are enabled but every part has the placeholder title "Description" / text "none".
- **Final page name**: "Completed Build" here vs "Completed View" in Part 1 and the Full Build.
- **Cross-guide conflict**: here black lead -> j16 and red lead -> j5 [023]; the Full Build [041] labels black -> j5 and red -> j16. This guide's version matches its own seated wires (red seats in row 5, black in row 16 by hole pitch).
- **Cross-guide order**: here panel onto base (Step 12) comes before the USB cable (Step 13); the Full Build does USB (Step 20) before the panel (Step 21).

## 6. Relation to the other LSM guides

- **Part 1** (`…_-_part_1`, Steps 1-8, ends "Completed View") builds the board this guide starts from.
- **Part 1 + 2 combined** (`…_part_1_2`, 47 steps): its [017]-[046] (Steps 9-21, "LED Matrix Diagram", "Transition", "Mini USB Cable", "Completed Build") are this guide step for step with the same annotation objects, same stale descriptions and near-identical label positions. This guide is that second half renumbered 1-13; both share one annotation inventory (19 labels, 19 images, 3 arrows, 20 lead lines). The combined guide names one step "Step 20C" and shows a stray 8.8 mm lead line on its Step 20; this guide does not.
- **Full Build** (`…_-_full_build`, 88 steps): Steps 9-21 cover the same content with the same scheme (hole labels, V+/V-In/V- disc pairs, arrow + 1600 ms Transition for the nut, one lead line per button/nut move, eye on USB socket). Differences: no descriptions; first "i2" label is 3 em; far-end hole labels are anchored to the breadboard instead of the connector; nut line is solid; j5/j16 swapped; USB before panel.
- **Part 3** (13 viewer steps) is next in the series; not analysed here.
