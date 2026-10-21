# LAC round 2, note 1: the breadboard's joining tabs as on the LSM's (21 Oct 2026)

Lee: "make the same tab placement adjustments on the breadboard as was done on the LSM's breadboard ... the tabs should match the new
post-revision LSM breadboard."

Read-only study: no project file was changed, nothing regenerated. Everything below was measured with the project's
`.venv.nosync/bin/python` and `tools/glbio.py` (one mesh at a time, under 400 MB peak); scratch scripts and a trial cut of the part are
in the session scratchpad only.

## Answer in short

- **It is the same CAD part.** The LAC's breadboard (NAUO1 in `lac-guide.glb`, mesh `Breadboard`) and the LSM's original
  (`lsm-electronics.glb` `Breadboard`, the mesh assemble.py starts from) have the same 66,284 vertices, **identical to 0.0 mm**, and the
  same own-frame box `[-69.285, -5.25, -42.17] .. [-13.205, 4.27, 40.84]` mm. Only the triangulation differs (6,116 of 56,640 triangles
  split along the other diagonal of the same quads: two STEP conversions of one model; nothing shows).
- **Same rows and columns in the part's own frame.** a1 is at own (-55.98, 4.25, -36.87) in the LAC and (-55.97, 4.27, -36.83) in the
  LSM; j30 at (-27.88, 4.25, 36.79) / (-27.85, 4.27, 36.83) (LAC from `wire-paths.json` holes, LSM from assemble.py `ROW_X`/`COL1_Z`).
  So the LAC's CAD has its tabs on the **j side and the column 1 end**, exactly as the LSM's had, and the LSM's revised mesh (tabs on
  the **a side and the column 30 end**) drops straight into the LAC's frame.
- **Where that is in the LAC.** The LAC turns the board half round (NAUO1's matrix: rotation diag(-1, 1, -1), translation
  (633.2657, 892.8584, 1305.2480) mm). Today the two long-side tabs are on the **back** (j side, -X, towards F2) and the three end tabs
  on the **+Z end** (column 1, the Nano's USB end, towards F5). After the change: two on the **front** (a side, +X, the edge with the
  red and blue rails the guide uses, towards F1) and three on the **buzzer's end** (column 30, -Z). Those are the two sides the house
  view (BENCH_LOOK, from the front at the buzzer's end) looks at, so Lee will now see them in Steps 1 - 2 and on through the build.
- **Least-risk way: copy the LSM's revised breadboard in as an extra part** (one `tools/cut_part.py` command, as the LAC's Nano was
  made), give the body rule the LSM's `atlas_frame` and add a `Breadboard tabs` rule. The holes, `wire-paths.json` and every wire stay
  exactly where they are (checked: all 300 hole tops see the same mesh round them; every body vertex lands on a CAD vertex to 3e-13 mm).
- **F3 has no slots for the tabs, and needs none** (neither does the LSM's D1): the tabs are on the board's sides, their undersides
  1.00 mm above F3's top face (they start above the board's 1 mm adhesive layer). What F3 has round the board is four L-shaped corner
  marks; they and the new tabs do not meet (details below).
- **Nothing else is hit.** At rest in every one of the 116 views, no part comes within 3.06 mm of a new tab (F3 1.00 mm below, by
  design); no moving part's swept box comes within 2 mm of one in any step (the LCD's, Step 51, closest at 8.3 mm); no wire route used
  by any view comes within 3 mm (centre line).

## 1. What was done to the LSM (commit fadb906, 20 Oct 2026)

- `LSM Build Instructions/assemble.py` `move_breadboard_tabs()` (lines ~298 - 381 after the commit): on the breadboard placed in the
  LSM assembly (a pure translation, so assembly axes = the part's axes), finds the j side's face plane (own x -14.535) and the column 1
  end's plane (own z -40.84), takes every face beyond them (+0.2 mm) as tab faces (2 tabs + 3 tabs, 50 triangles), closes the five
  openings in the body with flat fans built from the body's own border points (20 triangles, so no outline is drawn where a tab was),
  and mirrors the tab faces across the board (x -> x0 + x1, z -> z0 + z1, winding flipped) onto the a side (own x -69.285) and the
  column 30 end (own z 40.84). Written back in the part's own frame as two meshes: `Breadboard` (66,219 vertices, 56,610 triangles) and
  `Breadboard tabs` (100 vertices, 50 triangles).
- `LSM Build Instructions/materials.json`: the body rule gained `"atlas_frame": [[-69.285, -5.25, -42.17], [-13.205, 4.27, 40.84]]`
  (the mesh's box no longer equals the atlas's, which made the atlas match fail) and a new rule `^Breadboard tabs$`, `"color":
  "#ffffff"`, `"simplify_mm": 0`.
- `tools/build_model.py`: `colour_from_atlas(..., frame=)` reads `atlas_frame` (already in the tools, nothing to add for the LAC).
- `LSM Build Instructions/guide.py`: Step 1's camera written as `view_dir=` + `frame=` (it would have moved with the new box), Step 2's
  corner lines on the body's own corners, Step 25's lead lines written as `lines_at=` (D4 touches the board's end there).

## 2. The LAC's breadboard compared

| | LAC (lac-guide.glb NAUO1) | LSM (lsm.glb BREADBOARD, revised) |
|---|---|---|
| mesh | `Breadboard`, 66,284 v / 56,640 t | `Breadboard` 66,219 v / 56,610 t + `Breadboard tabs` 100 v / 50 t |
| own box | x -69.285 .. -13.205, z -42.17 .. 40.84 | body x -69.285 .. -14.535, z -40.84 .. 40.84; tabs x -70.617 .. , z .. 42.173 |
| placement | R = diag(-1, 1, -1), t = (633.2657, 892.8584, 1305.2480) | R = I, t = (680.467, 867.654, 1204.737) |
| row a / row j (own x) | -55.98 / -27.88 | -55.97 / -27.85 |
| column 1 / 30 (own z) | -36.87 / 36.79 | -36.83 / 36.83 |
| tabs now | j side + column 1 end | a side + column 30 end |
| atlas | colour-atlas-lac.json `Breadboard`, bbox = the CAD box above, 134 solids | colour-atlas-lsm.json, same bbox |

LAC world positions (seated), mm:

- Board body without tabs: x 647.80 - 702.55, y 887.61 - 897.13, z 1264.41 - 1346.09.
- Tabs today (CAD): back x 646.47 - 647.80 at z 1276.06 - 1279.91 and 1330.59 - 1334.44; +Z end z 1346.09 - 1347.42 at x
  650.55 - 654.40, 673.25 - 677.10, 695.95 - 699.80. All at y 888.61 - 893.11.
- Tabs after: front x 702.55 - 703.88 at z 1276.06 - 1279.91 and 1330.59 - 1334.44; -Z end z 1263.08 - 1264.41 at x 650.55 - 654.40,
  673.25 - 677.10, 695.95 - 699.80. Same y.
- The whole board's box (what `g.model.inst[BREADBOARD].bounds` returns) goes from x 646.47 - 702.55, z 1264.41 - 1347.42 to
  x 647.80 - 703.88, z 1263.08 - 1346.09 (y unchanged): a 1.33 mm shift in x and in z, no change of size.

## 3. F3: slots?

F3 (NAUO2, 3.0 mm plate, top y 887.61) has, round the breadboard, only these cut-outs (through the plate in the CAD):

- **Four L-shaped corner marks**, legs 6.35 mm long and 1.59 mm wide (an outline 54.22 x 82.55 mm). Inner edges: back x 647.80
  (= the body's back face), front x 702.03 (0.52 mm inside the body's front face 702.55), +Z end z 1346.09 (= the body's +Z face),
  -Z end z 1263.54 (0.87 mm beyond the body's -Z face 1264.41). Outlines (x, z of the top edge):
  back/-Z (646.21 - 652.56, 1261.95 - 1268.30), back/+Z (646.21 - 652.56, 1341.33 - 1347.68),
  front/-Z (697.27 - 703.62, 1261.95 - 1264.47), front/+Z (697.27 - 703.62, 1341.33 - 1347.68).
- F1's tab slots in front of the board at x 704.47 - 717.18; F2's along the back at x 641.45 - 644.63; F5's at z 1354.28 - 1357.28.

No slot anywhere receives a breadboard tab, today or after the change, and none is needed: the tabs hang 1.00 mm above F3's top.
The LSM's D1 has the same four corner marks and likewise no tab slots. One difference between the kits, for the record: the corner
marks sit mirror-wise round the two boards. In the board's own frame the LAC's marks hug the j side and the column 1 end and leave
0.87 mm at the column 30 end (0.52 mm overlap on the a side); the LSM's D1 marks hug the a side and the column 30 end and leave 0.87 mm
at the column 1 end. Consequences, all invisible at guide scale and none a clash (the tabs are 1 mm above the plate):

- LAC after the change: the two outer column-30 tabs reach 0.46 mm over the inner edge of the two -Z corner marks (in plan view, at
  x 650.55 - 652.56 and 697.27 - 699.80). Today the column-1 tabs lie over the +Z marks by their full 1.33 mm, so this is less.
- The two front tabs (z 1276 - 1280, 1331 - 1334) are well clear of the front marks (z <= 1264.47 and >= 1341.33), and 0.59 mm short of
  F1's nearest slot in plan (x 704.47).

Moving the board to sit in the marks as the LSM's sits in D1 would move every hole; not proposed.

## 4. The recipe (least risk): the LSM's revised breadboard as the LAC's NAUO1

Why this way: it is the LSM's mesh itself (so the tabs match it exactly, which is what Lee asked), it needs no new code (`cut_part.py
--like` and an `extra_parts` entry replacing a part by its own id are both in use: the LAC's Nano, the MRA's C3 - C5), and the
part keeps its id NAUO1, so guide.py, wire-paths.json and steps.json keep referring to it. The CAD's own NAUO1 stays in lac-guide.glb
(trim_source.py unchanged); both tools drop it in favour of the extra part.

### 4.1 Cut the part (one command, from the project root)

    .venv.nosync/bin/python tools/cut_part.py "LSM Build Instructions/lsm.glb" BREADBOARD "LAC Build Instructions/breadboard-lsm.glb" --like "LAC Build Instructions/lac-guide.glb" NAUO1

Tried into the scratchpad: `breadboard-lsm.glb: BREADBOARD from lsm.glb, 3 nodes, 2 meshes, 2.3 MB, placed like NAUO1 in
lac-guide.glb`. Its nodes: `BREADBOARD_frame` -> `BREADBOARD` (NAUO1's matrix: t 633.2657, 892.8584, 1305.2480 mm, R diag(-1, 1, -1))
-> `BREADBOARD:Breadboard`, `BREADBOARD:Breadboard tabs` (meshes `Breadboard`, `Breadboard tabs`, float positions, no extension
needed). 2.3 MB; commit it (the LAC's other extra GLBs are in git). It is a frozen copy: re-running the LSM's assemble.py later does
not change it.

### 4.2 materials.json ("LAC Build Instructions/materials.json")

Replace the breadboard rule (lines 95 - 100) with these two rules:

```json
    {
      "match": "^Breadboard$",
      "simplify_mm": 0.02,
      "edge_min_size_mm": 0.0,
      "atlas_frame": [[-69.285, -5.25, -42.17], [-13.205, 4.27, 40.84]],
      "_about": "the half breadboard: body white, legends black, the (+) rail stripes red and the (-) blue, from the LAC atlas. The mesh is the LSM's (extra part NAUO1, breadboard-lsm.glb), its joining tabs on the a side and the column 30 end as the real board has them (Lee, 21 Oct 2026), which changes the mesh's box: atlas_frame lines it up with the atlas by the CAD mesh's own box"
    },
    {
      "match": "^Breadboard tabs$",
      "color": "#ffffff",
      "simplify_mm": 0,
      "_about": "the breadboard's joining tabs, two on the a side (the front, +X) and three on the column 30 end (-Z), as on the LSM's breadboard (Lee, 21 Oct 2026): the body's white"
    },
```

And add to `"extra_parts"` (line 174), beside NANO:

```json
    "NAUO1": {
      "glb": "breadboard-lsm.glb",
      "pose": [0.0, 0.0, 0.0],
      "_about": "the breadboard, in place of the CAD's NAUO1: the LSM's breadboard as revised (Lee, 20 - 21 Oct 2026: the two joining tabs on the a side and the three on the column 30 end, where the real board has them; the CAD has them on the j side and the column 1 end). The same CAD part, vertex for vertex; cut from lsm.glb by tools/cut_part.py where NAUO1 sits: python tools/cut_part.py \"LSM Build Instructions/lsm.glb\" BREADBOARD \"LAC Build Instructions/breadboard-lsm.glb\" --like \"LAC Build Instructions/lac-guide.glb\" NAUO1. Holes unchanged (wire-paths.json)."
    },
```

(`"#ffffff"` as the LSM's rule, the atlas's body white; the LAC palette's `white_plastic` #f5f5f6 would not match the body.)

### 4.3 guide.py ("LAC Build Instructions/guide.py")

Step 1's camera and label spot would move by 1.3 mm with the board's new box (its camera is fitted to the box of the board and the
backing: target 674.5, 914.3, 1305.8 -> about 675.8, 914.3, 1304.6; radius 58.4 -> 58.3; the label's spot is the visible face nearest
the box middle). Keep them as they are (CLAUDE.md: never change a step's camera unasked). Lines 253 - 255, replace

```python
        labels=[dict(id=BREADBOARD, text='Breadboard', side='top')], look_from=BENCH_LOOK)   # (clear of the arrow)
```
with
```python
        labels=[dict(id=BREADBOARD, text='Breadboard', side='top', anchor=[663.9, 897.1, 1302.6])],   # (clear of the arrow)
        # (the camera and the label's spot as they were before the breadboard's tabs moved to the a side and the column 30 end: Lee,
        # 21 Oct 2026; BENCH_DIAG is the view look_from=BENCH_LOOK gave)
        view_dir=BENCH_DIAG, frame=([674.5, 914.3, 1305.8], 58.4))
```

Step 2's corner lines (`BB_CORNERS`, line 257 - 258) come from the whole board's box, so with the tabs on the other sides the front and
-Z lines would move 1.33 mm outwards (to 0.67 mm inside the body's front and -Z faces) and the back and +Z lines 1.33 mm inwards. As the
LSM did (its Step 2 "on the board's own corners"), put them 2 mm in from the body's own corners; replace line 257

```python
_lo, _hi = g.model.inst[BREADBOARD].bounds
```
with
```python
# (the breadboard's body without its joining tabs, which are on the a side and the column 30 end, as on the real board: Lee, 21 Oct
# 2026; the corner lines 2 mm in from the body's own corners)
_lo, _hi = np.array([647.80, 887.61, 1264.41]), np.array([702.55, 897.13, 1346.09])
```
(line 258 unchanged). The lines then go to x 649.80 / 700.55, z 1266.41 / 1344.09 at y 887.61: the front (x 700.55) and -Z (z 1266.41)
ones exactly as today, the back and +Z ones 1.33 mm further in (today they are only 0.67 mm in from the body's back and +Z faces,
because the box counted the tabs). To keep all four exactly as today instead:
`BB_CORNERS = [[x, 887.61, z] for x in (648.47, 700.55) for z in (1266.41, 1345.42)]`.

Nothing else in guide.py reads the board's shape (`g.model.inst[BREADBOARD]` is used only at line 257; Step 1's arrow is placed from
the backing, NAUO141, which is unchanged; every hole label uses `HOLES` / `CAPS`).

### 4.4 Words

README.txt, under LEE'S SECOND ROUND (or the parts notes): "- The breadboard's joining tabs on the sides the real one has them, as on
the LSM's (Lee, 21 Oct 2026): two on the a side (the front) and three on the column 30 end (the buzzer's end); the CAD has them on the j
side and the column 1 end. The breadboard is the LSM's, revised (breadboard-lsm.glb, extra part NAUO1: the same CAD part, holes
unchanged)."

CLAUDE.md, Layout, the LAC's entry, after "nano-mra.glb and usb-a-end.glb (the MRA's)": "; breadboard-lsm.glb (the LSM's breadboard,
its tabs on the a side and the column 30 end: Lee, 21 Oct 2026)".

### 4.5 Then (the parent session)

1. Save a copy of steps.json first (for the camera diff below), then
   `.venv.nosync/bin/python tools/build_model.py "LAC Build Instructions"` (materials.json changed; the set of parts did not, so
   guide.py would not rebuild the model by itself), then `.venv.nosync/bin/python "LAC Build Instructions/guide.py"`. One heavy job
   at a time: swap was 10.3 of 11.3 GB used when this was written.
2. model.report.json should show `Breadboard`: 133 solids, `atlas match 99%`, colours `#000000 #0074d9 #ff0e00 #ffffff`, "30605 faces
   under a skin recoloured" (as today), and a new `Breadboard tabs`: 5 solids, 50 triangles, `#ffffff`. Without `atlas_frame` the match
   falls to 3% and the whole board would come out in the default grey (simulated with build_model's own functions, below).
3. Cameras: diff every view's `camera` (and the four close-ups' `inset`) against the saved copy; with 4.3 there should be no change.
   Expected other differences: Step 2's two corner lines (if the body-corner version is used); possibly the F3 label's spot on Step 2
   (the generator's own pick: not expected to move, as no new tab stands between its spot and the camera).
4. In the browser: Steps 1, 2, 3 (tabs now on the front and the buzzer's end, facing the camera); Step 51c and Step 55c close-ups
   (55c looks at the back near column 2, 5 - 9 mm from today's back tab at columns 4 - 6, which goes); open `parts.html` to re-render `parts/Breadboard.png`;
   `_runthrough()`. wirecheck / motioncheck as usual (the measures below say nothing should change).

### 4.6 The other way (not recommended)

The same edit as assemble.py, in trim_source.py: lift `move_breadboard_tabs()` and call it on NAUO1's mesh in its own frame with
`P = I` (its planes are found per axis, so in the part's own frame it picks the same j side and column 1 end and gives the same
result, with the LAC export's triangulation). It needs trim_source.py to write new geometry for one mesh instead of copying the CAD's
bytes (about 100 lines more), plus the same materials.json `atlas_frame` and `Breadboard tabs` rule and the same guide.py edits. More
code for no visible difference.

## 5. How it was checked

- Mesh identity: `lac-guide.glb` NAUO1 `Breadboard` vs `lsm-electronics.glb` `Breadboard`: same vertex arrays (max |dV| 0.0 mm, normals
  identical), face lists differ in 6,116 rows (same faces, other diagonal). The revised LSM body: 66,214 of its 66,219 vertices are
  LAC/LSM CAD vertices; the other 5 are the fan centres closing the openings.
- Frame: hole tops from `wire-paths.json` (`holes`, `rows`, `column_z`) taken into NAUO1's own frame; the LSM's from assemble.py
  `ROW_X`, `COL1_Z`, `PITCH` into BREADBOARD's frame (table in section 2).
- The cut: ran `tools/cut_part.py ... --like ... NAUO1` into the scratchpad. Loaded it as stepgen does (stepgen `Model` with the kit's
  `extra_parts` plus this one): `Model.inst['NAUO1']` bounds [647.801, 887.608, 1263.075] .. [703.883, 897.128, 1346.088], 56,660
  triangles (the CAD copy replaced, not added); 105 vertices not on a CAD vertex (the 100 tab vertices and 5 fan centres), all others
  on one to 2.5e-13 mm; the 60 CAD vertices gone are the old tabs' (x 646.47 or z 1347.42); nearest-vertex distance from every one of
  the 300 hole tops identical before and after. Placed as build_model does (`add_extra_parts` on lac-guide.glb in memory): one assembly
  child NAUO1, the CAD's renamed "NAUO1 (replaced)", both meshes' world matrix equal to NAUO1's.
- Colours: `weld_positions` / `split_components` / `colour_from_atlas` from tools/build_model.py on the revised body against
  colour-atlas-lac.json `Breadboard`: with `atlas_frame` 99.2% (133 solids; faces white 47,370, black 9,232, red 4, blue 4: the same
  as the CAD mesh today less the 50 tab faces plus the 20 cap faces); without it 3.0% (below `atlas_min_match` 0.6: grey).
- Clearance at rest: every part of the kit (lac-guide.glb parts and the extra parts F2, F4, F5, F6, NANO, USB_A, posed as
  materials.json has them; omitted wire bodies left out), sampled on its triangles, against the five new tab boxes: F3 1.00 mm (below),
  the backing 1.00 mm (gone after Step 1), then the jumper caps NAUO14 3.06 mm and NAUO82 3.09 mm (in the front rail holes), F8 4.04 mm,
  cap NAUO49 4.98 mm, F2 6.01 mm. Every view of steps.json with each part at its view pose (offsets, or its carrier's pose composed with
  its ride): nothing within 3 mm.
- Clearance in motion: every moving part of every step, along its path (41 samples per stretch), swept box against the new tabs: only
  the LCD (Step 51) comes within 2 mm of a tab box, and its surface stays 8.28 mm away. (Against today's tabs: F2 in Step 55 passes
  1.84 mm from the back tab; with the back plain it clears by about 3.2 mm.)
- Wires: all 106 routes in steps.json as drawn (world mm): no route used by any view comes within 3 mm (centre line) of a new tab;
  the one at 1.57 mm (route 3, a straight resistor leg) is used by no view. The resistor going into the (-) blue rail beside the front
  tab (Step 5) has its leg tip at x 699.20, 3.35 mm from the tab, inside the board's wall.
- Lead lines and labels on the board's sides: none in steps.json ends within 1.5 mm of the old or new tab zones except Step 2's corner
  lines (section 4.3). F5 stands 18.65 mm beyond the board's +Z end, so nothing there ever touched the column-1 tabs.
- No other kit's CAD source (mra.glb, rcc.glb, pmg-guide.glb) has this breadboard mesh (by name, or by its vertex count and box).

## 6. What Lee will see, and what would not match

- The LAC's breadboard looks exactly like the revised LSM one: two tabs on the a side and three on the column 30 end, the j side and
  the column 1 end flat. In the LAC that is the front edge (by the rails it uses) and the buzzer's end, the sides the house view faces,
  so the tabs are now in view on Steps 1 - 2 and over the board until F1 and the end panels close the box; the back and the Nano's end
  are plain (Step 55c's close-up at the back, if its frame reaches today's back tab, shows a plain side).
- Parts List: the breadboard's picture needs re-rendering (parts.html); it will show the tabs on the new sides.
- Step 1 stays framed as now (pinned); its arrow is placed from the backing and does not move (the -Z tabs, x 695.95 - 699.80, are
  beside it, 3.8 mm nearer the end and 2.2 mm higher than its tail: worth a glance in the browser).
- Not matching the LSM exactly: (a) the board sits in F3's corner marks mirror-wise to how the LSM's sits in D1's (section 3), so the
  -Z tabs overhang the corner marks' inner edges by 0.46 mm in plan where the LSM's lie over its marks by 1.33 mm; nobody will see it.
  (b) The LAC's own research scripts that read `lac.glb` directly (docs/research/lac/scripts: lacload.py, make_wire_paths.py,
  lac_atlas.py) still see the CAD's tabs; the routing harness (scripts/routing/harness.py) reads materials.json `extra_parts`, so it sees
  the new board. Nothing that builds or publishes the guide reads either.
