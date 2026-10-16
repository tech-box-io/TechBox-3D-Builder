# Dimension report: Visual style and the part colour library

Scope: all 20 published TechBox Cadasio guides (LSM x8, LAC x7, PMG x5). Everything below was recomputed from the raw payloads (`cadasio_raw/*.json`) and the digests, then checked against Cadasio's own saved renders (`thumbs_raw/*.webp`). The per-guide reader reports were used as leads only; where they disagree with the data it is said so.

Working files (scripts, per-solid colour dumps, machine-readable library): `reports/_work_dim_style/`
- `colour_library.json` - the part colour/material table in machine-readable form (same content as section 3 and 4).
- `extract.py` -> `solids_<guide>.json` (displayed colour of every solid on every viewer step), `xcmp.py` (cross-guide comparison per sub-feature), `annos.py` (styles of the 1,010 annotation objects that are ever shown), `toonval.py` (render check of the shading formula), `styleop.py`, `colchange.py`, `scene2.py`.

How colours were read: a solid's displayed colour on a step = the nearest `colour_main` set on it or an ancestor by any earlier step, else the CAD material colour (`versionMtlData` Kd). A solid counts as shown on a viewer step when its nearest explicit `visible` flag is true (leaf first, then ancestors), else the CAD tree's hidden flag. Counts called "solid-steps" are (solid x viewer step) pairs. Hex values in the library are base (albedo) colours, not screen pixels; section 2 gives the exact base-to-pixel rule.

Frames looked at (Read tool, 29 frames across the three kits): LSM Part 1 [000] [005] [007] [011]; LSM Part 2 [010] [019] [027]; LSM Part 3 [001] [012]; LSM Part 4 [016] [023]; LSM Full [000]; LAC Electronics [000]; LAC Part 1 [014] [019]; LAC Part 2 [001] [002] [025]; LAC Part 3 [008]; LAC Part 4 [034]; LAC Decon [049]; PMG Part 1 [001] [002] [006] [030]; PMG Part 2 [013]; PMG Part 3 [008] [023]; PMG Full [000].

---

## 1. Scene and render settings

### 1.1 What is identical in all 20 guides

| Setting | Value | Count |
|---|---|---|
| Background | single colour `#ffffff` (project default `#EEEEEE` is overridden in the first authored step) | 20/20 |
| Scene render style | `matt` at scene level, but every visible solid is overridden to `toon` | 20/20; 579,103 of 579,220 visible solid-steps are `toon` (99.98%) |
| Part edges | `style_edges = normal` on every visible solid | 579,042 of 579,220 solid-steps (99.97%) |
| Edge colour / width / crease angle | `#000000`, 1, 40 degrees | 20/20 |
| Silhouette | `none` | 20/20 |
| Camera | perspective, FOV 45 | 20/20 (one step uses FOV 50: LSM Part 1 [011] Capacitor card) |
| Ambient light colour / directional light colour | `#333333` / `#cccccc` | 20/20 |
| View cube shown, up axis `+y` at start | true, `+y` | 20/20 |
| Shadows, ground plane, reflections | none (no such property; none visible in any render) | 20/20 |
| Animation | show = fade, hide = fade, move = tween; camera tween speed 2, no orbit animation | 1,105 of 1,105 authored steps |
| Project flags | `autoStart`, `animateStepsViewer`, `animatePreviousStep`, `edgesVisibleOnAnimate`, `tooltips` true; nav overlay `horizontal_bottom`; `baseFontSize` 20; `stepPrefix` "Step"; no transparent background | 20/20 |
| Opacity of parts | 1.0 | all but 30 solid-steps (the one ghosting step, section 5 rule STYLE-7) |

### 1.2 What differs by kit (light intensity, scene edge flag, light-follow flag, default font)

| Guides | ambient intensity | directional intensity | `scene_edge_style` | `scene_light_follow_camera` | `defaultFont` |
|---|---|---|---|---|---|
| LAC x7 (Parts 1-4, Full, Decon, Electronics) | 1.75 | 1.0 | `normal` | unset | PublicSansMedium, `#637381` |
| LSM Part 1, Part 2, Part 1+2 | 1.875 | 1.0 | `none` | unset | Part 1: PublicSansMedium; Part 2 and 1+2: unset |
| LSM Part 3, Part 4, Part 3+4, Full, Decon | 2.0 | 1.0 | `none` | unset | Full: PublicSansMedium; others unset |
| PMG x5 | 1.875 | 1.15 | `none` | `false` (explicit) | PublicSansMedium, `#637381` |

Project default lighting before the first step is ambient 1.2 / directional 1.0; all 20 guides raise the ambient in their first authored step (to 1.75, 1.875 or 2). The scene-level edge flag has no visible effect because the edges are switched on per part: renders of `none` guides (LSM, PMG) and `normal` guides (LAC) both show the same thin black outlines.

Where the style is applied: in the first authored step (hidden in 15 guides, the visible Start page in 5). 92% of all 29,364 colour overrides (27,006) are set at or before the first viewer step; the remainder are late fixes, not step effects (section 5, STYLE-6).

---

## 2. How a base colour becomes a pixel (toon shading)

Finding: the saved renders are reproduced, to within 1-2 levels per channel, by the default two-tone ramp of a three.js toon material:

    pixel = min(255, base * (0.2 * ambient + 0.8 * directional * tone))     per sRGB channel
    tone  = 1.0 on lit faces, 0.7 on shaded faces  (lit when N.L > 0.4)

0.2 and 0.8 are the ambient and directional light colours `#333333` and `#cccccc`. The two tone values (1.0 and 0.7) and the additive form are measured from the renders; the 0.4 threshold is the three.js default for this ramp and was not measured. Resulting multipliers:

| Lighting | lit x | shade x |
|---|---|---|
| LAC (1.75 / 1.0) | 1.150 | 0.910 |
| LSM Part 1, 2, 1+2 (1.875 / 1.0) | 1.175 | 0.935 |
| LSM Part 3, 4, 3+4, Full, Decon (2.0 / 1.0) | 1.200 | 0.960 |
| PMG (1.875 / 1.15) | 1.295 | 1.019 |

Check against renders (dominant pixel clusters in `thumbs_raw`, script `toonval.py`):

| Frame | base | predicted lit -> found | predicted shade -> found |
|---|---|---|---|
| LSM Part 1 [005] | wood `#deb887` | `#ffd89f` -> `#ffd89f` | `#d0ac7e` -> `#d0ad7e` |
| LSM Part 1 [005] | breadboard `#ffffff` | `#ffffff` -> `#ffffff` | `#eeeeee` -> `#efefef` |
| LSM Part 2 [019] | D2 face `#855e42` | `#9c6e4e` -> `#9d6d4e` | (not present) |
| LSM Part 3 [012] | wood `#deb887` | `#ffdda2` -> `#ffdda2` | `#d5b182` -> `#d5b282` |
| LSM Part 3 [012] | wire purple `#4e008e` | `#5e00aa` -> `#5e00ab` | `#4b0088` -> `#4b0189` |
| LAC Part 1 [019] | wood `#deb887` | `#ffd49b` -> `#ffd49c` | `#caa77b` -> `#c9a77c` |
| LAC Part 1 [019] | RTC board `#0074d9` | `#0085fa` -> `#0086fa` | `#006ac5` -> `#026cc5` |
| LAC Part 3 [008] | LCD board `#1a7e26` | `#1e912c` -> `#1d912d` | `#187323` -> `#197323` |
| LAC Part 3 [008] | LCD glass `#cccccc` | `#ebebeb` -> `#ebebeb` | - |
| PMG Part 1 [002] | shield `#224bbe` | `#2c61f6` -> `#2c61f5` | - |
| PMG Part 3 [023] | wood `#deb887` | `#ffeeaf` -> `#ffeeb0` | `#e2bb8a` -> `#e3bb8b` |
| PMG Part 3 [023] | button cap `#0074d9` | `#0096ff` -> `#0097ff` | `#0076dd` -> `#0275dd` |

Consequences worth knowing:
- The same wood (`#deb887` in all 20 guides) is drawn as `#ffd49b/#caa77b` in LAC, `#ffd89f/#d0ac7e` or `#ffdda2/#d5b182` in LSM and `#ffeeaf/#e2bb8a` in PMG. The kits look different only because the light intensities differ, not because the materials do.
- Bright colours clip: white is `#ffffff` lit in every kit, and in PMG even shaded `#ffffff` stays `#ffffff`, so a pure white part has no visible shading there. The PMG white wire (`#e4e4e4`) is `#ffffff` lit and `#e8e8e8` shaded; the Part 1 reader notes it almost disappears against the background in [009]-[010].
- Predicted lit / shade pixels for the main swatches:

| base | LAC lit / shade | LSM 1.875 lit / shade | LSM 2.0 lit / shade | PMG lit / shade |
|---|---|---|---|---|
| wood `#deb887` | `#ffd49b` / `#caa77b` | `#ffd89f` / `#d0ac7e` | `#ffdda2` / `#d5b182` | `#ffeeaf` / `#e2bb8a` |
| wood dark face `#855e42` | `#996c4c` / `#79563c` | `#9c6e4e` / `#7c583e` | `#a0714f` / `#805a3f` | - |
| white `#ffffff` | `#ffffff` / `#e8e8e8` | `#ffffff` / `#eeeeee` | `#ffffff` / `#f5f5f5` | `#ffffff` / `#ffffff` |
| engraving black `#1e1616` | `#231919` / `#1b1414` | `#231a1a` / `#1c1515` | `#241a1a` / `#1d1515` | `#271c1c` / `#1f1616` |
| silver `#a6a9aa` | `#bfc2c4` / `#979a9b` | `#c3c7c8` / `#9b9e9f` | `#c7cbcc` / `#9fa2a3` | `#d7dbdc` / `#a9acad` |
| PCB navy `#000f41` | `#00114b` / `#000e3b` | `#00124c` / `#000e3d` | `#00124e` / `#000e3e` | `#001354` / `#000f42` |
| shield blue `#224bbe` | - | - | - | `#2c61f6` / `#234cc2` |
| module blue `#0074d9` | `#0085fa` / `#006ac5` | `#0088ff` / `#006ccb` | `#008bff` / `#006fd0` | `#0096ff` / `#0076dd` |
| lead red `#ef3340` | `#ff3b4a` / `#d92e3a` | `#ff3c4b` / `#df303c` | `#ff3d4d` / `#e5313d` | - |

Light direction (partly resolved):
- Faces that point along the scene up-axis are lit in every frame checked (11/11: LSM Part 1 [005], Part 3 [001] [012], Full [000]; LAC Part 1 [019], Part 2 [002] at camera elevation 17, Part 4 [034]; PMG Part 1 [001] [002], Part 3 [008] [023]). In PMG Part 3 [008] the scene up-axis is `-y` and the camera is below the model: the faces now on top are the lit ones, so the light follows the scene up-axis, not world +Y.
- PMG (`scene_light_follow_camera = false`): every vertical face sampled is shaded (Part 3 [023]: H1, H2, H8 faces and the rear wall `#e3bb8b`, deck `#ffeeb0`). The light is effectively along the up-axis.
- LSM and LAC (flag unset): some vertical faces are lit and it changes with the camera. LSM side panel D5 (world normal +X) is lit in Full [000] (azimuth 54) and shaded in Part 3 [012] (azimuth 35); LAC front panel F1 is lit while end panel F5 is shaded in Part 4 [034]. A world-fixed light cannot produce that, and no single camera-relative direction fitted the 16 faces I tested in 6 frames. See open questions.
- Outline widths measured on 2,560 px wide renders: part edges 1-2 px, red lead lines 4 px, cyan underline/leader 4-5 px.

---

## 3. Part colour library

Reading the tables: one row per sub-feature (a solid or group of solids inside the component). "Same in all" means every guide of that kit that shows the part uses the hex. `#cad1ee` / `#cad1ed` is the SolidWorks default grey-blue of a solid nobody recoloured; where it is on screen it is an authoring leftover, not a choice (listed under anomalies).

Share of visible solids whose colour is a step override rather than the CAD colour: LAC 84%, LSM 76%, PMG 17%. LAC and LSM were repainted in Cadasio with a small swatch set; PMG mostly keeps the colours of the imported CAD models.

### 3.1 Laser-cut wood (all three kits)

| Sub-feature | Hex | Evidence |
|---|---|---|
| Panel body (one solid, 3.0 mm thick; 3.2 mm for LSM top lens plate and side D3) | `#deb887` | 100% of wood-body solid-steps in all 20 guides (LSM 11 panel component types, LAC F1-F9, PMG H1-H14 and 4 keys) |
| Engraved ID (D1..D11, F1..F9, H1..H14, H9): one zero-thickness surface decal per character, 2 per panel, 3 for two-digit IDs | `#1e1616` | 100% in LSM and LAC; PMG 98% (H14 pose copy has one decal left at `#deb887`) |
| LSM button panel D2 (`LSM_Side3`): full-face surface overlay on the outer face, 95.3 x 50.8 mm | `#855e42` | LSM only, 7/7 LSM guides that show D2 (seen in Part 2 [019], Part 3 [001] [012], Full [000]) |
| LSM light-guide stems (64x, 3.2 x 3.2 x 66.7 mm) | `#ffffff` | LSM Part 4 [023], Full [000] |

There is no wood grain, no texture and no separate edge (burnt) colour: the darker panel edges in the renders are the shaded tone of the same `#deb887`. D2 is the only panel with a second face colour.

### 3.2 Breadboard (LSM, LAC)

| Sub-feature | Hex | Notes |
|---|---|---|
| Body 83.0 x 56.1 x 8.5 mm and base plate 81.7 x 54.8 x 1.0 mm | `#ffffff` | same in all |
| Hole squares, row letters and column numbers (surface decals) | `#000000` | 128 decals in LAC, 132-134 in LSM |
| Power rail line (+), 2 lines 71.7 x 0.5 mm | `#ff0e00` | same in all |
| Power rail line (-), 2 lines | `#0074d9` | same in all |
| Adhesive backing sheet (`Paper`, 0.2 mm) | `#aaaaaa` | LSM Part 1/2/1+2, LAC. In LSM Part 4, 3+4, Full and Decon the same solid reappears inside the housing recoloured `#deb887` (stray part, see anomalies) |

### 3.3 Arduino Nano

Two different CAD models are used: LSM uses `Arduino Nano v12.step` (155 solids), LAC and PMG use `nano` (293-295 solids). They are painted alike.

| Sub-feature | LSM Part 1 / 2 / 1+2 | LSM Part 3 / 4 / 3+4 / Decon | LSM Full | LAC | PMG |
|---|---|---|---|---|---|
| PCB (43 x 18 mm) | `#000f41` | `#000f41` | `#000f41` | `#000f41` | `#000f41` |
| Long pin-header plastic (2 strips) | `#1e1616` | `#000f41` | `#181818` | `#1e1616` | `#191919` |
| 2x3 ICSP header plastic | `#1e1616` | `#191919` | `#191919` | `#181818` / `#191919` | `#191919` / `#181818` |
| Header pins (30) | `#a6a9aa` | `#a6a9aa` | `#a6a9aa` | `#a6a9aa` | `#e4e4e4` |
| ICSP pins (6) | `#c8b273` | `#c8b273` | `#c8b273` | `#a6a9aa` | `#e4e4e4` |
| USB socket shell | `#a6a9aa` | `#f5f5f6` | `#f5f5f6` | shell `#cccccc`, core `#a6a9aa` | `#e4e4e4` |
| Main IC and other IC bodies | `#191919` | `#191919` | `#191919` | `#191919` | `#191919` |
| IC legs, SMD passives | `#c4c5c4` | `#c4c5c4` | `#c4c5c4` | `#a6a9aa` | `#e4e4e4` |
| Solder pads, LED bodies | `#f6f6f3` | `#f6f6f3` | `#f6f6f3` | `#d3d6d3` / `#efefef` | `#d3d6d3` / `#efefef` |
| Small light components (regulator, crystal, LED base, USB contacts) | `#f5f5f6` | `#f5f5f6` | `#f5f5f6` | `#d3d6d3` | `#d3d6d3` |
| Reset button | - | - | - | `#a6a9aa` | shell `#e4e4e4`, core `#d3d6d3` |
| Tan SMD capacitors | - | - | - | `#a5936d` | `#a5936d` |
| LED lamp (LSM model) | `#f2cb7c` | `#c8b273` | `#c8b273` | - | - |

Always true: the board is dark navy `#000f41` (20/20 guides, all visible Nano instances). Usually true: header plastic near-black, pins silver. Exceptions: in LSM Part 3, Part 4, Part 3+4 and Deconstruction the two long header strips are the same navy as the board (100% of their solid-steps), so the headers do not read as a separate black part; the LSM Full Build has them `#181818` (98%).

### 3.4 Nano I/O expansion module / shield (PMG only)

| Sub-feature | Hex | Notes |
|---|---|---|
| PCB 57.2 x 53.3 x 1.6 mm | `#224bbe` | override of CAD `#d8d8d8`; 5/5 PMG guides |
| Pin-header blocks, plastic (all S / V / G rows; 4-pin and 8-pin blocks) | `#ffff80` | CAD colour; every block, every row |
| 3-pin header block, plastic | `#fffc9f` | CAD colour |
| Header pins on those blocks | `#e3e3e3` | override |
| Nano socket strips (2 x 15) | `#181818` | override of CAD `#f1ff97` |
| DC power jack body | `#000000` | pad `#c0c0c0` |
| Electrolytic capacitor (6.3 mm can) | `#191919` | no stripe |
| Regulator, small SMD | `#cccecc`; resistors `#d1d1d1`; packs / LEDs `#d8d8d8` | |
| Reset button | shell `#e5eaed`, core `#191919` | |

All header rows (S, V and G) are the same pale yellow, which matches the product photo shown beside the model on the PMG Part 1 [001] card (confirmed in [001] and [002]). The rows are therefore told apart only by the label text (S4 / V4 / G4), never by colour.

### 3.5 Dupont housings ("Wire Cap")

| Sub-feature | LSM Part 1 / 2 / 1+2 / 3 / 4 / 3+4 | LSM Full / Decon | LAC | PMG |
|---|---|---|---|---|
| Female housing (`Wire Cap`, one solid) | `#1e1616` | `#1e1616` | `#1e1616` | `#000000` |
| Male housing sleeve (`Wire Cap V2` Cut-Extrude) | `#1e1616` | `#1e1616` | `#1e1616` | `#000000` |
| Male pin (`Wire Cap V2` Fillet) | `#cccccc` on stand-alone housings; `#a6a9aa` on the housings built into the ribbon component | `#a6a9aa` | `#a6a9aa` | `#e4e4e4` (CAD colour; male ends are rare in PMG) |

Housings are always black regardless of wire colour (every guide). A wire is three components: wire body + two housings.

### 3.6 Jumper wires and leads

Wire bodies are single solids, about 58 mm long, 1.2 mm diameter when loose. Loose and routed models of one wire carry the same hex except where noted.

LSM (7/7 guides that show wires agree; Part 1 has none):

| Wire | Hex | Used for |
|---|---|---|
| 3-way M-F ribbon, wire 1 | `#ffffff` | i2 -> V+ |
| wire 2 | `#b1b3b3` | i3 -> V- |
| wire 3 | `#4e008e` | b19 -> In |
| Push-button lead | `#ef3340` | red lead |
| Push-button lead | `#2d2926` | black lead |

LAC (each hex is identical in every LAC guide that shows the wire):

| Wire | Hex | Used for (Full Build step) |
|---|---|---|
| 6-way M-M ribbon | `#2d2926` | i23 -> (+) rail (Step 9) |
| | `#10cc62` (loose model `#2ecc40`) | i24 -> (-) rail (Step 10) |
| | `#611b6c` | i22 - a8 (Step 11) |
| | `#0074d9` | i21 - a9 (Step 12) |
| | `#cccccc` (loose model `#aaaaaa`) | a14 -> (-) rail (Step 13) |
| | `#800000` | a12 -> (+) rail (Step 14) |
| M-M jumper pair | `#ff851b`, `#eac80d` | j1 - i27, j3 - i29 (Steps 20-21) |
| 4-way M-F ribbon (LCD) | `#611b6c`, `#eac80d`, `#13a3a3`, `#0074d9` | GND, VCC, SDA, SCL (Steps 36-39) |
| Pre-wired leads (switch, potentiometer) | `#ef3340`, `#b28362`, `#2d2926` | red, tan, black |
| Buzzer leads | `#ef3340`, `#2d2926` | red, black |

PMG (5/5 guides agree):

| Wire set | Hex in ribbon order |
|---|---|
| 12-way F-F ribbon (buttons, Steps 3-14) | `#b70101`, `#e4e4e4`, `#343232`, `#21f17a`, `#7c5a30`, `#ffdc00`, `#85144b`, `#737980`, `#3876ac`, `#a75294`, `#ff4136`, `#3d9970` |
| 9-way F-F ribbon (display 4 + matrix 5, Steps 16-24) | `#ac9400`, `#000000`, `#ab53ca`, `#bb3d3d`, `#411900`, `#339f3f`, `#2a2f62`, `#662639`, `#377e89` |

Facts about the palette:
- 40 distinct hexes on wire bodies across the kits (LSM 6, LAC 13, PMG 23, counting the USB cable and the three near-duplicate variants listed under anomalies). LSM and LAC wires reuse the house swatches (`#2d2926`, `#ef3340`, `#0074d9`, `#ffffff`, `#b1b3b3`, `#cccccc`, `#ff851b`); PMG's two ribbons use 21 colours of which only `#000000`, `#ffdc00` and `#e4e4e4` occur anywhere else in the kit.
- The same nominal colour is a different hex in each kit: purple is `#4e008e` (LSM), `#611b6c` (LAC), `#ab53ca` / `#a75294` (PMG); red is `#ef3340` (LSM, LAC leads), `#b70101` / `#bb3d3d` / `#ff4136` (PMG); green is `#10cc62` (LAC), `#21f17a` / `#339f3f` / `#3d9970` (PMG).
- Colour never encodes function: black goes to (+) (LAC Step 9), red is GND (PMG Step 19), purple is GND and yellow VCC on the LCD. Colour identifies which physical wire to pick up.

### 3.7 Through-hole passives (LSM, LAC)

| Part | Sub-feature | Hex |
|---|---|---|
| Resistor | body 11 x 4.9 mm | `#0074d9` |
| | leads (bent model) | `#a6a9aa` |
| | 12 kOhm bands, in order | `#a36315`, `#ff0e00`, `#000000`, `#ff0e00`, `#a36315` |
| | 330 Ohm bands, in order | `#ff851b`, `#ff851b`, `#000000`, `#000000`, `#a36315` |
| Capacitor (LSM) | can 10 x 5 mm | `#000000` (Part 1, 2, 1+2), `#1e1616` (Part 3, 4, 3+4, Full, Decon) |
| | polarity stripe and top disc | `#a6a9aa` |
| | legs | `#a6a9aa` |

LAC uses the 12 kOhm band set on both resistors. Bands are five ring-shaped surface decals on the body solid.

### 3.8 USB cable (all kits)

| Sub-feature | LSM | LAC | PMG |
|---|---|---|---|
| Plug overmoulds (USB-A end 49.5 mm, right-angle mini-B end 24 mm) | `#1e1616` | `#1e1616` | `#1e1616` |
| Cable (128.5 mm, 4.6 mm dia) | `#2d2926` | `#2d2926` | `#1e1616` |
| USB-A metal shell | `#a6a9aa` (`#aaaaaa` in Part 2 / 1+2) | `#a6a9aa` | `#a6a9aa` |
| USB-A tongue and window decals (3) | `#ffffff` | `#ffffff` | `#e4e4e4` |
| Mini-B metal tip | `#ffffff` / `#a6a9aa` (Part 2, 1+2); `#cccccc` plus one solid at `#cad1ee` (Part 3, 4, 3+4, Full; Decon `#cccccc`) | `#a6a9aa` | `#e4e4e4` / `#a6a9aa` |

### 3.9 LSM-specific modules

| Part | Sub-feature | Hex |
|---|---|---|
| 8x8 LED matrix (323 solids) | board 63.8 x 60.4 mm | `#000000` (Part 2, 1+2), `#1e1616` (Part 3 onward) |
| | 64 LED bodies 6.3 x 5.0 x 1.5 mm | `#fbfbfb` |
| | 64 lens discs 3.6 mm | `#b1b3b3` (Part 2, 1+2); Part 3 onward `#a6a9aa` on 74% of solid-steps, `#b1b3b3` on the rest (differs per pose copy) |
| | solder pads, pin stubs | `#a6a9aa` (Part 2, 1+2); Part 3 onward `#b1b3b3` on 69-86%, `#a6a9aa` on the rest |
| Panel push button (8 solids) | body, cap, lead sleeves | `#1e1616` |
| | flange ring 21 x 18 x 1.5 mm | `#cccccc` |
| | lead stubs | `#ef3340`, `#2d2926` |
| | two terminal tabs | `#cad1ee` (never recoloured) |

### 3.10 LAC-specific modules

| Part | Sub-feature | Hex |
|---|---|---|
| RTC module (HW-84) | PCB 38.3 x 21.9 mm | `#0074d9` |
| | battery holder, ICs, pin-strip plastic | `#191919` |
| | 6 header pins | `#f4e5a7` |
| | SMD parts | `#a6a9aa` (also `#a0a0a0`, `#c4c5c4`) |
| | coin cell CR2025 | `#a6a9aa` |
| LCD 2004 + I2C backpack | PCB 98 x 60 mm | `#1a7e26` |
| | bezel 97 x 40 x 13 mm | `#1e1616` |
| | glass 76 x 25.2 mm | `#cccccc` |
| | backpack PCB, header plastic | `#1e1616` |
| | header pins (16 + 4) | `#a6a9aa` |
| | I2C IC | `#404040` |
| | trimmer / its legs | `#0064d8` / `#e1e1e1` |
| | SMD 0603 body / ends | `#2d2926` / `#99aaaa` |
| | SMD 0805 body / ends | `#cad1ed` (never recoloured) / `#e5e5e5` |
| Rocker switch (13 solids) | body, rocker, 3 terminal sleeves | `#1e1616` |
| | legend marks (4 decals) | `#ffffff` |
| Potentiometer | metal can and shaft | `#a6a9aa` (`#808080` in the pose copies used in Part 4, Full, Decon: 19-71% of solid-steps) |
| | phenolic base | `#855e42` |
| | knob body / cap and pointer | `#1e1616` / `#a6a9aa` (`#e4e4e4` on some pose copies) |
| | nut, washer | `#a6a9aa` |
| Piezo buzzer | body 47.5 x 40.2 x 15.5 mm | `#1e1616` |
| | lead stubs | `#ef3340`, `#2d2926` |

### 3.11 PMG-specific modules

| Part | Sub-feature | Hex |
|---|---|---|
| Push-button module (11 solids) | PCB 22 x 13 mm | `#000f41` |
| | tact switch body | `#1e1e1e` |
| | cap, one per module | `#000000`, `#ffdc00`, `#ffffff`, `#0074d9` (left to right, D4-D7) |
| | 3-pin header plastic / pins | `#1a1a1a` / `#c6c1bc` |
| TM1637 4-digit display (41 solids) | PCB | `#224bbe` |
| | display block | `#000000` |
| | 30 segment decals (4 x 7 + colon) | `#ffffff` |
| | header pins (two solid groups) | `#e3e3e3`, `#cccccc` |
| 32x8 LED matrix (500 solids) | PCB 129.5 x 32 mm | `#234bbf` |
| | 4 matrix blocks 31.8 mm | `#ffffff` with top mask `#1a1a1a` |
| | LED dots (256) and pins | `#e4e4e4` |
| | MAX7219 ICs | `#232323` |
| | input header plastic | `#0a0a0a` |

### 3.12 How multi-colour parts are broken down

The pattern is the same for every part: one solid per material region, plus zero-thickness "Surface-Offset" decals for markings.
- Printed or engraved markings (panel IDs, breadboard holes and legends, rail stripes, resistor bands, capacitor stripe, switch legend, display segments, D2's dark face) are separate surface solids laid 0.1 mm proud of the body, each with its own flat colour. Nothing is a texture.
- Boards are split into PCB, header plastic, pins, IC bodies and SMD parts as separate solids.
- Pre-wired components carry short coloured lead stubs as part of the component; the long wire body and the housings are separate components.
- Solids ever shown in the full builds: LSM 2,182 of 2,909 in the CAD; LAC 1,546 of 1,569; PMG 3,557 of 5,829 (the rest are unused pose copies).

### 3.13 Same part, different colour between guides (complete list of differences found)

| Part / sub-feature | Difference |
|---|---|
| Nano long header strips (LSM) | `#1e1616` (Part 1, 2, 1+2) vs `#181818` (Full) vs `#000f41` (Part 3, 4, 3+4, Decon) |
| Nano USB socket (LSM) | `#a6a9aa` (Part 1, 2, 1+2) vs `#f5f5f6` (Part 3 onward) |
| Nano pins | `#a6a9aa` (LSM, LAC) vs `#e4e4e4` (PMG) |
| Nano ICSP pins | gold `#c8b273` (LSM) vs silver (LAC) vs `#e4e4e4` (PMG) |
| Capacitor can, 8x8 matrix board (LSM) | `#000000` (Part 1, 2, 1+2) vs `#1e1616` (Part 3 onward) |
| 8x8 matrix pads (LSM) | `#a6a9aa` (Part 2, 1+2) vs `#b1b3b3` (Part 3 onward) |
| Male Dupont pin | `#cccccc` (LSM parts) vs `#a6a9aa` (LSM Full / Decon, LAC) vs `#e4e4e4` (PMG) |
| Dupont housing | `#1e1616` (LSM, LAC) vs `#000000` (PMG) |
| USB cable | `#2d2926` (LSM, LAC) vs `#1e1616` (PMG); mini-B tip four different greys / whites |
| LAC green wire | loose `#2ecc40` vs routed `#10cc62` |
| LAC grey wire | loose `#aaaaaa` vs routed `#cccccc` |
| LAC potentiometer can | `#a6a9aa` vs `#808080` on later pose copies |
| LAC knob cap | `#a6a9aa` vs `#e4e4e4` on later pose copies |
| PMG shield's built-in Nano copy (pose copies in Part 3 [042]-[043], Full [100]-[101]) | board `#002e37`, headers `#ffdd87`, IC `#e4e4e4`; Decon repaints it `#000f41` / `#181818` |
| Backing sheet (LSM) | `#aaaaaa` when it is the backing; `#deb887` when the same solid is left on inside the housing |

Within the LAC kit the Full Build and Parts 1-4 agree on every sub-feature (they are slices of one project). Within PMG the five guides agree on every sub-feature except the built-in Nano copy. LSM is the kit with real drift, between the Part 1 / 2 / 1+2 project and the Part 3 / 4 / 3+4 / Full / Decon project.

---

## 4. Annotation colours, fonts and title page

Statistics are over the 1,010 annotation objects that are actually shown in a viewer step (19 of 20 guides; LAC Electronics shows none).

### 4.1 Colours

| Element | Value | Count |
|---|---|---|
| Lead lines | `#ff0000` | 362 / 362 (16 guides) |
| 3D arrows | `#ff0000` | 104 / 104 (15 guides) |
| Label underline | `#7fdbff` | 212 / 212 (12 guides) |
| Label text | `rgb(0,0,0)`, bold | 212 / 212 |
| Leader lines (labels, eye icons, insets, badges) | `#7fdbff` | 454 set explicitly; 42 have no stored colour and still render cyan (PMG Part 2 [013] VCC / V11); 2 are `#7fb9ff` |
| Anchor ring ("Life Saver Circle", dashed, 30 x 30 px) | `#7fdbff` | 491 / 498; exceptions `#39cccc` x3 (the LSM underside step: Part 4 [016], Part 3+4 [030], Full [075]), `#ff5F0B` x2 (PMG Push Buttons card, Part 1 [006] and Full [006]), `#7fb9ff` x2 (the same inset in PMG Part 3 [016] and Full [074]) |
| Inset frame (rounded rectangle, white fill) | border `#7fdbff` | 44 / 46; `#7fb9ff` x2 (same PMG inset) |
| Eye icon | one black raster PNG, same asset in all 19 guides | 224 objects |
| Quantity label | `#7fdbff` ("64X" / "64x", LSM x3), `#0074d9` ("2x", LAC x2) | 5 |
| Highlight rectangles inside inset pictures | red, baked into the image | - |
| Pin badges (LSM V+ / V-In / V-) | cyan-filled disc on the pin, white disc with thin outline on the wire end, black bold text, raster images | 14 objects |

No other annotation colour appears. Red is used only for motion (lines, arrows) and for the boxes inside pictures; cyan only for pointing.

### 4.2 Geometry of the callout furniture

| Element | Value | Count |
|---|---|---|
| Label container | `underline`, thickness 5, white fill, no box | 210 / 212 (thickness 6 x2, LSM c16) |
| Label box size | 175 x 90 px (LSM 2.5em labels 175 x 75); wider for long text (up to 258 px) | 177 / 212 are 175 wide |
| Leader | straight line, solid, thickness 5, leaves the underline at its left or right end (`leader_start_position` x = 0 or 1, y = 1) | 208 / 212 at an end |
| Text alignment | centred | 210 / 212 |
| Lead line | style `solid`, scale 5, screen-space width (`world_units` false) | 326 solid, 36 stored `dashed` (all LSM) that render solid |
| Arrow | straight, body 5, head 20 x 17, head at end | body 5: 92 / 104; head width 20: 88 / 104; head length 17: 76 / 104 |
| Eye icon width | 7.81% of viewport width (LSM, LAC), 8.2% (PMG) | 142 and 62 of 224; 20 others between 6.3 and 9.4 |
| Inset frame | rectangle, border thickness 5, corner radius 0.1, no shadow | 44 / 46 thickness 5 |
| Inset width | 7.8-36.7% of viewport width, median 17.6% | 46 |

### 4.3 Fonts

| Text | Font | Where |
|---|---|---|
| Hole / pin labels, LSM and LAC build guides | Arial bold (explicit `font-family: Arial`), 3em (LAC 80/80; LSM Full 7) or 2.5em (LSM 37) | 124 labels |
| Hole / pin labels, PMG; LAC Deconstruction (GND / VCC / SDA / SCL) | no font-family stored, so the project default applies: Public Sans Medium, bold, 3em | 88 labels (PMG 84, LAC Decon 4) |
| Quantity labels | Arial bold 6em | 5 |
| Photo caption "NANO I/O MODULE LABELS" (PMG Part 1 [001]) | Public Sans Medium 20 px, `#637381` (the project default text style) | 2 |
| Title page | baked into a PNG: heavy condensed sans title and subtitle in dark grey `#585858`, copyright line in a serif face | 19 guides |
| Viewer UI default | Public Sans Medium, base size 20, colour `#637381` | 14 guides set it; 6 LSM guides leave it unset |

The reader report for LAC Deconstruction describes its four labels as Arial; the data has no font-family on them and the render (Decon [049]) shows Public Sans letterforms. The newer projects (LAC Decon Nov 2025, PMG 2026) stopped forcing Arial.

At base size 20 px, 3em is 60 px and 2.5em is 50 px; the saved renders are about 2,560 px wide, so a 3em label is about 2.3% of viewport width tall.

### 4.4 Title page

| Element | Value | Count |
|---|---|---|
| Logo | one SVG, same file in all 19 guides: white "TECHBOX" wordmark and bulb-and-gear icon on a rounded `#00b0ef` panel | 19 / 19 |
| Logo position / width | x 1.8-2.5%, y 4-8% (PMG Decon x 5.1%); width 33.2% (LSM Part 1, 2, 1+2), 37.6% (other LSM), 38.9% (LAC), 39.5% (PMG), 36.4% (PMG Decon) | |
| Title block | PNG, text `#585858`: kit name, part name, copyright; x 1.6-3.8%, y 61-65%; width 42.1-48.4% | 18 / 19; LSM Part 1 is at y 24%, width 58.3% |
| Both images | no frame, no leader, no anchor, opacity 1 | 38 / 38 |
| Model | finished state of that guide, right half of the frame, same toon style | 19 / 19 |

---

## 5. Patterns as rules

STYLE-1. Draw every part with flat two-tone toon shading and thin black outlines on a pure white background; no shadows, ground, textures or gloss.
- Stats: background `#ffffff` 20/20; toon on 579,103 of 579,220 visible solid-steps; edges on 579,042; edge colour `#000000` width 1, crease angle 40 in 20/20.
- Exceptions: 117 solid-steps not toon (one wire solid on LSM Full [087] and Part 4 [028] Completed View; D2 panel and USB plug solids with style unset in LSM Part 2, 1+2 and 3+4); 61 solid-steps with edge style unset in PMG Part 3, Full and Decon. Not noticeable in the renders.

STYLE-2. Compute the two tones as base x (0.2 x ambient + 0.8 x directional x tone), tone 1.0 lit and 0.7 shaded, clamp at 255. Use ambient 1.75-2.0 and directional 1.0-1.15.
- Stats: 12 colour / frame pairs across the four lighting set-ups match prediction within 2 levels per channel (table in section 2).
- Exceptions: none found in the colours large enough to measure.

STYLE-3. Light from the scene's up side: faces pointing along the up-axis get the lit tone; when the scene up-axis is flipped for an underside view the lighting flips with it.
- Stats: up-facing faces lit in 11/11 frames checked, including PMG Part 3 [008] with up-axis `-y`.
- Exceptions: in LSM and LAC some vertical faces are also lit and this varies with the camera (open question).

STYLE-4. Give each physical material one flat colour from a small swatch set, and keep that colour for the part in every guide of the kit.
- Stats: wood `#deb887` in 20/20; engraving `#1e1616`; Nano board `#000f41` 20/20; LAC Parts 1-4 and Full agree on every sub-feature; PMG guides agree on all but one sub-assembly copy.
- Exceptions: the 15 differences listed in 3.13, mostly between the two LSM projects.

STYLE-5. Model markings as separate flat decals, not textures: engraved panel IDs, breadboard holes and legends, rail stripes, resistor bands, polarity stripe, switch legend, display segments.
- Stats: 100% of markings in all three kits are zero-thickness surface solids with their own colour.
- Exceptions: none.

STYLE-6. Never recolour, tint or dim a part to draw attention; a part looks the same when it is new, hovering, seated or finished.
- Stats: 156 visible-solid colour changes between consecutive viewer steps out of 579,220 solid-steps, all of them corrections when leaving the Start page (LSM Full [001]: 139 breadboard decals from `#cad1ee` to their real colours; LAC [001] x4 guides: 4 rail decals; PMG Part 3 [045]: 1 solid). Zero during build steps.
- Exceptions: none intentional.

STYLE-7. Use transparency only to see through a covering part, at 50% opacity, for the single step that needs it.
- Stats: opacity 0.5 on 5 solids (base D1 and front wall D5) for 2 viewer steps in 3 guides (LSM Full [075]-[076], Part 3+4 [030]-[031], Part 4 [016]-[017]); every other solid-step is opacity 1.
- Exceptions: none.

STYLE-8. Engrave the part ID on every wood panel in near-black and leave the wood otherwise unmarked.
- Stats: every panel in LSM (D1-D11), LAC (F1-F9) and PMG (H1-H14, H9 keys) has 2-3 `#1e1616` character decals.
- Exceptions: LSM D2 also has a dark `#855e42` outer face; no other panel in any kit has a second face colour.

STYLE-9. Colour Dupont housings black and their metal pins light grey, whatever the wire colour; colour each jumper wire with its own saturated colour taken in ribbon order.
- Stats: housings `#1e1616` (LSM, LAC) or `#000000` (PMG) in 20/20; 44 wire hexes; no two wires in one ribbon share a colour.
- Exceptions: PMG dark wires `#000000`, `#411900`, `#662639`, `#343232` are hard to tell apart (reader note, confirmed by the hex values).

STYLE-10. Reserve pure red `#ff0000` for motion annotations and light cyan `#7fdbff` for pointing annotations; text and the eye icon are black.
- Stats: 466/466 lines and arrows red; 491/498 anchors, 212/212 underlines, 44/46 inset frames cyan.
- Exceptions: 7 anchors and 2 frames in three other colours (`#39cccc`, `#ff5F0B`, `#7fb9ff`), all one-offs.

STYLE-11. Set callout text in a bold sans at 3em of a 20 px base, black, centred on a 5 px cyan underline; leader and ring in the same cyan, 5 px.
- Stats: 3em 175/212 (2.5em in the older LSM guides), bold 212/212, underline thickness 5 in 210/212, leader thickness 5 in 188/190.
- Exceptions: font family is Arial in LSM / LAC builds (124) and Public Sans in PMG and LAC Decon (88).

STYLE-12. Build the title page from two flat images on white: logo top-left at about 2% / 6% and 33-40% wide, title block lower-left at about 2% / 63% and 42-48% wide, finished model on the right.
- Stats: 19/19 guides with a title page; logo file identical in all.
- Exceptions: LSM Part 1 title block sits at y 24% and is 58% wide; PMG Decon logo starts at x 5%.

STYLE-13. Keep the camera a 45 degree perspective lens.
- Stats: 20/20 guides; 1 step at FOV 50 (LSM Part 1 [011]).

---

## 6. Numeric defaults

| Name | Value | Basis |
|---|---|---|
| Background | `#ffffff` | 20/20 |
| Edge colour / width / crease angle | `#000000` / 1 px / 40 degrees | 20/20 |
| Toon tones | 1.0 lit, 0.7 shaded, threshold N.L 0.4 | render fit, 4 lighting set-ups |
| Ambient light | colour `#333333`, intensity 1.875 (range 1.75-2.0) | LAC 1.75 x7, 1.875 x8, 2.0 x5 |
| Directional light | colour `#cccccc`, intensity 1.0 (PMG 1.15) | 15 guides 1.0, 5 guides 1.15 |
| Lit / shade multiplier | 1.175 / 0.935 at 1.875 / 1.0 | formula |
| Camera FOV | 45 degrees perspective | 20/20 |
| Ghost opacity | 0.5 | 3 guides, one step each |
| Wood | `#deb887` | 20/20 |
| Engraving / black plastic | `#1e1616` | LSM, LAC, PMG wood decals |
| Metal | `#a6a9aa` | override on 6,482 solid-in-guide instances in LSM + LAC (the most used override) |
| Nano PCB | `#000f41` | 20/20 |
| Shield / display PCB | `#224bbe` | PMG 5/5 |
| Module PCB blue | `#0074d9` | LAC RTC; also resistor body, rail (-) |
| Motion annotation colour | `#ff0000` | 466/466 |
| Callout colour | `#7fdbff` | 491/498 anchors |
| Label text | black bold, 3em of 20 px base | 175/212 at 3em |
| Underline / leader thickness | 5 | 210/212, 188/190 |
| Anchor ring | 30 x 30 px dashed ring | 498/498 |
| Lead line width | scale 5, screen space (about 4 px on a 2,560 px wide view) | 362/362 |
| Eye icon width | 7.81% of viewport width (8.2% in PMG) | 142 + 62 of 224 |
| Inset frame | 5 px `#7fdbff`, corner radius 0.1, white fill; width median 17.6% | 44/46 |
| Logo panel / title text | `#00b0ef` / `#585858` | sampled on 5 Start frames |
| Step animation | 800 ms, fade show / hide, tween move | 20/20 guides |

---

## 7. Anomalies (not conventions)

1. Unpainted solids on screen in the CAD default `#cad1ee` / `#cad1ed`: LSM push-button terminal tabs (all LSM guides that show the button), one solid of the right-angle USB plug (LSM Part 3, 4, 3+4, Full), straight resistor leads (LSM Part 3+4, Part 4, Full, Decon), 21 solids of an 8x8 matrix pose copy (LSM Part 2, 1+2), seven SMD 0805 bodies and other small LCD solids (LAC Part 3, 4, Full, Decon: 143-429 solid-steps), rocker-switch terminal sleeves on a pose copy (LAC Part 4, Full, Decon). Share of solid-steps: 0.4-1.4% in the affected guides, 0 in all PMG guides and in LAC Part 1, Part 2, Electronics, LSM Part 1.
2. Colours corrected only when leaving the Start page: in LSM Full Build all 138 breadboard decals are still the default `#cad1ee` on [000] and get their real colours on Step 1 [001] (the breadboard is inside the closed housing on the title page, so this is not seen). In LAC Full, Decon, Part 1 and Part 4 four breadboard decals have the wrong colour on the Start page (two red and one blue become black, one blue becomes red on [001]).
3. Nano header strips painted the same navy as the PCB in LSM Part 3, Part 4, Part 3+4 and Deconstruction; black in the other LSM guides.
4. PMG shield's built-in Nano copy appears with a teal board `#002e37` and cream headers `#ffdd87` in the pose copies used around Steps 45c-46 (Part 3 [042]-[043], Full [100]-[101]); the stand-alone Nano is navy.
5. LAC loose and routed models of two wires differ slightly: green `#2ecc40` vs `#10cc62`, grey `#aaaaaa` vs `#cccccc`. PMG white is `#e4e4e4` on most models and `#e3e3e3` on one.
6. LAC potentiometer can `#808080` and knob cap `#e4e4e4` on later pose copies (CAD colours showing through).
7. LSM backing sheet (`Paper`) is switched on again inside the housing, repainted wood colour `#deb887` (Part 4, 3+4, Full, Decon).
8. Anchor ring colours: `#39cccc` (LSM underside step), `#ff5F0B` (PMG Push Buttons card; the same value is stored, unused, on all 41 unanchored images, so it looks like the tool default), `#7fb9ff` (one PMG inset, frame and leader too).
9. 36 LSM lead lines are stored `dashed` but render solid; 42 leaders have no stored colour but render cyan.
10. Label size is mixed inside LSM Full Build (3em x7, 2.5em x7).
11. Quantity label colour differs: `#7fdbff` in LSM ("64X", "64x"), `#0074d9` in LAC ("2x"). Text case differs too.
12. Title text says "Laser Stem Matrix" (not "STEM"); LSM Part 1 title block is placed mid-left (y 24%) instead of lower-left.
13. Font drift: explicit Arial in LSM and LAC builds, inherited Public Sans in PMG and LAC Deconstruction.
14. Saved thumbnails come in several aspect ratios (2.0:1, 2.07:1, 2.79:1, 1.86:1, 1.2:1), so stored viewport-percentage positions do not map one-to-one to pixels across frames.

---

## 8. Open questions

1. Light direction in LSM and LAC. Up-facing faces are always lit, but some vertical faces are lit depending on the camera (D5 lit at azimuth 54, shaded at azimuth 35). `scene_light_follow_camera` is unset in those 15 guides and explicitly `false` in PMG, where all vertical faces are shaded. I could not fit one camera-relative light vector to the 16 test faces, and the saved renders may not have been captured with the stored step camera. The live viewer needs to be orbited to settle it. Recommendation until then: use the PMG behaviour (light along the scene up-axis).
2. Is the lighting difference between kits (ambient 1.75 / 1.875 / 2.0, directional 1.0 / 1.15) intended, or drift? It changes how the same wood looks (`#ffd49b` to `#ffeeaf` lit). TechBox should pick one.
3. Which Nano palette is canonical: silver pins and black headers (LSM Part 1, LAC) or the PMG CAD defaults (`#e4e4e4` pins)? Same question for Dupont pins (`#a6a9aa` vs `#cccccc` vs `#e4e4e4`) and housings (`#1e1616` vs `#000000`).
4. Is the dark `#855e42` face on LSM panel D2 meaningful (outside face marker) or a one-off? No other panel in any kit has it.
5. Label font: Arial or Public Sans? The two newest projects use Public Sans.
6. The title-page fonts cannot be identified from data because the text is a raster image; TechBox will have the source artwork.
7. Wire palettes are per kit with no shared hexes for the same nominal colour. A single TechBox wire palette would need to be chosen; the guides do not provide one.
