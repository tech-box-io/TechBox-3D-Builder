# LSM: Lee's STEP files, what is wrong with them, and how the model was put back together (19 Oct 2026)

The kit folder `LSM Build Instructions/` came with four SolidWorks 2026 STEP exports (checksums in `cad-sources.sha256`):

| file | what it holds |
|---|---|
| `LSM Lab - Full Build.STEP` (42 MB, 13 Oct) | An old copy of the assembly behind TechBox's published Cadasio guide ("LSM Lab - Chapter 2"): the breadboard, capacitor, resistors, D1, D2 (in its "floating" pose only), D3, the four D11, one LED matrix (lying beside the base), the button, the right-angle Mini-B plug, the backing sheet, many loose Dupont caps and wire bodies in posed copies. **No Nano, no D4 - D10, no stems.** Six sub-assemblies point at files that are not in the export (orphan roots `Part13^`, `Part3^Wire Cables Split`, `Part8^`, `Part11^`, `Part12^`, `Copy of Part3^`). |
| `LSM Lab 1-2.STEP` (41 MB, 13 Oct) | The same for Parts 1 and 2 (electronics only). Not used. |
| `LSM_WoodSteps.STEP` (6.7 MB, 18 Oct) | One of each wood part (D3 twice, a second D2 variant `LSM_Side3_r2(1)`), **laid out loose**, not assembled. One D9, one D10, one D11 (the build has 2, 1 and 4). |
| `LSM_Electronics.STEP` (58 MB, 18 Oct) | One of each electronic part, **laid out loose**: LED matrix, breadboard, resistors (with straight and bent legs), capacitor, three M-F jumper wires, a Nano (a plainer model), a push button with its leads merged into one body, and a USB-C right-angle cable (not the kit's Mini-B). |

The 64 acrylic LED stems are in none of them.

## What made the repair possible

TechBox's published Cadasio guide (`docs/research/lsm/cadasio/raw/...json`, read from instructions.online) carries its whole assembly:
every part's placement, in the same coordinates as Lee's STEP (the breadboard's origin is at x 680.47, y 867.65, z 1204.74 in both),
and each part's own bounding box. Every part in Lee's two loose files has the same own frame as Cadasio's copy of it: the boxes agree
to 0.00 - 0.04 mm (wood, LED matrix, breadboard, resistors, capacitor, caps, USB A end). So each part is taken from Lee's files in its
own frame and placed with Cadasio's matrix.

`LSM Build Instructions/assemble.py` does this and writes `lsm.glb` (98 parts, one assembly node, the ids `guide.py` uses) and
`assembly-report.json` (each part's source, placement and box). Its inputs are the three STEPs converted with `tools/step_to_glb.py`
(`lsm-wood.glb`, `lsm-electronics.glb`, `lsm-fullbuild-raw.glb`, kept out of git) and two MRA files.

## Part by part

| part (id) | from | placed |
|---|---|---|
| D1 - D11 (`D1` ... `D11_D`) | `lsm-wood.glb`, its plate only (Cadasio's black sheets lying in the engraving pockets dropped: `build_model.py` inks the pockets) | Cadasio's matrix. D2 = `LSM_Side3_r2-1` (seated; `-2` is its floating pose). D6 = `LSM_Lens_Bottom-3`. |
| breadboard, backing sheet, LED matrix | `lsm-electronics.glb` / `lsm-fullbuild-raw.glb` | Cadasio's (the matrix `8x8 LED-4`, 0.2 mm across as Cadasio shows it seated) |
| Nano Board | the MRA's model (`mra.glb` NAUO126), Lee's rule of 19 Oct 2026 | Into rows c and g, columns 2 - 16, USB socket at column 16, the header's plastic on the board (see below) |
| resistors, capacitor | `lsm-electronics.glb` | Cadasio's turn, moved so the legs stand in h3/h16, a11/a19, j2/j3. A resistor's legs are drawn as wires (bent in Steps 4 and 7). |
| push button, its nut | `lsm-fullbuild-raw.glb` `Push button` (the electronics file merges the leads into the body); its 8 solids split, the 21 x 18 x 1.5 mm one is the nut | Flange against D2's outer face, nut against its inner face |
| right-angle Mini-B plug | `lsm-fullbuild-raw.glb` `USB Right Angle` (kept: the MRA's plug is straight, and a straight plug would run into the push button) | Fully into the Nano's socket |
| USB A end | the MRA's `usb-a-end.glb` (the same model as the LSM's `USB Cable end`) | On the table outside D4 (Cadasio has it 24 mm under the table) |
| Dupont caps | `Wire Cap V2` (male, pin) / `Wire Cap` (female, the MRA's model) | Male straight in i2, i3, b19, j5, j16; female on the matrix's three pins |
| LED stems | drawn: a 3.175 x 66.675 x 3.175 mm rod (Cadasio's box for `LSM_Stem`) | Cadasio's 64 placements |

## Where the published assembly was put right (all under 1.4 mm)

| what | Cadasio | here | why |
|---|---|---|---|
| Nano Board | its CAD seat, then moved -2.3 x, +2.0 y in the steps | rows c / g, plastic on the board | Part 1's own label "Pin D12 - c16"; then every wire and component lands on the right Nano pin (D7 through the 330 Ω resistor to b19, 5V at j5, D13 at j16 with the 12 kΩ to GND, VIN / GND at i2 / i3 and the capacitor) |
| D8 | 0.81 mm towards D3 | in line with D6 and D7 | D6 and D7 fit exactly between D3 and D2; D8 sits on the same posts |
| LED stems | 0.19 mm across, 0.77 mm along from the shelves' holes | in the middle of D6/D7's and D8's 3.3 mm holes | |
| D11_C, D11_D | 0.6 and 1.0 mm low | the same height as the other two | all four stand on D1 |
| D4, D5 | 0.19 / 0.22 mm along z | centred on the D2 / D3 tabs | D2's 3 mm tabs bound on the edges of their 3 mm slots (D3 is 3.17 mm thick in the CAD, in 3 mm slots) |
| female caps | 1.38 mm beside the matrix's pins, 0.56 mm low | on the pins | |
| button, nut | flange 0.46 mm off D2, nut 0.75 mm off | both against D2 | |

Cadasio's own oddities left alone: D10's pose on the held matrix (Cadasio turns it 90 degrees; here it keeps its seated relation to the
matrix, as the published pictures show it), five pose copies of the LED matrix and four of D10 (one part each here, moved by the guide),
the stray backing sheet that reappears inside the box at 28c.

## The breadboard

Rows a - j across x (a at x 624.50, j at 652.62), columns 1 - 30 along z (column 1 at z 1167.91), read from the breadboard mesh's hole
pockets with Cadasio's placement; the published guide's caps fall on b19, j5 and j16 to 0.03 mm.
