# RCC: materials.json, first draft (15 Oct 2026)

Written: `RCC Build Instructions/materials.json`, `RCC Build Instructions/colour-atlas-rcc.json`, and
`RCC Build Instructions/usb-a-end.glb` (a byte-for-byte copy of the MRA's). Nothing was built: `build_model.py`, `guide.py`
and `bundle.py` were not run. The checks below copy `build_model.py`'s own rule, component, region and atlas logic and run
it on `rcc.glb` mesh by mesh. They do not simplify the meshes or work out skins. The scripts were throwaway, kept in the
session scratchpad.

## 1. What the file sets

| Key | Value | Notes |
|---|---|---|
| `source`, `source_scale_to_mm` | `rcc.glb`, 1000 | as the MRA |
| `palette` | the MRA's palette plus `pcb_white #f4f4f4`, `ic_black #191919`, `plug_grey #404040`, `servo_fs90r #0073b3`, `servo_fs90r_label #00639a`, `servo_fs90r_spline #c6c1bc`, `tyre #2d2926`, `battery_grey #5f5f5f`, `lead_yellow #ffd500`, `silk_black #1e1616` | The FS90R colours go through palette names (via `atlas_colours`), so Lee's ruling on the motor colour is a change to one palette entry. |
| `defaults` | as the MRA (`edge_angle` 40, `simplify_mm` 0.04) | |
| `rules` | 38 rules (section 2) | |
| `atlas` | `colour-atlas-rcc.json` (section 3) | |
| `own_parts` | `NAUO86`, the car's Nano (inside NAUO23) | The node exists once, under NAUO23. |
| `extra_parts` | `USB_A`: `usb-a-end.glb`, pose `{"t": [401.0, 913.51, 1112.91], "r": [1, 0, 0, -90]}` | The pose is the one `reuse_and_colours.md` 1.5 proposes. It lies flat on the controller's table (underside y 913.36, the same as the guards' underside), in line with the Nano (z 1104.96..1120.86). The plug tip is at x 535.3, pointing away from the controller, and the cable end at x 585.0. That leaves the MRA's 56 mm gap to the Mini-B's cable end (x 640.92). The guards start at x 653.4, so nothing overlaps. |
| `move_engraving` | `NAUO1: {"by": [0, 0, 0], "turn": 180}` | L1's code is turned half round in place, as `cad_study.md` 2.5 says (its other option, `by [-0.7, 0, -1.0]`, would also shift it by up to 1 mm). There was no decals report when I finished. If the decals agent decides to draw "L1" itself, this key changes to match. |
| `decals` | `"decals.json"` | **That file does not exist yet.** `build_model.py` loads it without checking that it is there, so the first build fails until the decals agent has written it. |
| `adjust_mm`, `stickers` | not set | See section 5. |
| `_notes` | `unconfirmed` (14 items), `decided` (8), `adjusted`, `wires`, `car_nano`, `extra_parts`, `not_carried_over` | |

## 2. Colours by part

"Atlas MRA" means the MRA atlas entry, copied unchanged. "Atlas RCC" means TechBox's published RCC Cadasio project, read with
`tools/cadasio/atlas.py`. **U** means the colour is unconfirmed and waits on Lee (`_notes.unconfirmed`).

| Part (ids) | Rule | Colours | Source |
|---|---|---|---|
| L1-L7 (NAUO1-7) | `^L[1-7]$` | wood `#deb887`, engraving ink `#1e1616` | house |
| Wheels (NAUO8/9) | `^rim$`, `^tyre$` | rim `#1e1616`, tyre `#2d2926` (outlined) | house; the published guide has them black too. U |
| nRF24L01 (NAUO10/11) | `^RadioFrequency…` | Board and the header plastic under it (one solid) and the 0.1 mm antenna sheet: black `#1e1616`. The 4 x 4 mm chip: `#191919`. The 0.8 x 0.8 x 1.5 mm parts: tan `#a5936d`. The crystal, pins and pads: silver. The parts are picked by solid size, not rank. | house; the published model is one black solid. U |
| Joysticks (NAUO12/13) | MRA rules | MRA atlas: board `#303030` with pads and print `#e4e4e4`, case silver, rotator `#808080`, thumb button `#303030` | atlas MRA, 100 % match |
| 9 V battery (NAUO14) | `^9V-battery$` | Body (three pieces) grey `#5f5f5f`; the two terminals (ranks 2 and 3) silver | report 2.1. U |
| Battery clip (NAUO15) | `^DC_Adaptor$` | Housing black. Snaps (ranks 1 and 2) silver. Lead stubs `#2d2926`, except the stub at own z < 0, which is red `#ef3340` (a `regions` box). | Traced (section 4). U |
| Mini-B (NAUO16) | `^Mini USB B$` | The MRA rule renamed: overmould black, plug silver (9 % of faces) | MRA |
| FS90R (NAUO17/18) | `^Fitec FS90R` | Case `#0073b3`, label `#00639a`, spline `#c6c1bc`. The lead stubs are brown `#975100`, red `#bd291f` and yellow `#ffd500`, the colours of the leads the player will draw. | atlas RCC, 100 % (6 solids against 6, the boxes the same in the mesh's own frame). U |
| Servo plugs BLS-3 (NAUO19-22) | `^BLS-3` | Housing `#404040`, the three contacts silver | the MRA's servo plugs. U |
| I/O module (NAUO23) | MRA rules | Board navy `#000f41`. Header bases yellow `#ffff80` (skin). SSW sockets `#181818`. The 47 µF capacitor a silver can. Jack, regulator, LEDs, caps and resistors from the MRA atlas. | MRA, Lee's rulings |
| Car Nano (NAUO86) | 7 rules, `^nano-board$` to `^(15pin_header__…)$` | Board `#000f41`. The ATmega and FT232 bodies `#191919`, with their legs silver (regions beyond 3.95 / 3.35 mm). Diode and USB insert `#191919`. Crystal, USB shell, contacts and solder pads silver. The resistor arrays black with silver ends. The header spacers black (regions, own y 0..2.5) with silver pins. Regulator, LEDs, caps, reset button and resistors from the MRA atlas (same names and geometry). | Option (c) in report 1.4. U |
| Guards (NAUO24/25) | `^2024-RCC_ControllerHandles` | black `#1e1616` | Lee's photo; house |
| Adapter (NAUO26) and controller (NAUO30) boards | `^(Board~j5tP\|BottomCopper~j5tP\|Board~hwXZ)` | white `#f4f4f4` (the controller's 0.09 mm sheet and its 2.54 mm slab alike) | photo. U |
| Both C1 | `^CAP-SMD_BD6\.3` | A silver can on a black base (regions: own z below 2.05, where the base ends at 1.9 and the can starts at 2.16). The terminal tabs beyond the base are silver. | photo |
| Every header on both boards | `^HDR-TH_` | Plastic (rank 0) `#181818`, pins silver. The controller's radio socket is a single solid, so it is all black. | house. Pins silver (U: the photo shows gold) |
| Controller Nano (NAUO27) | `^nano_` | MRA rule and atlas | MRA, 100 % |
| Barrel plug (NAUO28/29) | 4 rules | Grip and tip ring black; sleeve and inner part silver. Stubs: the published red and black (atlas `Wires`) swapped to `#ef3340` / `#2d2926`. | atlas RCC + house |
| Lead bodies NAUO31-42 | `^(Fitec (Right\|Left) Wires? \|Batt?ery Wires )` | `omit` (12 meshes; the BLS-3 housings and barrel plugs are kept) | |

## 3. colour-atlas-rcc.json

- **From the MRA atlas, unchanged:** 18 multi-solid entries: `5x_Ang_Conn_1`, `PCB_1`, both potentiometers, `Tactile-Switch_1`,
  `nano_Varsayılan`, `cap106C`, `nano - reg`, `led`, the eight `Samtec-TLW-*`, and `User Library-PJ-002AH_Pad`. There are also 13
  `_single_colour` meshes. In each entry, `instances` now lists the RCC ids and the MRA's are kept in `mra_instances`. Every entry
  matches rcc.glb's solids at 100 % with the identity axis map, even where rcc.glb has fewer solids: `nano_Varsayılan` has 273
  against the atlas's 293, and `PCB_1` has 27 against 31.
- **From the RCC Cadasio:** the FS90R (`Fitec FS90R Micro Servo NoConnector.step_По умолчанию`) and the barrel plug's
  `Wires`. Both match at 100 %.
- **`_conductors`:** how the battery lead and the servo stubs were traced.
- **`_skipped`:** every published RCC colour not used, with the reason. The main ones:
  - the royal-blue shield, against Lee's navy ruling;
  - the teal Nanos;
  - the car Nano's SolidWorks defaults;
  - the pure black joystick board;
  - the Mini-B's `#cbd2ef` slip;
  - the gold pins, against Lee's silver ruling;
  - the white silkscreen;
  - the BLS-3 contacts that change colour from step to step.

## 4. Checks

- **Every rule matches at least one mesh name.** The names come from rcc.glb and from `usb-a-end.glb`, whose mesh is
  `USBCableend`. The matches range from 1 mesh (for example `^Mini USB B$`) to 19 (`^Samtec-TLW-`).
- **No mesh is left in the default grey.** Every mesh takes one of these:
  - a rule's colour;
  - a rule's components or regions;
  - an atlas entry (the 12 entries in use match at 100 %, and so do all 20 in the file; the eight `Samtec-TLW-*`
    entries are not used, because their rule names a colour);
  - an atlas single colour (Baseplate_1, Case, Rotator-Unit_1, Thumb-Button, User Library-PJ-002AH_Body,
    Samtec-SSW-115-01-F-S, smt_resistor222_a, m7 diode, blm21, reset core, reset shell).
  The 12 lead bodies are omitted on purpose.
- **Every colour resolves** to a palette entry or a `#rrggbb`.
- **The red battery-clip stub.** NAUO41's conductor 0 runs from the clip's stub at own z -1.7..-0.3 (assembly x 640.7) to the
  barrel plug's stub at own z > 0, which Cadasio colours red. Conductor 1 runs from the stub at x 642.7 to the black one. The
  unplugged pair, NAUO42 with NAUO28, runs the same way. The red `regions` box catches all of that stub except its end cap on
  the floor of the housing's pocket, which is hidden. The box starts at x 39.55 so that it does not pick up the pocket floor
  (x 39.5), which is part of the housing.
- **FS90R stubs.** On NAUO17 the brown, red and yellow stubs sit at assembly y 907.96 / 906.86 / 905.76. That is how the CAD's own
  lead bodies have them, and both plugged leads end brown on G, red on V and yellow on S.
- **L1's engraving.** The engraving test finds L1's pocket (10 % of L1's faces), so `move_engraving` has something to turn.

## 5. Open points

1. **`decals.json` is missing.** The first `build_model.py` run fails until it exists. It should carry the I/O module's silkscreen
   (the MRA's moved, `reuse_and_colours.md` 1.3), the two white boards' print, and L1's FRONT.
2. **Lee's rulings needed** (`_notes.unconfirmed`):
   - FS90R colour and its label;
   - signal wire yellow or orange;
   - radio boards black or green;
   - the wheels;
   - which 9 V battery, and whether it is in the kit;
   - BLS-3 housings `#404040` or `#1e1616`;
   - silver or gold pins;
   - the white boards;
   - the car Nano (a / b / c);
   - whether the I/O module is the same board as the MRA's.
3. **Car Nano.** This draft colours the plainer model (option c). Option (b), swapping in the controller's Nano at the car's seat
   (NAUO27's pose + [0, 0, 225.000] mm), needs a small tool step, because `extra_parts` takes a GLB. Option (a) is a re-export by
   TechBox.
4. **`adjust_mm` is not set.** Two candidates from the CAD study:
   - Level the joysticks, which are tipped 3° about z (`reuse_and_colours.md` 1.2).
   - Lower the shield's reset button by 0.3 mm, so that it does not clip L4 / L5 as the shield slides in.

   Both are for whoever owns the geometry. A guide can also work around them with hand-set motion.
5. **At the first build, look at:**
   - the atlas percentages in `model.report.json`;
   - the tyre's outline;
   - whether the controller board's via holes clutter the white top with edge rings;
   - the red stub on the battery clip.
6. **Wire colours for `guide.py`:** `lead_brown`, `lead_red` and `lead_yellow` (servo leads, matching the stubs on the
   motors), and `wire_red` and `cable_black` (battery lead, matching the clip and plug stubs).
