# Verification notes: Visual style and the part colour library

Skeptic pass over `reports/dim_style.md`. Everything below was recomputed with my own scripts in
`reports/_work_verify_style/` (walker `walk.py`, then `style1.py`, `style4.py`, `style6.py`, `opac*.py`, `scene.py`,
`light.py`, `lightpred.py`, `toon.py`, `tones.py`, `decals*.py`, `panels.py`, `wood.py`, `wires.py`, `annos*.py`).
Renders were checked on `thumbs_raw/*.webp` by pixel sampling, not by eye alone.

Verdict summary: 7 confirmed, 8 qualified, 0 refuted outright. The one claim with a real hole is STYLE-3 (lighting):
its headline has a pixel-verified counter-example, its PMG exception note is wrong, and the data field that settles it
(`light_directional.position`, stored in step properties) was not read.

## 0. Two things that affect every count

1. Visibility rule. The analyst counts a solid as shown when its nearest explicit `visible` flag (leaf first, then
   ancestors) is true. `scripts/digest.py` (which the README calls ground truth) requires every ancestor to be visible
   and starts from the CAD `hidden` flag. Totals: 579,220 solid-steps (analyst rule, reproduced exactly) vs 501,702
   (digest rule). Renders side with the analyst: LSM Part 4 [016] shows side wall `LSM_Side4_r2` (CAD-hidden parent,
   leaves explicitly shown), and the green LCD PCB `#1a7e26` is never visible under the digest rule (0 solid-steps in
   all 5 LAC guides) although it is on screen in LAC Part 3 [000]/[008]. So the digest's `visible_solids` undercounts by
   about 13%. I report both where it matters.
2. Saved renders are not one size: 2559x1236/1239 (LSM late, LAC), 2560x1279 (LSM Part 1/2/1+2), 2560x919 and
   3840x1919/1967 (PMG), 1920x729/1034 (PMG Decon), 3152x2596 (LAC Electronics [001]). Pixel measures quoted "on a
   2,560 px view" only hold for LSM/LAC.

## 1. Per-claim results

### STYLE-1 toon + black edges on white: QUALIFIED (rule holds; one default is incomplete)
- Reproduced exactly: toon 579,103 / 579,220 (99.98%); edges normal 579,042 (99.97%). Digest rule: 501,667 / 501,702
  (99.993%) and 501,606.
- Scene values at every one of 1,037 viewer steps: background `#ffffff`, edge colour `#000000`, width 1, angle 40,
  silhouette none, render style matt, in 20/20.
- 0 `map_` texture lines in any CAD material of the 20 payloads; all `Tr 0`.
- Corrections:
  - Crease angle 40 is only the scene default. PMG sets a per-part `edge_angle` of 69 on jumper-wire bodies: 3,941 of
    4,148 wire solid-steps in the 5 PMG guides (95%), plus 48 on 54 solid-steps. LSM and LAC: none.
  - The default-style wire (`Part25^LSM Lab`) is in three guides, not two: LSM Full [087], Part 4 [028], Part 3+4 [042].
  - `scene_edge_style` is `normal` on one LSM Full viewer step ([008] Step 4), so "none in the other 13" has 1 exception.
  - Exceptions otherwise as stated: 114 style-unset solid-steps (D2 `Surface-Offset3` decals in LSM Part 2 x14,
    Part 1+2 x14, Part 3+4 x82; 2+2 USB solids on step 0) and 61 edge-unset (PMG Decon 17, Part 3 22, Full 22).

### STYLE-2 toon formula: CONFIRMED (and strengthened)
- Wood `#deb887` lit and shade clusters in 5 frames per guide: 141 colour/frame pairs in 19 guides, 138 within 1 level,
  3 within 3 (small clusters). LAC `#ffd49c/#c9a77a`, LSM 1.875 `#ffd89f/#d0ad7e`, LSM 2.0 `#ffdda2/#d5b282`,
  PMG `#ffeeb0/#e3bb8b`.
- Other bases on large clusters within 1: `#0074d9`, `#000f41`, `#224bbe`, `#a6a9aa`.
- Light colours `#333333` / `#cccccc` and intensities 1.75 x7, 1.875 x8, 2.0 x5; directional 1.0 x15, 1.15 x5: confirmed.
- New: the switch point, which the analyst left unmeasured, is bracketed by faces whose N.L is known from the stored
  light (section 2): N.L 0.38 is shaded (PMG Part 3 [002] H2), N.L 0.46 is lit (LSM Full [000] D5), 0.29 shaded (LAC
  Decon [031]), 0.63 lit (LSM Part 4 [019]). So 0.38 < threshold <= 0.46, consistent with 0.4.

### STYLE-3 light from the up side: QUALIFIED (headline has a counter-example; see section 2)

### STYLE-4 one flat colour per material region: QUALIFIED
- Reproduced: 29,364 colour-override events, 27,006 (92.0%) at or before the first viewer step; `#a6a9aa` 6,482
  solid-in-guide instances in LSM + LAC. Override shares: LAC 83.7% (6,271/7,490), LSM 76.9% (7,761/10,089), PMG 16.6%
  (2,013/12,112) on the analyst's rule (theirs: 84 / 76 / 17); 86.3 / 74.4 / 14.9 on the digest rule.
- Wrong: "wood `#deb887` in 20/20 guides". PMG Part 1 and Part 2 show no wood solid at all. It is 18 of 18 guides
  that show wood.
- "Small swatch set": distinct hexes on screen are LSM 28, LAC 45, PMG 53; 8, 12 and 11 of them cover 90% of
  solid-steps. PMG is 83% CAD colours, so the swatch discipline is an LSM/LAC property.
- Nano PCB `#000f41` 20/20: confirmed. Header-strip drift confirmed (`#1e1616` Part 1/1+2, `#000f41` Part 3/4,
  `#181818` on 65/66 steps of Full).

### STYLE-5 markings as decal solids: CONFIRMED (numbers tightened)
- Panel ID decals are zero-thickness in every panel of the three full builds (bbox min dimension 0.0000 mm);
  breadboard decals likewise (132 LAC = 128 black + 2 red + 2 blue; 136-138 LSM = 132-134 + 4).
- Offset from the body is not a uniform 0.1 mm: 0.127 mm on LSM and PMG panels, 0.249 mm on LAC panels and LSM matrix
  supports, 0.005-0.06 mm on the breadboard.
- Resistor bands (5 per resistor), rocker legend (4 per switch, 3 pose copies), TM1637 segments (30 per display)
  counted and confirmed. Ring-shaped decals cannot be shown zero-thickness from bounding boxes.

### STYLE-6 no recolouring for emphasis: QUALIFIED
- Reproduced exactly on both visibility rules: 156 colour changes of a visible solid between consecutive viewer
  steps (LSM Full [001] 139 = 138 breadboard decals + 1 Paper; LAC Full/Decon/Part 1/Part 4 [001] 4 each; PMG Part 3
  [045] 1). All 1,010 annotations have `animation_attention: none`.
- "0 during build steps" is off by one: PMG Part 3 [045] is Step 22, a build step (shield pose copy `#000f41` to
  `#224bbe`). It is a correction, not emphasis.
- "A part looks the same" misses size: per-part `scale` is used on two info cards. LSM Part 1 [011] Capacitor card
  scales the capacitor x2 (with FOV 50) and resets on [012]; the Mini USB Cable card (LSM Part 2 [027], Part 1+2 [043])
  scales the plugs x0.95 and resets on the next step.

### STYLE-7 ghosting: QUALIFIED
- Reproduced: 30 solid-steps at opacity 0.5, LSM Full / Part 3+4 / Part 4 only; CAD `Tr 0` everywhere.
- Breakdown is not 5 solids x 2 steps. On the hover step (Full [075], 3+4 [030], Part 4 [016]) 6 solids are at 0.5:
  D1 body + 2 ID decals and side wall `LSM_Side4` body + 2 decals. On the following "c" step ([076], [031], [017]) the
  two bodies are back at 1.0 and only the 4 decals stay at 0.5 until the next Transition resets them. Render check:
  [016] translucent, [017] opaque. So a panel is ghosted for exactly one viewer step; the decals are a leftover.
- Under the digest visibility rule the side wall is not counted, giving 15.

### LIB-WOOD: QUALIFIED
- Panel body `#deb887` on 100% of panel-body solid-steps, 3.0 mm (3.2 mm lens top and Side1); ID decals `#1e1616`
  100% in LSM and LAC; 2 per panel, 3 for two-digit IDs: confirmed.
- 18 guides, not 20 (PMG Parts 1-2 have no panels; LAC Electronics has them on [001] only).
- PMG exception is misdescribed: H14 carries 6 ID decals (two copies of "H14"); one whole copy, 3 decals
  (`Surface-Offset1[1..3]`), is left `#deb887` on 5 steps (Part 3, Full) or 3 steps (Decon). Share black: 1,406/1,421
  = 98.9% (Part 3, Full), 1,174/1,183 = 99.2% (Decon).
- D2 overlay is two `#855e42` solids (50.8 x 95.3 mm and 3.4 x 4.9 mm), 7/7 LSM guides that show D2.

### LIB-BOARDS: CONFIRMED
- Checked: Nano PCB `#000f41` 20/20; shield PCB `#224bbe` 5/5; matrix PCB `#234bbf`; button module PCB `#000f41`,
  switch `#1e1e1e`, caps `#000000/#ffdc00/#ffffff/#0074d9`, socket `#1a1a1a`, pins `#c6c1bc`; RTC `#0074d9`, pins
  `#f4e5a7`; LCD `#1a7e26` in 5 LAC guides; header blocks `#ffff80`, 3-pin `#fffc9f`; LSM ICSP pins `#c8b273` 8/8.
- One count: TM1637 `#224bbe` appears in 4 PMG guides, not 5 (Part 1 does not show the display).

### LIB-HARDWARE: CONFIRMED (within its LSM/LAC scope and listed exceptions)
- Checked: breadboard body/decals/rails; resistor body `#0074d9`, band sets (LSM totals brown 3, black 3, red 2,
  orange 2 = 12k + 330R; LAC red 4, brown 4, black 2 = two 12k); capacitor can `#000000` early / `#1e1616` late, stripe
  and legs `#a6a9aa`; USB; rocker; potentiometer; buzzer; push button incl. unpainted `#cad1ee` tabs.
- "All metal" is not kit-wide: PMG metal is `#e4e4e4`, the LSM button flange is `#cccccc`.

### LIB-WIRES: QUALIFIED (minor)
- Housings black in the 19 guides that have any (LSM Part 1 has no wires); 12 solid-steps of unpainted
  `#cad1ee/#cad1ed` housing on first/last steps of LSM Full, Part 3+4, Part 4.
- Wire-body hexes on single-solid in-context parts: LSM 5, LAC 11, PMG 23 (37 distinct); with the two LAC loose
  variants and the cable this reaches the analyst's 40. Their own report also says 44 in section 5.
- Hex lists per kit match. Ribbon order and "identity not function" were not re-derived.
- Missed: PMG wires carry `edge_angle` 69 (see STYLE-1).

### STYLE-10 red for motion, cyan for pointing: QUALIFIED
- All counts reproduce: 362/362 lines and 104/104 arrows `#ff0000`; 212/212 underlines `#7fdbff`; anchors 491/498
  with the same 7 exceptions; leaders 454 + 2 `#7fb9ff` + 42 unset; frames 44/46.
- Red is reserved only by exact hex. Part colour `#ff0e00` (breadboard (+) rails and resistor bands) is on 2,861
  solid-steps in 15 guides and `#f40000` on 45; on screen these are the same red as a lead line. Cyan is truly
  reserved: no visible solid is within 25 levels of `#7fdbff`.
- Small counts: 503 anchored objects (498 Life Saver Circle + 5 `Basic Circle` `#000000` on quantity labels, not
  drawn in LSM Part 4 [023]); eye PNG used 225 times (one inside a frame).

### STYLE-11 callout label style: CONFIRMED
- 212 labels in 12 guides: bold 212, black 212, centred 210, 3em 175 / 2.5em 37, underline 5 in 210, leader 5 in
  188/190, width 175 in 177, heights 90 x167 and 75 x31, Arial 124 / none 88. Leader leaves the end nearer the target
  in 208/208 end-anchored labels. Underline measures 5 px on a 2,559 px render.
- Stored but not visible: `shadow_enabled: true` on all 212 label containers (no shadow in LAC Part 1 [019]).

### STYLE-12 title page: CONFIRMED (one listed exception is an artefact)
- 19/19 Start steps carry exactly 2 images; positions and widths reproduce.
- LSM Part 1 is not placed differently on screen. Its title PNG is taller (aspect 0.56 vs 0.19-0.29) with empty
  space above the text. Measured text extents: LSM Part 1 y 69-84%, others y 62-87%. Its visible text is 37% wide.
- Logo panel `#00b0ef` 19/19; title text `#585858` 18/19, `#5b5b5b` in PMG Decon. In PMG Decon the model overlaps the
  title text.

### STYLE-13 FOV 45: CONFIRMED
- 1,036 of 1,037 viewer steps at FOV 45, perspective in all; the one FOV 50 step is LSM Part 1 [011].

## 2. STYLE-3 in detail

What the data holds that the analyst did not use: step properties contain `light_directional: {position}`.
It is set 59 times across the 20 guides: once in each PMG guide and in LSM Part 1/2/1+2, LAC Part 1, LAC
Electronics; 2-13 times in the others (LSM Full 13). Direction = unit(position), i.e. the light aims at the world
origin (aiming at the orbit target fails LSM Part 4 [019] and LSM Full [000]).

Test: face lit when N.unit(position) > 0.4. Faces classified by pixel counts of the lit vs shade wood tone inside
boxes (`tones.py`).

| Frame | Up | Stored light | Predicted | Found |
|---|---|---|---|---|
| PMG Part 3 [002] | +y | (-0.69, 0.61, 0.38) | -X lit, +Z shade | H1 lit, H2 shade |
| PMG Part 3 [004] | +y | same | -X lit, -Z shade | H1 lit, H3 shade |
| PMG Part 3 [006] | +y | same | +X shade, +Z shade | 94% of wood pixels shade |
| LSM Part 3 [001] | +y | (-0.20, 0.70, 0.69) | -X shade, +Z lit | D4 shade, D2 lit |
| LSM Part 3 [008] | +x | (0.46, 0.65, 0.61) | -Y shade, -Z shade | both shade |
| LSM Full [000] | +y | (0.46, 0.65, 0.61) | +X, +Y, +Z lit | all lit |
| LSM Part 4 [019] | +y | (0.63, 0.78, -0.06) | +X lit, -Z shade | D5 lit, D3 shade |
| LAC Part 4 [034] | +y | (0.71, 0.70, -0.08) | +X lit, +Z shade | F1 lit, F5 shade |
| LAC Decon [031] | -x | (-0.29, 0.64, -0.71) | -X shade, +Y lit, -Z lit | top edge `#c9a77a` shade, face lit |

All 24 faces in these 9 frames match. These are frames where the up-axis has not changed since the light was last
stored. The analyst's unexplained pair (F1 lit, F5 shaded in LAC Part 4 [034]) is exactly what the stored light gives.

Consequences for the claim:
- Counter-example to "faces pointing along the scene up-axis get the lit tone": LAC Decon [031] Step 12, up-axis -x.
  The up-facing edge of F1 is the shaded tone `#c9a77a`; the big +Y face is lit `#ffd49c`. The stored light gives
  the same for [031]-[040].
- "In PMG every vertical face sampled is shaded" is wrong. PMG's light is fixed at 38 degrees elevation, not along
  the up-axis, so the wall family facing it is lit: H1 outer face in Part 3 [001] [002] [004] and [008]; rear wall in
  [030]. It is true of [023].
- "Lighting flips with the up-axis" is supported for -y steps where no new light is stored: PMG Part 3 [008] and LSM
  Part 4 [017] show the underside lit although the stored light has +Y. After such a round trip the horizontal part of
  the light is not restored: PMG Part 3 [023] and [030] behave as (+0.69, 0.61, -0.38); LSM Part 3 [012] (back to +y
  from +x) matches the stored light rotated by the same quarter turn. These are the only misses of the as-stored rule.
- Up-axis is not only an underside device. 148 of 1,037 viewer steps are not +y: -x 68 (all LAC), -y 53, +x 21, -z 6
  (LSM plan views looking straight down).
- Over all +y steps (889) the stored light has N_up.L between 0.46 and 0.88 (0.46 on one step, LSM Full [060]), so top
  faces are lit there by data.
- Stored light vs camera direction: median angle LAC 37, LSM 54, PMG 31 degrees. It is a snapshot roughly from the
  viewer's side, not a headlight and not a fixed rig, in LSM/LAC.

Not settled from disk: what the live viewer does between stored positions in LSM/LAC (flag unset), and the exact
rotation applied on an up-axis change. The saved renders are authoring-time captures.

## 3. Numeric defaults

Confirmed as stated: background; edge colour and width; toon tones 1.0 / 0.7; tone formula; ambient 1.75 x7 / 1.875 x8
/ 2.0 x5; directional 1.0 x15 / 1.15 x5; lit/shade multipliers; camera FOV; wood, engraving, soft black, metal, Nano
PCB, shield and header hexes, RTC, LCD, breadboard, resistor bands, lead colours, Dupont housing and pins, PMG caps;
motion and callout colours; label text, font split 124/88, underline and leader thickness, box size; inset frame;
quantity label; logo; UI default font (14 set, 6 LSM unset; base 20 in 20/20).

Corrected:
- Crease angle: 40 scene default; 69 on PMG jumper wires (95% of wire solid-steps).
- Toon switch: 0.38 < N.L threshold <= 0.46 (measured), consistent with 0.4.
- Ghost opacity 0.5: panel bodies for 1 viewer step; decals linger 1 more.
- Light direction: unit(`light_directional.position`); PMG (-0.69, 0.61, 0.38) fixed; LSM 21 and LAC 5 distinct
  stored directions, median elevation 41-44 degrees.
- Wood: 18 of 18 guides with wood.
- Lead line width: 4-5 px, mode 5, on both 2,559 px and 3,840 px renders (does not scale with render width).
- Anchor: 498 Life Saver Circle 30 x 30 plus 5 Basic Circle (black, not drawn).
- Eye icon: 143 at 7.81% and 62 at 8.2% of 225.
- Title block: image box x 1.6-3.8%, y 61-65%, width 42-48% in 18/19; visible text y 62-87% in 19/19.
- Title text `#585858` 18/19, `#5b5b5b` PMG Decon.
- TM1637 PCB `#224bbe`: 4 PMG guides.
- Decal offset: 0.127 mm (LSM, PMG panels), 0.249 mm (LAC panels), under 0.06 mm (breadboard).
- Solid-step base: 579,220 (nearest-flag rule) or 501,702 (digest rule).

## 4. Missed by the analyst

1. Per-step stored light position (section 2).
2. PMG per-part edge crease angle 69 on jumper wires.
3. Part `scale` used on info cards (capacitor x2, USB plugs x0.95), reset on the next step.
4. Up-axis used on 148 viewer steps with four different non-default axes.
5. Digest visibility rule disagrees with renders (CAD-hidden parents with explicitly shown children).
6. Part red `#ff0e00` collides visually with annotation red.
7. Ghost step composition (bodies 1 step, decals 2).
8. LSM Part 1 title "exception" is PNG padding.
9. Label containers store `shadow_enabled: true` that does not render; quantity labels store a black Basic Circle
   anchor that does not render.
10. LSM 8x8 matrix pose copies carry `scale` 0.95 and 1.03 from step 0 in the late LSM project (646 solids).
