# Guide report: `19075-lac_electronics` ("LAC Electronics")

Kit: LCD Alarm Clock (LAC). Role: parts overview / kit inventory. 3 authored steps, **2 shown** ("All Electronics", "All Wood"), 1 hidden ("Start").

Sources read: `digest/19075-lac_electronics.md` (all), `sheets/19075-lac_electronics/sheet_000-001.jpg`, `thumbs/19075-lac_electronics/000.jpg` + `001.jpg`, the full-resolution `thumbs_raw/*.webp`, and targeted queries on `cadasio_raw/19075-lac_electronics.json`.
Working files (scripts, overlays, zoom crops): `reports/_work_lac_elec/`.

> **Read this first - the digest is wrong in two ways for this guide.** I re-derived the scene geometrically (`_work_lac_elec/model.py`), projected every visible solid through the stored camera, and overlaid the result on the published thumbnails (`overlay_000_left.png`, `overlay_000_right.png`, `overlay_001.png`). The projection lands on the rendered parts to within a few pixels, so the numbers below are trustworthy; where they differ from the digest, the digest is the one that is off. Details in section 8.
> 1. "All Wood" shows **9** wood parts (F1 to F9, one each), not the 5 the digest lists.
> 2. The digest's `MOVE [713, 865, 1642]mm (1989mm)`-style lines are artefacts, not motion. Nothing moves 2 m.

---

## 1. Summary

This is not a build guide. It is a two-view **3D line-up of the kit contents** for the LCD Alarm Clock, apparently made by copying the LAC Full Build project, deleting almost every step, and dragging parts out of the assembled clock into a single row along the clock's long axis. View 1 "All Electronics" shows 9 kit items (31 CAD components, 772 solids): USB cable, two resistors, potentiometer with knob, LCD, Nano, real-time-clock module, rocker switch, buzzer, breadboard. View 2 "All Wood" shows the 9 laser-cut plywood pieces F1 to F9, all turned to face the same way and sorted by part number. There is **no title page, no section card, no Step N / Step Nc pair, no Transition, no Completed View, no on-screen label, no lead line, no arrow, no eye icon and no image inset** - zero annotations are visible in either view. The only naming mechanism is the hover tooltip, bound to a per-solid "Description" property that carries the student-facing part names ("LCD Screen", "Front Side - Part F1", ...). Styling is the house style used in every LAC guide (white background, toon shading, 1 px black edges, 45 degree perspective camera, three-quarter view from above). The parts are small in the frame (3.75% and 1.31% of pixels are non-white), not uniformly spaced, drawn at up to 2.1x different scales because of perspective, and in the electronics view three items overlap on screen, so the two views are **not usable as-is as a source of per-part images**; the single-part "section card" views in the LAC Part guides are a much better model for that.

---

## 2. What the guide is and how it was made

| Fact | Evidence |
|---|---|
| Same CAD as every other LAC guide | `cadId 10dab12f...`, `originalCadId 585ab7b0...`, root component "LAC Full Build", 188 top-level components, 1569 solids |
| Cloned from the Full Build project | Carries the identical unused annotation inventory as LAC Full Build / Parts 1-4 (53 images, 41 labels, 7 arrows, 49 lead lines = 150 objects). **None of the 150 is referenced by any of the 3 steps**; all have `visible:false`. Counters `stepNumber 237`, `visibleStepCount 128` are far larger than the 3 steps present |
| Newest LAC project | created 2026-02-16; Full Build 2025-10-06, Deconstruction 2025-11-26, Parts 1-4 2025-12-10/11 |
| Published, then edited | `publishVersion 3`, `status published_dirty`, `newVersionAvailable true`; last modified 2026-02-27; thumbnails saved 2026-03-01 (view 1) and 2026-05-08 (view 2) |
| Guide title vs content | Title is "LAC Electronics" but the second view is wood, not electronics |

It tells the student nothing to *do*. Its purpose is "here is what is in the box", in two groups: electronic parts, wooden parts.

---

## 3. Step table (every viewer step)

| Index | Name | Kind | What is shown / done | Annotations | Camera |
|---|---|---|---|---|---|
| [000] | All Electronics | static inventory view, `pause` | 31 components / 772 solids = 9 kit items in one row. Nothing is added, nothing seats. Everything else (157 components incl. all wood, all loose jumper wires) hidden. Scene set to white background, edges on, ambient 1.75 | none (0 of 150) | perspective, FOV 45, distance 513 mm, elevation 34.4, azimuth 129.9; row runs upper-left (far) to lower-right (near), 25 degrees below horizontal on screen |
| [001] | All Wood | static inventory view, `pause` | All 31 electronics components fade out; 9 wood parts F1-F9 fade in (digest says 5 - wrong). 7 fade in place; F5 slides 85 mm and F6 slides 65 mm along the row while fading in | none (0 of 150). Step `description` holds leftover placeholder text | tweens over 800 ms: rotates 11.9 degrees, target shifts 246 mm, pulls back 513 to 1505 mm (zoom x0.34); elevation 44.4, azimuth 138.3; row 37.5 degrees below horizontal |
| (hidden) | Start | hidden authoring step, **last** in order | Resets every part to assembled pose (position 0, rotation identity) and restores visibility. Never reached by the student | - | distance 377 mm |

Numbering: none. No step prefix is used; the two names are plain titles.
Behaviour: both shown steps are `pause` (wait for Next). No `play` (auto-advance) step exists. Animation settings on all 3 steps: duration 800 ms; parts `show: fade`, `hide: fade`, `move: tween`; camera `move: tween`, `animate_orbit: false`, `animation_speed: 2`.

---

## 4. Layout in detail

World frame: Y is up; the row runs along world **Z**; the camera sits on the +X, +Y, -Z side, so low Z is near the camera (right/bottom of the screen) and high Z is far (left/top).

### 4.1 [000] All Electronics - 9 kit items

Screen boxes are % of the frame at the stored aspect 2.066:1 (thumbnail 2559 x 1239). "px" columns are for the 1400 x 678 thumb.

| Row pos. (far to near, = screen left to right) | Kit item (tooltip name) | CAD components shown | World size X x Y x Z (mm) | Gap along row to previous (mm) | Depth from camera (mm) | Screen box x% / y% | Size on 1400 px thumb |
|---|---|---|---|---|---|---|---|
| 1 | USB Cable | `USB Right Angle-1`, `Part67` (cable), `USB Cable end-1` | 90 x 35 x 104 | - | 680 | 13.5-22.9 / 16.3-27.4 | 132 x 75 |
| 2 | 12 kOhm Resistor (two shown) | `LAC Resistor 1.SLDPRT-1`, `-2` | 34 x 11 x 29 | 38.0 | 610 | 17.2-21.7 / 23.4-28.1 | 63 x 32 |
| 3 | Potentiometer | `LAC Potentiometer-1`, `LAC Knob-1`, `LAC Nut-2`, `Washer-2` | 31 x 26 x 18 | 38.7 | 558 | 18.6-23.3 / 22.0-28.8 | 66 x 45 |
| 4 | LCD Screen | `LCD V1-1` (163 solids) | 20 x 60 x 98 | 34.5 | 519 | 22.9-31.6 / 20.5-39.8 | 120 x 131 |
| 5 | Nano Board | `nano-1` (295 solids) | 18 x 19 x 45 | 21.8 | 488 | 33.3-38.4 / 36.3-44.0 | 71 x 52 |
| 6 | Real Time Clock | `HW-84 v7-1`, `CR2025-50003LC-1`, `-2`, `Wire Cap-9/11/12/13` | 15 x 49 x 22 | 27.9 | 432 | 38.1-41.5 / 34.7-46.8 | 47 x 82 |
| 7 | 3-Position Rocker Switch | `Rocker Switch-2`, leads `Part75/76/77`, `Wire Cap V2-44/45/46` | 21 x 68 x 15 | 33.3 | 434 | 42.6-46.4 / 42.5-61.2 | 52 x 126 |
| 8 | Alarm Buzzer | `Piezo Buzzer-1`, leads `Part37/38`, `Wire Cap V2-37/39` | 87 x 15 x 47 | 30.6 | 425 | 47.9-58.1 / 48.0-63.5 | 143 x 105 |
| 9 | Breadboard | `Breadboard-1` (134 solids) | 56 x 10 x 83 | 44.6 | 351 | 60.5-77.5 / 58.0-83.4 | 238 x 172 |

Measured properties of this layout:

- **One row, one axis.** Row length 731 mm (Z 1082 to 1813). Sideways scatter of item centres about +/-25 mm in X; height scatter +/-15 mm in Y (centres Y 890 to 920). Parts are *not* resting on a common ground plane and *not* centred on a common line; each simply kept roughly the height it has inside the clock.
- **Gaps are hand-placed, not uniform:** 22, 28, 31, 33, 35, 38, 39, 45 mm (mean 34 mm).
- **Parts keep their as-assembled orientation.** 30 of 31 components have zero rotation relative to the assembled clock (LCD upright facing +X, Nano and breadboard horizontal, switch upright with its three leads hanging down, buzzer flat with its lead pair sticking out sideways). Exception: the RTC module and its coin cells are flipped 179 degrees (not 180 - a free-hand gizmo rotation) so the battery faces the camera.
- **Sub-assemblies travel as one rigid group** (identical displacement vector for every member): potentiometer + knob + nut + washer (0, 0, +359 mm); switch + 3 leads + 3 pin housings (146.6, -49.9, +36.9); buzzer + 2 leads + 2 housings (24.9, 0, -167.4); the three USB components (57.6, 0, +373.3). So a "kit item" is shown the way it comes out of the bag: knob already on the pot shaft, leads already on the switch and buzzer.
- **Most displacements are pure single-axis slides** along Z (LCD +190 mm, breadboard -182 mm, pot group +359 mm): the author used the axis-constrained move handle and pulled each part out of the clock along its long axis.
- **One representative per kind, not kit quantities.** The CAD holds 4 potentiometer and 3 rocker-switch instances; one of each is shown. No "2x"/"3x" quantity text is used (a "2x" label exists in the inherited inventory but is not shown). Exceptions: both resistors are shown, and two coin-cell instances are shown stacked 2.5 mm apart (reads as one battery).
- **On-screen overlap.** The three leftmost items collide: USB/resistor boxes overlap by 86% of the smaller box, USB/potentiometer 73%, resistor/potentiometer 70%. One resistor is almost entirely hidden behind the knob (only one bent leg shows). Pot/LCD touch (7%), Nano/RTC touch (5%). The four items from the switch rightwards are cleanly separated.
- **Perspective scale drift.** Nearest item (breadboard, 351 mm) is drawn at 2.33 px/mm, farthest (USB cable, 680 mm) at 1.20 px/mm on the 1400 px thumb: a factor 1.9 between row ends (2.1 between nearest and farthest single component). The 83 mm breadboard is drawn twice as wide as the 98 mm LCD.
- **Not shown although they are named kit items:** the loose jumper wires ("Breadboard Wires (M-M)", "Breadboard Wires (M-F)") and "Adhesive Backing".
- **Order along the row** is USB, resistor, pot, LCD, Nano, RTC, switch, buzzer, breadboard. It is not sorted by size or name, and it does not match the Full Build's order of first use (there, per its digest: Nano, resistor, breadboard, RTC, switch, potentiometer, buzzer, LCD, USB). I could find no rule.

### 4.2 [001] All Wood - 9 plywood pieces

Screen boxes are % of the saved frame, aspect 1.214:1 (3152 x 2596). At the 2.066:1 aspect used for view 1 the same row would span only x 29.9% to 63.1%; the y values are unaffected by aspect.

| Row pos. (far to near) | Tooltip name | CAD instance | World size X x Y x Z (mm) | Gap to previous (mm) | Depth (mm) | Screen box x% / y% | Size on 1400 x 1153 thumb | Rotation applied to stand it in the common plane |
|---|---|---|---|---|---|---|---|---|
| 1 | Front Side - Part F1 | `F1-2` | 3 x 76 x 165 | - | 2082 | 15.9-20.7 / 13.0-20.6 | 67 x 87 | none |
| 2 | Rear Side - Part F2 | `F2-2` | 3 x 76 x 165 | 88.3 | 1948 | 22.1-27.4 / 18.5-26.7 | 73 x 95 | 180 |
| 3 | Bottom Side - Part F3 | `F3-1` | 3 x 86 x 159 | 112.4 | 1810 | 29.9-35.6 / 25.2-34.6 | 79 x 108 | 90 |
| 4 | Top Side - Part F4 | `F4-3` | 3 x 86 x 159 | 71.7 | 1673 | 36.6-42.8 / 31.9-42.2 | 87 x 118 | 90 |
| 5 | Left Side - Part F5 | `F5-1` | 3 x 76 x 89 | 49.0 | 1617 | 44.6-48.5 / 39.5-47.3 | 53 x 89 | 90 |
| 6 | Right Side - Part F6 | `F6-1` | 3 x 76 x 89 | 63.0 | 1534 | 50.8-55.0 / 45.4-53.6 | 59 x 94 | 90 |
| 7 | Alarm Bracket - Part F7 | `F7-2` | 3 x 77 x 20 | 97.3 | 1422 | 59.3-60.8 / 53.4-58.8 | 21 x 62 | none |
| 8 | Right LCD Bracket - Part F8 | `F8-1` | 3 x 77 x 17 | 77.5 | 1369 | 64.4-66.1 / 57.8-63.2 | 22 x 61 | 90 |
| 9 | Left LCD Bracket - Part F9 | `F9-1` | 3 x 77 x 31 | 79.2 | 1330 | 69.5-72.4 / 62.8-69.0 | 39 x 71 | 90 |

Measured properties:

- **Sorted by part number**, F1 farthest/top-left to F9 nearest/bottom-right. Always true (9 of 9).
- **Every piece is turned to the same orientation**: 3 mm thickness along world X, face toward the camera side. 7 of 9 were rotated (exact, snapped 90 or 180 degrees) to achieve this; F1 and F7 already had it. The result looks like a row of cards standing on edge, all facing the same way.
- **Common centre height**: 7 of 9 centres are at exactly Y = 919.5 mm (the clock's mid-height); F3 is at 919.0 and F4 at 927.8. Lateral scatter +/-9 mm in X. This row is noticeably tidier than the electronics row.
- **Gaps hand-placed**: 49, 63, 72, 78, 79, 88, 97, 112 mm (mean 80 mm). Row length 1532 mm - twice the electronics row, which is why the camera pulls back 3x.
- **No overlap on screen**; clear white gutter between every pair of neighbours.
- **Perspective scale drift** 1.57x between F1 (2082 mm away) and F9 (1330 mm).
- **Each piece carries its own ID**: the engraved "F1" to "F9" marks are modelled as two black surface solids per piece (the letter and the digit) and are legible in the render on F3 to F9; on F1 and F2 they are only a dark smudge at this zoom.
- **One of each**, although the CAD contains F1 x4, F2 x2, F4 x3, F7 x2 instances.

---

## 5. Conventions found (with evidence and exceptions)

Sample size is two views, so "always" here means 2 of 2.

### Structure
- **S1. A parts overview is a separate guide, not a chapter inside a build guide.** It has no Start/title page, no logo, no copyright line, no section cards, no Step/Step c pairs, no Transition, no Completed View. Evidence: [000], [001] are the only shown steps; compare `lac_full_build` [000] which has the TECHBOX logo, title and copyright. Exceptions: none.
- **S2. One view per material class**, named "All <class>": [000] "All Electronics", [001] "All Wood". Electronics first, wood second.
- **S3. Views wait for the student** (`pause` 2 of 2); no auto-advance.

### Granularity
- **G1. A kit item, not a CAD component, is the unit.** Anything that arrives pre-attached is shown attached and shares one name: pot + knob + nut + washer; switch + 3 leads + pin housings; buzzer + 2 leads + housings; RTC + battery; 3-piece USB cable. 31 components collapse to 9 items in [000]. In [001] item = component (9 = 9).
- **G2. One representative per kind**; quantities are not shown. Exception: two resistors (deliberate or not is unclear), two coincident coin cells (almost certainly accidental).

### Ordering
- **O1. Wood is ordered by part number F1..F9** along the row, far to near. 9 of 9.
- **O2. Electronics have no detectable ordering rule** (see 4.1). Treat as unordered.

### Motion
- **M1. No assembly motion at all.** No hover offset, no seating move, no straight-to-routed wire swap. Parts are simply present.
- **M2. View change = cross-fade plus camera tween, 800 ms.** All outgoing parts fade out, incoming parts fade in, camera tweens. Exceptions: F5 (85 mm) and F6 (65 mm) slide along the row while fading in, because in the hidden state they were parked on top of each other and the author separated them only in the wood step; `LAC Knob-1` shifts 56 mm while fading out. These are side effects, not design.

### Lead lines and arrows
- **L1. None used.** 49 lead lines and 7 arrows exist in the project (inherited) and all stay invisible in both views.

### Labels, callouts, eye icon, images
- **T1. No on-screen text of any kind.** 41 labels and 53 images (including the eye icon) exist in the project and all stay invisible. The step description is empty for [000].
- **T2. Names are delivered only by hover tooltip.** Project flag `tooltips: true`; [000] sets `tooltip_show: true`, `tooltip_title: "Description"`, `tooltip_text: "none"` on 1561 nodes; every visible solid in both views has it. The "Description" value is stored per solid, so hovering any face of an item gives the same name. Coverage of visible solids: 761 of 772 in [000] carry a name (the 11 without: 2 of 3 solids of each of the two coin cells, 1 of 2 solids of each of the two buzzer-lead housings, the four `Wire Cap-9/11/12/13` housings, 1 of 134 breadboard solids); 27 of 27 in [001]. *I could not open the live viewer, so the exact tooltip appearance is inferred from the data, not observed.*
- **T3. Naming vocabulary** (21 values in this project; the same list is present in every LAC guide):
  - Electronics: `LCD Screen`, `Nano Board`, `Breadboard`, `Real Time Clock`, `3-Position Rocker Switch`, `Potentiometer`, `12 kOhm Resistor`, `USB Cable`, `Alarm Buzzer`, `Breadboard Wires (M-M)`, `Breadboard Wires (M-F)`, `Adhesive Backing`.
  - Wood, pattern "<Role> - Part F<n>": `Front Side - Part F1`, `Rear Side - Part F2`, `Bottom Side - Part F3`, `Top Side - Part F4`, `Left Side - Part F5`, `Right Side - Part F6`, `Alarm Bracket - Part F7`, `Right LCD Bracket - Part F8`, `Left LCD Bracket - Part F9`.
  - 18 of the 21 are visible across the two views; the two jumper-wire names and `Adhesive Backing` are not.
- **T4. Wood parts self-identify** through their engraved F-number, rendered black.

### Camera
- **C1. One fixed camera per view**; it moves only on the view change.
- **C2. House viewing direction**: perspective, vertical FOV 45, three-quarter view from the front-right and above. [000] elevation 34, azimuth 130; [001] elevation 44, azimuth 138. Other LAC guides sit in the same band (Full Build Start 37/143, Part 2 Start 35/141, Part 3 Start 30/142, Part 2 "Rocker Switch" card 44/137).
- **C3. The row recedes diagonally**, upper-left = far, lower-right = near. The camera looks about 50 degrees ([000]) and 42 degrees ([001]) off the row axis, so parts neither stack behind one another nor line up flat.
- **C4. Zoom is "whole row in frame", not "part fills frame".** Distance scales with row length: 513 mm for a 731 mm row, 1505 mm for a 1532 mm row. Tallest item is 25% of frame height in [000] (breadboard) and 10% in [001] (F4); smallest is 5%. Non-white pixels: 3.75% and 1.31%.
- **C5. Framing is loose and off-centre.** [000] occupies x 13.5-77.5%, y 16-83%; [001] occupies y 13-69% (centre of mass well above the middle, bottom 31% empty). The orbit target is not on the row. The view cube is enabled (`show_viewcube: true`), i.e. the student is expected to orbit and zoom for themselves.

### Look
- **K1. Background pure white `#ffffff`**, single colour (set in [000]; the project default was `#EEEEEE`).
- **K2. Toon shading on every visible solid** (772 of 772, 27 of 27 have `style: toon`), scene render style `matt`.
- **K3. Black outline edges**: `scene_edge_style: normal`, colour `#000000`, width 1, crease angle 40, no separate silhouette style.
- **K4. Lighting**: ambient intensity 1.75 (colour `#333333`), directional 1.0 (`#cccccc`), directional light placed about 70 mm above the [000] camera position (it is not re-keyed for [001]). Result is essentially flat, bright colour with no cast shadow; curved parts show at most two tones (see the coin cell).
- **K5. Parts keep their real-world colours** (section 6); no highlight colour, no ghosting/transparency, no dimming.

---

## 6. Part looks (from the renders; hex = source colour in data, "renders as" = sampled pixels)

| Part | Look |
|---|---|
| Plywood pieces F1-F9 | Flat light tan, source `#deb887`, renders as about `#F8D098`; thin black outline on every cut edge, slot and tab; engraved ID "F<n>" as black `#1e1616` surface patches |
| Breadboard (400-point half size, 83 x 56 x 10 mm) | Pure white body `#ffffff` with black outline; each tie-point is a small black-outlined square (125 black solids); row numbers 1-30 and column letters a-j in black; red `#ff0e00` and blue `#0074d9` power-rail stripes exist but are hairline-thin and effectively invisible at this zoom. Reads as a black-and-white line drawing |
| Nano board | Dark navy PCB `#000f41`; black pin-header strips with pins that read black at this size (source silver `#a6a9aa`); silver mini-USB socket `#d3d6d3`; black chip; tiny white silkscreen specks; 2x3 ICSP header |
| LCD 2004 (98 x 60 mm) | Green PCB `#1a7e26` (renders about `#189028`); black bezel `#1e1616`; light grey screen `#cccccc` (renders `#E8E8E8`); 16-pin header with silver pins along the top edge; mounting holes at the corners |
| Real-time-clock module (HW-84) | Bright blue PCB `#0074d9` (renders about `#0080F8`); black battery holder `#191919`; silver coin cell `#a6a9aa` (renders `#C0C0C0`) with black embossed "CR2032 3 VOLTS" and "+"; black pin row along the bottom edge; a black block of four connector housings on the top header |
| Potentiometer | Brown round body `#855e42` (renders about `#785038`); silver bushing, nut and washer; three short dark legs; black ribbed knob `#1e1616` with a silver skirt ring |
| 12 kOhm resistor | Blue body `#0074d9` with dark bands (data: brown `#a36315`, red `#ff0e00`, black, red, brown = 12 k, 1%; at this zoom the bands just read as dark stripes); silver leads bent down at 90 degrees |
| Rocker switch | All black `#1e1616` body and rocker with white `#ffffff` position marks; three black sleeved terminals; three pre-attached leads black `#2d2926`, tan `#b28362`, red `#ef3340`, each ending in a black pin housing with a silver tip |
| Buzzer | All black disc with two mounting ears and a concentric-ring grille; red `#ef3340` and black `#2d2926` lead pair ending in black housings with silver tips |
| USB cable | Black cable `#2d2926` and black plugs `#1e1616`; silver shells; white `#ffffff` tongue inside the USB-A plug; one end is a right-angle plug |
| Dupont pin housings (`Wire Cap`, `Wire Cap V2`) | Black `#1e1616` rectangular sleeve; V2 adds a silver `#a6a9aa` pin tip |
| Screws / displays / loose jumper wires | Not shown in this guide |

---

## 7. What this means for per-part images (evidence only)

- This guide does **not** contain per-part images. It contains two wide line-ups in which a part is 21-238 px wide on a 1400 px render.
- If crops are taken from it anyway, the screen boxes in 4.1 and 4.2 are the crop rectangles. Wood crops are clean. Electronics crops are clean for switch, buzzer, breadboard, LCD, Nano and RTC; **USB cable, resistor and potentiometer cannot be cropped apart** (70-86% box overlap).
- Scale is not comparable between crops (up to 2.1x drift) because the camera is perspective and the row recedes.
- The reusable parts of this guide for a parts list are: (a) the grouping rule "kit item = pre-attached group", (b) the tooltip name list in T3, (c) the common-orientation and sort-by-F-number rule for wood, (d) the white/toon/black-edge look and the 3/4 viewing direction.
- A better per-part template already exists in the sibling guides: LAC Part 2 [001] "Rocker Switch" shows the *same* component group (switch + 3 leads) alone, centred, camera 175 mm away, elevation 44, azimuth 137, filling about 60% of frame height, no annotations (`thumbs/19075-lcd_alarm_clock_lac_-_part_2/001.jpg`).

---

## 8. Anomalies

### In the guide itself
1. **Leftover placeholder text.** [001] "All Wood" has the Cadasio default step description "A Start point for your project - feel free to rename, reorder or delete".
2. **Title/content mismatch.** Guide is named "LAC Electronics" (tag `lac_electronics`) but half of it is wood.
3. **Three items overlap on screen** in [000] (USB cable, resistors, potentiometer); one of the two resistors is hidden behind the knob.
4. **Two coin cells shown** (`CR2025-50003LC-1` and `-2`) stacked 2.5 mm apart; visible as a faint second rim.
5. **Battery name mismatch.** Component is called `CR2025-50003LC` but the model is embossed "CR2032".
6. **Orphan connector housings.** Four black Dupont housings (`Wire Cap-9/11/12/13`) sit on the RTC header with their wires hidden, and they have no tooltip name.
7. **Kit items missing from the overview:** jumper wires (M-M and M-F) and adhesive backing.
8. **Inconsistent tidiness between the two views:** wood is aligned, co-oriented and sorted; electronics is not aligned to a ground plane, not re-oriented and not sorted.
9. **Near-miss rotations.** RTC and coin cells are rotated 179.0 degrees, not 180.
10. **Hidden "Start" step is last** in the step order (index 2), whereas every other LAC guide has a visible "Start" first.
11. **Thumbnails saved at different window shapes**: 2559 x 1239 (2.07:1) for [000], 3152 x 2596 (1.21:1) for [001], the latter saved ten weeks after the last edit.
12. **150 dead annotation objects** and stale step counters carried over from the Full Build project.
13. **Unintended slides** of F5/F6 during the view change (M2).

### In the study data (affects other guides too - please pass on)
- **D1. Digest visibility under-counts parts whose assembly reference is flagged `hidden` in the CAD tree.** `digest.py` requires every ancestor to be visible; the thumbnails show that a step setting `visible:true` on the leaf solids is enough. Here that hides F2, F4, F5, F6 from [001] (digest: 5 parts / 15 solids; truth: 9 parts / 27 solids) and 39 solids of the LCD from [000] (digest 733 solids; truth 772). Running both models over the other LAC raws, they disagree on 74 of 131 Full Build steps, 20 of 42 Part 2, 16 of 21 Part 3, 42 of 42 Part 4, 74 of 130 Deconstruction, 0 of 32 Part 1 - always about wood panels F4, F5, F2, F6, F1. Spot check: the Full Build [000] thumbnail clearly shows the top panel F4 and side panel F6, which the digest model treats as hidden. 27 top-level references are tree-hidden in the LAC CAD (F2-1, F2-2, F4-1, F4-3, F5-1, F6-1, LAC Knob-3, Part8-14, Part16, Part20-25, Part68-70, Part74, Wire Cap-22/23).
- **D2. Digest `MOVE` / "appear displaced" vectors of 1.7-2.0 m are not motion.** A component's `position` property is its local translation and equals the reference transform's translation when unmoved; the digest adds it as if it were an offset. Real offset = `position - transform translation`. Example here: resistor leads "MOVE [713.4, 865.5, 1642.0]mm (1989mm)" are really (44.3, 0, 371.8) mm. Same artefact in `lac_full_build` [000] ("F1-1 MOVE [720.8, 992.2, 1206.7]mm").
- **D3. Digest direction words for sub-solid offsets are in the parent component's local frame, not world.** Example: F3-1 "appears displaced [-755.3, -3.1, -21.2]mm (-X)" is really a world displacement of (17.7, 32.9, 755.3) mm, i.e. along +Z. In LAC Part 2 [001] the digest reports the switch-lead housings as displaced "+Z" while the switch is "+Y (up)"; in world space all of them are (0, +81.2, 0), straight up.
- **D4. Digest step [000] "MOVE"/"camera MOVES 175 to 513mm" lines** are differences against the un-keyed default state, not something a student watches.
- **D5. The digest header's annotation inventory, label texts and image list for this guide describe unused inherited objects.**

---

## 9. Relation to the other LAC guides

- **Same model, same look.** Identical CAD, identical scene style (white, toon, black edges, ambient 1.75, FOV 45) and the same tooltip mechanism and name list as `lac_full_build`, `lac_deconstruction` and LAC Parts 1-4. (The tooltip-by-"Description" mechanism is in fact present in all 20 guides.)
- **Different genre.** It shares none of the build-guide structure (Start page, section cards, Step N / Step Nc, Transition, Completed View) and uses none of the annotation types.
- **Closest relatives inside the build guides** are the section cards (e.g. Part 2 [001] "Rocker Switch", Part 3 [001] "Alarm Buzzer", Full Build [014] "Real Time Clock", [078] "LCD Screen", [087] "USB Cable"), which isolate one kit item on a white background. The grouping is the same (switch shown with its three leads in both), and the camera direction is the same band; the difference is one item filling the frame versus nine in a row.
- **Section-card titles and tooltip names agree** for the items I compared: "Rocker Switch" card / "3-Position Rocker Switch" tooltip; "Alarm Buzzer", "Real Time Clock", "LCD Screen", "USB Cable" identical.
- I did not read the other LAC guides in full; the comparisons above come from their digest headers, step-name lists, three thumbnails and targeted queries on their raw payloads.

---

## 10. Files

- Report: `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/reports/guide_19075-lac_electronics.md`
- Geometry model (corrected visibility and offsets, projection to screen): `reports/_work_lac_elec/model.py`, output `reports/_work_lac_elec/model.json`
- Cross-guide visibility check: `reports/_work_lac_elec/vis_check.py`
- Verification overlays: `reports/_work_lac_elec/overlay_000_left.png`, `overlay_000_right.png`, `overlay_001.png`
- Zoom crops used for part looks: `reports/_work_lac_elec/c0_*.png`, `c1_*.png`, `z_*.png`
