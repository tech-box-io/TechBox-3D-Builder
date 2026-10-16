# RCC: what carries over from the MRA, and the colours

Study of 15 Oct 2026 (light work: GLB headers, one read of rcc.glb to count solids, the RCC Cadasio payload through
`tools/cadasio/atlas.py`, Lee's photos). Nothing in the kit folders was changed.

Sources: `RCC Build Instructions/rcc.glb`; `MRA Build Instructions Prototype/` (materials.json, colour-atlas-mra.json,
silkscreen.py, decals.json, mra.glb, usb-mini-b.glb, usb-a-end.glb, js/core.js); the RCC Cadasio payload
`docs/research/rcc/cadasio/raw/19075-rcc_remote_controlled_car.json` and its step pictures; Lee's photos in
`docs/research/rcc/lee_images_2026-10-15/`.

All coordinates are **RCC assembly mm** (rcc.glb x 1000, Y up) unless marked "MRA".

## 0. In short

- **Same CAD models as the MRA:** the KY-023 joysticks, the Nano I/O shield (every component in the same place), the
  controller's Nano (`nano_Varsayılan`, the MRA's NAUO126 model) and the USB Mini-B plug (`Mini USB B` = the MRA's
  `usb-mini-b.glb`, same frame). Their MRA colour rules and atlas entries apply as they are. The I/O shield's
  silkscreen (decals.json) carries over by changing only the four decal headers (origin, u, v): one rigid transform,
  given in 1.3.
- **Different:** the Nano on the car's shield is a *different* Nano model (many small meshes, no pads or print) inside
  the shield's node (`NAUO86`), so the car and the controller would show two different-looking Nanos. Best fixed by
  using the controller's Nano model in both places (1.4).
- **New to the RCC:** FS90R servos (not the MG90S: nothing of the MRA's servo atlas, labels or dot stickers applies),
  wheels, nRF24L01 modules, the controller PCB and its black guards, the L adapter board, the 9 V battery, its snap and
  barrel plug, the BLS-3 servo plug housings.
- **Silkscreen:** the RCC Cadasio project carries the controller PCB's own silkscreen as 67 flat solids
  (`TopSilkscreen~j5tP-*`) in the same frame as our `Board~j5tP` mesh, so every printed item on the controller has an
  exact position (3.1). Lee's photo matches it in layout and in the logo's size to 0.5 mm, but **the small lettering on
  the real board is about 1.47 x the size modelled**. The L adapter has no silkscreen in the CAD or the Cadasio: its print
  is placed from the photo, calibrated on its headers (3.2).
- **The guards:** the published guide shows them **black** in every step picture and the payload has them `#000000` in
  every visible step; the light grey `#e3e3e3` in the digest is only the colour left set after the last step. The colour
  issues the published guide does have are listed in 2.3.

## 1. Parts the RCC shares with the MRA

How compared: the same mesh names, the same bounding box of each mesh *in its own frame* (glTF accessor min/max), and,
for multi-mesh parts, whether one rigid transform carries every MRA mesh node onto an RCC mesh node of the same name.

| RCC part | MRA part | Same model? | Evidence |
|---|---|---|---|
| NAUO12, NAUO13 joysticks (KY-023) | NAUO80, NAUO81 | **Yes** | All 9 meshes (PCB_1, 5x_Ang_Conn_1, Baseplate_1, Case, Rotator-Unit_1, Potentiometer_01/02_1, Tactile-Switch_1, Thumb-Button) same names, same own-frame boxes (to 0.002 mm); one transform maps all 9 (worst 0.0008 mm). |
| NAUO23 Nano I/O shield ("Ensamblaje_Shield_NANO") | NAUO82 | **Yes, the shield** | All 36 shared mesh instances (board, Samtec headers _N/_R/_B/_W, SSW sockets, 47 µF cap, DC jack, diode, regulator, reset, LED, blm21, resistors, caps) map with one transform, worst 0.001 mm. |
| the Nano on the car's shield (node NAUO86 inside NAUO23) | NAUO126 (nano_Varsayılan inside NAUO82) | **No** | The RCC keeps the shield's original "arduino nano" sub-assembly: 30 meshes (`nano-board`, `atmega328`, `ftdi FT232rl`, `MINIUSBSHELL`/`CORE`/`CONTACT`/`SOLDER`, `15pin_header__` x2, `2pin_header__02` x3, resistor packs, crystal, …). It sits in the same seat as the MRA's Nano. |
| NAUO27 controller Nano | NAUO126 | **Yes** | `nano_Varsayılan`, same own-frame box (to 0.001 mm). |
| NAUO16 "Mini USB B" | extra part USB_B (`usb-mini-b.glb`, mesh `MiniUSBB`) | **Yes** | Own box [-47, -3.75, -5.25]..[7, 3.95, 5.25] in both (the plug toward +x). The Cadasio's "Mini USB B" has the same 54.0 x 7.7 x 10.5 box. |
| (none) | extra part USB_A (`usb-a-end.glb`) | not in the RCC CAD | The RCC Cadasio has "USB Cable end" with the same 49.7 x 15.9 x 8.6 box: the same TechBox STEP. |
| NAUO10, NAUO11 nRF24L01 | — | MRA has none | |
| NAUO17, NAUO18 FS90R servos | MG90S (NAUO45/58/66/72) | **No** | Different model: one mesh, 6 solids (case, output spline, a 0.1 mm label sheet 11.2 x 20 mm, three wire stubs). |
| NAUO8, NAUO9 wheels | — | MRA has none | `rim`, `tyre`, one solid each. (NAUO9's box in cad_tree.md, 78.4 mm, is the same 60 mm wheel turned about 18° on its axle.) |

**Tessellation.** The shared meshes are the same CAD bodies but rcc.glb has 55-80 % of the MRA's vertex count for most
of them (nano_Varsayılan 174,569 against 290,945; the Thumb-Button is the other way, 16,637 against 9,579). Flat parts
(the Samtec headers, SSW sockets) are identical. Harmless for colours, since an atlas is matched by solid boxes, but read
the "atlas match" percentages in `model.report.json` after the first build (the rules want 60 % or more).

### 1.1 Colour rules and atlas: what carries over

The MRA's atlas entries are keyed by mesh name and written in each mesh's own frame. For every shared mesh the RCC's
frame is the same, so **the MRA entries can be copied into an RCC atlas unchanged** (`colour-atlas-rcc.json`). I
recommend doing that for the shared parts, rather than reading them again from the RCC Cadasio project, which colours
them differently (pure black joystick PCB and pots, royal-blue shield, teal Nano: see 2.3) and so would undo Lee's MRA
look and rulings. Read the RCC Cadasio (with `tools/cadasio/atlas.py`) only for meshes the MRA lacks, and override with
rules wherever 2.3 lists a problem.

MRA `materials.json` rules, one by one:

| MRA rule | In the RCC |
|---|---|
| `^MiniUSBB$` (black, with a `regions` box making the plug silver) | Reuse with `"match": "^Mini USB B$"`. The box is in the mesh's own frame, which is the same. (The RCC mesh is 2 solids, overmould and plug, so `components` would also do.) |
| `^USBCableend$` | Reuse unchanged if the A end is added as an extra part (1.5). |
| `^(ARA\|TB)_` wood + `"engraving": "ink"` | The RCC wood meshes are named `L1` … `L7`: use `"match": "^L[1-7]$"`, same colour and engraving ink. |
| `^M3x` screws | No screws in the RCC CAD (nor in its Cadasio). Drop. |
| `^MG90S`, `Shoulder`, `^Part[4-7]\^`, omit `(\^ARA_Pathways$\|Cable_JR)` | MRA only. The RCC's CAD cable bodies (NAUO31-NAUO42: `Fitec … Wires 4/5`, `Fitec … Wire Brown/Red/Yellow 4`, `Battery Wires 1`, `Batery Wires 2`) want an omit rule of their own, if the player draws the wires. |
| `^nano_` (with `atlas_colours {"#cccccc": "pin"}`) | Reuse unchanged: catches NAUO27. |
| `^Shield_Arduino` navy, `^Samtec-TLW-` (yellow skin), `^47uf CAP`, `^cap106C`, `^(m7 diode\|smt_resistor\|nano - reg\|blm21\|reset core)`, `^reset shell`, `^led$` | Reuse unchanged: catch the same meshes on NAUO23. The last four also catch the car Nano's own resistors, LEDs, regulator, reset button and caps (same mesh names; the MRA atlas's single colours apply). |
| `^PCB_1`, `^5x_Ang_Conn`, `^Thumb-Button`, `^Tactile-Switch` | Reuse unchanged (joysticks). |
| `own_parts {"NAUO126": …}` | Use `{"NAUO86": "the car's Nano: inside the I/O module (NAUO23) in the CAD, its own part in the guide"}`. The controller's Nano NAUO27 is already a part of its own. |
| `stickers` (motor dots) | Nothing carries over. The two wheel servos are told apart by their row (`LWh` / `RWh` on the adapter). Stickers only if TechBox marks the real servos. |
| `extra_parts` USB_B | Not needed: the Mini-B is in the RCC CAD (NAUO16). |
| `extra_parts` USB_A | Copy `usb-a-end.glb` into the RCC folder and give it a new pose (1.5). |
| `adjust_mm`, `move_engraving` (NAUO46, NAUO17) | MRA only. |
| `decals` | Carry over for the shield with new headers (1.3), plus new decals for the two white boards (section 3). |

### 1.2 The joysticks are tipped 3° in the RCC CAD

Not a colour point, but it came out of the transform: the RCC joysticks are turned 3.0° about the assembly z axis
compared with the MRA's (rotation [[0.9986, 0.0523, 0], [-0.0523, 0.9986, 0], [0, 0, 1]]). The MRA's joystick PCB lies
level (y 118.93..120.54, its 1.61 mm thickness). The RCC's spans y 916.96..920.35: its connector end (x ≈ 725) is
1.8 mm lower than its far end (x ≈ 692). Each joystick sits in a square hole in the controller PCB, its 5-way angled
connector in the L-JS / R-JS socket. This looks like a mate left loose in the CAD. Worth a look in the geometry study;
an `adjust_mm` turn would level them.

### 1.3 Reusing the I/O shield's silkscreen (decals.json)

The shield is the same model with every component in the same place, so one rigid transform takes the MRA assembly to
the RCC assembly for it (checked on all 36 shared mesh nodes, worst 0.001 mm):

    p_RCC = R · p_MRA + t,    R = [[0, 0, -1], [0, 1, 0], [1, 0, 0]]   (a quarter turn about +y),
                              t = [864.282, 812.112, 1268.449] mm
    i.e.  x' = 864.282 - z,   y' = y + 812.112,   z' = x + 1268.449;   directions: u' = R·u, v' = R·v

The items are in picture mm and do not change. Only each decal's `origin`, `u` and `v` change, and the key becomes
`"NAUO23"`:

| decal | origin (RCC) | u | v | size |
|---|---|---|---|---|
| silkscreen top | [691.122, 918.562, 1311.809] | [1, 0, 0] | [0, 0, 1] | [57.2, 53.34] |
| silkscreen underside | [748.322, 916.872, 1365.149] | [0, 0, -1] | [-1, 0, 0] | [53.34, 57.2] |
| capacitor print | [709.437, 924.382, 1352.464] | [1, 0, 0] | [0, 0, 1] | [5.8, 5.8] |
| regulator print | [709.652, 920.162, 1336.509] | [1, 0, 0] | [0, 0, 1] | [6.5, 3.5] |

Checks: the MRA board's top (y 106.43) lands on the RCC board's top (918.544); the origin lands on the RCC board's
corner (x 691.12, z 1311.81). The simplest RCC `silkscreen.py` imports the MRA's item lists and applies R and t to these
headers.

Two cautions:
- **Same board revision?** The CAD is the same. Whether the RCC kit's real shield is the board in Lee's MRA photos is
  for Lee to confirm.
- **The adapter covers part of the print.** The L adapter plugs onto the shield's rows, so part of the top print lies
  under it, which is right. (From the transformed MRA row positions, its underside sockets land on rows AREF (G V S),
  D13/D12 and D11-D8 (S), D6/D5 (G V S), the 3V3/GND pair and D0 (G V S). That is about 0.3-0.45 mm off on the last two,
  because the MRA's row positions are label positions. A point for the wiring study, not checked further.)

### 1.4 The car's Nano

The car's Nano (NAUO86) is a plainer, different model from the controller's: `nano-board` is one navy-able solid with
no pads or print, and its pin headers are single solids (plastic and pins merged). Shown side by side, the student
would see two different Nanos for the same board. Options, for Lee:
- **(a) recommended:** TechBox re-exports the RCC STEP with the car's Nano swapped for the same Nano model as the
  controller's and the MRA's (that is what the MRA's CAD has).
- **(b)** We do it at build time. Omit NAUO86's meshes and add the controller's Nano as an extra part (a small GLB of
  NAUO27's mesh) at the car seat. The seat is exactly **NAUO27's pose moved by [0, 0, +225.000] mm**: the MRA→controller
  and MRA→car-shield transforms share R and differ only by 225.000 mm in z, and both Nanos sit at the same height above
  their boards (both board tops at y 918.54). This needs a small tool step, since `extra_parts` takes a GLB file.
- **(c)** Keep it and colour it with rules: `nano-board` #000f41; `atmega328`, `ftdi FT232rl`, `NANO DIODE`, `MINIUSBCORE`
  #191919; `16mhz crystal - measured`, `MINIUSBSHELL`, `MINI USB CONTACT`/`SOLDER` #a6a9aa; resistor packs: 2 solids,
  body #191919 and ends #a6a9aa; `15pin_header__` / `2pin_header__02`: one solid each, so a `regions` band for the black
  spacer and silver for the pins.

### 1.5 USB cable

- **Mini-B end:** NAUO16, in the CAD, plugged into the controller's Nano: identity rotation, at [687.918, 933.053,
  1112.91], plug along +x with its tip at x 694.92, about 5.5 mm into the socket (the MRA's is 5.2 mm). Rule: the MRA's
  `^MiniUSBB$` renamed (1.1). The RCC Cadasio shows it in SolidWorks' default blue-grey `#cbd2ef`, a colour slip.
- **A end:** copy `usb-a-end.glb` and add it as `extra_parts.USB_A`. In that mesh's own frame the **plug is at x ≈ 134
  (the 12.2 x 4.7 mm shell)** and the cable leaves at x = 184 (checked by slicing the mesh). A pose that lays it flat on
  the table beyond the controller's grips, plug pointing away from the controller (−x), in line with the Nano, with the
  56 mm gap the MRA leaves between plug and A end:

      "USB_A": {"glb": "usb-a-end.glb", "pose": {"t": [401.0, 913.51, 1112.91], "r": [1, 0, 0, -90], "at": [0, 0, 0]}}

  (Own x → +x, own z (thickness) → +y, own y → −z. The cable end is at x 585, the plug tip at x 535.3, the underside at
  the guards' underside, y 913.36.) It is a proposal: the camera and the table layout may want it elsewhere.

## 2. Colour plan for the RCC

### 2.1 Part by part

House library = rulebook section 8. "MRA" = the MRA's materials.json, atlas or Lee's MRA rulings (`_notes.decided`).
**R** in the last column = needs Lee's ruling (listed again in 2.4).

| Part (id) | Meshes / solids | Proposed colour | Basis | R |
|---|---|---|---|---|
| L1-L7 wood (NAUO1-7) | `L1`…`L7`, one solid each | wood `#deb887`, engraving ink `#1e1616` | house; MRA | |
| L1 etching | "FRONT" top left, "L1" top right, as in Lee's drawing | same ink `#1e1616` | Lee 2026-10-15 | |
| Wheels (NAUO8/9) | `rim`, `tyre`, 1 solid each | rim `#1e1616` (black plastic); tyre `#2d2926` (house cable-jacket black, so rim and tyre tell apart) | house; Cadasio has `#191919` / `#272727` | R (real wheel colour) |
| nRF24L01 (NAUO10 car, NAUO11 controller) | one mesh, 40 solids (header body, a thin 11.6 x 8.7 sheet, many small parts) | board `#1e1616` ("black boards"), chip `#191919`, pins `#a6a9aa`, header `#181818`, crystal `#a6a9aa`, by component at build time | house; Cadasio all `#000000` | R (black or green board?) |
| Joysticks (NAUO12/13) | as the MRA | **the MRA atlas as it is**: PCB `#303030` with pads / print `#e4e4e4`, Case `#a6a9aa`, Rotator `#808080`, Thumb-Button and Baseplate `#303030`, connector pins `#a6a9aa` | MRA | |
| 9 V battery (NAUO14) | 5 solids: 2 snap terminals, body in 2-3 pieces | body dark grey `#5f5f5f` (so it reads against the black snap), terminals `#a6a9aa` | Cadasio's end-state grey; no house colour | R (which battery? is it in the kit?) |
| 9 V snap (NAUO15 "DC_Adaptor") | 5 solids: housing 25.1 x 4.2 x 12, snaps, two lead stubs | housing `#1e1616`, snaps `#a6a9aa`, stubs red `#ef3340` / black `#2d2926` | house; Cadasio `#000000` | |
| Mini USB B (NAUO16) | 2 solids | overmould `#1e1616`, plug `#a6a9aa` | MRA rule | |
| USB A end (extra part) | as the MRA | the MRA rule (black, silver shell, white tongue) | MRA | |
| FS90R servos (NAUO17/18) | 6 solids: case, spline, label sheet, 3 lead stubs | case: **blue `#0073b3` (Cadasio) or black `#2d2926` (MRA `servo_body`)**; spline white `#f5f5f6`; label (white or blue?); stubs as the leads | see 2.2 | R |
| BLS-3 servo plugs (NAUO19-22) | 4 solids: housing + 3 contacts | housing `#404040` (the MRA servo plugs' colour, `Copy of JR-3` in the MRA atlas) or `#1e1616` (rulebook: Dupont housings); contacts `#a6a9aa` | MRA / house | R (match the MRA's plugs?) |
| I/O shield (NAUO23) | as the MRA | **MRA rules as they are**: board navy `#000f41` (Lee 2026-10-14), every header base yellow `#ffff80` with pins (Lee 2026-10-13), SSW sockets `#181818`, DC jack body `#181818` / pads silver, 47 µF cap silver can (MRA "unconfirmed") | MRA | |
| Car Nano (NAUO86) | 30 meshes | as the controller's if swapped (1.4 a/b); else the rules in 1.4 (c) | rulebook: Nano board `#000f41` | R (a/b/c) |
| Controller guards (NAUO24/25) | 1 solid each | black plastic `#1e1616` | Lee's photo; house | |
| L adapter board (NAUO26) `Board~hwXZ` | 1 solid | white `#f4f4f4` | photo; no house colour for a white board (see note) | R (confirm white) |
| L adapter headers | U1, U2 (3P male, 4 solids each); U3 (2x4 female, 9); underside sockets 2P x2, 3P x2, 4P, 6P (3-7 solids each) | bodies `#181818` (rulebook socket strips), pins `#a6a9aa` (rank 1 = body, the rest pins) | house; photo | R (gold pins? see 2.2) |
| L adapter C1 (470 µF) | `CAP-SMD…~hwXZ`, **1 solid** | can `#a6a9aa`, base `#1e1616` by a `regions` height band; top print and its dark band as a decal (3.3) | photo; Cadasio `#323232` all over | |
| Controller Nano (NAUO27) | as the MRA | MRA rule and atlas as they are | MRA | |
| Barrel plug (NAUO28 and NAUO29: two poses of one plug) | `Component3` barrel, `Component4` grip, `Insolation`, `eBom-FreeParts`, `Wires` (2 stubs) | barrel and inner part `#a6a9aa`, grip and insulator `#1e1616`, stubs red `#ef3340` / black `#2d2926` | Cadasio (same solids); house leads | |
| Controller PCB (NAUO30) `Board~j5tP` | 1 solid, **0.09 mm thick** in the CAD | white `#f4f4f4` | photo; Cadasio `#f4f4f4` | R (confirm white) |
| Controller `BottomCopper~j5tP-43` | 1 solid filling the 2.54 mm under the board | the board's white | Cadasio `#ebebeb` | |
| Controller sockets | H1/H2 (15P), NRF (2x4, one solid), L-JS/R-JS (10P right-angle, 11 solids) | bodies `#181818`, pins `#a6a9aa` | house | R (gold pins?) |
| Controller C1 (470 µF) | 1 solid | as the adapter's C1 | photo | |
| Servo leads (player-drawn) | brown / red / signal | brown `#975100`, red `#bd291f` (the MRA's servo-lead colours), signal yellow `#ffd500` (the CAD calls it Yellow; Cadasio `#ffd500`) | MRA; CAD; Cadasio | R (yellow or orange?) |
| Battery leads (player-drawn) | red / black | red `#ef3340`, black `#2d2926` | house pre-wired leads | |

**Note on the white boards.** The player shades with linear multipliers (lit 1.38, shaded 0.9, js/core.js
`TONE_LIT`/`TONE_SHADE`). Anything near white clips to pure white on a lit face, so a white board's
top will read as page-white and be outlined only by its black edges. That is what the photo and the Cadasio both look
like: the black guards frame the controller, and the navy shield frames the adapter. A base colour dark enough to stay below
white when lit (somewhere between `#b9` and `#dc` grey, depending on whether the multipliers act on linear or sRGB values)
would read as a grey board, not a white one. So keep it white (`#f4f4f4`) and let the edges
carry it. On the boards' edges the photos show the cream FR4 core. Optional; the MRA boards don't do it.

New palette entries this implies: `pcb_white #f4f4f4`, `silk_black #1e1616` (decal ink on the white boards),
`lead_yellow #ffd500`, `tyre #2d2926`, `battery_grey #5f5f5f`, and `servo_fs90r` (blue `#0073b3` or the existing
`servo_body #2d2926`, after Lee's ruling).

### 2.2 Points the photos and the products raise

- **FS90R colour.** The Cadasio shows them blue (`#0073b3` / `#00639a`, with `#1aa2ef` on the other servo model in the
  project), and the published step pictures show bright blue servos. I could not confirm the real colour: no text source
  states it ([Pololu #2820](https://www.pololu.com/product/2820), [Pololu FAQ](https://www.pololu.com/product/2820/faqs),
  [Pololu blog](https://www.pololu.com/blog/356/new-product-feetech-fs90r-micro-continuous-rotation-servo),
  [Botland](https://botland.com.pl/en/servo-continuous-operation-360/4689-servo-feetech-fs90r-micro-continuous-work-360-degrees.html),
  [Rapid](https://rapidonline.com/feetech-fs90r-analog-micro-servo-continuous-rotation-559636), and others: none
  describes the case in words, and I could not view their photos here). From memory, Feetech's own FS90R (as Pololu and
  Adafruit sell it) is black with a white label, and blue "FS90R"-style servos are clones. That is unverified: **Lee to
  rule from the kit's servo.** The CAD has a separate 0.1 mm label sheet, so a label colour is needed too.
- **Gold pins.** Lee's controller photo shows **gold** pins on the L-JS / R-JS right-angle sockets, and the adapter's U1 /
  U2 pins look gold-tan too. The rulebook and Lee's MRA ruling say pins are silver `#a6a9aa`. I propose silver, for one
  look across kits, unless Lee wants gold (the Cadasio's `#d3aa21`).
- **Plain pads on the adapter are not missing parts.** The empty-looking pads in the adapter photo are the solder joints
  of its **underside** sockets (2P x2, 3P x2, 4P, 6P), which the CAD has: they hang below the board (y 920.08..931.78
  against the board at 928.58..930.18) and plug onto the shield's rows. Every pad in the photo lines up with one of
  their pins (3.2).
- **The capacitors.** On both boards C1 is an RVT 470 µF / 10 V can on a black base. On the controller its dark polarity
  band is on the −z side; on the adapter, on the −x side. The CAD body is one solid; the Cadasio paints it all
  `#323232`.

### 2.3 Colour issues in the published RCC guide (for Lee)

Read from the payload's per-solid colours (the colour each solid has most often while visible) and the step pictures:

1. I/O shield board royal blue (house `#224bbe`-like). Lee's MRA ruling is navy `#000f41`.
2. Both Nanos dark teal (`#002e37` / `#002d37`), with the controller Nano's pads and print left at SolidWorks grey. The
   house colour is `#000f41`.
3. Mini-B plug in SolidWorks' default `#cbd2ef`: the CAD-default slip listed in the rulebook, appendix B.
4. KY-023 PCB, pots and nRF24L01 pure `#000000`, so they read as silhouettes. (The MRA uses `#303030` for the joystick
   board.)
5. Adapter header pins gold (`#f2c22e`, `#d3aa21`) and C1 a uniform `#323232`.
6. The controller's silkscreen solids are coloured `#ffffff` in the payload, on a `#f4f4f4` board (Lee's photo: black print).
   The step pictures still show the lettering dark, presumably by its black edge lines, so this may not show as a fault.
7. BLS-3 contacts flip between white `#eeeeee` and tan `#f6e099` from step to step (24 overrides each).
8. Not an issue: the guards are black in the published guide (see 0).

### 2.4 Rulings needed from Lee

1. FS90R case colour (blue as published, or black), and its label's colour.
2. Servo lead signal wire: yellow (as the CAD names it) or orange.
3. Wheel colour (published: black).
4. nRF24L01 board colour (black as published, or green).
5. 9 V battery: which one (for its colour), and whether it is in the kit.
6. BLS-3 plug housings: `#404040` like the MRA's servo plugs, or `#1e1616`.
7. Header pins: silver (house) or gold (as on the real controller).
8. The car's Nano: (a) re-export with the common Nano model, (b) swap at build time, or (c) keep and colour (1.4).
9. Confirm the RCC kit's I/O shield is the board in the MRA photos, so its print carries over (1.3).
10. Confirm the two white boards stay white `#f4f4f4`, outlined by their edges (2.1 note).

## 3. Silkscreen on the two RCC boards (input for an RCC `silkscreen.py`)

Ink: black on white (`silk_black #1e1616`, or `#000000` like the breadboard legends). Decal frames that read like Lee's
photos (both satisfy the player's "seen from v x u" rule, v x u = +y):

| board | key | origin (photo's top-left) | u (photo right) | v (photo down) | size | picture coords |
|---|---|---|---|---|---|---|
| controller top | NAUO30 | [744.46, 918.56, 1046.21] | [0, 0, 1] | [-1, 0, 0] | [149.71, 87.0] | (u, v) = (z − 1046.21, 744.46 − x) |
| adapter top | NAUO26 | [692.67, 930.20, 1348.56] | [0, 0, -1] | [1, 0, 0] | [33.80, 57.41] | (u, v) = (1348.56 − z, x − 692.67) |
| controller C1 top | NAUO30 | can centre (702.02, 1130.18), y 926.26 | [0, 0, 1] | [-1, 0, 0] | 6.3 circle | |
| adapter C1 top | NAUO26 | can centre (743.66, 1331.01), y 937.90 | [0, 0, -1] | [1, 0, 0] | 6.3 circle | |

(The adapter's u and v are the MRA top decal's u and v.) Board tops: controller y 918.54 (the 0.09 mm `Board~j5tP`
sheet), adapter y 930.18.

**Orientation of the photos in the CAD.**
- **Controller photo:** up = +x (the L-JS / R-JS edge), right = +z (the right handle). Checked: L-JS socket at z
  1078.2..1091.5 (photo left), H2 at z 1105.29 left of H1 at 1120.53, the NRF socket right of H1, the USB plug at the
  bottom (−x).
- **Adapter photo:** down = +x (U3 at the bottom, x 746.3), left = +z (the short arm). Checked: U1 x 717.5 above U2 x
  730.2, C1 at (743.66, 1331.01) left of U3.

### 3.1 Controller PCB (NAUO30): exact positions from the CAD, sizes from the photo

The RCC Cadasio project models the board's top silkscreen as 67 flat solids (`TopSilkscreen~j5tP-*`), and its
`Board~j5tP` box ([-1.801, 54.241, 0]..[147.912, 141.244, 0.09]) is our mesh's own box (to 0.003 mm). Mapped with our
`Board~j5tP` node matrix (own x → assembly z, own y → assembly x, own z → assembly y, t = [603.216, 918.445,
1048.013]), every item lands where the photo has it. **Our rcc.glb has no TopSilkscreen or TopCopper meshes** (the
STEP or its conversion lost those surface bodies), so the decals are the only way to show them.

Photo calibration (on the H1-H2 spacing, the NRF socket and C1; about 7.05 px/mm, close to orthographic): the TECHBOX
wordmark measures z 1161.4..1189.3, x 681.4..687.3 in the photo against z 1161.05..1188.70, x 681.73..687.92 in the CAD,
which agree to 0.5 mm. **But every small label on the real board is about 1.47 x larger than in the CAD** (L-JS 4.0 mm
long against 2.74; NRF24L01 7.9 against 5.39; USB 5.3 against 3.56; CONTROLLER 18.9 against 12.5). The board was
evidently made with bigger text than this model has. Use the photo's sizes, anchored as the photo shows (below).

Text reads +z (left to right in the photo) with letter tops toward +x, unless stated otherwise. "h" = letter height.

| # | Item | CAD position (exact) | On the real board (photo) | Anchor for the decal |
|---|---|---|---|---|
| 1 | Outline of the L-JS socket (2 rects) | x 727.56..734.60 and 725.84..727.54, z 1078.06..1091.63 | mostly under the socket; a corner peeks out at its +z end | rect(s) as in the CAD, line about 0.15 |
| 2 | "L-JS" | z 1092.20..1094.94, x 733.34..734.17 (h 0.81) | z 1092.9..1096.9, centre x 732.8, h ≈ 1.2 | left-aligned just past the outline's +z end (z ≈ 1092.2), centre x ≈ 733.3, h 1.2 |
| 3 | Outline of the R-JS socket | x 727.43..734.48 and 725.71..727.41, z 1150.83..1164.40 | | as in the CAD |
| 4 | "R-JS" | z 1146.31..1149.11, x 733.21..734.05 | z 1146.4..1150.7, x ≈ 733.0, h ≈ 1.4 | right-aligned to end just short of the outline (z ≈ 1150.6), centre x ≈ 733.4, h 1.2 |
| 5 | Outline of H2 (15-way Nano socket) | x 693.41..732.23, z 1103.91..1106.67 | under the socket | rect |
| 6 | "H2" | z 1104.52..1105.85, x 732.97..733.78 | centre z ≈ 1105.9, x ≈ 732.6 | centred on the socket axis (z 1105.29), just beyond its +x end (x ≈ 733.4), h 1.2 |
| 7 | Outline of H1 | x 693.41..732.23, z 1119.15..1121.91 | | rect |
| 8 | "H1" | z 1119.89..1120.94, x 732.97..733.78 | centre z ≈ 1121.0 | centred on z 1120.53, x ≈ 733.4, h 1.2 |
| 9 | "NANO BOARD" (line 1) | z 1113.81..1115.23 (h 1.42), x 721.97 → 709.00 | x 721.6 → 702.9, centre z 1115.0, h ≈ 2.1 | **reads toward −x** (top to bottom in the photo), letter tops toward +z, starting at x ≈ 721.8, centre z ≈ 1114.9, h 2.1 (rot 90 in a decal whose v is −x) |
| 10 | "CONTROLLER" (line 2) | z 1110.51..1111.93, x 722.09 → 709.58 | x 721.6 → 702.7, centre z 1111.5 | as line 1, centre z ≈ 1111.4. Both lines lie between H2 and H1, under the Nano once it is fitted. |
| 11 | Outline of the NRF24L01 socket | x 709.26..714.60, z 1125.10..1136.03 | | rect |
| 12 | "NRF24L01" | z 1126.37..1131.76, x 707.57..708.38 (h 0.81) | z 1126.6..1134.5, x 706.9..708.1, h ≈ 1.2 | centred under the socket (z 1130.57), x ≈ 707.6, h 1.2 |
| 13 | Outline of C1 (two brackets, open at the terminals) | x 702.63..705.48 and 698.57..701.42, z 1126.73..1133.64 | under the cap's base | two bracket shapes, or two rects |
| 14 | Polarity marks inside C1's outline | "−" z 1127.08..1127.88, x 703.44..703.64; "+" z 1132.49..1133.29, x 702.88..704.21 | hidden by the cap | optional |
| 15 | "C1" | z 1133.35..1134.43, x 705.03..705.84 | z 1133.5..1135.2, x 704.3..705.4, h ≈ 1.2 | left-aligned at z ≈ 1133.4, centre x ≈ 705.2, beside the cap base's +x / +z corner |
| 16 | "USB" | z 1110.37..1113.93, x 691.24..692.65 (h 1.41) | z 1110.5..1115.8, x ≈ 692.4 (half under the guard rim) | centred z ≈ 1112.9 (the Nano's axis), x ≈ 692.0, h 2.1: below the −x ends of H1 / H2 |
| 17 | TechBox icon (bulb in a half gear, zig-zag arrow, three bars of the screw base) | 5 solids: gear arc x 684.70..688.66, z 1155.04..1159.34; bulb x 683.10..687.45, z 1156.11..1159.83; bars at x 682.50..682.98 (2.31 wide), 681.95..682.41 (1.86), 681.45..681.85 (1.17), centred z ≈ 1157.7 | same | as in the CAD (the photo agrees). Bulb top toward +x. |
| 18 | "TECHBOX" wordmark (bold condensed caps) | x 681.86..687.80 (cap height 5.94; C, O 6.19); T 1161.05..1164.45, E 1164.92..1167.90, C 1168.41..1172.09, H 1172.63..1176.21, B 1176.99..1180.60, O 1181.12..1184.70, X 1184.97..1188.70 | same | as in the CAD. Below the right-hand joystick hole, on the right grip. |
| 19 | C1 can top: "470" / "10V" / "RVT" + dark band | — | three lines upright (reading +z, tops +x), line pitch ≈ 1.4, h ≈ 1.1, centred on the can; dark crescent on the can's −z side, from its edge to about z 1128.0 | a decal like the MRA's "capacitor print" (circle + band + 3 lines) |

Not print: the faint lines on the board (in the photo: a chamfered outline round the Nano and diagonals toward the
joystick sockets) are copper traces under the white mask. Leave them out. No underside photo, and no bottom silkscreen
in the Cadasio, so no underside decal.

### 3.2 L adapter board (NAUO26): from the photo

Neither the CAD nor the Cadasio has print for this board. Positions are measured on Lee's photo, calibrated on features
the CAD has: U1 / U2 centres (x 717.5 / 730.2), the underside sockets' pads, U3 and C1. Scale about 16.5 px/mm; the
pads land within 0.3 mm. Mapping: x = 694.64 + (Y − 268) / 16.45, z = 1320.97 + (1160 − X) / 16.5 (photo pixels). Feature
positions from the CAD: U1 (3P male) x 716.23..718.77, z 1317.16..1324.78, pins at z 1318.43 / 1320.97 / 1323.51; U2
the same at x 728.93..731.47; U3 (2x4) x 743.83..748.83, z 1315.69..1326.26; C1 base x 740.16..747.16, z 1327.71..1334.31,
can centre (743.66, 1331.01); board x 692.67..750.08, z 1314.76..1348.56 (an L: the long arm along x at z
1314.8..~1327.5, the short arm along z at x ~736..750).

| # | Item | Where (assembly mm) | Notes |
|---|---|---|---|
| 1 | "U1" | centre z ≈ 1325.5, x ≈ 716.3 | at U1's outline's +z / −x corner, h ≈ 0.8 |
| 2 | Outline of U1 | z 1317.0..1324.8, x 716.0..718.7 | rect hugging the header body, line about 0.15 |
| 3 | **"LWh"** | centre z ≈ 1316.1, x ≈ 717.2 (length ≈ 3.5, along x) | between U1 and the board's −z edge; **reads toward −x** (bottom to top in the photo), letter tops toward +z (`rot: -90` in the adapter decal); h ≈ 1.3 |
| 4 | **"S V G"** under U1 | centre x ≈ 719.9; S at z 1323.5, V at 1320.97, G at 1318.4 | each centred on its pin, on U1's +x side; upright in the photo (tops toward −x), h ≈ 1.6. **S is the +z pin, G the −z pin.** |
| 5 | "U2" | centre z ≈ 1325.7, x ≈ 729.2 | as U1 |
| 6 | Outline of U2 | z 1317.0..1324.8, x 728.8..731.6 | |
| 7 | **"RWh"** | centre z ≈ 1316.1, x ≈ 730.1 | as LWh |
| 8 | **"S V G"** under U2 | centre x ≈ 732.8; same z as item 4 | |
| 9 | "U3" | centre z ≈ 1316.1, x ≈ 743.1 | just −x of U3's top edge, above its −z end, h ≈ 0.8 |
| 10 | Outline of U3 | z 1315.6..1326.2, x 743.6..749.1 | |
| 11 | TechBox icon (no wordmark), black line art | z 1335.8..1341.8, x 739.1..748.3 (about 6.0 x 9.1) | on the short arm, +z of C1; bulb top toward −x, gear ring on its −x / +z side |
| 12 | "C1" | centre z ≈ 1329.3, x ≈ 748.7 | just +x of C1's base, near its −z end, h ≈ 0.8 |
| 13 | C1 can top: "470" / "10V" / "RVT" + dark band | lines at z ≈ 1329.5 / 1330.8 / 1332.3, spanning x 742.6..745.5 | **reads toward +x** (top to bottom in the photo), letter tops toward −z (`rot: 90`), "470" the −z line; h ≈ 1.05, line pitch ≈ 1.4; dark crescent on the can's −x side, from its edge (x 740.5) to about x 741.7 |
| 14 | (optional) pads: round, with one square per socket | underside 3P at x 694.64, z 1318.43 / 1320.97 / 1323.51 (square at 1318.43); 2P at z 1323.51, x 699.71 / 702.25 (square at 702.25); 4P at z 1323.51, x 707.34 / 709.88 / 712.42 / 714.96 (square at 714.96); 2x3 at x 722.58 / 725.12 × z 1318.43 / 1320.97 / 1323.51 (square at x 725.12, z 1318.43); 2P at x 740.36, z 1343.19 / 1345.73 (square at 1345.73); 3P at x 740.36, z 1318.43 / 1320.97 / 1323.51 (square at 1318.43) | silver solder joints, about 1.7 mm across, with the pin tips (the CAD's pins) poking 1.6 mm up through them. Metal, not ink: a `circle` / `fill` in `#a6a9aa` if wanted. |

Not print: two faint diagonal lines near the top of the long arm are traces under the mask.

### 3.3 What the decal format lacks

`js/core.js` `addDecal` draws `text` (Arial, any weight), `rect`, `fill` and `circle`. Two things here need more:
- **The TechBox logo** (the icon on both boards, and the wordmark on the controller) is a picture, and the wordmark is a
  bold condensed face that Arial Bold will not match. Needs either an `image` item (a small black-on-transparent PNG
  cut from the kit's `logo.webp`, whose icon and wordmark are the same artwork in white on blue) or `path` items.
- **The C1 brackets and the capacitor's dark crescent** want a polygon / arc fill (the MRA's capacitor decal used a
  circle and a ring only).

Both are small additions to `addDecal`, but they are player changes, so they are for whoever owns the player.
