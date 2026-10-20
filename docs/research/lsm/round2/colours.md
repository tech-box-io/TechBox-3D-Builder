# LSM round 2: why D2 looks dark, and the black marks on the capacitor's top (19 Oct 2026)

Read-only investigation of two look problems in Lee's notes (`docs/research/lsm/lee_notes_2026-10-19.md`): "D2 in the parts list
is dark ... like the camera lighting is not shining on it correctly", "the lighting on D2 is consistently bad" (draft Step 18,
the button through D2), and "the top of the capacitor has some weird black texture bleed on the top grey surface" (draft Step 6).
Nothing in the repository was changed; every number below was measured from `LSM Build Instructions/lsm.glb`, `lsm-wood.glb`,
`steps.json`, `parts/*.png` and Cadasio's payload, with `tools/build_model.py`'s own functions run in memory (scripts in
`/private/tmp/claude-501/colours/`). Coordinates are assembly mm, Y up, unless a part's own frame is named.

## 1. D2: the darkness is the brown colour, made darker by the fixed light. The normals are fine.

### No lighting fault in the geometry

| part (mesh) | placement det | own +z goes to | faces whose stored normal disagrees with the winding | signed volume |
|---|---|---|---|---|
| D2 (`LSM_Side3_r2`, plate only) | +1.0000 | +z (outer face, own z 3.0, at z 1254.93) | 0 of 2916 | +11806 mm3 (outward) |
| D3 (`LSM_Side1_r8`) | +1.0000 | -z | 0 of 2600 | +12946 mm3 |
| D4 (`LSM_Side2_r2`) | +1.0000 | -x | 0 of 1172 | +15490 mm3 |
| D5 (`LSM_Side4_r2`) | +1.0000 | -x | 0 of 1296 | +15683 mm3 |
| D1, D10 | +1.0000 | +y | 0 | positive |

D2 is not mirrored (det +1, so three.js does not flip its front faces), its stored normals agree with its winding everywhere (mean
dot 1.0000), and its winding faces outward (positive signed volume): the own-z = 3.0 face has normal (0, 0, +1) both stored and
by winding, the own-z = 0 face (0, 0, -1). Same for every wall. `build_model.py` keeps the CAD's normals through `roughen`
(build_model.py:377-437, "they keep their normals") and `weld_attributes` (build_model.py:445).

### What does make it dark

1. **The colour.** materials.json:40 gives `LSM_Side3_r2` a region that paints every face whose middle has own z in [2.95, 3.05]
   (the outer face) `wood_dark` #855e42; the other walls are `wood` #deb887 on both faces (materials.json:41).
2. **The player's light is fixed in the scene, not on the camera.** `player/js/core.js:12` `LIGHT = (-0.45, 0.8, -0.4)`
   normalised = (-0.449, 0.799, -0.400); the toon shader (core.js:18-33) gives a face the "lit" tone (colour x 1.38, linear) if
   its world normal looks towards that direction and the "shade" tone (x 0.9) otherwise. Nothing in `player.js` moves the light
   (only `parts.js:66` does, for the part pictures). D2's outer face looks along +z, so dot = -0.400: **in every step, from every
   camera, D2's brown face is drawn in the shade tone.** (So are the +x faces, e.g. D5's outer face, and the -y faces.)

The tones, computed with the shader's own maths and checked against the rendered PNGs (pixel values read from the files):

| face | lit tone (sRGB) | shade tone (sRGB) | where it is seen |
|---|---|---|---|
| D2 outer, #855e42 | (154, 110, 77) | **(127, 89, 63)** | lit: `parts/D2.png` (measured (154, 110, 77)); shade: every step that shows D2's outer face |
| wood, #deb887 | (255, 212, 156) | (212, 175, 129) | `parts/D3.png`, `D4.png` measured (255, 212, 156) |
| published Cadasio guide | | | D2's face in Lee's picture 6 measured (160, 113, 79); its lit wood (255, 221, 162) |

The steps that show D2's outer face (camera `dir` with +z): Start, Step 18 / 18c (the button through D2: dir (0.579, 0.574,
0.579)), Steps 32 - 34c (dir (-0.579, 0.574, 0.579)) and the Completed View. In all of them the face is (127, 89, 63), about half
the brightness of the shaded wood beside it and darker than the published guide's (160, 113, 79). Steps 19 - 31 and 35 - 39 look
at D2's inner face (dir with -z), plain wood in the lit tone, which is why Lee notices it at Step 18 and in the parts list. In the
parts picture the light is put over the camera's shoulder (parts.js:66), so the brown face is lit there: its darkness in
`parts/D2.png` is the colour alone.

So: **the darkness is the brown colour (both places), made worse in the steps by the fixed light, which always puts that face in
shade. There are no inverted normals.**

### Where the brown comes from

Cadasio's D2 (`LSM_Side3_r2-1`, and its floating copy `-2`) has five solids (read with `tools/cadasio/atlas.py` from the raw
payload): the plate `Cut-Extrude1` (own box x -6.206 .. 89.106, y 0 .. 50.8, z 0 .. 3.0, #deb887), a face copy
`Surface-Offset2[1]` lying 0.127 mm proud of the outer face (z 3.127, the whole face, #855e42), the two black sheets in the "D2"
engraving pockets (z 2.873) and a brown copy over the island of the "D" (`Surface-Offset2[2]`, z 3.127). D3 and D4 have only the
plate and the two black engraving sheets. So the brown is a sheet someone added in SolidWorks over D2's outer face only (0.127 mm
= 0.005 in, a sticker or veneer thickness), and the published guide shows it. `assemble.py:225` keeps the plate only
(`main_solid=True`), and materials.json:40 repaints the outer face to imitate the sheet.

`lsm-wood.glb` (Lee's LSM_WoodSteps.STEP) has two D2 meshes:

| mesh (node) | plate box (own mm) | thickness | solids |
|---|---|---|---|
| `LSM_Side3_r2` (NAUO11), used for D2 | x -6.206 .. 89.106 (95.31 wide), y 0 .. 50.8 | 3.0 | plate 2916 tris, **brown face sheet at z 3.127 (700 tris)**, two engraving sheets at z 2.873, the "D" island sheet at z 3.127 |
| `LSM_Side3_r2(1)` (NAUO10), unused | x -5.924 .. 88.474 (94.40 wide), y 0 .. 50.8 | 3.175 | plate 2708 tris, two engraving sheets at z 3.048; **no brown sheet** |

`LSM_Side3_r2(1)` has the button hole too (vertices from radius 4.42 mm round (41.28, 28.93)), but D3's outline extents and
thickness (3.175, like `LSM_Side1_r8`): its tabs are 0.28 and 0.63 mm shorter than D2's. Its normals are as sound as the other's
(0 reversed faces, det +1). Swapping to it would change D2's fit in D4's and D5's slots and D1, and the collision tests; it is
not needed to fix the colour. It does show that a D2 without the brown sheet exists in Lee's CAD.

### Fix

Lee's two remarks read the brown as a fault ("for some reason", "like the camera lighting is not shining on it correctly"):
he did not take it for a different material. README.txt question 5 asked exactly this and the notes do not answer it in words,
but the remarks point to **plain wood like the other walls**. Recommended (with a one-line confirmation to Lee):

- materials.json:40: delete the `^LSM_Side3_r2$` rule. The `^LSM_` rule (materials.json:41) then colours D2 as D1, D3 - D11:
  #deb887 on both faces, roughened, engraving inked. In Step 18 (which shows only D2, the button and its two pins, so the
  brown panel fills the view) the outer face becomes (212, 175, 129), the shade tone of plain wood, as D5's outer face is in the
  Completed View; in the parts picture (255, 212, 156), as D3 and D4.
- materials.json:58: take the D2 line out of `_notes.unconfirmed`; put "D2 plain wood on both faces, as the other walls (Lee,
  19 Oct 2026)" under `_notes.decided`.
- Wording that names the brown side: guide.py:391 ("through the round hole in D2 from its brown side") and the comment at
  guide.py:351; README.txt ("D2's outer face is brown", "the button through D2 from the brown side", question 5). The engraved
  "D2" is on the outer face (its pockets go in from own z 3.0 to 2.873, the face the button's flange sits on), so "from the side
  with the D2 code on it" says the same thing.
- Then `tools/build_model.py "LSM Build Instructions"` (a colour change does not change the set of parts, so `guide.py` will not
  rebuild the model by itself), re-render `parts/D2.png` (parts.html), and the card (`_dev.card()`): the Completed View shows D2's
  outer face.

If Lee wants the brown kept (the real panel is a different material), the darkness in the steps can only be eased, not removed,
without changing the player's light for every kit: a lighter brown whose shade tone matches the published (160, 113, 79) is
#a87753 (linear (160, 113, 79) / 0.9), which would be (194, 138, 97) in the parts picture. Changing `LIGHT` or making it
follow the camera would alter every face of every kit (MRA, RCC, LAC, PMG) and is not recommended for this.

## 2. The capacitor's top: black body faces and their edge lines left under the silver skin

### The mesh

`Capacitor body` in lsm.glb (from lsm-electronics.glb NAUO8), own frame, 4 solids (all with outward winding and stored normals
that agree with it: 0 reversed faces):

| solid | Cadasio name | colour (atlas) | own box | faces |
|---|---|---|---|---|
| body | `Split Line2` | #1e1616 | x -2.498 .. 2.498, y 0 .. 10.0, z -2.5 .. 2.5; ends rounded (flat disk to r 2.2 - 2.285, then a fillet to the r 2.5 side; side vertex rings at y 0.257, 0.3, 9.7, 9.743) | 3276 |
| skin | `Surface-Offset1[1]` | #a6a9aa | y -0.05 .. 0.3, r to 2.55: an open cap (disk, fillet, band down to y 0.3) | 1586 |
| skin | `Surface-Offset1[2]` | #a6a9aa | y 9.7 .. 10.05, the same at the other end | 1586 |
| skin | `Surface-Offset2` (stripe) | #a6a9aa | x 2.04 .. 2.548, y 0.3 .. 9.7, z -1.53 .. 0.51: 7 facets at r 2.55 between -36.87 and +11.54 degrees round own y | 14 |

Placement (CAP node x the body's node): own +x -> (0, 0, 1), own +y -> (-0.1045, -0.9945, 0), own +z -> (0.9945, -0.1045, 0),
det +1. **Own y 0 is the top in the assembly** (own (0, 0, 0) -> (654.60, 883.59, 1171.72); own (0, 10, 0) -> (653.55, 873.64,
1171.72)): the cap seen from above is `Surface-Offset1[1]` (own y -0.05 .. 0.3), not `[2]` (own y 9.7 .. 10.05), which is at the
legs. The can leans 6 degrees towards +x, as Cadasio has it.

### What the build makes of it

`build_model.py` matches the atlas (100 %), marks the three silver solids as skins (`make_atlas.py`: every `Surface-Offset`), and
`faces_under_skin` (build_model.py:615-645, called at :1051 with the fixed `reach_mm=0.05`) gives the skin's colour only to body
faces whose three corners and middle are all within 0.05 mm of the skin. The skins are 0.05 mm offsets, but over the rounded ends
the offset is tessellated differently from the body, so the body's faces there are 0.0423 - 0.0523 mm from the skin: over a third
of them fail the test, by a few microns. Rerun in memory with the build's own functions (it reproduces model.report.json exactly: 1883
triangles, 1643 edge segments):

- 2018 body faces recoloured silver, but **585 body faces at the top end stay black** under the silver cap (own y 0.002 - 0.286,
  r 2.224 - 2.497: the fillet and the band), and 583 at the leg end; of the flat top disk (own y 0) 244 of 303 faces are silver
  and 59 black. 907 black faces lie under a skin's interior (more than 0.1 mm from its edge).
- Each colour is a primitive of its own and `feature_edges` draws every open border of a primitive (build_model.py:94,
  `count == 1`), so the ragged border between the black and the recoloured faces becomes black edge lines: **1555 of the 1643
  edge segments lie 0.02 - 0.08 mm under a skin, 1188 of them under a skin's interior** (769 under the top cap alone). A clean can
  needs about 300.

### Why it shows through

The player draws every face with `polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1` (core.js:30), so that edge
lines lying on a face win the depth test; the lines themselves (`LineBasicMaterial`, core.js:80) get no offset. A line lying less
than about one pixel's depth slope behind a face is therefore drawn over it. At Step 6's camera (fov 45, radius 74.9, so 211 mm
from the target and about 209 mm from the capacitor) one device pixel of a ~1350 px high canvas is about 0.13 mm, and the top is
seen 57 degrees off its normal: the skin is pushed back about 0.13 x tan 57 = 0.2 mm, four times the 0.05 mm gap. **The black
"texture" is the lines of that patchwork drawn through the silver**, plus, on the fillet, black facets whose slope (and so offset)
differs from the skin facet over them. It is in `parts/Capacitor.png` too: dark specks and dashes along the top's rim. (Depth
precision alone would not do it on a 24-bit depth buffer: `fitDepth`, core.js:277-287, keeps near at 1 mm or more, which resolves
about 0.003 mm at 209 mm; on a 16-bit buffer the two surfaces would fight outright.)

### The stripe and the legs

The stripe skin in assembly mm: x 652.06 .. 655.07, y 873.89 .. 883.45, z 1173.76 .. 1174.27; the normal at its middle (own angle
-12.66 degrees) is (-0.218, 0.023, 0.976): it faces +z. The legs (own x -1.25 and +1.25, to assembly z 1171.72 -/+ 1.25) end at
(652.62, 863.64, 1170.47) = **j2** and (652.62, 863.64, 1172.97) = **j3**. **The stripe is over the j3 leg**, as the caption says
(j3 is in column 3, the Nano's GND at g3). The build already colours it: all 14 body faces under it are recoloured, no line is
left under it. It is not seen in Step 6 / 6c because their camera, dir (-0.579, 0.574, -0.579), looks at the other side of the can
(dot with the stripe normal -0.43). The diagonal (-0.579, 0.574, +0.579) faces it best (dot +0.705); (0.579, 0.574, 0.579) gives
+0.452. That is the camera Lee asks for ("further to the left ... so that we can see the grey strip and j3").

### The rule that makes it read correctly

Replace materials.json:46 with:

    {"match": "^Capacitor body$", "color": "black_plastic", "simplify_mm": 0,
     "regions": [{"box": [[-2.6, -0.1, -2.6], [2.6, 0.31, 2.6]], "color": "metal_can"},
                 {"box": [[-2.6, 9.69, -2.6], [2.6, 10.1, 2.6]], "color": "metal_can"},
                 {"box": [[2.0, 0.3, -1.54], [2.6, 9.7, 0.52]], "color": "metal_can"}],
     "_about": "the electrolytic capacitor, as published: black can, silver caps at both ends (own y 0 is the top in the assembly) and the silver stripe over the negative leg, in j3. Painted by boxes in the mesh's own frame, not from the atlas: Cadasio's silver caps are copies 0.04 - 0.05 mm over the rounded ends, and faces_under_skin left a patchwork of black faces and edge lines under them that showed through the silver"}

- A rule that names a colour does not take the atlas (build_model.py:473), so no skin matching is done. `regions`
  (build_model.py:1056-1059) then colour every face, body and skins alike, whose middle lies in a box: both caps (own y up to 0.31
  and from 9.69: the body's own rings at y 0.3 and 9.7, where the skins' edges are) and the stripe (the box catches exactly the 14
  body facets and the 14 skin facets between -36.87 and +11.54 degrees; the body is split there). `black_plastic` (#1e1616) and
  `metal_can` (#a6a9aa) are the atlas's own colours, under palette names; all three regions must use the same name, because the
  build makes one primitive per colour name (build_model.py:1082) and two names for one grey would draw a line between them.
- Simulated with the build's functions: no black face left in either cap or under the stripe; edge segments 1643 -> 304; the only
  lines left under a skin are the body's colour rings at own y 0.3 and 9.7 (r 2.5) and the stripe's two edges, each 0.05 mm inside
  the skin's own edge line, so they draw the cap's and the stripe's outlines. Triangles 1883 -> 6462 with `simplify_mm: 0` (small
  beside the model's 133,402). With `simplify_mm` 0.02 it is 1203 triangles and 187 segments, but 12 short creases are left on
  the rounded ends under the skin (8 at 0.01, 6 at 0.005): hence 0.
- The same output keeps the atlas: leave out `"color"` and write the regions' colour as the atlas's literal `"#a6a9aa"` (so it
  groups with the skins).
- Then `tools/build_model.py "LSM Build Instructions"`, re-render `parts/Capacitor.png`, and check Step 6 / 6c in the player (the
  top, and the stripe once the camera turns to it).

Not recommended for this: raising `reach_mm` in `faces_under_skin` (0.06 would catch the 0.0523 mm faces) is a tools change that
re-colours the skins of every kit's model (MRA, RCC, LAC, PMG) and would need all of them checked.

## 3. Other skins over bodies

The same check (body faces under a skin's interior left in another colour; edge segments 0.02 - 0.08 mm under a skin, and how many
of those lie more than 0.1 mm inside its edge), run in memory on each atlas mesh with skins. Each rerun reproduced the edge count
in model.report.json.

| mesh | skins | body faces under a skin interior, wrong colour | edge segments under a skin / under its interior | verdict |
|---|---|---|---|---|
| Capacitor body | 3 | 907 of 2636 | 1555 / 1188 | broken (section 2) |
| Resistor body 12k | 5 bands | 0 (every face inside each band recoloured: 354, 175, 174, 188, 246) | 454 / 0 | fine: the 454 are the bands' own edges |
| Resistor body 330 | 5 bands | 0 | 458 / 0 | fine |
| Breadboard | 130 (print: black, blue #0074d9, red #ff0e00) | 0 of 8 | 1526 / 0 | fine (most print strokes are under 0.2 mm wide; `edge_min_size_mm` 1.0 drops their islands' lines) |
| Push button | 6 | 0 | 131 / 16 | negligible: 16 short segments under the two light grey (#cad1ee) skins where its leads leave it (own x +-3.4 .. 4.0, z -21.2 .. -19.8), behind D2 once built (seen from inside in Steps 19 - 22) |
| USB Right Angle (Mini-B plug) | 2, nested (#cccccc over the body, #cad1ee over part of that, own x -15.0 .. -8.0) | 89 (the two near-identical greys swapped) | 175 / 50 (own x -15.0 .. -11.5) | the same fault, small: possibly a few dark ticks on the plug's grip; look at Step 22 / 22c before changing anything |

The resistors' bands and the breadboard's printing are flat or straight-sided copies whose tessellation matches the body's, so
every covered face is within 0.05 mm and is recoloured. The capacitor fails because its skins are offsets of rounded ends. Not
checked: the 8x8 LED (186 skins; to be remodelled after Lee's Step 13 note), and the Nano (the MRA's model and rule).

## Summary

1. D2: the brown (#855e42, materials.json:40, imitating Cadasio's 0.127 mm brown sheet over D2's outer face) is the darkness; the
   player's light, fixed at (-0.45, 0.8, -0.4) in the scene, puts that +z face in the shade tone in every step that shows it, (127, 89, 63)
   against the published (160, 113, 79). D2's placement is not mirrored (det +1) and its normals are outward and agree with its
   winding: no lighting fault. Lee's wording reads the brown as a fault, so: delete materials.json:40 (plain wood, as the other
   walls), record the decision, reword "from its brown side" (guide.py:391, :351, README), rebuild the model, D2's picture and the
   card.
2. Capacitor: the atlas's silver caps are 0.05 mm copies over rounded ends; `faces_under_skin` (reach 0.05) leaves 585 black body
   faces under the top cap, and their ragged borders become 769 black edge segments under it, which the faces' polygon offset lets
   through the silver. Fix: the materials.json rule above (black_plastic, three metal_can regions, simplify 0). The stripe is over
   the j3 leg and faces +z; Step 6's camera looks at the other side.
3. Resistor bands and breadboard printing are fine; the Mini-B plug may have a few such lines (look at Step 22).
