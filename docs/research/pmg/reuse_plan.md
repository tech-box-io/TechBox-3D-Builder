# PMG: what the Piano Memory Game reuses from the MRA and RCC, its colours, and a trimmed source

Study of 19 Oct 2026. Lee asked to replace each item in the PMG CAD with the version used on the MRA or RCC where there is one
("the IO Module, Nano Board, etc."). This report says what that means part by part, what the PMG's `materials.json`, colour atlas,
`silkscreen.py` and `guide.py` need, and how to keep the 167 MB CAD export from taking the Mac down.

Nothing in the kit folders, `tools/` or `player/` was changed. Everything was read from GLB headers (`tools/glbio.py`-style: the
JSON chunk plus memory-mapped accessors of single meshes); the whole `pmg.glb` was never loaded. Scripts and drafts are in
`docs/research/pmg/scripts/` (all named `reuse_*`, plus `trim_source.py`, `trim.example.json`, `silkscreen.proposed.py`) and
`docs/research/pmg/` (`reuse_poses.json`, `materials.proposed.json`, `colour-atlas-pmg.proposed.json`).

All coordinates are **PMG assembly mm** (pmg.glb x 1000, Y up), as `stepgen.Model` reads them, unless marked "MRA". The assembly node
`PMG Full 3D Cadasio Build` is the scene root with the identity transform. **TechBox's Cadasio project for this build is in the same
frame** (1 Cadasio unit = 23.608 mm, no other transform): 167 of its 415 components land on a GLB instance to 0.5 mm, most to 0.0 mm (script
`reuse_cadasio_frame.py`; the CAD study's `cadasio_map.md` finds the same).

## 0. In short

- **The I/O module is the MRA's board, exactly.** Every one of the MRA module's 36 meshes (board, headers, sockets, jack, regulator,
  capacitors, resistors, LED, reset) sits in the PMG module in the same place to 0.0001 mm. The PMG's module is in fact the RCC's
  module `NAUO23` (all 70 meshes to 0.004 mm): the shield plus the plain "arduino nano" model inside it. The MRA's rules, atlas
  entries and silkscreen carry over unchanged; only the silkscreen's four picture corners move (2.4).
- **The Nano Board is the MRA's model too** (`nano_Varsayılan`, same own-frame box to 0.001 mm), but the PMG's two Nano copies
  (NAUO2, NAUO3) are **not seated**: NAUO3 floats 15.2 mm above the sockets, NAUO2 44.9 mm. The guide should use the MRA's Nano
  export (`mra.glb` NAUO126, as the RCC does), placed by the module's own transform, which puts it exactly in the sockets (2.2).
- **The I/O module's CAD carries a plain Nano inside it** (node NAUO301, 34 meshes, 213,141 vertices): it must be left out, or the
  module would show two Nanos.
- **USB cable:** the A end is the MRA's mesh (identical vertices). The Mini-B end is not: the PMG's cable is **right-angle**, the
  MRA's straight. In the new CAD the module hangs on the back panel H4 with the Nano's USB socket facing **down**, 15.3 mm above the
  table: a straight plug (54 mm long) would reach about 32 mm **through the table**. Keep the PMG's right-angle end, coloured as
  the MRA's Mini-B (question 1). The published guide has the module the other way up (USB at the top): question 2.
- **Jumper wires** use the MRA's method and the MRA's cap mesh (identical vertices): caps are CAD parts, the wire is drawn. The new
  CAD has **17** jumper wires (two per button), the published guide **21** (three per button): question 3.
- **The PMG's own parts** (four button modules, TM1637 display, MAX7219 32x8 matrix, wood H1-H14) get rules in the house colours and
  TechBox's published Cadasio colours (section 3). The four button caps are one mesh in the CAD, so to colour them black / yellow /
  white / blue each needs a mesh name of its own (done by the trimmed source, 5.3).
- **Memory: pmg.glb is too big to use as the source.** `stepgen.Model` (every `guide.py` run) loads the whole file with trimesh:
  6.5 million vertices, 10.7 million triangles, an estimated 2-4 GB. A **trimmed source** of the 60 parts the guide shows plus the
  MRA Nano is **16.7 MB** (715,710 vertices); `stepgen.Model` loads it in 1.8 s with a 224 MB peak (measured, on a test copy in the
  scratchpad). Proposed script: `scripts/trim_source.py` + `scripts/trim.example.json` (section 5). pmg.glb (167 MB) is also over
  GitHub's 100 MB file limit.
- **model.glb** should come out about **1.4 MB** (1.2-1.7), smaller than the MRA's 2.1 MB and the RCC's 2.0 MB (section 6).

## 1. What the CAD holds, and which copy the guide uses

The engineer modelled most parts several times, once per position in the Cadasio guide. Our player moves one copy of each part,
with poses relative to where it sits when the game is built; so the guide keeps the **built** copy and turns every other copy into
a pose. All pose copies are exact copies (every mesh lands on its counterpart to 0.0 mm). The poses, ready for `guide.py`
(`turned(axis, degrees, at, t)` about the built part's middle, or a plain move), are in **`docs/research/pmg/reuse_poses.json`**
(script `reuse_poses.py`); the main ones:

| Part | Built copy (kept) | Other copies (become poses) |
|---|---|---|
| I/O module | **NAUO78**, standing on edge on the back face of H4, components facing out (+x) | NAUO1 on the bench, flat (turned 120 deg about (-0.577, -0.577, 0.577) through [600.7, 932.5, 1290.5], then moved [72.8, -48.2, 8.9]); NAUO94 held 104.7 mm above its place ([0.0, 104.7, 0.1]) |
| Nano Board | **NANO** (the MRA's model, in the module's sockets: 2.2) | NAUO2 (44.9 mm above the bench seat), NAUO3 (15.2 mm above it) |
| Buttons | **NAUO76** black, **NAUO83** yellow, **NAUO84** white, **NAUO85** blue: in the case, under H5 | NAUO7, NAUO6, NAUO5, NAUO4 on the bench (the same colours; each a 179.9 deg turn about (0.750, -0.662, -0.004) plus about [134.7, 43.0, 34.0 / 15.3 / -3.3 / -21.8]) |
| 4-digit display | **NAUO79**, on its brackets | NAUO80 on the bench (40.0 deg about +z through its middle, then [96.9, -56.6, -73.2]), NAUO129 80.0 mm along +z |
| LED matrix | **NAUO81**, in the case | NAUO44 on the bench (180 deg about (-0.940, 0.342, 0)), NAUO82 143.3 mm along -z, NAUO267 85.9 mm up |
| USB Mini-B end (right-angle) | **NAUO282**, in the Nano on NAUO78 | NAUO279 on the bench (rides with the bench module to 0.06 mm), NAUO281 with the lifted module (to 0.27 mm) |
| USB A end | **NAUO278** (its resting place is the guide's choice: it lies 6.7-15.2 mm below the table, y 872.6-881.1) | NAUO280 upright beside the module, NAUO283 on the bench |
| Wood | NAUO60-75, NAUO77 (H1-H14, keys H9 x4 = NAUO69-72): one copy each | none |
| Jumper caps | the 34 on the built parts' pins (2.5) | 105 more: on the bench copies, the lifted copies and the two loose ribbons |
| Wire and cable bodies | none (drawn by the player) | 114 sweep bodies (`PartNN^PMG Full 3D Cadasio Build`, `Copy of ...`) |

Bulk of the file by kind (vertices): wire and cable bodies 3,895,478 (60 %); LED matrix copies 941,312; I/O module copies 843,540;
the two Nanos 592,140; button copies 108,384; jumper caps 53,156; USB ends 36,816; wood 22,518; displays 11,592.

## 2. Parts the PMG shares with the MRA / RCC

How compared (script `reuse_compare.py`): same mesh names; same own-frame boxes (accessor min/max); and for a multi-mesh part, one
rigid transform taken from one mesh (the board) carrying every mesh of one onto a same-named mesh of the other.

| PMG part | MRA / RCC part | Same? | Evidence |
|---|---|---|---|
| I/O module NAUO78 (and NAUO1, NAUO94), shield meshes | MRA NAUO82 without its Nano | **Yes** | all 36 meshes, worst 0.0000 mm |
| I/O module NAUO78, all 70 meshes | RCC NAUO23 (shield + plain Nano NAUO86) | **Yes** | worst 0.0035 mm |
| Nano NAUO2 / NAUO3 `nano_Varsayılan` | MRA NAUO126 | **Same model, other export** | own box [-3.82, -8.52, -16.62]..[41.18, 10.11, 1.38] in both (to 0.001 mm); mesh node placed the same inside its part; 296,070 vertices against the MRA's 290,945 (the RCC's own export had 174,569 and sliver triangles) |
| USB A end NAUO278/280/283 `USB Cable end` | MRA `usb-a-end.glb` `USBCableend` | **Yes** | same 8,678 vertices to 1e-13 mm (triangle order differs) |
| USB Mini-B NAUO279/281/282 `USB Right Angle` | MRA `usb-mini-b.glb` `MiniUSBB` | **No** | right-angle, 3 solids, own box [-15.03, 0, -6]..[4.83, 7.5, 18.0]; the MRA's is straight, 54.0 mm long |
| Jumper caps `Wire Cap` (1.75 x 1.75 x 8.0) | MRA NAUO95-110 `Wire Cap` | **Yes** | same 348 vertices, 0.0 mm |
| `Wire Cap V2` (1.75 x 1.75 x 12.0) | none | | only on the CAD's two loose ribbons (NAUO203-206, 215-218) |
| everything else (buttons, display, matrix, wood) | none | | the MRA's joysticks, servos, screws and the RCC's radios, wheels, boards are not in the PMG |

### 2.1 The I/O module (NAUO78)

Transform, MRA module -> PMG NAUO78 (exact on all 36 meshes):

    p_PMG = R . p_MRA + t,   R = [[0, 1, 0], [0, 0, -1], [-1, 0, 0]]   (a third of a turn, 120 deg, about (1, 1, -1)/sqrt 3),
                             t = [490.546, 1077.982, 1360.501] mm
    i.e.  x' = y + 490.546,   y' = 1077.982 - z,   z' = 1360.501 - x
    (MRA up, +y, becomes +x: the components face out of the back panel, away from the case.)

(The bench copy NAUO1 is the MRA module moved by [603.545, 774.168, 1153.856] with no turn; NAUO94 is NAUO78 raised 104.679 mm.)

**materials.json: copy these MRA / RCC rules unchanged** (each pattern checked against pmg.glb's names; script `reuse_drafts.py`):

| Rule (MRA / RCC) | Catches in NAUO78 |
|---|---|
| `^Shield_Arduino` pcb_navy | `Shield_Arduino NANO` |
| `^Samtec-TLW-` pin + rank 1 yellow skin | the 19 header strips (`-103-` x2, `-104-..._N/_R/_B` x4 each, `_W` x2, `-108-..._B/_R/_N`) |
| `^47uf CAP` metal can, black sleeve | `47uf CAP Dcase` |
| `^cap106C` | `cap106C` x2 (atlas) |
| `^(m7 diode\|smt_resistor\|nano - reg\|blm21\|reset core)` | `m7 diode`, `smt_resistor222_a` x3, `nano - reg`, `blm21`, `reset core` |
| `^reset shell`, `^led$` | `reset shell`, `led` |
| (no rule: atlas) | `User Library-PJ-002AH_Pad` (atlas), `Samtec-SSW-115-01-F-S` x2 and `User Library-PJ-002AH_Body` (atlas single colours) |

**Atlas:** the MRA's entries carry over unchanged (they are in the mesh's own frame, which is the same). I copied them from
`colour-atlas-rcc.json` (which holds the MRA's, unchanged) into `docs/research/pmg/colour-atlas-pmg.proposed.json`, with
`instances` set to the PMG ids. **Matched on the PMG's own meshes of NAUO78 with build_model's `colour_from_atlas`: 100 % for
every entry** (`Samtec-TLW-*` x8, `nano - reg`, `cap106C`, `led`, `User Library-PJ-002AH_Pad`), although the PMG's export has
slightly different vertex counts (e.g. `cap106C` 6,300 against 6,270).

**The plain Nano inside the module.** Each module copy holds the shield's original "arduino nano" sub-assembly (RCC-style:
`nano-board`, `atmega328`, `ftdi FT232rl`, `MINIUSBSHELL`, `15pin_header__` x2, ... plus its own LEDs, regulator, reset button, caps
and resistors, which share mesh names with the module's own). In NAUO78 and NAUO94 it is node **NAUO301**; in the bench copy NAUO1
it is NAUO387 and has lost its board and pin headers but kept its chips (they float where the board would be). With the MRA Nano
fitted, it must go. Three ways:
- **(a) recommended:** the trimmed source leaves it out (`trim.json` `"drop": {"NAUO78": ["NAUO301"]}`, section 5).
- (b) `own_parts: {"NAUO301": ...}` makes it a part of its own, which the guide never shows, so build_model leaves it out (as the
  RCC's NAUO86). Caution: the name NAUO301 also exists under NAUO94 (the export repeats inner node names in each copy; 98 names
  repeat). `build_model.promote` takes the first, which is NAUO78's (node 210; NAUO94's is node 358), but stepgen goes through
  trimesh, which renames repeated node names, so this is fragile on the full file.
- (c) mesh-name omit rules cannot do it alone: they catch the plain Nano's own chips but not its LEDs, regulator, reset, caps or
  resistors (same names as the module's).

**Which way up on H4 (question 2).** In the new STEP the module on H4 has its USB end **down**: the Nano's USB socket at y
903.1-912.5 (mouth at the bottom, y 903.1), the DC jack at y 903.0-917.4. In TechBox's published Cadasio project the same module on
H4 (`Ensamblaje_Shield_NANO-2`) is turned end for end: USB socket at y 950.6-960.0, jack at 945.7-960.1, the right-angle plug above
it (Cadasio step [102] shows it so), and the module 3.7 mm lower. The bench module NAUO1 is the Cadasio's bench module exactly.

### 2.2 The Nano Board

Use the MRA's export of the Nano (`mra.glb` NAUO126), as the RCC does for both its Nanos. Its seat on NAUO78 is the MRA Nano carried
by the module's transform (2.1): box **[599.5, 903.1, 1282.0]..[618.1, 948.1, 1300.0]**. Check: its board lands exactly on the board
of the plain Nano the CAD has in that seat (x 606.49-611.09, y 904.92-948.12, z 1282.04-1300.04, to 0.01 mm), so the seat is right.

The PMG's own Nano copies are no help for the seat: **NAUO3 is 15.243 mm straight above the sockets of the bench module, NAUO2
44.900 mm** (same x and z). TechBox's Cadasio project has the seated copy (`nano-3`, y 883.1-901.7, the one its guide shows) and one
on the module on H4 (`nano-4`); the STEP has neither. So `tools/cut_part.py --like pmg.glb NAUO3` would put the Nano 15.2 mm
proud of its sockets. Two ways that work:

- **(a) in the trimmed source** (recommended with section 5): `trim.json` `"graft": {"NANO": {"glb": "../MRA Build Instructions
  Prototype/mra.glb", "node": "NAUO126", "pose": {"t": [490.546, 1077.982, 1360.501], "r": [0.57735, 0.57735, -0.57735, 120.0],
  "at": [0, 0, 0]}}}`. The part is called **NANO**: pmg.glb already has a part called NAUO126 (a jumper cap). Tested: stepgen.Model
  puts NANO at [599.47, 903.12, 1282.04]..[618.09, 948.12, 1300.04].
- **(b) extra_parts, as the RCC:** cut the Nano out of mra.glb **without** `--like` (the file then holds it where the MRA has it):

      .venv.nosync/bin/python tools/cut_part.py "MRA Build Instructions Prototype/mra.glb" NAUO126 "PMG Build Instructions/nano-mra.glb"

  and in materials.json:

      "extra_parts": {"NANO": {"glb": "nano-mra.glb", "pose": {"t": [490.546, 1077.982, 1360.501], "r": [0.57735, 0.57735, -0.57735, 120.0], "at": [0, 0, 0]}}}

  (not run: it writes into the kit folder). The output should be about 11.5 MB (cut_part.py now copies only each accessor's bytes).
  Aside: the RCC's `nano-mra.glb` is 41.7 MB because its buffer views are mra.glb's whole views (13.1 + 13.1 + 15.5 MB), i.e. it was
  cut before cut_part.py copied accessors only; re-cutting it would save 30 MB in git (not verified by running).

Rule and atlas: the MRA's `^nano_` rule (simplify 0.06, edge_min_size 2.0, max_tris 16000, `atlas_colours {"#cccccc": "pin"}`) and
its `nano_Varsayılan` atlas entry, unchanged (the atlas was made from this very mesh). No sticker (the MRA has none; the RCC's dots
tell its two Nanos apart). If Lee would rather keep the PMG's own export (0.4 % finer), the same seat applies: `--like` is still
wrong, use the pose above relative to the MRA frame, or move NAUO3 by [0, -15.243, 0] and then by the bench-to-H4 transform.

### 2.3 The USB cable

**A end:** NAUO278 (or 280 / 283) is the MRA's `usb-a-end.glb` mesh with the same vertices, already in the CAD: no extra part
needed. Rule: the MRA's `^USBCableend$` renamed to `^USB Cable end$` (overmould black, rank 1 shell and ranks 3-4 contacts silver,
rank 2 tongue white; checked: the PMG mesh splits into the same 5 solids). The cable leaves it at **[596.7, 876.8, 1374.1]**, along
-z. Its resting place is for the guide (as the MRA's `A_ON_THE_TABLE`): the CAD's copies lie under the table (y 872.6-881.1).

**Mini-B end: right-angle in the PMG, straight in the MRA.** NAUO282 (`USB Right Angle`, 3 solids: rank 0 overmould 7.5 x 19.8 x 24.0,
rank 1 shell 3.1 x 6.9 x 7.0, rank 2 its insert) sits with its 7.0 mm metal plug fully in the Nano's socket (plug y 903.1-910.1), its
body below the socket down to y 890.2, **2.4 mm above the table** (y 887.8), and the cable leaving sideways at **[611.2, 893.3,
1309.0]** along +z (exit 4.5 mm across, so the MRA's 3.5 mm cable, radius 1.75, fits).

What the MRA's straight end would mean there (question 1): the socket faces down with its mouth 15.3 mm above the table. The MRA's
`MiniUSBB` is 54.0 mm long (plug 7.0, overmould and strain relief 47.0) and goes straight out of the socket. Plugged in, its body
would run from y 903.1 down to about **y 856** (cable end), i.e. **about 32 mm below the table**: the game could not stand with
the cable in. It is clear of the case itself (it is behind H4, x 607-615, beyond H4's outer face at 590.4 and below everything
else back there). With the module the published way up (USB at the top), a straight plug would stand about 47 mm above the
socket, to about y 1007-1009, level with the top of H14 (1006.7), behind the case: possible, but not what the kit's cable is (the
published guide shows a right-angle cable). **Recommendation: keep the PMG's own right-angle end (NAUO282), coloured as the MRA's Mini-B**:
`"match": "^USB Right Angle$", "color": "black_plastic", "components": [{"rank": [1, 2], "color": "pin"}]` (the Cadasio has the
same three colours: overmould #1e1616, shell #a6a9aa, insert #e4e4e4).

**The cable itself** is drawn by the player as on the MRA (`g.wire('usb cable', 'cable_black', 1.75, name='USB Cable')`, routed
between the two exits above). The CAD's own cable pieces (NAUO277 `Copy of Part23`, NAUO284 `Part152`, NAUO285 `Part153`) are
sweep bodies: omitted. Note that NAUO285 dips to y 882.3, 5.5 mm below the table.

### 2.4 The I/O module's silkscreen

The MRA's decals carry over exactly as the RCC's do: same items, only each picture's `origin`, `u` and `v` go through R and t (2.1),
and the key becomes **NAUO78**. Proposed script: **`scripts/silkscreen.proposed.py`** (the RCC's shield section with the PMG's R and
t; for the kit folder as `silkscreen.py`; it writes `decals.json` only when it sits beside pmg.glb or is given a path). Result:

| decal | origin (PMG) | u | v | size |
|---|---|---|---|---|
| silkscreen top | [596.996, 904.822, 1317.141] | [0, 1, 0] | [0, 0, -1] | [57.2, 53.34] |
| silkscreen underside | [595.306, 962.022, 1263.801] | [0, 0, 1] | [0, -1, 0] | [53.34, 57.2] |
| capacitor print | [602.816, 923.137, 1276.486] | [0, 1, 0] | [0, 0, -1] | [5.8, 5.8] |
| regulator print | [598.596, 923.352, 1292.441] | [0, 1, 0] | [0, 0, -1] | [6.5, 3.5] |

Checks: the top picture lies 0.02 mm above the board's top face (x 596.978), as on the MRA; its corners land on the board's corners
(y 904.82 / 962.02, z 1317.14 / 1263.80); v x u = +x, the side the components face. The underside picture faces H4 and is mostly
hidden by it. Same caution as the RCC: this assumes the PMG kit's module is the same board revision as Lee's MRA photos (the RCC's
was confirmed, 16 Oct 2026). The decals belong to the part, so they ride with it on the bench.

### 2.5 Jumper wires

As the MRA: each wire is a kit part made of two CAD caps (parts, `Wire Cap`, the MRA's mesh) and a wire the player draws between
them (`g.wire(id, colour, 0.625, name=...)`; the CAD's wire bodies are 1.2-1.4 mm across, matching the MRA's 1.25 mm). The caps are
unlisted and named on hover only (`HOVER_NAMES`, `UNLISTED`); the kit part is listed by hand with `g.list_part('Breadboard Wire
(F-F)', [cap_a, cap_b], n, after=...)` and pictured with `g.part_picture(..., wires=[...])`, as the MRA's guide.py does (lines
545-554). The MRA calls them "Breadboard Wire (F-F)" (question 7).

**Caps the guide uses (34, on the built parts' pins):** 17 on NAUO78 (NAUO95-102 and NAUO111-119, 8 mm long along x at x 598.5-606.5),
8 on the case buttons (NAUO86-93, two per button), 4 on the display (NAUO259-262), 5 on the matrix (NAUO134-138). All 34 are one mesh
(byte for byte), so build_model builds it once.

**17 wires, not 21 (question 3).** The new CAD wires two pins of each button (the middle pin and one end pin: caps NAUO86 / NAUO87 on
NAUO76 at z 1244.2 / 1241.6, the pins at z 1239.1, 1241.6, 1244.1) and models 17 wire bodies on the bench (Part36-43: 8 button wires,
Part44-47: 4 display, Part48-52: 5 matrix) and 17 caps on each module copy. The published guide wires VCC, OUT and GND of every
button: 12 + 4 + 5 = 21. Which pins the two are, and the wire colours, are for the wiring study (`cad_wire_paths.md`).

**Colours.** The MRA chose a colour per pin (`JUMPER_COLOURS`); the PMG's published guide gives each of its 21 wires a colour of its
own in ribbon order (rulebook section 8). Caps: the MRA's are #404040 (its atlas), the PMG Cadasio's #000000, the rulebook's Dupont
housings #1e1616; the draft keeps the MRA's (palette `jumper_cap`, question 4). `Wire Cap V2` is only on the loose ribbons; the draft
rule `^Wire Cap( V2)?$` covers it if the guide shows a ribbon.

## 3. The PMG's own parts: rules

Colours: house library (rulebook section 8) where it has one, else TechBox's published PMG Cadasio colours (read per solid with the
atlas rule: the colour each solid shows most often while visible; script `reuse_cadasio_frame.py`), with Lee's standing rulings (pins
silver, edges at 40 deg). The Cadasio solids have exactly our solids' own-frame boxes for the button, display and right-angle plug,
so an atlas made with `tools/cadasio/atlas.py` would also match them; rules are simpler here. Solids are counted as build_model
counts them (welded, ranked by box volume; script `reuse_solids.py`).

| Part | Mesh (in pmg.glb) | Solids | Rule (draft) | Cadasio / house |
|---|---|---|---|---|
| Button board | `Board^Big Button Module_По умолчанию` | 1 (13 x 22 x 1.2) | `^Board\^Big Button Module` pcb_navy | Cadasio #000f41; rulebook "PMG button boards #000f41" |
| Button header | `Socket_Blok` x4 per module | 2: pin 0.8 x 8.4 x 9.4 (rank 0), spacer 2.0 x 2.5 x 2.5 (rank 1) | `^Socket_Blok$` pin, rank 1 header_black | Cadasio pins #c6c1bc, spacers #1a1a1a; Lee: pins silver |
| Tactile switch | `Tactal Switch - THRU(12mmx12mmx8mm)-Blue.stp_По умолчанию` | 21: body + 20 small 0.25 mm marks | black_plastic, simplify 0.05, max_tris 3000, edge_min_size 1.5 | Cadasio #1e1e1e (one colour) |
| Button cap | `Push_Button_Cap.step_По умолчанию` (renamed per button, 5.3) | 1 (13.1 dia x 7.8) | `^Push_Button_Cap black$` cap_black #1e1616, `yellow` #ffdc00, `white` #f5f5f6, `blue` #0074d9; outline, max_tris 1500 | Cadasio: NAUO76 #000000, NAUO83 #ffdc00, NAUO84 #ffffff, NAUO85 #0074d9 (bench: NAUO7 black, NAUO6 yellow, NAUO5 white, NAUO4 blue) |
| 4-digit display | `Display TM1637_По умолчанию` (one mesh) | 41 = the Cadasio's 41 | pin; rank 0 pcb_blue, rank 1 led_face, rank 2 ic_black, thin 0-0.02 led_white; two region boxes (own [-13.7, -6.45, 1.35]..[15.7, 6.45, 8.25] and z 8.45-8.55) led_face | Cadasio: board #224bbe (= rulebook display board), shell #000000, chip #000000, 30 segments #ffffff, pins #e3e3e3 / #cccccc |
| Matrix board | `PCB` | 1 (129.5 x 32 x 1.5; 20,664 vertices) | `^PCB$` pcb_blue, simplify 0.03, max_tris 6000, edge_min_size 1.0 | Cadasio #234bbf |
| Matrix sockets | `8x female rounded header` x8 | 1 each (11,951 vertices each, all but hidden between board and blocks) | header_black, simplify 0.05, max_tris 1500, edge_min_size 1.5 | Cadasio #232323 |
| LED block | `1088AS` x4 | 79: body (rank 0), 56 loose dots, 16 legs, 6 flat print pieces | pin; rank 0 led_white; thin 0-0.02 ink; region: face (own y -0.15..0.01) led_face, then 64 dot boxes (2.2 mm square, own y -0.15..0.01) led_white; max_tris 8000 | Cadasio: sides #ffffff, face (TOP MASK) #1a1a1a, 64 dots and legs #e4e4e4 |
| MAX7219 chips | `MAX7219--3DModel-STEP-56544_Défaut` x4 | 1 | ic_black | |
| Matrix input header | `90 5xHeader Pins` | 11: plastic (rank 0) + 10 pin pieces | pin, rank 0 header_black | |
| Wood H1-H14 | `H1` ... `H14`, `H4v2`, `H11v2`, `H12v2`, `H13v2`, `H9` x4 | 1 each | `^H([1-9]\|1[0-4])(v2)?$` wood, simplify 0, **roughen_mm 0.1**, engraving ink | house #deb887 / #1e1616; publish.py requires roughen_mm |
| Wire / cable bodies | `PartNN^PMG Full 3D Cadasio Build`, `Copy of ...`, `Copy (2) of ...` (114) | | `\^PMG Full 3D Cadasio Build$` omit | drawn by the player |
| Plain Nano in the module | `nano-board`, `atmega328`, `ftdi FT232rl`, `NANO DIODE`, `MINIUSB*`, `MINI USB *`, `16mhz crystal - measured`, `102/189 RESISTOR PACK`, `15pin_header__`, `2pin_header__02` | | omit (only a safety net: see 2.1) | |

Detail settings follow the MRA / RCC rules for similar purchased parts (`nano_` 0.06 / 16000 tris; `Thumb-Button` outline for a
round cap; `Tactile-Switch` 0.05 + edge_min_size 3; the RCC's `HDR-TH_` sockets 0.02). The heavy ones are the Nano (290,945
vertices: the MRA's rule) and the matrix (235,328 vertices per copy, but its 4 blocks, 8 sockets and 4 chips are each one mesh
repeated, so build_model builds each once: about 16k triangles out for the whole matrix).

Points to look at on the first build (they could not be checked without building):
- **Display:** in this CAD the board solid includes the display block, and the black "shell" (rank 1) sits 0.1 mm over it, outside
  the 0.05 mm reach of build_model's `skin` handling, so the draft colours the block black with two boxes instead. The segments are
  flat pieces at own z 8.3 in pockets of the block (floors at 8.2, rim at 8.5); check they show, and that the pockets' 0.3 mm walls
  (left blue) do not.
- **LED blocks:** the black face and the white body are one welded solid, and the dot column at own x 2.0 is welded into it too
  (56 loose dots of 64), so all 64 dots are coloured by boxes (half-size 1.1 mm, inside each dot's 1.5 mm radius). Check for white
  specks or black rims; adjust the half-size. If the face should simply be black all round, rank 0 led_face and the dot boxes alone do.
- **Buttons:** each module has four `Socket_Blok`, two of them the same pin in the same place (harmless when one colour). The four
  built buttons (NAUO76/83/84/85) lie tipped 7.1 deg from flat (board normal (-0.124, 0.992, 0.007)); the bench ones are exactly
  upright. Not a colour point; for the geometry study.

## 4. Drafts written, and what they were checked against

- **`docs/research/pmg/materials.proposed.json`**: a complete draft materials.json: `source` pmg-guide.glb, the RCC's palette less
  its RCC-only colours plus `jumper_cap`, `cap_*`, `led_white`, `led_face`; the RCC's defaults; 28 rules (the PMG's own, then the
  MRA / RCC module and Nano rules unchanged); `atlas` colour-atlas-pmg.json; `decals` decals.json; `_notes` with what is reused and
  what is unconfirmed; and, under `_extra_parts_instead_of_graft`, the extra_parts entry to use if the Nano is not grafted.
- **`docs/research/pmg/colour-atlas-pmg.proposed.json`**: the MRA's atlas entries for the module and the Nano (via the RCC's file),
  plus the MRA's `Wire Cap` single colour. (Another agent's `colour-atlas-pmg-draft.json` in the same folder is a raw per-Cadasio-
  component dump; this one is keyed by our mesh names, as build_model reads an atlas.)
- **Checked** (`reuse_drafts.py`): against the guide's 60 parts + NANO, every mesh is caught by a rule or an atlas entry, **none would
  be left grey**, and only the fallback `^Push_Button_Cap` rule catches nothing (it is for the untrimmed file). Against all 616
  meshes of the full pmg.glb, the omit rules catch the 114 wire / cable bodies and the 57 plain-Nano meshes, and no name is left
  without a rule or atlas entry.
- Not done (need the kit files): engraved codes (`engraved-codes.json`), `move_engraving`, the Parts List grouping, wire colours.

## 5. Memory, and a trimmed source

### 5.1 How the tools use the source

- **`tools/stepgen.py` `Model`** (every `guide.py` run, and the deconstruction's): `trimesh.load(source)` loads every mesh of the
  file, then copies every mesh node into assembly mm, groups them by top-level instance, concatenates each group and welds it. For
  pmg.glb that is 616 meshes, 6,504,936 vertices and 10,708,671 triangles; one float64 copy of all of it is about 570 MB, and the
  load, the copies and the concatenations hold two to three at once: an **estimated 2-4 GB** (not tried: this Mac had 0.6-0.8 GB of
  swap free while I worked). Measured on the trimmed test file below: 1.8 s, 224 MB peak footprint (433 MB resident).
- **`tools/build_model.py`**: `read_glb` reads the whole 167 MB binary into memory, and `add_extra_parts` makes a new copy of it for
  each extra part (`blob = blob + ... + eblob`), so 330 MB or more before any work; then it processes only the meshes of the parts
  the kit's steps files show (`parts_shown`: top-level ids in any `steps*.json`; everything else is dropped by subtree). So
  build_model would cope, wastefully; stepgen would not.
- **`tools/cut_part.py --like pmg.glb ...`** also reads all of pmg.glb (read_glb) just for one node's matrix.
- **Repeated inner node names** (2.1) make `own_parts` fragile on the full file.
- **Git:** pmg.glb is 167 MB; GitHub refuses files over 100 MB, and this repository has a GitHub remote (origin
  tech-box-io/TechBox-3D-Builder). It cannot be committed as mra.glb and rcc.glb are.

### 5.2 The proposal: `trim_source.py` + `trim.json` in the kit folder

**`docs/research/pmg/scripts/trim_source.py`** (proposal; for `PMG Build Instructions/trim_source.py`) generalises what cut_part.py
does to a list of parts: it writes a GLB with the same assembly node and, under it, only the kept top-level instances, each with its
own name, matrix and sub-tree (so part ids stay NAUO78 etc. and guide.py works with either file), copying only those meshes' bytes
(each accessor's own bytes, through a memory map; identical accessors stored once). `trim.json` (draft:
**`scripts/trim.example.json`**) lists:
- `keep`: the 60 built copies of section 1 (NAUO78; buttons NAUO76/83/84/85; NAUO79; NAUO81; wood NAUO60-75 and 77; USB NAUO282 and
  NAUO278; the 34 caps);
- `drop`: `{"NAUO78": ["NAUO301"]}` (the plain Nano inside the module);
- `rename`: each button cap under a name of its own (5.3);
- `graft`: the MRA Nano as NANO (2.2).

It records the source's size and SHA-256 in the output's `asset.extras`, and has `--check` (report only). Then materials.json
`"source": "pmg-guide.glb"` and `Guide(..., source='pmg-guide.glb')` in guide.py.

**Tested on a copy in the scratchpad** (not in the kit; deleted after): 61 parts, 715,710 vertices, 411 accessors stored as 147,
**16.7 MB** (5.2 MB without the grafted Nano), written in 1.4 s with a 74 MB peak; `stepgen.Model` loads it in 1.8 s (224 MB peak),
NANO at [599.47, 903.12, 1282.04]..[618.09, 948.12, 1300.04], NAUO78 without its plain Nano (x up to 607.98).

### 5.3 Why the button caps need renaming

The four caps are byte-for-byte one mesh under one name, and build_model builds identical geometry under the same name once and
shares it (`first_like`), and a rule matches mesh names only: all four would take one colour. The trimmed source gives each cap's
mesh its own name (`Push_Button_Cap black` / `yellow` / `white` / `blue`), so four rules colour them. (The alternative is a
build_model feature matching a rule to an instance id: a tool change, for every kit.)

### 5.4 Order of work, and what must come from the full file first

1. Measure everything that needs the pose copies or the wire bodies from the **full** pmg.glb first: the wire centre lines
   (`wire-paths.json`: the 114 sweep bodies are not in the trimmed file), the poses of the bench / lifted copies (`reuse_poses.json`),
   anything else the guide author wants from the copies. Keep pmg.glb on this Mac (outside git, with its SHA-256 in
   `cad-sources.sha256`, as the STEP), so the trimmed file can be made again.
2. Make `pmg-guide.glb` with trim_source.py; commit it (16.7 MB) instead of pmg.glb. Adding a part later = add its id to `keep`, run
   again (a few seconds).
3. Point materials.json and guide.py at it.

## 6. model.glb size

Measured on the two finished kits: 8.8 bytes per output triangle plus edge segment in both (MRA 2,135,080 bytes for 172,822
triangles + 69,427 edge segments; RCC 1,986,248 for 153,334 + 71,199). Estimate for the PMG, unique meshes after simplification:
I/O module about 22,000 triangles (the MRA's module: 22,216), Nano 34,193 (as the MRA and RCC), matrix about 16,000 (one each of
board, socket, block, chip, header), wood about 20,000, buttons about 8,000 (four caps now separate), USB ends about 5,000, display
about 3,000, caps 126: **about 110,000 triangles and 50,000 edge segments, so about 1.4 MB** (1.2-1.7 MB). The website's copy is
cut to the parts each guide shows, as for the MRA and RCC.

## 7. Questions for Lee

1. The PMG's USB cable has a **right-angle** Mini-B end (the CAD and the published guide); the MRA's is straight. Keep the PMG's
   right-angle end, coloured like the MRA's (recommended)? A straight end, with the module as the new CAD mounts it, would stick
   about 32 mm down through the table.
2. **Which way up does the I/O module go on the back panel H4?** The new CAD has the Nano's USB end at the bottom (plug just above the
   table, cable out to the side); the published guide has it at the top.
3. **How many wires per button?** The new CAD wires two pins of each button (17 jumper wires in all); the published guide wires VCC,
   OUT and GND of each (21).
4. Jumper wire caps grey #404040 like the MRA's, or black like the published PMG guide?
5. Button caps black / yellow / white / blue on D4 / D5 / D6 / D7, as published?
6. The Nano Board: the MRA's model, as on the MRA and RCC (the PMG CAD's own copies are the same model but not seated): agreed?
7. Parts-list name for the jumpers: "Breadboard Wire (F-F)" as on the MRA, or another name for the PMG?
8. LED matrix blocks: white sides with a black face and white dots, as published?
9. pmg.glb (167 MB) is over GitHub's limit: keep it on this Mac only (like the STEP) and commit the trimmed `pmg-guide.glb`?

## 8. Files

- `docs/research/pmg/reuse_poses.json`: every pose copy as a pose of the built copy (with its 4x4 and the check), and the Nano's seat and
  extra_parts pose.
- `docs/research/pmg/materials.proposed.json`, `docs/research/pmg/colour-atlas-pmg.proposed.json`: the drafts (section 4).
- `docs/research/pmg/scripts/trim_source.py`, `trim.example.json`: the trimmed-source proposal (section 5).
- `docs/research/pmg/scripts/silkscreen.proposed.py`: the module's print for NAUO78 (2.4).
- Study scripts: `reuse_hdr.py` (header + memory-mapped reads), `reuse_meshlist.py`, `reuse_compare.py` (same-model tests and
  transforms), `reuse_poses.py`, `reuse_cadasio_frame.py` (frame check, Cadasio colours by place), `reuse_solids.py` (solids per mesh),
  `reuse_drafts.py` (writes and checks the drafts).
