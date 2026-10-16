# RCC: study of the published Cadasio guide (19075)

Source: https://instructions.online/?id=19075-rcc_remote_controlled_car, read from its data
(`cadasio/raw/19075-rcc_remote_controlled_car.json`, digest `cadasio/19075-rcc_remote_controlled_car.md`) and its 52 step
pictures, downloaded with `tools/cadasio/thumbs.py` into `cadasio/thumbs/19075-rcc_remote_controlled_car/NNN.jpg` (contact sheets
in `cadasio/thumbs/sheets/19075-rcc_remote_controlled_car/`, the original .webp files in `cadasio/thumbs/raw/`). Checked against
Lee's STEP (`RCC Build Instructions/rcc.glb`, read with `tools/glbio.py`) and Lee's photos and drawing of 15 Oct 2026
(`lee_images_2026-10-15/`). Written 15 Oct 2026.

**Directions used here.** The Cadasio project uses the same frame as Lee's STEP: SolidWorks millimetres, Y up (the project's
root box, X 591-774, Y 868-982, Z 1042-1413, matches the GLB). On the car, **front = +X** (the wheel end: L1's servo notches
and Lee's FRONT etching are at +X), **up = +Y**, so **the car's right = +Z and its left = -Z**. The CAD agrees: the servo, wheel
and lead named "Right" are at +Z. The controller lies beside the car at -Z, with its handles (the end the student holds)
at -X and its joystick sockets at +X.

**Thumbnail numbers.** `[NNN]` is the picture's index (000-051). The published step names are different, because each action
takes two numbers (see 4.4). The table in section 2 gives both.

---

## 1. Cadasio names and CAD ids

Each of these was checked against the geometry in rcc.glb, not only against the names.

| Cadasio name | CAD id | What it is, and how it was checked |
|---|---|---|
| Controller-with-vias | NAUO30 | Controller board, 87 x 150 mm, white. Sub-meshes: H1 / H2, two 15-pin sockets along X (z 1105.3, 1120.5); the 2x4 `NRF24L01` socket (x 711.9, z 1130.6); C1 (x 702.0); L-JS / R-JS, two right-angle 2x5 sockets (x 732.2, z 1084.8 / 1157.6). |
| 2024-RCC_ControllerHandles_mod1_Left / _mod1 | NAUO24 / NAUO25 | The black left / right guards (z 1042-1120 / 1122-1200). Each is a tray round its half of the board, with the floor of the joystick pocket. |
| nano (nano-4) | NAUO27 | The controller's Nano Board. Its USB socket is at -X, the end where the board is printed "USB". |
| nano (nano-3), and the shield's own "arduino nano" | **inside NAUO23** | The car's Nano Board. In Lee's STEP it is part of the shield assembly (board NAUO117, pin rows NAUO121/122, ICSP pins NAUO118-120, Mini-USB NAUO145-152). The guide needs it as a part of its own (`"own_parts"`, as the MRA did with its Nano). |
| Ensamblaje_Shield_NANO | NAUO23 | The Nano I/O shield: board NAUO82 (57.2 x 53.3 mm) with rows of G / V / S pins. Its barrel jack NAUO153 is at the rear right (x 689-704, z 1350-1359) and opens towards the battery. |
| RadioFrequencyCommunicationModule_nRF24L01 (-4 / -1) | NAUO11 / NAUO10 | Radio modules. NAUO11 sits on the controller (x 709-738, so it lies towards +X from its socket). NAUO10 sits on the car's adapter (x 744-773, hanging out past the front of the shield). |
| KY-023_Joystick-Module | NAUO12 / NAUO13 | Left joystick (z 1085, into L-JS) / right joystick (z 1158, into R-JS). The 5 right-angle pins point +X (tips at x 731.8). |
| Mini USB B + USB Cable end | NAUO16 | Only the Mini-B end is in the STEP, plugged into the controller's Nano. There is no A end (see 7). |
| 3D_1-PCB_PCB_RCC_nRF24L01_Capacitor_Adapter copy_2026-06-14 | NAUO26 | The L-shaped TechBox adapter board. Board NAUO74, 57.4 x 33.8 mm. The leg runs along X at z ~1315-1328 (the car's left of centre); the foot is at the front, reaching to z 1348.6. On top: U1 (3-pin male, x 717.5), U2 (3-pin male, x 730.2), both with pins at z 1318.4 / 1321.0 / 1323.5; U3 (2x4 socket, x 746.3) and C1 (x 743.7, z 1331). Underneath: two 3-pin, one 4-pin, two 2-pin and one 2x3 sockets, which go onto the shield's G/V/S pins (not onto the ICSP header). |
| Fitec FS90R Micro Servo NoConnector.step (-1 / -2) | NAUO17 / NAUO18 | Right wheel motor (z 1395) / left wheel motor (z 1282). Each sits between L4 and L5, in L1's side notch. |
| Pololu Wheel 60mm (-1 / -2) | NAUO8 / NAUO9 | Right / left wheel (rim + tyre), on the motor's shaft, just outside L1's edge. NAUO9's box in cad_tree.md (78.4 mm) is only its two meshes' union: both meshes are 60 mm. |
| BLS-3.step | NAUO21 / NAUO22, NAUO19 / NAUO20 | The 3-pin plug of each lead. NAUO21 (right) and NAUO22 (left) are the loose pose. NAUO19 (right, on U2) and NAUO20 (left, on U1) are the plugged pose. |
| Fitec Right Wires 4 + Right Wire Yellow/Red/Brown 4 | NAUO31 + NAUO32-34 | Right lead, loose pose. It leaves the motor at x ~712, **passes through the slot at L4's end** (x 713-716, y 906-913) and lies back along L1 to the plug at x 638-652. The three 13 mm pieces are the coloured conductor ends at the plug. |
| Fitec Left Wires 4 + ... | NAUO35 + NAUO36-38 | Left lead, loose pose (the same, at z 1292). |
| Fitec Right Wires 5 | NAUO39 | Right lead, routed up and over to U2. |
| Fitec Left Wires 5 | NAUO40 | Left lead, routed to U1. |
| L1 ... L7 | NAUO1 ... NAUO7 | The wood. The CAD names match the codes engraved in the published pictures (L3 [027], L5 [033], L4 [035], L7 [041], L6 [043], L1 / L2 [045]). Engraved faces in the STEP: L1 on top (+Y), front-right corner; L2 on its -Z face; L3, L4 and L5 on their +X faces; L6 on its +Z face and L7 on its -Z face, both on the front "handle" under L1. |
| 9V-battery | NAUO14 | Stands upright through L1's square hole, in the cradle formed by L3. |
| DC_Adaptor | NAUO15 | The 9 V battery clip, on top of the battery. |
| DC_barrel_connector_9V | NAUO28 / NAUO29 | The battery lead's barrel plug in two poses: NAUO28 is 9 mm out of the jack, NAUO29 is pushed in (its tip is in NAUO153). |
| Battery Wires 1 / Batery Wires 2 | NAUO41 / NAUO42 | The lead from the clip to the barrel plug, in two poses. NAUO41 reaches x 659.8, the back of the plugged-in NAUO29. NAUO42 reaches x 650.8, the back of NAUO28. |

Lee's note about the servos is borne out: each servo has one lead, and the STEP poses it twice. The loose pose (NAUO21/22 +
NAUO31-38) lies threaded through L4 and back along L1. The plugged pose (NAUO19/20 + NAUO39/40) is routed to the adapter.

---

## 2. The build as the published guide tells it

The guide has 52 views and no caption text anywhere. Its only cues are 8 red lead lines (in 5 views) and 4 eye icons (in 2 views).
Every step lasts 800 ms. There are no labels, no section cards and no parts list.

### 2.1 Title page [000]
The logo, "Remote Controlled Car (RCC)", "Full Build" and "© 2026 TechBox. A division of TARIS Industries, LLC. All Rights
Reserved." The finished car is seen from the front left, above, with the controller behind it to the left.

### 2.2 The controller [001]-[012]
The camera is close on the controller. Everything else is hidden.

| View | Name | What happens | Camera / cues |
|---|---|---|---|
| [001] | Step 1 | Controller board and **both guards already fitted**. The Nano Board (NAUO27) hovers 30 mm above H1 / H2, its USB end towards the board's USB print. | New camera. No cue. |
| [002] | Step 2 | Nano down into H1 / H2. | Held. |
| [003] | Step 3 | Radio module (black) hovers 26 mm above the NRF24L01 socket, lying towards the top edge. | Held. No cue. |
| [004] | Step 4 | Radio down. | Held. |
| [005] | Step 5 | Left joystick appears **65 mm to the side, level with its seat**, pins towards L-JS. | New camera, from the handle end. No cue. |
| [006] | Transition | It slides 65 mm sideways (auto-advance). | Held. |
| [007] | Step 6 | The last 2 mm, with a slight turn: seated in its pocket. | Held. |
| [008]-[010] | Step 7 / Transition / Step 8 | The right joystick, the same way, into R-JS. | New camera, from the other end. |
| [011] | Step 9 | USB cable appears, its Mini-B end 6 mm from the Nano's socket. | New camera, high (62°). No cue. |
| [012] | Step 10 | USB plugged in. | Held. |

### 2.3 The car's electronics, and the servos plugged in [013]-[022]
The controller is hidden. The shield appears in its place in the car, without the car around it.

| View | Name | What happens | Camera / cues |
|---|---|---|---|
| [013] | Step 11 | The shield appears (its own Nano hidden). A separate Nano model hovers 39 mm above the shield's sockets. | New camera. No cue. |
| [014] | Step 12 | Nano down. In the data this Nano is never "seated": the author placed it with an offset. **It looks reversed**: see 4.1 (E2). | Held. |
| [015] | Step 13 | Adapter board hovers 43 mm above the shield. | Held. No cue. |
| [016] | Step 14 | Adapter down. | Held. |
| [017] | Step 15 | Radio module (black) hovers 31 mm above U3, hanging out past the front. | Held. No cue. |
| [018] | Step 16 | Radio down. | Held. |
| [019] | Step 17 | Left servo, **with its wheel already on**, and its lead loose. The lead is the CAD's loose pose (lying back), so from this camera the plug seems to stand up. | New camera, from the front. No cue. |
| [020] | Step 18 | The left lead is swapped for the routed one, plugged into the rear header (U1, LWh). | Held. No cue, no label. |
| [021] | Step 19 | Right servo + wheel, lead loose. | Held. |
| [022] | Step 20 | Right lead plugged into the front header (U2, RWh). | Held. |

This reads as a bench test: everything on the bench, both servos plugged in. But nothing powers the car (no USB, no battery),
and no step says to test.

### 2.4 The chassis base, upside down [023]-[028]
The electronics are hidden. The scene's "up" is turned over (`up_axis -y`), so the kit is seen turned over, from above.

| View | Name | What happens | Camera / cues |
|---|---|---|---|
| [023] | Step 21 | L1 lies upside down. L2 hovers tilted, 80 mm off. | New camera. **One bent lead line** (two legs) from L2's notch to L1's long slot. |
| [024] | "Step 32" (auto-advance) | L2 moves 55 mm towards L1. | Held. |
| [025] | Step 22 | L2 slides 56 mm along, its edge into L1's long slot. | Held. One short lead line (22 mm). |
| [026] | Step 23 | L2 goes the last 25 mm and swings upright. | Held. |
| [027] | Step 24 | L3 hovers 55 mm above (on screen) its place across the rear, over L2's cross slot. Its code reads upside down. | Held. **Two lead lines** to L1's short slots. |
| [028] | Step 25 | L3 home. | Held. |

### 2.5 Back to the bench: the servos unplugged [029]-[032]

| View | Name | What happens |
|---|---|---|
| [029] | Step 26 | Electronics and servos reappear exactly as left at Step 20, both plugged in. The chassis is hidden and the scene turned back upright. |
| [030] | Step 27 | Right lead swapped back to loose (unplugged). |
| [031] | Step 28 | Left lead unplugged. |
| [032] | Step 29 | The electronics are hidden. The two servos and wheels stay. No cue on any of these. |

### 2.6 The servo block [033]-[038]
This is bench work: the chassis is hidden for [033]-[036].

| View | Name | What happens | Camera / cues |
|---|---|---|---|
| [033] | Step 30 | L5 appears. **Both servos** (with wheels and loose leads) hover beside its two end notches. | New camera. No cue. |
| [034] | Step 31 | Both servos move together into L5's notches. | Held. |
| [035] | Step 32 | L4 hovers about 100 mm behind the servos. | Held. **Two lead lines from the servo plugs to the slots at L4's ends**: the plugs have to go through those slots. |
| [036] | Step 33 | L4 slides 100 mm forward along the leads onto the servos. | Held. |
| [037] | Step 34 | L1, L2 and L3 reappear, upright. The block (L4, L5, servos, wheels, leads) hovers 74 mm above L1. | New camera. Two lead lines (L4 to L2, L2 to L5). |
| [038] | Step 35 | The block drops onto L1. The leads end up lying back along L1, as in the CAD's loose pose. | Held. |

### 2.7 The electronics onto the chassis; L7 and L6 [039]-[044]

| View | Name | What happens | Camera / cues |
|---|---|---|---|
| [039] | Step 36 | The shield, adapter and radio appear **111 mm off to the upper left. The Nano is missing.** | Closer camera. No cue. |
| [040] | Step 37 | They move diagonally onto L4 / L5. The shield's two long sockets are visibly empty. | Held. |
| [041] | Step 38 | L7 appears 86 mm in front, below L1. | **Camera below the car** (elevation -18°), looking up. No cue. |
| [042] | Step 39 | L7 slides 86 mm back, through the slots in L5 and L4, on the left of L2. | Held. |
| [043]-[044] | Step 40 / 41 | L6 the same, on the right of L2. | New camera, still from below. No cue. |

### 2.8 The servo leads plugged in [045]-[048]
The camera is from the front, above. L1's code is at the near left.

| View | Name | What happens | Cues |
|---|---|---|---|
| [045] | Step 42 | Nothing moves. | **Two eyes**: one on the left lead's plug, one on the rear header (U1). |
| [046] | Step 43 | The left lead is swapped for the routed one, plugged into U1 (LWh). | None. |
| [047] | Step 44 | Nothing moves. | Two eyes: the right plug and the front header (U2). |
| [048] | Step 45 | The right lead is plugged into U2 (RWh). | None. |

### 2.9 Battery [049]-[050], and the Completed View [051]
- [049] Step 46: the 9V battery, its clip and the barrel plug on its lead appear together, 43 mm above L1's square hole. No cue. Wider camera.
- [050] Step 47: the battery drops into the hole (into L3). **The barrel plug stays loose beside it.**
- [051] Completed View: car and controller (USB still plugged into the controller). On the car: no Nano, and the battery not
  plugged in.

---

## 3. The wiring

Nothing in this kit is wired with loose jumpers. Every connection is a module plugged into a socket, a servo plug onto a header,
the barrel plug, and the USB cable.

| Lead or module | Goes into | Orientation | Published guide | Lee's STEP |
|---|---|---|---|---|
| Controller Nano (NAUO27) | H1 + H2 (the two 15-pin sockets) | USB socket at the end printed "USB" (towards the handles, -X) | Steps 1-2, correct | Same |
| Controller radio (NAUO11) | 2x4 socket printed `NRF24L01` | The module lies over the board away from C1 and the USB end, towards the joystick sockets (+X) | Steps 3-4, correct | Same |
| Left joystick (NAUO12) | `L-JS` (right-angle 2x5 socket on the far edge of the left pocket) | Pins first. In the CAD the pins are in the **upper row** (pin height 3.5 mm above the board; the two rows sit at about 1.3 and 3.8 mm) | Steps 5-6 (motion wrong, see E4) | Same |
| Right joystick (NAUO13) | `R-JS` | The same | Steps 7-8 | Same |
| USB cable, Mini-B end (NAUO16) | Controller Nano | Into the Nano's socket, from -X | Steps 9-10. Stays in to the end | Plugged into the controller |
| Car Nano (inside NAUO23) | The shield's two 15-pin sockets | **USB socket at the same end as the power jack (rear)**: the Mini-USB is at x 690-699, beside the jack at x 689-704 | Steps 11-12, **reversed** (USB towards the front; see E2) | USB at the jack end |
| Adapter board (NAUO26) | The shield's G/V/S pins: the leg over the left-hand pin rows (x 693-741, z 1318-1324), the foot over the front pins | U3 and C1 at the front (the end away from the power jack and the Nano's USB socket) | Steps 13-14, correct | Same |
| Car radio (NAUO10) | U3 on the adapter | Hangs out past the front of the shield and of the car | Steps 15-16, correct | Same |
| **Left servo** lead (NAUO18) | **U1, printed `LWh`**: the header farther from the foot (rear, x 717.5) | **S V G**. S is the pin towards the middle of the car (+Z), G the pin towards the car's left edge (-Z): **yellow to S, red to V, brown to G** | Steps 18 and 43, correct (thumb [048]: yellow, red, brown from the car's middle outwards on both plugs) | Plug NAUO20 on U1. Tracing the lead's three conductors from the motor to the plug puts brown on G. |
| **Right servo** lead (NAUO17) | **U2, printed `RWh`**: the header nearer the foot (front, x 730.2) | Yellow to S (z 1323.5), red to V (1320.9), brown to G (1318.4) | Steps 20 and 45, correct | Plug NAUO19 on U2. All three conductors traced: yellow on S, brown on G. |
| Battery clip (NAUO15) | The 9V battery's terminals | On top of the battery | Never shown (the battery arrives with it on) | On |
| Barrel plug (NAUO28 / 29) | The shield's power jack NAUO153 (rear right, facing the battery) | Pushed in along +X, 9 mm | **Never plugged in** | Both poses: out and in |
| USB to the car's Nano | Nothing | | Not in the guide | Not in the STEP |

How U1 / U2 and S / G were mapped from Lee's adapter photo to the CAD: the photo is a top view. In it, U3 is on the foot under the leg,
C1 and the logo are to its left, and U2 is nearer the foot than U1. In the STEP, U3 is at the front (+X) and C1 is at +Z of U3.
So the photo's down is +X and its left is +Z. "S V G" reads left to right under each header, so **S is at +Z and G at -Z**.

---

## 4. Errors, colour problems and unclear steps in the published guide

### 4.1 Installation errors

| # | Where | What is wrong | What it should be |
|---|---|---|---|
| E1 | Step 29 [032] to the end [039]-[051] | **The car's Nano disappears.** It is pressed onto the shield at Step 12 and hidden with the electronics at Step 29, but it never comes back: the shield goes onto the chassis with its two long sockets empty ([040], [045]-[048]), and the Completed View [051] has no Nano. | The Nano rides with the shield from Step 12 on. |
| E2 | Steps 11-20 [013]-[022] (clearest in [019], camera from the front) | **The car's Nano looks reversed.** Its USB socket points to the front (towards the radio) and its ICSP pins to the rear, by the power jack. In Lee's STEP, the Nano that is part of the shield assembly has its USB socket at the jack end, as on the MRA ("its USB socket at the same end as the power socket"). The published author hid that Nano and placed a separate Nano model by offset only (it is never at its CAD seat), which would explain the reversal. | USB socket at the power-jack end, as in the STEP. Worth checking on a real kit, since students copy the picture. |
| E3 | Steps 46-47 [049]-[050], Completed View [051] | **The battery is never connected.** The barrel plug stays loose beside the battery, pointing out of the side of the car. | A last step pushes the plug into the jack (the STEP has both poses: NAUO28 out, NAUO29 in). Or, if TechBox wants it left out until driving, a caution saying so. |
| E4 | Steps 5-8 [005]-[010] | **The joysticks slide in through the guard.** Each starts 60-65 mm away, level with its seat, and glides sideways (partly on an auto-advancing Transition) through the black rim and the board edge into its pocket. In the CAD the joystick's board drops into a 31.5 x 28.8 mm hole in the controller board, and only its pins (6 mm) reach into the L-JS / R-JS socket. | Hover above the pocket, set it down a few mm short of the socket, then push the pins in: two stages of one step. |
| E5 | Steps 17-29 [019]-[032] | **The test is half there.** Both servos are plugged in on the bench, but nothing powers the car and no step says to test. The chassis base is then built (Steps 21-25) before the servos are unplugged (Steps 26-28), so the student unplugs things set aside four steps earlier. | A complete bench test, as decided for the MRA: plug in, power, Testing Checklist, unplug, set aside. Then the chassis. |
| E6 | Step 36 [039] | **The electronics come in diagonally from 111 mm,** with no cue. | Straight down onto L4 / L5, at most about 60 mm, with lead lines to the notches it sits in. |
| E7 | Step 1 [001] | **The guards are never fitted.** They are on the controller board from the first view. | One step per guard, before the joysticks (each guard carries the floor of a joystick pocket). |
| E8 | Steps 17 / 19 [019], [021] | **The wheels are never fitted.** Each servo arrives with its wheel on. | One step per wheel: "Press a wheel onto the shaft of a wheel motor." |
| E9 | Step 46 [049] | **The battery clip is never fitted.** Battery, clip, lead and barrel plug arrive together. | A bench step for the clip, then the battery into its cradle. |
| E10 | Step 32 [035] | **The plugs-through-L4 cue.** The two lead lines from the servo plugs to L4's slots mean "the plugs go through these slots". But L4 then glides 100 mm past plugs that never move, and nothing says to thread them. The idea is right (in the CAD the leads pass through those slots). | Keep the idea and say it in the caption ("Pass each plug through the slot at its end of L4..."), or give the threading its own steps (section 6, question 5). |

### 4.2 Colour problems

Pixel colours are sampled from the step pictures; data colours are from the digest.

| # | Where | What | Suggestion |
|---|---|---|---|
| C1 | Every car view, e.g. [019], [045] | Shield board bright blue (renders about `#2b60f5`) beside the navy Nano (`#051554`). This is the clash Lee settled for the MRA (rulebook 13: the I/O module's board is the Nano's navy `#000f41`). | Navy `#000f41`, unless the RCC's shield is really another colour (question). |
| C2 | Servos [019]-[048] | Servo bodies light blue (overrides `#1aa2ef` / `#0073b3` / `#00639a`; renders about `#0096e7`). | Check against the kit's FS90R. Many FS90R bodies are black; no published reference here. |
| C3 | Radios [003], [017], [040] | Radio boards set to black `#000000` in steps (CAD colour tan `#ffde86`). | Check against the kit (nRF24L01 boards come black or green). |
| C4 | Mini-B plug [011] | The plug keeps the CAD default `#cbd2ef` (rulebook appendix B lists the same slip, `#cad1ee`). | Metal `#a6a9aa`, black housing. |
| C5 | Wood, all chassis views | Lit faces render pale yellow (`#feeeae`), not the house wood (`#deb887`, about `#ffdda2` lit). The data ends the guide with the wood back at the CAD default light grey `#e3e3e3` (a late reset; the pictures stay yellow). | House wood `#deb887`; our colour library already does this. |
| C6 | Servo leads | The CAD and the guide use yellow `#ffd500` for signal. The MRA's captions say "orange to S". | Confirm the real lead colour, so the caption says yellow or orange to match the wire. |
| C7 | Controller [001] | Board white and guards black: **correct**, as in Lee's photo. The adapter board is white, also correct. | Keep. Lee's photos also give the silkscreen for decals: controller "L-JS", "R-JS", "H1", "H2", "NANO BOARD CONTROLLER", "NRF24L01", "C1", "USB" and the logo; adapter "U1", "U2", "U3", "LWh", "RWh", "S V G", "C1" and the logo. |

### 4.3 Departures from the rulebook

| # | Where | What | Rule |
|---|---|---|---|
| R1 | Whole guide | Each action takes two step numbers ("Step 1" hover, "Step 2" done), so 47 numbers cover about 24 actions. An auto-advancing view is named **"Step 32"** ([024], between Steps 21 and 22), and the real "Step 32" comes later ([035]). | Step N / Step Nc; Transitions named "Transition". |
| R2 | Most placements | No cue on the Nano Boards, radios, joysticks, adapter, servos, L5, L7, L6, electronics, battery or USB. 8 lead lines in the whole guide. | Section 6: every Step N carries a cue. |
| R3 | [019], [021], [033], [049] | Several parts at once: servo + wheel arrive together; both servos move into L5 together; battery + clip + lead + plug arrive together. | Section 3: one kit item per step. Two identical parts may share a first placement only with the same motion. |
| R4 | [041]-[044] | Camera below the car (elevation -17° / -18°) to show L7 / L6 going in underneath. | Section 7: the kit is turned over (our `flip=True`), never viewed from below. |
| R5 | [045], [047] | Eyes on plug and header, but no destination label. | Section 9; for us, `LWh` / `RWh` as printed (like the MRA's `Row 5`). |
| R6 | Whole guide | No section cards, although the controller and the adapter both have printed pin names the student must find. | Section 6 / 9. Lee's two photos are exactly what a card needs. |
| R7 | [039], [041], [043] | Hover distances too long: 111 mm for the electronics (diagonal), and 86 mm for L7 / L6 (1.3 x their 65 mm length). | Section 12: plug-in about 35 mm; sliding part 1.0 x its length. |
| R8 | [003], [017], [019] | Placements rely on the picture alone for orientation (radio antenna end, Nano USB end, plug S V G). The published guide has no text. | Our captions and cautions carry these (rulebook 13: "Remember brown to G...", Nano "USB socket at the same end as the power socket"). |

### 4.4 Smaller slips
- The shield arrives with one silver solid of a barrel connector ("eBom-FreeParts") from Step 11, and the Completed View hides two other
  solids of that connector. These are left-overs of the author's visibility work; they do not show as a separate part in the pictures.
- The title page and the Completed View put the controller beside the car by moving it 412 mm along several axes. Lee's STEP already
  places the controller about 217 mm to the car's left, so our title page needs no such move.

---

## 5. Proposed step list for our guide

This follows the rulebook: one kit item per step, Step N / Step Nc, the receiver appearing in place, a bench test before the
mechanical build (as on the MRA), wiring one lead per step, and captions in the MRA guide's voice. Hover directions, lead lines
and cameras come from `tools/stepgen.py`; the notes below say only what the generator cannot know. "flip" means `flip=True`
(work done with the kit upside down). Names are proposals (question 8). Numbers are indicative: the open decisions in section 6
add or remove a few steps.

### Part 1: the controller

| # | Moves | Draft caption | Notes |
|---|---|---|---|
| 1 | Left guard (the controller board appears in place) | Begin the controller with the controller board. Fit the left guard onto the left half of the board. | How a guard goes on (slides on from the side, or the board drops in) is for the collision test to say. |
| 2 | Right guard | Fit the right guard onto the other half. | |
| 3 | Nano Board (NAUO27) | Press a Nano Board into H1 and H2, its USB socket at the end marked USB. | 4 lead lines, at the corner pins. |
| 4 | Radio module (NAUO11) | Press a radio module into the socket marked NRF24L01, so that the module lies over the board, away from the USB end. | Caution (antenna end) if TechBox wants one. |
| 5 | Left joystick (NAUO12) | Set the left joystick into its pocket and push it towards L-JS until its pins are all the way into the socket. | Two stages: down into the pocket a few mm short, then pins in (fixes E4). Caution "Use the top row of holes" if confirmed (question 10). |
| 6 | Right joystick (NAUO13) | Do the same with the right joystick at R-JS. | Same camera, if one view shows both pockets. |
| 7 | USB cable (NAUO16 + an A end) | Connect the USB cable to the controller's Nano Board. | Hover and plug, one lead line, A end on the table (as on the MRA). It may belong in the test (question 1). |

### Part 2: the car's electronics, and the bench test

| # | Moves | Draft caption | Notes |
|---|---|---|---|
| 8 | Nano Board (car; `own_parts` out of NAUO23) | Begin the car's electronics with the I/O module. Press the other Nano Board into it, its USB socket at the same end as the power socket. | The MRA's wording. Fixes E2. |
| 9 | Adapter board (NAUO26) | Press the adapter board onto the I/O module, its sockets over the pins along the side, with U3 at the end away from the power socket. | 4 lead lines. A section card with Lee's photo would come just before (R6). |
| 10 | Radio module (NAUO10) | Press the other radio module into U3, so that it sticks out past the end of the I/O module. | |
| 11 | Wheel (NAUO9) onto the left motor (NAUO18), shown alone | Press a wheel onto the shaft of a wheel motor. | Bench: the motor alone with its lead. One lead line down the shaft. Here or at the end (question 3). |
| 12 | Wheel (NAUO8) onto the right motor (NAUO17) | Press the other wheel onto the second wheel motor. | |
| 13 | Left motor's plug | Plug the left wheel motor into LWh for the test. Remember brown to G, red to V, and yellow to S. | Label `LWh` on the pin tops, as with the MRA's `Row 5`. Caution on this first plug: brown to G. |
| 14 | Right motor's plug | Plug the right wheel motor into RWh for the test. Remember brown to G, red to V, and yellow to S. | Label `RWh`. |
| 15 | Battery clip (NAUO15) onto the 9V battery (NAUO14) | Snap the battery clip onto the 9V battery. | Only if the car is battery-powered for the test (question 1). |
| 16 | Barrel plug (NAUO28 to NAUO29) | Plug the barrel plug into the power socket on the I/O module. | The same. If USB powers the car, use "Connect the USB cable to the car's Nano Board." instead. |
| 17 | Note card | Testing Checklist (TechBox's wording, needed; a placeholder is in question 2). | A list card, as on the MRA. |
| 18 | Both plugs lift off (and the power comes out) | Unplug both wheel motors from the adapter board. | One step for both plugs, as Lee chose for the MRA. Caution: "Set the wheel motors, the I/O module and the controller aside for now. You will use them again in a bit." Then `put_away`. |

### Part 3: the chassis

| # | Moves | Draft caption | Notes |
|---|---|---|---|
| 19 | L2 (L1 appears in place) | Begin the car with L1, engraved side down. Angle L2 into the long slot in the middle of L1... | flip. A hook-and-swing (section 4), as published. |
| 20 | L2 | ...then swing it upright. | Same camera. Or one step with a hand-set path (question 4). |
| 21 | L3 | Slide L3 down over the end of L2 so its tabs go into the two short slots in L1. | flip. Show L3's code (its +X face). |
| 22 | Right motor into L5 (L5 appears in place, chassis hidden) | Push the right wheel motor into the notch at one end of L5, wheel outwards and wire pointing away from L5. | Bench. The lead rides with the motor, its plug on the loose end (rulebook 13, servos). |
| 23 | Left motor into L5 | Push the left wheel motor into the notch at the other end. | One motor per step (the published guide did both at once). |
| 24 | L4 | Pass each motor's plug through the slot at its end of L4, then press L4 onto the motors. | The published cue, with words. Or split into two lead steps + L4 (question 5). |
| 25 | L4 + L5 + motors + wheels (`g.seat`) | Turn the kit back over. Lower L4 and L5, with the motors, onto L1: their slots go over L2 and into the slots in L1. | The leads end lying back along L1 (the CAD's loose pose). |
| 26 | L7 | Slide L7 in from the front, through the slots in L5 and L4, on the left of L2. | flip, if the generator wants the code seen (it is on the handle under L1). Fixes R4. |
| 27 | L6 | Slide L6 in the same way on the right of L2. | Steps 26-27 may go after step 28, as published (question 4). |

### Part 4: electronics on the car, wiring, battery

| # | Moves | Draft caption | Notes |
|---|---|---|---|
| 28 | I/O module + Nano + adapter + radio, back from put-away (`g.seat`) | Lower the I/O module, with everything on it, onto L4 and L5, with the radio module over the front of the car. | Straight down, lead lines to the notches (fixes E1 and E6). |
| 29 | Left motor's plug | Plug the left wheel motor into LWh. Remember brown to G, red to V, and yellow to S. | Label `LWh`. The lead goes from lying back to routed (CAD pose 4 to pose 5). |
| 30 | Right motor's plug | Plug the right wheel motor into RWh. Remember brown to G, red to V, and yellow to S. | Label `RWh`. |
| 31 | 9V battery with its clip (clip fitted at step 15) | Push the 9V battery down through the square hole in L1 into L3, clip at the top. | If the clip was not fitted in the test, a clip step comes first. |
| 32 | Barrel plug | Plug the barrel plug into the power socket on the I/O module. | Fixes E3. Or leave it out with a caution (question 6). |
| 33 | USB cable (if the cable left the controller after the test) | Connect the USB cable to the controller's Nano Board. | Question 1. |
| CV | Camera only | Completed View | Car from the front above, controller beside it (Lee's MRA title-page decision: from the front). |

Engraved codes come in build order L1, L2, L3, L5, L4, L7, L6. Renaming L4 / L5 and L6 / L7 at source would make them run in order
(rulebook 13, "engraved codes in build order"), if the parts can still change.

---

## 6. Decisions for Lee

1. **Power for the test and when driving.** How is the car powered in the bench test: the 9V battery through the barrel jack, or a USB
   cable into the car's Nano? Is there one USB cable or two? Does the controller always run from USB (a computer or a power bank),
   and should the Completed View show the cable plugged in, as the published one does?
2. **The RCC Testing Checklist**, word for word, as for the MRA. Placeholder until it comes:
   "Testing Checklist / Go through the following checklist to make sure you have tested each part of your RCC: / • The controller was
   powered on by connecting a Mini-USB cable to its Nano. / • The car was powered on by plugging in the 9V battery. / • Pushing the left
   joystick forward made the left wheel turn. / • Pushing the right joystick forward made the right wheel turn. / • Each wheel stopped when
   its joystick was released. / • The battery was unplugged after testing."
   Also: which joystick drives which wheel? And does the FS90R's stop trim need adjusting during the test?
3. **Wheels**: on during the test, as published (the student sees them turn), or pressed on at the end of the build?
4. **Order in the chassis**: do L6 / L7 hold the I/O module down? If so they go on after it, as published; if they only lock L4 / L5
   to L1, they go on before it, with the other underside work. And L2: one step with a path, or two steps (angle in, swing upright)?
5. **L4 and the plugs**: one step ("pass each plug through ... then press L4 on", with the published plug-to-slot lead lines), or
   two threading steps (an eye on each plug) and then L4?
6. **The barrel plug at the end**: plugged in as the last step, or left out with a caution ("plug in to drive; unplug when you stop")?
7. **Colours**: the shield's board (navy `#000f41` per the MRA decision, or its real colour?); the servo bodies (light blue as published,
   or black?); the radio boards (black or green?); the servo signal wire (yellow, as the CAD has it, or orange as on the MRA, which
   decides the caption "... and yellow to S").
8. **Names** (the published project has tooltips switched off, so there are none to copy). Proposed: Controller Board, Left / Right
   Controller Guard, Nano Board, Radio Module, Left / Right Joystick, USB Cable, Nano I/O Module, Radio Adapter Board, Left / Right
   Wheel Motor, Wheel, 9V Battery, Battery Clip, L1-L7.
9. **The car's Nano**: confirm its USB socket goes at the power-jack end (the STEP and the MRA wording) and not towards the radio, as
   the published pictures show (E2).
10. **The joystick sockets**: L-JS / R-JS are 2-row sockets, and the CAD puts the joystick's pins in the upper row. Is that the row
    students must use? If so, it needs a caution.
11. **The guards**: how do they go on (slid on from each side, or the board pressed into them), and before the Nano, as proposed?
12. **L1's etching**: Lee's drawing has the wheel end (front) at the top and reads upright from behind the car. In that view, FRONT is
    at the front-left corner and L1 at the front-right, both about 7.6 mm tall and about 5 mm in from the edges. The STEP's "L1" is
    already in the front-right corner (x 763-769, z 1390-1398, on the top face), but it reads upright from the *front* of the car,
    so it is upside down against the drawing, and it is 6.3 mm tall. FRONT is not there. If the drawing shows the top face (it
    reads as cut), the fix is: turn "L1" 180° and add "FRONT" at the front-left corner (`materials.json` `"move_engraving"`, which
    can turn a code, plus a new engraving for FRONT).
13. **Section cards** with Lee's two photos (the controller's and the adapter's pin names boxed in red) before steps 3 and 9? The
    player has text-only cards so far (rulebook 14).

## 7. Notes for whoever builds the model and guide.py

- **Car Nano**: inside NAUO23 (NAUO117, 118-122, 145-152 and their small parts), so it needs `"own_parts"`, like the MRA's Nano Board.
- **Servo leads**: omit the CAD lead bodies NAUO31-40 and draw the leads as wires (`wire-paths.json`). The loose pose (through L4's
  slot, back along L1) and the routed pose (up and over to U1 / U2) are the two routes. One plug per lead: NAUO21 / NAUO22 and
  NAUO19 / NAUO20 are the same plug in its two poses, so keep one and pose it.
- **Battery lead**: NAUO41 / NAUO42 and NAUO28 / NAUO29 are the same lead and plug, out of the jack and in it.
- **USB**: only the Mini-B end is in the STEP (NAUO16, on the controller). The MRA's `usb-a-end.glb` (`"extra_parts"`) could give the
  A end, and the MRA's drawn cable the rest.
- **Joystick seat**: the board hole is 31.5 x 28.8 mm (x 695.8-727.3). The joystick's pins reach from x 725.8 to 731.8, into a socket that
  starts at x 725.75. So the joystick can be set down about 6-7 mm short of the socket, then pushed in along +X.
- **Silkscreen**: Lee's photos of the controller and adapter boards are the source for decals, as `silkscreen.py` did for the MRA's I/O
  module (placed from the CAD's pin positions given in section 1).
- **Engraved code faces** (for the camera's "code readable" preference): L1 +Y (front-right), L2 -Z, L3 +X, L4 +X, L5 +X, L6 +Z and L7 -Z
  (on the handles under L1, so a flip view if the codes must be read).
