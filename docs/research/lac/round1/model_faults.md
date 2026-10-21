# LAC, Lee's first round (20 Oct 2026): three faults in the model

(a) the knob (NAUO13): "a silver ring at the end of it, and some bleed through of the underlying black texture";
(b) the resistors (NAUO6, NAUO7): "the colour bands are blending with the underlying surface";
(c) "the Potentiometer is backwards in the Parts List" (parts/Potentiometer.png).

Measured from `LAC Build Instructions/lac-guide.glb` with build_model.py's own functions (one Python process, scripts in the
session scratchpad, nothing in the project changed but this file). Not rendered: no server was run. The look still has to be checked in the
browser after the rebuild (end of this file).

| Fault | Cause | Fix |
|---|---|---|
| (a) knob | Two silver CAD "Surface-Offset" face copies lie 0.020 mm outside the black body. The atlas does not mark them `skin`, so the black faces underneath stay black and show through. | Add `"skin": true` to the two `LAC Knob-Surface-Offset1[...]` atlas solids. Or, if Lee wants no silver ring, use a black rule (option B). |
| (b) resistors | The same cause. The five band copies lie 0.0199 mm (median) outside the blue body and are not marked `skin`. | Add `"skin": true` to the five `LAC Resistor 1-Surface-Offset1[...]` atlas solids. The LSM already does this for the same resistor model. |
| (c) pot picture | parts.js gives every non-flat part the house view from -X. The knob points +X. | Add `'Potentiometer': {'dir': [0.5417, 0.6428, -0.5417]}` to `PART_VIEWS` in guide.py (optionally also `g.part_picture('Potentiometer', poses=DELIVERED)`). |

---

## Cause shared by (a) and (b): coloured face copies not marked as skins

**The geometry.** In TechBox's CAD, a band or ring is a SolidWorks *Surface-Offset*: an open copy of some of the body's faces,
pushed out by 0.02 mm and given its own colour. In `lac-guide.glb`, after welding and splitting into solids (build_model.py
`weld_positions` / `split_components`):

- **`LAC Resistor 1`** (mesh 4, one per resistor; NAUO6/NAUO7 > NAUO231). Six solids:
  - solid 0, the body: closed, 8,678 faces, blue `#0074d9`.
  - solids 1-5, the bands: open, 200-300 faces each, with 92-100 open edges each.
  - Gap from each band to the body, measured face by face, by solid: min 0.009-0.018 mm, median 0.0199-0.0200 mm, max 0.024-0.027 mm.
  - The bands face the same way as the body (100 % of faces).
- **`LAC Knob`** (mesh 17, NAUO13), in its own frame: axis through (45, 50), its outer end at z = 17, its open end at z = 0.
  Three solids:
  - Solid 0, the body: closed, 3,814 faces, black `#1e1616`.
  - Solid 1, `Surface-Offset1[2]`: open, 358 faces. It holds:
    - the 45° chamfer round the outer end, r 6.514-7.514 mm, z 16.014-17.014. Lee's silver ring, 60.9 mm².
    - the pointer groove cut across the end face: floor at z 16.02, x 44.52-45.48, y 42.50-45.48. On the knob as built it points down (-Y). Floor 2.75 mm², walls 5.40 mm².
  - Solid 2, `Surface-Offset1[1]`: open, 268 faces. A flat annulus at z 2.98, r 2.5-6.5, 88.8 mm². It is the floor inside the open end, round the shaft hole, facing the potentiometer.
  - Both copies are 0.0200 mm from the body.

**What the published guide shows.** TechBox's Cadasio project colours these copies on purpose:

- The resistor bands, starting from the -x end: brown, red, black, red, brown (`colour-atlas-lac.json:17-120`). That is 120 x 100 = 12 kΩ, ±1 %, which agrees with Lee's "12 kOhm Resistor".
- The knob: body black, both copies silver `#a6a9aa` (`colour-atlas-lac.json:3917-3969`; digest `docs/research/lac/cadasio/19075-lac_full_build.md:35`).
- Read per instance from the raw project: Surface-Offset1[2] is silver in all four knob instances. Surface-Offset1[1] is silver in three; in `LAC Knob-4` it is left at its CAD colour `#e4e4e4`.
- The published Step 22 and Step 28 pictures show the silver chamfer ring (`docs/research/lac/cadasio/thumbs/19075-lac_full_build/046.jpg`, `061.jpg`).

So the colours are right. The fault is that the black (or blue) body under each copy is still drawn in its own colour, 0.02 mm
behind it.

**Why the body shows through.**

- The colours are applied to whole solids. Then the triangles of each colour are simplified separately (`tools/build_model.py:1101`, `:1115`), to 0.02 mm for the resistor (`materials.json:118-123`) and 0.03 mm for the knob (`materials.json:124-129`).
- Each simplification tolerance is as large as the 0.02 mm gap, or larger. The simplified body therefore crosses its copy in places.
- Everywhere else the two surfaces sit 0.02 mm apart. Every part material has the same `polygonOffset` (`player/js/core.js:30`), so it does not separate them. Which surface wins then depends on the depth slope at grazing angles: it flickers from view to view.

I simulated the build's per-colour simplification and measured it:

| | Body area under a copy (same facing, within 0.1 mm) | Of which at or through the copy (gap < 0.002 mm) |
|---|---|---|
| resistor, as built now | 35.1 mm² of blue under the bands | 0.48 mm², up to 0.0076 mm outside |
| resistor, with `skin` | 0.28 mm² (band edges) | 0 |
| knob, as built now | 154.7 mm² of black under the silver | 0.29 mm², up to 0.017 mm outside |
| knob, with `skin` | 0 | 0 |

The fault is plain in the current `parts/Resistor.png`: the black and red bands are broken with blue.

**The mechanism that already exists.**

- An atlas solid with `"skin": true` is a skin: `colour_from_atlas` reads the flag (`tools/build_model.py:502`, `:522`) and `colour_components` returns it (`:586-590`).
- `faces_under_skin` (`:615-646`) then gives the body faces under a skin the skin's colour (`:1062-1070`), before simplification. Both layers are then one colour, and whichever is drawn in front, nothing changes.
- The MRA's Nano uses it: `model.report.json:466` "141247 faces under a skin recoloured".
- The LSM uses it for the very same resistor model: `LSM Build Instructions/make_atlas.py:7-8` and `:48` mark every `Surface-Offset` solid as skin, and `LSM Build Instructions/model.report.json:343` reads "1162 faces under a skin recoloured".
- The LAC atlas was written by `docs/research/lac/scripts/lac_atlas.py:44`, which does not set the flag. Its only skins (238) are the Nano's, copied from the MRA. The report shows the result: no "under a skin" note on `LAC Resistor 1` or `LAC Knob` (`model.report.json:114-127`, `:179-190`).

**What the flag changes** (computed with `faces_under_skin` itself):

- Resistor: 1,150 body faces take their band's colour (black 170, brown 602, red 378).
- Knob: 620 body faces become silver (the chamfer, the groove, the annulus inside).
- Nothing else changes colour.

One side effect, as on the LSM: each band edge gets its outline line drawn (an open border of a colour), so the resistor's edge segments go
up from 222 to roughly the LSM's 678. On the LSM, Lee has seen this and it reads as band edges.

---

## (a) The knob

**Recommended default (option A): keep the published look, cure the bleed-through.**

- Mark the knob's two `Surface-Offset` solids as skins (the edit is below, together with the resistor's).
- The knob is then black with a clean silver chamfer ring, a silver pointer groove, and a silver annulus inside its open end, exactly as TechBox's Cadasio project draws it.
- No materials.json change.
- This follows the house rule: colours follow the atlas unless Lee rules otherwise (`materials.json:166`).

**Option B: no silver ring (if Lee meant the ring itself is wrong).** In `materials.json`, put this rule just before the rule at
`materials.json:124-129`:

```json
    {
      "match": "^LAC Knob$",
      "color": "black_plastic",
      "simplify_mm": 0.03,
      "outline": true,
      "_about": "the potentiometer's knob, all black (Lee, 20 Oct 2026: no silver ring). The CAD's two silver face copies (Surface-Offset1[2]: the chamfer round its end and the pointer groove; Surface-Offset1[1]: the ring inside its open end; both 0.02 mm proud of the body) are drawn black like the body. TechBox's Cadasio project has them silver."
    },
```

Then make `materials.json:125` read `"match": "^(LAC Potentiometer|LAC Nut|Washer)$",`, and add to `_notes.decided` (`materials.json:164-168`):
`"2026-10-20 (Lee): the potentiometer's knob is all black (the published project's silver ring and pointer are not on the real knob)."`

- A rule that names a colour overrides the atlas (`tools/build_model.py:471-478`). The copies then lie black over black, so nothing can show through.
- The pointer groove still reads, because its sides are 90° creases and get outline lines.
- `black_plastic` is `#1e1616`, the atlas's black for the knob.

**Option B' (black knob, silver pointer only; untested):** option B's rule plus

```json
      "regions": [{"box": [[44.45, 42.45, 15.95], [45.55, 45.55, 17.05]], "color": "steel", "cut": true}],
```

- The box is in the knob mesh's own frame and holds the groove's floor and walls.
- It also turns silver the 1 mm of chamfer where the groove runs out, so the pointer reaches the edge.
- `steel` is `#a6a9aa`.
- Look at Steps 22, 28 and the Completed View before keeping it.

**Question for Lee:** "Does the real knob have a silver ring round its end, as the published guide draws it? If yes, we keep the ring and just clean it up. If not, we make the knob black."

---

## (b) The resistor bands

The fix is the skin flags (below). The bands then cover the body completely. They are the same five colours as now, and the body
cannot show through. No materials.json change. The rule at `materials.json:118-123` stays as it is.

---

## The edit for (a) option A and (b): `LAC Build Instructions/colour-atlas-lac.json`

It adds `"skin": true` to seven solids:

- the resistor's band solids, named at lines 45, 60, 75, 90 and 105;
- the knob's two copies, named at 3945 and 3960.

Run once from the project root. It is tiny, and it rewrites the file byte for byte except for those seven lines: I checked the round trip
on a copy.

```bash
python3 - <<'EOF'
import json
path = 'LAC Build Instructions/colour-atlas-lac.json'
atlas = json.load(open(path))
KEYS = ['LAC Resistor 1', 'LAC Knob']      # option A; with option B the knob's flags do no harm (its rule then names a colour)
for key in KEYS:
    for solid in atlas[key]['solids']:
        if 'Surface-Offset' in solid['name']:
            solid['skin'] = True
open(path, 'w').write(json.dumps(atlas, indent=1, ensure_ascii=False))
EOF
```

**For the record**, so that a regenerated atlas keeps the flags, make the same change in `docs/research/lac/scripts/lac_atlas.py:44`, as `LSM Build Instructions/make_atlas.py:48` does. Append to the `dict(...)` there:

```python
**({'skin': True} if 'Surface-Offset' in refs[L]['name'] else {})
```

Also add a line to the atlas's `_about` (`colour-atlas-lac.json:2`): "Cadasio's coloured face copies (Surface-Offset: the resistors' bands, the knob's silver) are marked skin, so the face underneath takes their colour (as the LSM's atlas)."

**The same flaw elsewhere in the LAC (Lee has not reported it; recommended with the same edit).** These atlas meshes have
`Surface-Offset` copies that are not marked as skins:

- **Breadboard**: 132 copies of its printing, only **0.005 mm** above the white body, and simplified at 0.02 mm (`materials.json:95-100`). With the flag, 30,605 faces change colour: black 30,565, blue 20, red 20. That is the same count the LSM gets for the same breadboard. The legends are almost certainly speckled now.
- **USB Right Angle**: 2 silver copies 0.030 mm out. 792 faces change.
- **Rocker Switch**: 6 copies 0.030 mm out. 60 faces change (`#181818` 52, white 8).
- **Piezo Buzzer**: its copies are 0.076 mm out. Nothing would change.

To cover these, use `KEYS = ['LAC Resistor 1', 'LAC Knob', 'Breadboard', 'USB Right Angle', 'Rocker Switch']`. Then look at the breadboard's legends, the Mini-B plug and the switch's marks too.

---

## (c) The potentiometer in the Parts List

**Cause.**

- `player/js/parts.js:18-24` (`viewFor`) gives every part that is not a flat panel the guide's three-quarter view, `HOUSE = (-0.5417, 0.6428, -0.5417)` (`parts.js:10`). It does this unless the parts.json entry carries `view.dir` (`parts.js:20`).
- `HOUSE` is the direction from the part to the camera. It looks from -X, from above, from the -Z end.
- The picture shows the potentiometer in its built pose. There the knob points +X: the knob's local +z maps to world (1, 0, 0), and its outer end is at x 741.05, on the axis y 919.53, z 1235.26.
  - The pot body spans x 709.83-719.03.
  - The knob spans x 724.05-741.06.
  - The lugs point -Y.
- The camera therefore sees the brown back of the body, with the knob pointing away: the current `parts/Potentiometer.png`.

**Fix.** In `LAC Build Instructions/guide.py:133` (the same line in HEAD; another session has uncommitted edits elsewhere in the file),
`PART_VIEWS` is passed as `Guide(part_views=)` (`guide.py:134`). stepgen writes it into the parts.json entry as `view`
(`tools/stepgen.py:689`, `:2052`). Make it:

```python
PART_VIEWS = {'LCD Screen': {'dir': [0.8, 0.45, 0.4]},             # (the parts list pictures the LCD from the front, its screen showing)
              'Potentiometer': {'dir': [0.5417, 0.6428, -0.5417]}}  # (the house view from the front: the knob's end towards the viewer)
```

- This is the house three-quarter view, mirrored front to back: the same 40° from above as every other electronics picture.
- On screen, the knob (+X) comes towards the viewer at the lower left. The brown body sits behind it at the upper right, and the lugs (-Y) point down. That is how the published Step 22 picture shows the part (`docs/research/lac/cadasio/thumbs/19075-lac_full_build/046.jpg`).
- The knob's end face, with its ring and pointer, is seen 57° off its axis.
- For a more face-on end, `[0.8, 0.45, -0.4]` matches the LCD's elevation instead: 36° off the axis, with the body still showing beside the knob.

**Optional: show it as it comes.** The picture draws the knob, nut and washer in their built places. The washer and nut then sit
where F1 goes, 4.8 mm off the body.

- Step 22 shows the potentiometer as delivered: `DELIVERED`, `guide.py:404` (HEAD `:403`), applied by `g.carry(..., by=POT, pose=DELIVERED[part])` at `guide.py:409-410`.
- A carry pose is relative to the rider's own seat with the carrier in place (`tools/stepgen.py:721-727`), so the same offsets are right for the picture, where the pot is at its seat.
- To match Step 22, add after `guide.py:404`:

```python
g.part_picture('Potentiometer', poses=DELIVERED)                    # (the parts list pictures it as it comes: the knob out 4.6 mm, nut and washer against the body)
```

(`part_picture`, `tools/stepgen.py:742-758`, writes `poses` into the entry and parts.js applies them, `parts.js:49`, `:62`.)

---

## Then: rebuild and check, one heavy job at a time

When this was written, swap was at 7.1 of 8 GB and the disk had 18 GB free. `build_model.py` peaks near 2 GB.

1. `.venv.nosync/bin/python tools/build_model.py "LAC Build Instructions"`.
   - `model.report.json` should then note "atlas match 100%; 1150 faces under a skin recoloured" on `LAC Resistor 1`, and "...; 620 faces under a skin recoloured" on `LAC Knob`.
   - With option B, the knob's note is empty and its colours read only `black_plastic`.
   - With the wider KEYS, the Breadboard's note reads "...; 30605 faces under a skin recoloured".
2. `.venv.nosync/bin/python "LAC Build Instructions/guide.py"`.
   - This is needed even though the parts did not change: it writes the new model stamp into steps.json (`tools/stepgen.py:2111`) and the `view` / `poses` into parts.json.
   - Then diff every view's camera against a copy of steps.json saved beforehand: none should change.
3. Serve the kit (port 8793). Open `parts.html` to re-render `parts/Resistor.png` and `parts/Potentiometer.png`; all the pictures need re-rendering anyway, because the model changed.
4. In `player.html`, look at:
   - Steps 4-6 (the resistors, close up);
   - Steps 22-28 and 52-53 (the knob: its end, and its open end while it is off the shaft);
   - the Completed View;
   - the Parts List pages.
   Then run `_runthrough()`.
5. Commit the atlas (and materials.json / guide.py) with the regenerated `model.glb`, `model.report.json`, `steps.json`, `parts.json` and `parts/`.
