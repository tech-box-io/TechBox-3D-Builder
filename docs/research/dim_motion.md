# Dimension report: part motion, hover offsets and seating

Scope: all 20 published TechBox Cadasio guides (16 build guides, 3 deconstruction guides, 1 parts overview; 1037 viewer steps).
Kits: LSM = Laser STEM Matrix, LAC = LCD Alarm Clock, PMG = Piano Memory Game. `-F` = that kit's Full Build. Step indices in square brackets are viewer indices of the named guide (e.g. LAC-F [098]).

## 0. How the numbers were produced (read this before trusting any digest MOVE line)

The per-guide digests are unreliable for motion: they miss parts whose parent node is flagged hidden, report offsets in part-local axes, and treat absolute positions as offsets (every per-guide reader hit one of these). All figures here come from a tracker written for this report that replays the raw payloads (`reports/_work_dim_motion/track.py`, `events.py`, `analyze.py`, `master.py`, `wires.py`, `swaps.py`, `tables.py`). Its rules, each verified:

- Visibility is per leaf solid: the solid's own last explicit `visible`, else the CAD hidden flags. Checked against corrected reader counts (LAC Electronics [001] = 9 parts / 27 solids; LSM Part 3 = 26-28 parts / 684-690 solids; PMG Part 2 [001] = 1 part, [024] = 74 parts).
- A node's local matrix is `T(position or CAD translation) * R(rotation quaternion or CAD rotation)`; world pose is the product down the tree. `origin` is the authoring pivot and is already folded into `position` (checked on LAC F7: `(I - R) * origin` reproduces the stored position to 0.01 units).
- Every offset below is the world-space displacement in mm (Y up) of the largest solid of the part, measured between two frames of the same guide (pose in Step N minus pose in Step Nc), so it does not depend on where the CAD pose is.
- Spot checks against reader reports recomputed from raw: LAC Part 4 F7 80.3 / F8 94.2 / F5 56.0 / F6 67.5 / F9 103.9 then 25.8 deg / F2 21.4 deg then 78.1 mm; LSM D4 69.4, D3 45.8 + 21.6 deg, D5 42.0; PMG H11 53.1 + 6.7, H12 44.5 + 7.6. All match.
- "Unique" statistics use the three Full Builds only (they contain every build action once); "all 16" counts every copy, so the same authored step can be counted up to 3 times.
- 17 contact sheets (136 step renders) and 2 single frames were inspected across the three kits (LSM-F [000]-[007], [016]-[023], [032]-[039], [048]-[055], [064]-[071]; LAC-F [016]-[023], [048]-[063], [096]-[103], [120]-[127]; PMG-F [008]-[015], [056]-[071], [088]-[103]; PMG Deconstruction [016]-[023]; LSM Deconstruction [000]-[007]; LAC Electronics [000], [001]).

There are no screws in any of the three kits. The only threaded fasteners are two panel nuts (LSM push button, LAC potentiometer) plus one washer and one push-on knob.

## 1. What happens between Step N and Step Nc

| What happens between Step N and Step Nc | 3 full builds | all 16 build guides | 3 deconstruction guides |
|---|---|---|---|
| swap: loose wire -> routed wire | 49 | 104 | 23 |
| tween: single straight move to seat | 36 | 88 | 3 |
| swap: wired sub-assembly re-posed | 17 | 39 | 5 |
| tween: removal on Transition | 6 | 12 | 36 |
| tween: single straight move, stops short (stage 1 of 2) | 8 | 18 | 0 |
| tween: swing/tilt to seat (second stage) | 7 | 15 | 0 |
| tween: multi-leg (2 legs via Transition) | 5 | 11 | 1 |
| tween: wires fan out / separate | 5 | 10 | 0 |
| swap: wired sub-assembly re-posed (flipbook via Transition) | 3 | 6 | 6 |
| swap: shape change (same part, new model) | 3 | 8 | 0 |
| slide while fading out | 0 | 0 | 11 |
| fade-in: routed wire/cable only | 2 | 7 | 0 |
| fade-in: parts appear seated | 2 | 4 | 0 |
| tween: flex/pull away | 1 | 3 | 1 |
| tween: removal on c step | 0 | 2 | 2 |
| tween: in-place turn | 1 | 2 | 0 |
| tween: multi-leg (3 legs via Transition) | 1 | 2 | 0 |
| fade-out only | 0 | 0 | 3 |
| fade-out: wires | 0 | 0 | 3 |
| no c step | 0 | 0 | 1 |
| **pairs** | 146 | 331 | 95 |

Notes: "swap: loose wire -> routed wire" in the build columns includes 3 ribbon-split swaps (LSM Step 9 and its two part-guide copies), so true wire connections are 101 (48 in the Full Builds). In the deconstruction column the same category is the reverse swap (routed wire -> loose or hanging wire). The deconstruction column files PMG's two-stage removals under "removal on Transition" and its three wire or cable slide-fades under "fade-out", so section 10 has the per-kit breakdown. One of the 8 "stops short" rows in the Full Builds (LSM-F Step 3, Nano) is a 4 mm data residue, not an authored stage.

Reading of the build columns (331 pairs): 163 pairs tween something (49%), 157 pairs cross-fade between two models (47%), 11 only fade something in (3%). The tween is used for rigid parts; the cross-fade is used for anything with a wire attached and for shape changes.

## 2. Rigid parts: hover pose, then one move home

### 2.1 Every first-stage insertion tween in the three Full Builds (50 rows)

"Net hover" is pose at Step N minus pose at Step Nc. "Extent along travel" is the part's bounding box projected on the hover direction.

| Guide | Step [N idx] | Part | Kind | Net hover mm | World axis of hover offset | Tilt at hover | Motion to seat | How it got to hover | Extent along travel mm | hover/extent |
|---|---|---|---|---|---|---|---|---|---|---|
| LAC-F | 2 [004] | Breadboard | breadboard | 46.9 | +Y | - | c 46.9 mm -Y | visible before, slides 46.9 mm to hover on entering a Step N | 9.5 | 4.94 |
| LAC-F | 3 [006] | Nano | board | 39.8 | +Y | - | c 39.8 mm -Y | fades in at hover on Step N | 18.6 | 2.14 |
| LAC-F | 5 [010] | resistor | passive | 37.1 | +Y | - | c 37.1 mm -Y | swapped in at hover on the previous prep c-step | 10.5 | 3.53 |
| LAC-F | 6 [012] | resistor | passive | 40.0 | +Y | - | c 40.0 mm -Y | fades in at hover on Step N | 10.5 | 3.81 |
| LAC-F | 7 [015] | coin cell + RTC module | board | 33.6 | +Y | - | c 33.6 mm -Y | fades in at hover on the section card before | 46.1 | 0.73 |
| LAC-F | 15 [032] | leads + Rocker Switch | module | 81.2 | +Y | - | c 81.2 mm -Y | fades in at hover on the section card before | 30.2 | 2.69 |
| LAC-F | 25 [055] | potentiometer + leads | module | 79.1 | +Y | - | c 79.1 mm -Y | visible before, slides 79.1 mm to hover on entering a Step N | 28.0 | 2.82 |
| LAC-F | 26 [057] | Washer | hardware | 61.3 | -Y | - | c 61.3 mm +Y | fades in at hover on Step N | 0.4 | - |
| LAC-F | 27 [059] | nut | hardware | 55.9 | -Y | - | c 55.9 mm +Y | fades in at hover on Step N | 1.9 | - |
| LAC-F | 28 [061] | knob | hardware | 60.5 | -Y | - | c 60.5 mm +Y | fades in at hover on Step N | 17.0 | 3.56 |
| LAC-F | 41 [090] | F7 | wood | 80.3 | +Y | - | c 80.3 mm -Y | fades in at hover on Step N | 76.6 | 1.05 |
| LAC-F | 45 [098] | F9 | wood | 93.9 | +X&+Y | - | Transition 103.9 mm -X -> Transition 15.0 mm +X + 25.8 deg -> c 33.0 mm -Y | fades in at hover on Step N | 55.3 | 1.7 |
| LAC-F | 50 [111] | F8 | wood | 94.2 | +X | - | c 94.2 mm -X | fades in at hover on Step N | 16.5 | 5.71 |
| LAC-F | 55 [123] | F5 | wood | 56.0 | +Z | - | c 56.0 mm -Z | fades in at hover on Step N | 3.0 | - |
| LAC-F | 56 [125] | F2 | wood | 93.5 | -X&-Z | 21.4 | Transition 78.1 mm +X&+Z -> c 28.2 mm +X + 21.4 deg | fades in at hover on Step N | 110.6 | 0.85 |
| LAC-F | 57 [128] | F6 | wood | 67.5 | -Z | - | c 67.5 mm +Z | fades in at hover on Step N | 3.0 | - |
| LSM-F | 2 [004] | Breadboard | breadboard | 49.2 | +Y | - | c 49.2 mm -Y | visible before, slides 49.2 mm to hover on entering a Step N | 9.8 | 5.02 |
| LSM-F | 3 [006] | Nano | board | 44.1 | +Y | - | c 44.1 mm -Y | fades in at hover on Step N | 11.5 | 3.83 |
| LSM-F | 5 [010] | resistor 1 | passive | 32.4 | +Y | - | c 32.4 mm -Y | visible before, slides 1.6 mm to hover on entering a Step N | 10.5 | 3.09 |
| LSM-F | 6 [013] | capacitor | passive | 29.1 | +Y | - | c 29.1 mm -Y | visible before, slides 0.5 mm to hover on entering a Step N | 20.3 | 1.43 |
| LSM-F | 8 [017] | resistor 2 | passive | 30.3 | +Y | - | c 30.3 mm -Y | swapped in at hover on the previous prep c-step | 10.5 | 2.89 |
| LSM-F | 17 [037] | leads + push button | module | 102.5 | +Z | - | c 102.5 mm -Z | already hovering (previous step) | 24.9 | 4.12 |
| LSM-F | 18 [039] | push button | module | 83.1 | -Z | - | c 83.1 mm +Z + 115.1 deg | fades in at hover on Step N | 24.9 | 3.34 |
| LSM-F | 22 [048] | D4 | wood | 69.4 | -X | - | c 69.4 mm +X | fades in at hover on Step N | 3.0 | - |
| LSM-F | 24 [053] | D3 | wood | 45.8 | +X&-Z | 21.6 | c 45.8 mm -X&+Z | fades in at hover on Step N | 85.0 | 0.54 |
| LSM-F | 26 [057] | D5 | wood | 42.0 | +X | - | c 42.0 mm -X | fades in at hover on Step N | 3.0 | - |
| LSM-F | 27 [060] | D9 | wood | 64.6 | +Y | - | c 64.6 mm -Y | fades in at hover on Step N | 18.5 | 3.49 |
| LSM-F | 29 [064] | D10 | wood | 43.6 | -Y&+Z | - | Transition 21.8 mm +Y -> c 39.9 mm -Z | fades in at hover on Step N | 16.8 | 2.6 |
| LSM-F | 31 [069] | D6 | wood | 64.3 | +Y | - | c 64.3 mm -Y | fades in at hover on Step N | 3.0 | - |
| LSM-F | 32 [071] | D11 post | wood | 81.6 | +Y | - | c 81.6 mm -Y | fades in at hover on Step N | 79.7 | 1.02 |
| LSM-F | 33 [073] | D11 post | wood | 77.4 | +Y | - | c 77.4 mm -Y | fades in at hover on Step N | 79.7 | 0.97 |
| LSM-F | 33 [073] | D11 post | wood | 83.1 | +Y | - | c 83.1 mm -Y | fades in at hover on Step N | 79.7 | 1.04 |
| LSM-F | 35 [078] | D7 | wood | 67.8 | +Y | - | c 67.8 mm -Y | fades in at hover on Step N | 3.0 | - |
| LSM-F | 36 [080] | D8 | wood | 54.1 | +Y | - | c 54.1 mm -Y | fades in at hover on Step N | 3.2 | - |
| LSM-F | 37 [083] | stem | stem | 43.5 | +Y | - | c 43.5 mm -Y | visible before, slides 1.0 mm to hover on entering a Step N | 66.7 | 0.65 |
| PMG-F | 1 [002] | Nano | board | 29.8 | +Y | - | c 29.8 mm -Y | fades in at hover on Step N | 18.6 | 1.6 |
| PMG-F | 25 [057] | cable stub + USB plug | cable | 22.9 | +Z | - | c 22.9 mm -Z | fades in at hover on the section card before | 49.7 | 0.46 |
| PMG-F | 26 [059] | H2 | wood | 40.0 | +X | - | c 40.0 mm -X | fades in at hover on Step N | 136.9 | 0.29 |
| PMG-F | 27 [061] | H3 | wood | 43.2 | +X | - | c 43.2 mm -X | fades in at hover on Step N | 136.9 | 0.32 |
| PMG-F | 28 [063] | H4 | wood | 65.0 | +X | - | c 65.0 mm -X | fades in at hover on Step N | 3.0 | - |
| PMG-F | 29 [065] | H5 | wood | 117.1 | -Y&-Z | 23.6 | c 117.1 mm +Y&+Z | fades in at hover on Step N | 129.9 | 0.9 |
| PMG-F | 31 [069] | H6 | wood | 122.4 | -Y&-Z | 18.1 | c 122.4 mm +Y&+Z | fades in at hover on Step N | 134.4 | 0.91 |
| PMG-F | 35 [077] | H7 | wood | 139.4 | -Z | 11.7 | c 139.4 mm +Z | fades in at hover on Step N | 138.7 | 1.01 |
| PMG-F | 37 [081] | H8 | wood | 94.5 | +Y | - | c 94.5 mm -Y | fades in at hover on Step N | 30.9 | 3.06 |
| PMG-F | 38 [083] | H9 key | wood | 107.7 | -X | - | c 107.7 mm +X | fades in at hover on Step N | 130.4 | 0.83 |
| PMG-F | 40 [087] | H10 | wood | 126.0 | -X | 7.9 | c 126.0 mm +X | fades in at hover on Step N | 78.3 | 1.61 |
| PMG-F | 42 [091] | H11 | wood | 53.5 | +Y | - | Transition 53.1 mm -Y -> c 6.7 mm +X | fades in at hover on Step N | 86.3 | 0.62 |
| PMG-F | 43 [094] | H12 | wood | 45.1 | +Y | - | Transition 44.5 mm -Y -> c 7.6 mm +X | fades in at hover on Step N | 89.0 | 0.51 |
| PMG-F | 44 [097] | H13 | wood | 80.1 | -X&+Y | - | c 80.1 mm +X&-Y | fades in at hover on Step N | 51.5 | 1.56 |
| PMG-F | 51 [113] | H14 | wood | 58.5 | +X&+Y | 10.3 | Transition 57.8 mm -X&-Y -> c 3.0 mm +X&-Y + 12.6 deg | fades in at hover on Step N | 58.4 | 1.0 |

### 2.2 Hover distance by class

| Class | n (3 full builds) | min | median | max | n (all 16 build guides) | min | median | max | Hover direction (all 16) |
|---|---|---|---|---|---|---|---|---|---|
| Breadboard onto base | 2 | 46.9 | 48.0 | 49.2 | 5 | 39.3 | 46.9 | 49.2 | +Y x5 |
| Controller / module board into breadboard or socket (Nano, RTC) | 4 | 29.8 | 36.7 | 44.1 | 9 | 29.8 | 35.3 | 44.1 | +Y x9 |
| Two-lead passive (resistor, capacitor) | 5 | 29.1 | 32.4 | 40.0 | 13 | 29.1 | 32.9 | 40.0 | +Y x13 |
| USB plug into socket | 1 | 22.9 | 22.9 | 22.9 | 2 | 22.9 | 22.9 | 22.9 | +Z x2 |
| Panel-mount component with trailing leads (switch, potentiometer, push button) | 4 | 79.1 | 82.2 | 102.5 | 10 | 79.1 | 81.2 | 103.2 | +Y x4, +Z x3, -Z x3 |
| Hardware on a shaft (washer, nut, knob) | 3 | 55.9 | 60.5 | 61.3 | 6 | 55.9 | 60.5 | 61.3 | -Y x6 |
| Light-guide stem | 1 | 43.5 | 43.5 | 43.5 | 3 | 43.5 | 50.3 | 55.1 | +Y x3 |
| Wood panel moving face-on (along its 3 mm thickness) | 8 | 42.0 | 64.7 | 69.4 | 21 | 42.0 | 64.3 | 69.4 | +Y x9, +X x5, -X x3, +Z x2, -Z x2 |
| Wood part moving edge-on / lengthwise / tilted | 22 | 40.0 | 80.9 | 139.4 | 50 | 40.0 | 80.3 | 139.4 | +Y x20, +X x6, +X&+Y x4, -Y&-Z x4, -X x4, +X&-Z x3, -Y&+Z x3, -X&-Z x2, -Z x2, -X&+Y x2 |
| ALL first-stage insertion tweens | 50 | 22.9 | 60.9 | 139.4 | 119 | 22.9 | 60.5 | 139.4 | +Y x63, +X x11, +Z x7, -Z x7, -X x7, -Y x6, +X&+Y x4, -Y&-Z x4, +X&-Z x3, -Y&+Z x3, -X&-Z x2, -X&+Y x2 |

Observations behind the table:

- No constant is used. Identical parts in one guide differ (LAC-F resistors 37.1 mm [010] vs 40.0 mm [012]; LSM-F D11 posts 81.6 / 77.4 / 83.1 mm [071]-[073]). The same part differs between guide copies (LSM breadboard 39.3 mm in Part 1 and Part 1+2 vs 49.2 mm in the Full Build; Nano 35.3 vs 44.1; stem 43.5 / 50.3 / 55.1; D9 64.6 / 65.3 / 68.0). Values are not round numbers in mm or in scene units: they were dragged by hand.
- Hover distance tracks part size only weakly. Pearson r between hover and the part's extent along the travel direction: 0.46 (50 unique), 0.49 (119, all copies); Spearman 0.31 / 0.35. Against the largest dimension: r = 0.46 / 0.49, Spearman 0.38 / 0.40.
- What does predict it is the kind of fit:
  - parts dropping into a breadboard or socket: 29-49 mm regardless of size (all 22 board and passive insertions, copies included, lie within 29.1-44.1 mm; breadboard 39.3-49.2);
  - a 3 mm panel moving face-on: 42-69 mm, median 64.7 (8 unique);
  - a part that slides lengthwise into slots or over a shaft: about its own length along the travel. hover / extent for the 22 unique edge-on wood parts: quartiles 0.8 / 1.0 / 1.6. Close to 1.0 for D11 posts (0.97-1.04), F7 (1.05), H5 (0.90), H6 (0.91), H7 (1.01), H14 (1.00), key H9 (0.83);
  - a component trailing leads through a hole: far enough for the leads to clear, 79-103 mm for parts 25-30 mm long (switch 81.2, potentiometer 79.1, LSM button 102.5-103.2).
- Exceptions to "about its own length": PMG H2 and H3 hover only 40.0 and 43.2 mm although they are 137 mm long in the travel direction (ratio 0.29-0.32; the gap shown is just the tab gap, see PMG-F [059], [061]); H11 / H12 0.62 / 0.51; USB plug 22.9 mm for a 50 mm plug (0.46); stem 0.65.

### 2.3 Direction

Unique (50): straight down from above (+Y offset) 25 = 50 %; horizontal along one world axis 14 = 28 %; -Y 3 = 6 % (washer, nut, knob onto the potentiometer shaft, shown with the scene up-axis switched so it reads as horizontal, LAC-F [057]-[062]); oblique 8 = 16 %. All copies (119): single-axis 101 = 85 %, oblique 18 = 15 %.

- Everything that plugs into the breadboard or a socket strip comes straight down: 27 of 27 (breadboard, Nano, RTC, resistors, capacitor, all guides).
- Wood panels come along their tab axis, whatever that is: +Y 11, +X 5, -X 3, -Z 2, +Z 1 of the 22 single-axis unique wood rows.
- The 8 oblique unique cases are all explained by the physical path, not by a free choice of approach direction:
  - tilted hook-in panels that slide in their own tilted plane: LSM D3 [053] (21.6 deg), LAC F2 [125] (21.4 deg), PMG H5 [065] (23.6 deg), H6 [069] (18.1 deg), H14 [113] (10.3 deg). For the PMG deck panels the slide direction is inclined to the deck by exactly the tilt angle (H5 23.7 vs 23.6, H6 18.1 vs 18.1, H7 11.7 vs 11.7, H10 7.9 vs 7.9 deg);
  - two-leg L-paths whose net vector is oblique but whose legs are each along one axis: LSM D10 [064]-[066], LAC F9 [098]-[101];
  - PMG H13 [097]: 80.1 mm along the slanted slots of brackets H11 / H12 (offset [-61.3, +51.5, 0] mm, 40 deg above horizontal), single straight move.
- So the hover offset is always the reverse of the path the part physically takes. For single-leg seats (44 of 50 unique) that is the true insertion axis. For multi-leg seats the hover pose is the start of the path and is not on the final insertion axis.
- Anomaly: the LSM capacitor is modelled about 6 deg off vertical; in LSM Part 1 / Part 1+2 its hover is [3.4, 32.7, 0] mm, i.e. it travels along its own leaning axis ([012], [011]). In the Full Build the lean is removed on Step 6 [013] (6.0 deg, 1.6 mm correction) and it drops vertically.

### 2.4 How the part gets to its hover pose

All 119 first-stage insertions in the 16 build guides:

| How the mover reached the hover pose | n | Examples |
|---|---|---|
| Fades in, stationary, at hover in the Step N itself | 86 | LAC-F Nano [006], PMG-F H3 [061] |
| Fades in at hover one step earlier, on its section card (card isolates it; context returns on Step N) | 6 | LAC RTC [014], LAC switch [031], PMG USB plug [056], LSM stem [037] of Part 3+4 |
| Swapped in at hover on the previous prep c-step (bent-lead resistor model appears already at hover height) | 7 | LAC-F [009] -> [010]; LSM-F [016] -> [017] |
| Already on screen and visibly slides to hover on entering the step | 13 | see section 9 |
| Already on screen, nudged <= 1.6 mm | 4 | LSM-F [010], [013], [083] |
| Already hovering from the previous step (button after its nut came off) | 3 | LSM-F [037] |

For the 99 fade-in cases the hover pose was written while the part was still hidden in 97 (98 %): typically in the first numbered step after Start (LAC-F F5: position written at authored step 2, shown at 124) or one or two steps before it is shown. Only 2 write the pose in the same step that shows the part (LAC switch on its card [031], 81.2 mm; PMG-F H2 [059], 40.0 mm). The effect on screen is that a new part never flies in: it fades in standing still and only moves on the next press.

### 2.5 Legs

| Shape of the motion from hover to seat (first-stage insertions) | 3 Full Builds | all 16 build guides |
|---|---|---|
| One straight tween on Step Nc | 44 | 106 |
| Two legs: first on an auto-advancing Transition, last on Step Nc | 5 | 11 |
| Three legs: two Transitions, then Step Nc | 1 | 2 |

Of the 106 single-leg tweens 103 carry no rotation at all. The 3 exceptions are the three copies of the LSM nut going on with a spin.

The 6 unique multi-leg seats:

| Guide [frames] | Part | Legs (each 800 ms) |
|---|---|---|
| LSM-F [064] -> [065] T -> [066] | D10 clip onto the lifted matrix | 21.8 mm up, then 39.9 mm across |
| LAC-F [098] -> [099] T -> [100] T -> [101] | F9 upright | 103.9 mm across, tilt 25.8 deg (15.0 mm), drop 33.0 mm; stays tilted |
| LAC-F [125] -> [126] T -> [127] | F2 back | 78.1 mm slide while tilted 21.4 deg, then swing flat (28.2 mm, 21.4 deg) |
| PMG-F [091] -> [092] T -> [093] | H11 bracket | 53.1 mm down, then 6.7 mm sideways lock |
| PMG-F [094] -> [095] T -> [096] | H12 bracket | 44.5 mm down, then 7.6 mm sideways lock |
| PMG-F [113] -> [114] T -> [115] | H14 face plate | 57.8 mm in while tilted 10.3 deg, then 3.0 mm + 12.6 deg |

Alternative used when the second stage needs a different camera: the second stage is its own numbered step whose Step N shows the part resting in the intermediate pose (8 unique: LSM D3 24/25, LSM D11 32-33/34, LAC F9 45/46, LAC F7 41/42/44, PMG H5 29/30, H6 31/32, H7 35/36, H10 40/41).

### 2.6 Second stages, swings and other small moves (Full Builds)

| Guide | Step [N idx] | Part | Centroid travel mm | Rotation deg | Implied pivot radius mm | Part size mm |
|---|---|---|---|---|---|---|
| LAC-F | 29 [063] | knob (adjust) | 0.0 | 49.8 | - | [16.0, 17.0, 16.0] |
| LAC-F | 42 [092] | F7 (manip-out) | 8.4 | 15.1 | 32.0 | [3.0, 76.6, 20.1] |
| LAC-F | 42 [092] | F7 (manip-out) | 8.7 | 16.0 | 31.3 | [3.0, 76.6, 20.1] |
| LAC-F | 44 [096] | F7 (seat) | 8.4 | 15.1 | 32.0 | [3.0, 76.6, 20.1] |
| LAC-F | 44 [096] | F7 (seat) | 8.7 | 16.0 | 31.3 | [3.0, 76.6, 20.1] |
| LAC-F | 46 [102] | F9 (seat) | 15.9 | 25.8 | 35.6 | [31.2, 76.6, 3.0] |
| LSM-F | 25 [055] | D3 (seat) | 16.8 | 21.6 | 44.8 | [94.4, 50.8, 3.2] |
| LSM-F | 34 [075] | D11 post (seat) | 7.0 | 0 | - | [3.0, 79.7, 15.9] |
| PMG-F | 30 [067] | H5 (seat) | 28.4 | 23.6 | 69.4 | [137.8, 3.4, 139.3] |
| PMG-F | 32 [071] | H6 (seat) | 21.8 | 18.1 | 69.3 | [109.6, 3.3, 139.3] |
| PMG-F | 36 [079] | H7 (seat) | 14.3 | 11.7 | 70.1 | [109.6, 3.3, 139.3] |
| PMG-F | 41 [089] | H10 (seat) | 4.1 | 7.9 | 29.8 | [78.6, 3.0, 145.7] |

The implied pivot radius is the centroid travel divided by 2 sin(angle / 2). It is 0.85-1.0 of half the panel dimension across the hinge (H5 / H6 / H7: 69-70 mm for 139 mm panels; D3: 44.8 for 94.4; F9: 35.6 for 76.6), i.e. the panel turns about its engaged edge. Cadasio stores that pivot: 557 of the 576 rotation writes larger than 1 deg in the 20 payloads have a custom `origin` on the part (97 %).

## 3. Rotation

Rotation is rare and is used for exactly four things.

| Use | Angle | Where | Count |
|---|---|---|---|
| Hook-in panel is tilted (already at hover, or on a Transition leg for LAC F9) and later swings flat about its engaged edge | 7.9 / 10.3 / 11.7 / 18.1 / 21.4 / 21.6 / 23.6 / 25.8 deg | PMG H10, H14, H7, H6; LAC F2; LSM D3; PMG H5; LAC F9 | 8 unique parts |
| Flexing two posts apart and back | 15.1 and 16.0 deg | LAC F7 pair, LAC-F [093], [097] | 1 unique |
| Threaded part spins about its travel axis while it travels | 115.1-179.6 deg | LSM nut off [035] and on [040]; LAC nut off [050] 175.9 deg, washer off [053] 123.6 deg | 11 tweens over all guides (5 unique) |
| Turning a knob in place | 49.8 deg, 0 mm | LAC-F [064] | 1 unique |

- The end pose is stored as a quaternion, so the largest spin one step can encode is 180 deg; no step shows more than half a turn.
- Spin is not applied consistently: the LAC nut does not spin going back on (LAC-F [060], 0 deg), the LAC knob and washer do not spin going on, and the LSM nut spins 179.3 deg going on in Part 2 [022] but 115.1 deg in the Full Build [040].
- Ordinary insertions never rotate (103 of 106 single-leg first-stage tweens).

## 4. Removals inside build guides

| Guide | Step [N idx] | Part | Travel mm | Axis | Spin deg | Frame that moves | Duration ms | Then |
|---|---|---|---|---|---|---|---|---|
| LAC_full_build | 1 [001] | Paper | 53.2 | -Y | 0 | Transition | 800 | hidden at [003] |
| LAC_full_build | 22 [046] | knob | 37.6 | -Y | 0 | Transition | 800 | hidden at [048] |
| LAC_full_build | 23 [049] | nut | 37.9 | -Y | 175.9 | Transition | 800 | hidden at [051] |
| LAC_full_build | 24 [052] | Washer | 37.9 | -Y | 123.6 | Transition | 800 | hidden at [054] |
| LSM_full_build | 1 [001] | Paper | 39.3 | -Y | 0 | Transition | 800 | hidden at [003] |
| LSM_full_build | 16 [034] | push button | 100.7 | -Z | 179.6 | Transition | 1600 | hidden at [036] |
| LSM_part_1 | 1 [001] | Paper | 48.3 | -Y | 0 | Step Nc | 800 | hidden at [003] |
| LSM_part_2 | 8 [016] | push button | 98.9 | -Z | 170.9 | Transition | 1600 | hidden at [018] |
| LSM_part_1_2 | 1 [001] | Paper | 48.3 | -Y | 0 | Step Nc | 800 | hidden at [003] |
| LSM_part_1_2 | 16 [032] | push button | 98.9 | -Z | 170.9 | Transition | 1600 | hidden at [034] |
| LAC_part_2 | 8 [016] | knob | 37.6 | -Y | 0 | Transition | 800 | hidden at [018] |
| LAC_part_2 | 9 [019] | nut | 37.9 | -Y | 175.9 | Transition | 800 | hidden at [021] |
| LAC_part_2 | 10 [022] | Washer | 37.9 | -Y | 123.6 | Transition | 800 | hidden at [024] |
| LAC__part_1 | 1 [001] | Paper | 53.2 | -Y | 0 | Transition | 800 | hidden at [003] |

Pattern: Step N shows the part still in place (with an arrow); an auto-advancing Transition tweens it straight off along its axis and leaves it hanging there; Step Nc fades it out. 12 of 14; the two exceptions (LSM Part 1 and Part 1+2 peel) put the tween on the c-step and hide the sheet on the next step. Travel: 37.6-37.9 mm for knob / nut / washer on a 12-17 mm part (2-3 part widths); 98.9-100.7 mm for the LSM nut, because it has to pass the tips of the 75 mm leads (LSM-F [035]); 39.3-53.2 mm for the backing sheet. Hardware goes back on from a larger distance than it came off (55.9-61.3 mm vs 37.6-37.9 mm).

## 5. Wires

### 5.1 Counts per guide

| Guide | wire-connection swaps (loose -> routed) | routed wire fades in, no loose model | fan-out / separation tween | wires riding a rigid part | wired sub-assembly re-pose swaps |
|---|---|---|---|---|---|
| LAC_deconstruction | 20 | 0 | 0 | 2 | 5 |
| LAC_full_build | 20 | 1 | 3 | 2 | 8 |
| LSM_deconstruction | 3 | 0 | 1 | 0 | 2 |
| LSM_full_build | 8 | 1 | 0 | 1 | 4 |
| LSM_part_2 | 7 | 2 | 0 | 0 | 1 |
| LSM_part_3 | 0 | 0 | 0 | 0 | 1 |
| LSM_part_3_4 | 0 | 0 | 0 | 0 | 4 |
| LSM_part_4 | 0 | 0 | 0 | 0 | 2 |
| LSM_part_1_2 | 7 | 2 | 0 | 0 | 1 |
| LAC_part_2 | 8 | 0 | 1 | 2 | 0 |
| LAC_part_3 | 6 | 1 | 1 | 0 | 0 |
| LAC_part_4 | 0 | 0 | 0 | 0 | 8 |
| LAC__part_1 | 6 | 0 | 1 | 0 | 0 |
| PMG_deconstruction | 0 | 0 | 0 | 0 | 4 |
| PMG_part_1 | 12 | 0 | 1 | 0 | 0 |
| PMG_part_2 | 9 | 0 | 1 | 1 | 0 |
| PMG_part_3 | 0 | 0 | 0 | 0 | 8 |
| PMG_full_build | 21 | 0 | 2 | 1 | 8 |

The LSM rows of the first column each include one ribbon-split swap (joined ribbon -> split ribbon), which is a shape change, not a connection.

- 101 wire-connection steps in 10 build guides (48 in the Full Builds: PMG 21, LAC 20, LSM 7). In all 101 the routed wire fades in on the c-step and the loose model fades out; none tweens. 100 of 101 add exactly one routed wire; LSM-F Step 19 [041]-[042] adds the two push-button leads together.
- 0 of the 101 hover steps carry a lead line or an arrow (cross-checked against the digest annotation lists). 116 of 116 first-stage tween-insertion steps carry lead lines. Lead line and tween go together; wire and swap go together.
- 7 further steps fade a routed wire or cable in with no loose model to remove: the plugged USB cable (LAC-F Step 40 [089], LAC Part 3 Step 8, LSM-F Step 20 [045], LSM Part 2 Step 13, LSM Part 1+2 Step 21) and the push-button leads in LSM Part 2 Step 11 and Part 1+2 Step 19.
- The loose model first appears in the same Step N in 64 of 101; in 37 it was already on screen (captive leads of switch, potentiometer, buzzer and push button; the hanging ribbon in LSM; the first wire after a ribbon-split step).

### 5.2 Where the loose wire is shown (Full Builds; centroid of loose model to centroid of routed model)

| Kit | Loose model | n | Distance to routed position mm (min / median / max) | Where it sits |
|---|---|---|---|---|
| LSM | ribbon end / wire end hovering at its target | 7 | 13.8 / 16.8 / 25.8 | 8-16 mm sideways and 7-11 mm above or below the routed wire's centroid; LSM-F [021], [023] |
| LAC | fresh straight jumper | 10 | 80.3 / 106.2 / 127.2 | lying flat beside the base on the camera side: 76-118 mm sideways, 22-56 mm above the routed wire's centroid; LAC-F [019]-[029], [079]-[085] |
| LAC | captive lead, straight, still hanging from its component | 10 | 37.9 / 78.5 / 119.3 | wherever the component is; LAC-F [034]-[039], [065]-[075] |
| PMG | fresh straight jumper | 20 | 49.3 / 53.5 / 77.5 | lying flat in front-left of the shield: 47-57 mm sideways for the buttons, 70-77 for the display, 49-54 for the matrix, 4-18 mm below the routed centroid; PMG-F [007]-[055] |

The parking spot is constant within a wiring run. LAC-F Steps 10-14: all five wires within 0.8 mm of the run's mean position; Steps 36-39: within 2.2 mm. PMG-F Steps 3-14: each wire is 1.7-1.8 mm from the previous one (it keeps its slot in the fanned-out ribbon), 19 mm drift over 12 wires; the spot jumps 40 mm between the display run and the matrix run.

So two styles exist. LSM (the earliest project) hovers the loose end at its destination. LAC and PMG park the whole loose wire at a fixed spot one to two wire-lengths away and let labels say where it goes. LSM is also the only kit that connects one wire END per step, so each wire has a "near end seated" model and a "both ends seated" model.

### 5.3 Where a wire really does move

| Case | Instances (all guides) | Size |
|---|---|---|
| Ribbon or wire pair spread apart in a prep step, shown isolated | 10 (LAC-F Steps 8, 19, 35; PMG-F Steps 2, 15; and their part-guide copies) | sideways in the ribbon plane only: PMG 12 wires 1.1-17.3 mm (about 3.1 mm per wire position), PMG 9 wires 0.9-11.9 mm, LAC 4-way 8.4 / 11.3 / 14.4 mm (one wire stays), LAC pair 10.7 and 9.2 mm, LAC 6-way 4.4-15.2 mm (one wire stays, about 5.6 mm per wire position) |
| Captive leads riding rigidly with their component in a normal hover-to-seat tween | 7 in build guides (LAC switch + 3 leads 81.2 mm [033]; LAC potentiometer + 3 leads 79.0 mm [056]; LSM button + 2 leads 102.5 mm [038]; PMG USB plug + cable stub 22.9 mm [058]), 2 in LAC Deconstruction | same vector as the component |
| A loose wire kept on screen from the prep close-up is moved to the parking spot as the assembly fades back in | LAC-F [019] 177.3 mm, [042] 150.4 mm; PMG-F [037] 11.9 mm; LSM Part 2 [003] 3.4 mm | happens together with a camera move and the context fading back in; LAC-F [019] is under a step-level fade, [042] is not, so there the straight wire is seen sliding 150 mm |
| Deconstruction only: connector pulled off with a tween | LSM Deconstruction Step 15 (3-way connector, 30.5 mm, Transition), LAC Deconstruction Step 25 (USB cable and adaptor, 43.3 mm) | along the pin axis |
| Deconstruction only: wire bundle slides while it fades out | PMG Deconstruction Step 18 (5 wires, 89.9 mm), Step 22 (4 + 12 wires, 74.7 and 36.4 mm) | one vector per bundle |

No wire is ever tweened from loose to routed, and no routed wire is ever deformed.

## 6. Wired sub-assemblies: pose copies cross-faded

Any rigid part with wires attached is moved by fading one complete copy (part + its routed wires + housings) out and another in. 45 such step pairs in the 16 build guides, 20 in the Full Builds (LSM 4, LAC 8, PMG 8), 11 in the deconstruction guides.

| Guide | Step [frame] | Part re-posed | Jump between the two copies mm | Direction | Wires swapped with it |
|---|---|---|---|---|---|
| LAC-F | 43 [095] c | Piezo Buzzer | 170.2 | -Z | 2 |
| LAC-F | 47 [105] c | potentiometer | 519.6 | -Z | 3 |
| LAC-F | 47 [105] c | F1 | 501.6 | -Z | 3 |
| LAC-F | 48 [107] c | F4 | 122.2 | +X | 3 |
| LAC-F | 49 [110] c | Rocker Switch | 49.8 | -Y | 3 |
| LAC-F | 51 [114] c | LCD V1 | 84.8 | +Y&-Z | 4 |
| LAC-F | 52 [117] Transition | LCD V1 | 23.3 | -X&-Z | 4 |
| LAC-F | 52 [118] c | LCD V1 | 14.9 | +Z | 4 |
| LAC-F | 53 [120] c | F1 | 211.4 | +X&+Z | 3 |
| LAC-F | 53 [120] c | potentiometer | 217.1 | +X&+Z | 3 |
| LAC-F | 54 [122] c | potentiometer | 76.6 | -X | 3 |
| LSM-F | 21 [047] c | D2 | 56.9 | -Z | 2 |
| LSM-F | 23 [051] c | 8x8 LED | 184.4 | -X | 3 |
| LSM-F | 28 [063] c | 8x8 LED | 107.8 | +X&+Y | 3 |
| LSM-F | 30 [068] c | 8x8 LED | 56.8 | -Y | 3 |
| PMG-F | 33 [074] c | Big Button Module | 142.0 | -X&-Y | 3 |
| PMG-F | 34 [076] c | Big Button Module | 142.8 | -X | 9 |
| PMG-F | 45 [100] c | Ensamblaje_Shield_NANO | 170.7 | -X&+Y | 22 |
| PMG-F | 46 [102] c | Ensamblaje_Shield_NANO | 107.0 | -Y | 22 |
| PMG-F | 47 [104] c | Display TM1637 | 143.3 | -X&+Y&+Z | 4 |
| PMG-F | 48 [106] Transition | Display TM1637 | 11.1 | -Y | 4 |
| PMG-F | 48 [107] c | Display TM1637 | 3.3 | +X | 4 |
| PMG-F | 49 [109] c | LED Matrix 32x8 - 4 Modules  | 195.1 | -X&-Z | 1 |
| PMG-F | 50 [111] Transition | LED Matrix 32x8 - 4 Modules  | 20.4 | -Y | 5 |
| PMG-F | 50 [112] c | LED Matrix 32x8 - 4 Modules  | 6.1 | +X | 5 |

- Usual shape (7 of the 10 wired sub-assemblies in the Full Builds: LSM matrix; LAC F1, F4, LCD; PMG shield, display, matrix): two numbered steps. First a "pick it up" step whose c-frame swaps to a copy near the mount (jump 85-211 mm; LAC Step 47 additionally carries F1 502 mm across the layout). Then an "attach" step whose Step N shows that copy with lead lines or an arrow, and whose c-frame swaps to the seated copy. The other 3 go in one step (LSM D2 + button [047], LAC buzzer [095], PMG button modules [074], [076]).
- The jump of the final attach swap is a normal hover distance when the part has tabs: LAC F4 + switch 49.8 mm [110], LAC F1 + potentiometer 76.6 mm [122], LSM D2 + button 56.9 mm [047], LSM matrix + D10 56.8 mm [068]. Shield onto the housing: 107.0 mm with an 80 mm arrow, PMG-F [102].
- Hook-on modules get a flipbook: one extra copy on an auto-advancing Transition between Step N and Step Nc. LAC LCD 84.8 -> 23.3 -> 14.9 mm ([114], [117], [118]); PMG display 143.3 -> 11.1 -> 3.3 mm ([104], [106], [107]); PMG matrix 195.1 -> 20.4 -> 6.1 mm ([109], [111], [112]).
- One-step swaps jump further because there is no hover copy: LAC buzzer 170.2 mm [095]; PMG button modules 142 mm [074], [076].
- Sub-assemblies are built in an isolated view first, where the rigid tween is allowed because nothing else is attached: LSM button + nut on D2 with only those parts on screen (LSM-F [034]-[040]), LAC switch in F4 ([031]-[033]), LAC potentiometer in F1 ([046]-[064]), LSM D10 clipped onto the lifted matrix in mid-air ([064]-[066]). After that they only move by pose swap.
- Number of modelled copies: LSM 8x8 matrix 5; LAC F1 4, F4 3, LCD 4, switch 3, potentiometer 4, buzzer 2; PMG display 4, matrix 4, shield 3, button modules 2 each.

Shape changes use the same mechanism: straight-lead resistor -> bent-lead resistor (LSM-F [008] -> [009], [015] -> [016]; LAC-F [008] -> [009]), joined ribbon -> split ribbon (LSM-F [019] -> [020]). 11 step pairs over all guides, never a morph. The bent model appears already at hover height above its seat (29-40 mm) so the next Step N only has to bring the context back.

## 7. Parts that fade in already in place

First appearances in the three Full Builds that never tween:

| When | What | Where |
|---|---|---|
| Step N, new part is the stationary receiver; the part in the student's hand is the one that hovers | LSM D1 base [004] (breadboard drops onto it), LSM D2 [037] (button goes into it), LAC F3 [004], LAC F4 [032], LAC F1 [055], PMG H1 [059] (H2 hovers next to it) | 6 |
| Step Nc, the rest of an identical set after one exemplar was animated | LSM 63 stems [086] after 1 stem [083]-[084]; PMG 3 keys [086] after 1 key [083]-[084] | 2 |
| Auto-advancing Transition, next identical peripheral appears before its first wire | PMG button modules 2-4 at [013], [020], [027] | 3 |
| Section card, then simply present when the assembly returns; never "placed" by a step | LAC buzzer [071], LAC LCD [078], PMG button 1 [006], display [034], matrix [045], LSM LED matrix [028] | 6 |
| Step Nc, cable fades in plugged, no travel | LAC USB 40c [089], LSM USB 20c [045] | 2 (PMG USB instead tweens 22.9 mm, [058]) |
| Step Nc, every routed wire | 48 | see section 5 |

## 8. Isolation views and the parts overview

- A prep step or a section card hides everything else and shows one part (or one sub-assembly) alone; the next Step N brings the context back. In the three Full Builds: 22 hide events (LSM 8, LAC 9, PMG 5: 12 on cards, 9 on a Step N, 1 on a c-step) and 23 restores, 22 of them on a Step N.
- LSM and LAC mark most of these scene swaps with the step-level `transition: fade` (13 of 17 hides in the two Full Builds; 65 of 1037 steps overall). PMG never sets it (0 of 5 hides).
- On a card the part is usually already standing at the hover pose it will have in the following step, so restoring the context is a pure fade: LAC RTC [014] at +33.6 mm, LAC switch [031] at +81.2 mm, PMG USB plug [056] at +22.9 mm, LSM stem (Part 3+4 [037]).
- "Parts laid out" exists only in the LAC Electronics guide: 2 static views, no hover, no seat, no tween of interest. [000] nine electronic kit items in one diagonal row in their as-assembled orientation, [001] nine wood panels F1-F9 in part-number order, all turned edge-on to one orientation and one height. Pre-attached leads stay attached and move as one group. Build guides never lay parts out; the only staging they do is the parked loose wire (section 5.2) and loose wired modules lying beside the base.

## 9. Moves caused by state carry-over (report as anomalies, not conventions)

13 of the 119 first-stage movers were already on screen and visibly travel to their hover pose when the step is entered:

| Guide [frame] | Part | Slide to hover mm | Cause |
|---|---|---|---|
| LSM Part 1 [001], LSM Part 1+2 [001], LSM-F [001], LAC Part 1 [001], LAC-F [001] | breadboard | 39.3 / 39.3 / 49.2 / 46.9 / 46.9 | title page shows it seated; Step 1 lifts it for the peel and it stays up until Step 2c |
| LSM Part 3 [001] | D4 | 69.4 | title page shows the end state |
| LSM Part 4 [001] | D9 pair | 68.0 | same |
| LAC Part 4 [001] | F7 pair | 80.3 | same |
| PMG Part 3 [001] | H2 | 40.0 | same |
| LAC Part 2 [001] | switch | 81.2 | same, on the card |
| LAC Part 2 [025], LAC-F [055] | potentiometer | 79.1 | shown at its seat in empty space for Steps 22-24, backs off when panel F1 appears |
| LSM Part 1 [012] | capacitor | 69.5 | returns from its card, where it was moved aside and scaled x2 |

Other residues seen: LSM-F Nano is shifted 2.3 mm sideways with no step explaining it at Step 38 [085]; LSM Part 3+4 stems sit 9.7 mm high at 18c [040] and drop on the final view; PMG H14 moves about 1 mm and 2.5 deg more on Completed View (PMG-F [116], Part 3 [058]); the LAC nut is re-angled 21.4 deg on Step 30 (LAC-F [065]).

## 10. Deconstruction guides

| | LSM Decon (24 steps) | LAC Decon (47 steps) | PMG Decon (23 steps) |
|---|---|---|---|
| Rigid part tweens off on an auto Transition, then is hidden on Step Nc | 16 | 14 | 0 |
| Rigid part tweens on the c-step and stays on screen | 0 | 6 (switch, potentiometer pulled out of their panels; 3 refits; F7 spread) | 1 (H10, hidden on the next step) |
| Part gets its displacement and `visible = false` in the same frame (slides while fading) | 1 (D5, Step 4c) | 0 | 12 (9 rigid, 3 wire or cable bundles), plus 6 where a first-stage tween on a Transition precedes it (H14, H12, H11, H7, H6, H5) |
| Cross-fade between pose copies / routed and loose wire | 5 | 25 | 4 |
| Plain fade-out | 2 | 2 | 0 |

- Removal travel (41 tweened removals): min 2.5, quartiles 31.3 / 53.1 / 67.8, max 106.3 mm. Plug-in components 21.7-55.0 mm, hardware 52.8-58.7, panel-mount modules 66.7-94.8, wood 2.5-106.3.
- The removal vector is the build's hover-to-seat move reversed. Travel equals the build travel within 1 mm for 19 of 53 matched removals: LAC F2 106.3, F5 56.0, F6 67.5, F8 94.2; LSM D7 67.8, D8 54.1, capacitor 29.1, resistor 2 30.3; PMG H4 65.0, H5 117.1 + 28.4, H6 122.4 + 21.8, H7 139.4 + 14.3, H8 94.5, H11 53.1 + 6.7, H12 44.5 + 7.6, H13 80.1. The rest were re-set by hand (LAC Nano 55.0 vs 39.8; LSM stems 62.5 vs 43.5; PMG keys 142.5 vs 107.7).
- Two-stage joints are undone in reverse order with one Transition: PMG Decon [019] -> [020] T (H12 unlock 7.6 mm) -> [021] (lift 44.5 mm while fading); LAC Decon [004] -> [005] T (F2 tilt 21.4 deg) -> [006] T (slide 78.1 mm) -> [007].
- Wires are not animated except the three cases in section 5.3.
- Three steps in LAC Decon are insertions (washer 53.6, nut 37.8, knob 42.6 mm back onto the loose potentiometer, [043]-[048]) and follow the build pattern.

## 11. Animation timing settings

| Guide | viewer steps | 800 ms | 1600 ms | pause | play | step transition = fade |
|---|---|---|---|---|---|---|
| LAC_deconstruction | 130 | 128 | 2 | 99 | 31 | 0 |
| LAC_electronics | 2 | 2 | 0 | 2 | 0 | 0 |
| LAC_full_build | 131 | 131 | 0 | 121 | 10 | 13 |
| LSM_deconstruction | 69 | 69 | 0 | 50 | 19 | 4 |
| LSM_full_build | 88 | 87 | 1 | 82 | 6 | 13 |
| LSM_part_1 | 19 | 19 | 0 | 19 | 0 | 3 |
| LSM_part_2 | 31 | 29 | 2 | 30 | 1 | 4 |
| LSM_part_3 | 13 | 13 | 0 | 12 | 1 | 1 |
| LSM_part_3_4 | 43 | 43 | 0 | 39 | 4 | 2 |
| LSM_part_4 | 29 | 29 | 0 | 27 | 2 | 2 |
| LSM_part_1_2 | 47 | 45 | 2 | 46 | 1 | 7 |
| LAC_part_2 | 42 | 42 | 0 | 39 | 3 | 4 |
| LAC_part_3 | 21 | 21 | 0 | 21 | 0 | 4 |
| LAC_part_4 | 42 | 42 | 0 | 36 | 6 | 1 |
| LAC__part_1 | 32 | 32 | 0 | 31 | 1 | 7 |
| PMG_deconstruction | 61 | 61 | 0 | 47 | 14 | 0 |
| PMG_part_1 | 34 | 34 | 0 | 31 | 3 | 0 |
| PMG_part_2 | 27 | 27 | 0 | 27 | 0 | 0 |
| PMG_part_3 | 59 | 59 | 0 | 54 | 5 | 0 |
| PMG_full_build | 117 | 117 | 0 | 109 | 8 | 0 |
| **Total** | 1037 | 1030 | 7 | 922 | 115 | 65 |

- Step duration: 800 ms on 1030 of 1037 viewer steps (99.3 %). 1600 ms on 7: the LSM nut spin (Transition [035] in LSM-F, [017] in Part 2, [033] in Part 1+2; c-step [022] in Part 2 and [038] in Part 1+2) and two flipbook Transitions of the LCD in LAC Deconstruction ([016], [017]). The other 6 spin tweens run at 800 ms.
- Part animation options, identical on 1037 of 1037 steps: move = `tween`, show = `fade`, hide = `fade` (2 steps add `animation_attention: none`).
- Camera options, identical on all steps: move = `tween`, `animate_orbit` = false, `animation_speed` = 2.
- 2D annotation options, identical on all steps: move = `tween`, show = `fade`, hide = `fade`, `animation_behaviour_visibility` = `separate_visibility`.
- `animationChained` = false on all steps. Project flags on all 20 guides: `animateStepsViewer` true, `animatePreviousStep` true (going back is animated too), `edgesVisibleOnAnimate` true, `autoStart` true, `playStepTimeout` null.
- 922 steps wait for the student (`pause`), 115 auto-advance (`play`). All 115 are Transition steps; 2 Transitions in LAC Deconstruction are `pause` by mistake ([033], [118]). What the 115 carry: a part tween 67 (58 %), a cross-fade or fade 33 (29 %), camera or annotation only 15 (13 %). 108 of the 115 hide the navigation overlay and are hidden from the step picker.
- Camera travel and part travel never share a step: the camera is unchanged on 424 of 424 c-steps and on all 67 Transitions that tween a part; the 12 Transitions that move the camera change no part. The camera moves on 266 of 425 Step N frames, together with the fade-in of the hovering part.
- One step holds at most one motion leg per part. A multi-leg move is therefore 800 ms per leg with no dwell between legs: 1.6 s for two legs, 2.4 s for three.
- The easing curve is not in the data.

## 12. Rules extracted (summary)

1. Two beats per rigid part: fade in at the hover pose (Step N), one tween home (Step Nc). Never move a part while it is fading in.
2. Step Nc is a single straight 800 ms translation with no rotation; extra legs go on auto-advancing Transition steps, or the stage becomes its own numbered step when it needs a new camera.
3. Hover offset = reverse of the physical path. Electronics come straight down; panels come along their tab axis; hook-in panels arrive tilted by their swing angle.
4. Hover distance is set per part by fit type (table 2.2), not by a constant and only loosely by size.
5. Rotation only for swing-to-seat, flex, threaded spin and knob turn.
6. Wires are swapped, never tweened: loose straight wire in Step N, routed wire in Step Nc, one wire per step, loose wire parked at a fixed spot per run.
7. Anything with wires attached is re-posed by cross-fading whole copies; build it in an isolated view first.
8. The receiving part, repeats of an animated exemplar, free-standing modules and plugged cables fade in already in place.
9. Removal = hold, auto-tween out along the axis, fade.
10. Deconstruction = the build's hover move reversed, on the Transition; wires cross-fade.
11. 800 ms for everything; 1600 ms only where a threaded spin was given extra time.

## 13. Numeric defaults an in-house player should use

| Setting | Default | Basis |
|---|---|---|
| Step animation duration | 800 ms | 1030 of 1037 steps |
| Part move / show / hide | tween / fade / fade, all over the step duration | 1037 of 1037 |
| Camera | tween, no orbit animation, never in the same step as a part tween | all steps; camera fixed on 424 of 424 c-steps and 67 of 67 motion Transitions |
| Legs per press | 1; further legs as auto-advancing steps of 800 ms each, no dwell | 13 multi-leg seats; 115 play steps |
| Threaded spin | 180 deg about the travel axis; allow 1600 ms | spins 115-180 deg; 1600 ms on 5 of 11 |
| Hover, plug-in board or passive into breadboard / socket | 35 mm straight up | 22 values 29.1-44.1, median 34 |
| Hover, breadboard onto base | 47 mm up | 39.3-49.2, median 46.9 |
| Hover, USB plug | 23 mm along the socket axis | 22.9 (2 copies of 1) |
| Hover, panel-mount part with leads | 80 mm; 100 mm when body plus trailing leads is longer than 70 mm (hover is 1.2-1.4 x that length) | 79.1-103.2, median 81.2; LSM button 103 mm for 75 mm of button and leads |
| Hover, washer / nut / knob onto a shaft | 60 mm along the shaft | 55.9-61.3, median 60.5 |
| Hover, flat panel face-on | 60 mm along the tab axis | 42.0-69.4, median 64.7 |
| Hover, part sliding lengthwise or edge-on | 1.0 x its extent along the travel, clamped to 40-140 mm | ratio quartiles 0.8 / 1.0 / 1.6; values 40.0-139.4 |
| Hover, anything else | 60 mm | overall median 60.9, quartiles 43.5 / 81.5 |
| Tilt of a hook-in panel at hover | its swing angle, 20 deg if unknown | 7.9-25.8, median of 8 = 19.8 |
| Swing to seat | rotate about the engaged edge, own step or own leg, 800 ms | 8 unique; pivot radius 0.85-1.0 of half panel |
| Push-home stage | leave 7 mm proud, finish in a later step | LSM D11, 4 posts, 3 guide copies |
| Removal inside a build | 38 mm along the axis for small hardware; past the lead tips (100 mm) for a nut on a wired part | 37.6-37.9; 98.9-100.7 |
| Deconstruction travel | the build's hover distance for that part | equal within 1 mm for 19 of 53; median 53.1 |
| Loose wire parking | flat, straight, camera side, 50-60 mm from the routed position for a 58 mm jumper on a compact board, 80-125 mm on a spread-out layout; same spot (within 2 mm) for the whole run | PMG median 53.5; LAC median 106.2; run spread 0.8-2.2 mm |
| Ribbon fan-out | 3 mm per wire position (many wires) to 5.5 mm (few wires), in the ribbon plane | PMG 3.1 mm; LAC 5.6 mm |
| Wire connection | cross-fade loose -> routed in one 800 ms step, one wire per step | 101 of 101 |
| Wired sub-assembly | cross-fade whole copies; attach copy 50-77 mm off the seat for tabbed panels; up to 3 frames for hook-on modules | 49.8 / 56.8 / 56.9 / 76.6 mm; 3 flipbooks |

## 14. Open questions

1. Easing of the tween is not stored in the payload (linear or eased?). Needs one look at the live viewer.
2. What the viewer draws when a part changes pose and visibility in the same step is not knowable from data. Build authoring avoids it for show (97 of 99 hover poses are pre-staged while hidden); PMG Deconstruction relies on it for hide (18 removals). Should the in-house player really slide a part while it fades out?
3. Does Cadasio interpolate a rotation about the stored pivot (`origin`) or lerp position and slerp rotation separately? For a 20 deg swing the two differ by a few millimetres at the hinge.
4. Does a step-level `transition: fade` suppress part tweens (cut) or play both? It decides whether the 177 mm loose-wire relocation at LAC-F [019] and the 47-49 mm breadboard lift on Step 1 (LAC-F [001], LSM-F [001], both under a fade) are ever seen as motion.
5. Is 1600 ms for a threaded spin intended? It exists only in LSM and was dropped from one of the two LSM spin steps in the Full Build.
6. Is the difference between hovering the loose wire end at its hole (LSM) and parking the wire beside the model (LAC, PMG) a deliberate change of house style? LSM is the older project.
7. Should hover distances be standardised by class in the in-house tool (section 13), or kept free per part as they are now?
8. Scale changes were not tracked here (the LSM capacitor is shown x2 on its Part 1 card per the reader report).
