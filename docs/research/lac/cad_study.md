# LAC: what the CAD says (lac.glb)

Source: `LAC Build Instructions/LAC Full Build.STEP` (SolidWorks 2026, exported 19 Oct 2026 01:08), converted by `tools/step_to_glb.py`
to `lac.glb` (55 MB; 40 s, 2.1 GB peak). 159 top-level instances NAUO1 - NAUO159. Millimetres in assembly space, Y up, as assembled
(the same frame TechBox's published Cadasio project uses: its root box is identical). Scripts: `docs/research/lac/scripts/`
(steptree.py, dups.py, wires3.py, poses.py, make_wire_paths.py, lac_atlas.py; `lacload.py` loads instances from the GLB without
trimesh). Written 19 Oct 2026 for the first draft of the guide.

## 1. Summary

1. **The engineer's export carries most parts several times, once per pose** (the copies the published guide swaps between). The
   guide shows each part once, seated, and moves it: `LAC Build Instructions/trim_source.py` cuts lac.glb down to the 52 instances it
   uses (`lac-guide.glb`, 7.4 MB), which keeps each generator run light (about 15 - 30 s, small memory).
2. **Missing from the export: F2, F5 and F6** (the back panel and the two end panels; the published guide's Steps 55 - 57), **and F4
   seated**. F4 exists once, lying flat beside the base (NAUO50); seated it is that panel moved +117.68, -17.26, +0.06 mm, exactly the
   move between the rocker switch's flat and seated copies (NAUO51 -> NAUO46): the guide uses extra part `F4` (`f4.glb`, cut from
   NAUO50). Lee sent F2, F5 and F6 as STEP files of their own on 19 Oct 2026: section 7.
3. **Broken or doubled copies** (Lee: "some of which are broken"): the LCD lying face down (NAUO95) has no display (only the I2C
   backpack); two coin cells side by side (NAUO4 in the holder, NAUO5 half out of it); the dark red jumper (NAUO32) ends in a14,
   the hole the white one uses (the published guide: a12); several wire bodies Cadasio never shows (Part29/30, Part34-36/39,
   Part44/45/47/48), which turn out to be the leads in poses the guide uses (below).
4. **Reused from the MRA (Lee, 19 Oct 2026)**: the Nano Board (NAUO124 is the MRA's Nano model, 387,505 triangles here; the MRA's
   export of it, 380,001, is cut by `tools/cut_part.py` to sit exactly where NAUO124 is: `nano-mra.glb`); the USB cable's A end
   (NAUO121 is the MRA's `USBCableend` model, fitted vertex for vertex: `usb-a-end.glb`); the female Dupont cap ("Wire Cap") is the
   MRA's part already. The Mini-B end is a right-angle plug ("USB Right Angle"), unlike the MRA's and RCC's straight one: kept.
5. **Colours**: none in the STEP; from TechBox's published LAC Cadasio project per solid (`colour-atlas-lac.json`, every atlas match
   87 - 100 %, the LCD board 49 % taken nearest-first), the Nano's from the MRA's atlas.

## 2. The parts (seated copies the guide uses)

| id | part | where |
|---|---|---|
| NAUO2 | F3, the base | 85.8 x 3 x 158.8, y 884.6 - 887.6 (F3's underside is the "table") |
| NAUO1 | half breadboard | on F3, x 646.5 - 702.6, z 1264.4 - 1347.4; NAUO141 its backing paper |
| NANO (NAUO124) | Nano Board | rows c and g, columns 1 - 15; USB socket at column 1 (+z) |
| NAUO6 / NAUO7 | resistors | (-) blue rail to h27 / h29; each carries straight legs (Part6^..., omitted) and bent legs (Resistor stem 3) |
| NAUO3 + NAUO4 | real-time clock module (HW-84, DS3231) + CR2025 | pins in j19 - j24, coin cell towards the back |
| NAUO46 | rocker switch, seated in F4 | flat copy NAUO51 in NAUO50, hovering copy NAUO144 (+49.8 y) |
| NAUO10, 11, 12, 13, 146 | F1 (front), potentiometer, nut, knob, washer, seated | F1 copies: NAUO35 76.7 mm in front; NAUO125 face down beside the +z end; NAUO154 face up beyond the -z end |
| NAUO42 / NAUO43 | F7 x2 (a mirror-placed pair) | by the -z end, x 657 - 660 and 690 - 693 |
| NAUO62 | buzzer, clamped between the F7s | lying copy NAUO61 beside the +z end (120 degrees about (1, 1, -1)) |
| NAUO45 / NAUO44 | F9 / F8 | hold the LCD's two ends (z 1354 - 1357 / 1264 - 1267) |
| NAUO94 | LCD 20x4 with I2C backpack, seated behind F1's window | NAUO96 = 14.9 mm short of F9's notches; NAUO95 lying face down (broken) |
| NAUO122 | USB right-angle Mini-B, in the Nano | NAUO121 / USB_A its A end; Part67 the cable |

## 3. The breadboard

Rows a - e towards the front (+x), f - j towards the back; a = x 689.25, b 686.71, c 684.17, d 681.63, e 679.09, f 671.31, g 668.77,
h 666.23, i 663.69, j 661.15; column n at z = 1344.66 - 2.54 n (1 at +z). Rails used: (+) red x 696.68 and (-) blue x 699.2, along the
front edge, holes at z = 1284.92 + 2.54 k (half a pitch from the columns). Hole tops y 897.11. Fitted to the 28 male caps the CAD has
standing in holes; every published label (c15, g1, h27, h29, j19, j24, i21 - i29, a5, a8, a9, a12, a14, b8, b9, j1, j3, j4, j27, j29)
lands on a cap the CAD has there (dark red's a12 cap NAUO30 has no wire in the CAD).

## 4. The wires

Every wire body was reduced to its centre line (ordered along the mesh surface, binned and smoothed: `wires3.py`); radius 0.625 mm
(1.25 mm across). Male caps ("Wire Cap V2"): an 8 mm housing over an 8 mm pin, 4 mm of the pin below the housing; the CAD's wire
ends at the top of the pin, 4 mm inside the housing. All in `LAC Build Instructions/wire-paths.json`.

| wire | ends | CAD body (pose) |
|---|---|---|
| jumpers (M-M) | black i23 - (+), green (-) - i24, purple a8 - i22, blue a9 - i21, white a14 - (-), dark red a12 - (+), orange j1 - i27, yellow j3 - i29 | NAUO18, 23, 27, 24, 29, (32: wrong), 54, 57 (plugged) |
| switch leads | red j27, tan (+), black j29 | 134 - 136 hanging 30 mm (flat F4); 147 - 149 plugged, F4 over the frame |
| pot leads | red (+), tan a5, black (-) | 150 - 152 straight 50 mm (F1 face down beside); 157 - 159 plugged, F1 at the far end (280 - 320 mm) |
| buzzer leads | red j4, black (-) | 90 / 91 straight 39 mm (lying); 60 / 63 plugged (lying); 65 / 64 plugged (clamped) |
| LCD wires (M-F) | GND (-), VCC (+), SDA b8, SCL b9 | 83, 85, 87, 92 (lying); 117 - 120 (short of the notches); 101 - 104 (seated); 109 - 112 (a pose the STEP has no LCD for) |
| ribbons | 6-way M-M (NAUO8), 4-way M-F (NAUO66 - 77), 2-way M-M (NAUO137 - 143) | straight, in the air |
| USB | right-angle plug to the A end | NAUO123 |

TechBox's Cadasio project colours NAUO64 red and NAUO65 black; mapped back to the buzzer's own lead stubs, NAUO64 starts on the
black stub and goes to (-) blue, NAUO65 on the red stub to j4, as the published steps say.

## 5. Poses between copies (all rigid, fitted to 0.0000 mm)

In `wire-paths.json` "poses": F1 flat beside (180 degrees about (-1, 1, 0)/sqrt 2: face down), F1 flat at the far end (90 degrees
about z: face up), F1 in front (+76.66 x, +1.08 z); the potentiometer flat beside is 0.8 degrees off F1's (the guide uses F1's);
switch flat (-117.68, +17.26, -0.06) and over the frame (+49.8 y); buzzer lying; LCD short of the notches (-14.9 z) and lying (180
degrees about (-1, 1, 0)/sqrt 2: face down).

## 6. Wood

Engraved codes (0.25 mm pockets): F3 on its top (714.2, 887.5, 1234.4), F1 outward (723.7, 895.8, 1221.9), F7s outward, F8 towards -z,
F9 towards +z, F4 on its top. Tab tops: F7 at z 1228.4 / 1238.0, F9 at x 693.6 / 697.6, F8 at x 708.3 / 715.7, all y 957.84; F1's
top edge y 957.63 (through F4's front slots).

## 7. F2, F5 and F6 (Lee's STEPs, 19 Oct 2026)

`F2.STEP`, `F5.STEP`, `F6.STEP` (one part each, in its own part frame), converted by `tools/step_to_glb.py` to `f2.glb`, `f5.glb`,
`f6.glb` (extra parts in materials.json). They are placed where TechBox's published Cadasio project has F2-1, F5-1 and F6-1: its scene
is this assembly's frame scaled by 0.6054634 (fitted on F1, F3, the two F7s, F8 and F9 to 0.0006 mm; its F4-1 is the seated F4 above
to 0.004 mm), and its part frames are the STEPs' (`docs/research/lac/cadasio/raw`). Every tab then meets its slot:

- F5 (the breadboard's end, z 1366.07 - 1369.07; F1's and F2's hooks pass through it to z 1372.45): slots for F1's two hooks
  (x 722.33, y 888.4 / 949.8), F3's two tabs (x 663.68 / 701.78) and F4's; engraved code outward (+z) at (652.46, 895.62, 1368.94).
- F2 (the back, x 641.63 - 644.63): hooks at its F5 end (x 643.13, y 888.4 / 949.8, into F5's slots); the slit the USB cable leaves by,
  z 1336.9 - 1341.9 (5 mm), open from F2's bottom edge up to y 901 (rounded top at 902.7); code outward (-x) at (641.75, 895.78, 1358.52).
- F6 (the buzzer's end, z 1210.67 - 1213.67, the hooks through it to z 1207.29), with the speaker slots: slots for F1's and F2's
  hooks (x 722.33 / 643.13, y 888.4 / 949.8) and the tabs of F3 and F4; code outward (-z) at (712.82, 895.74, 1210.8).

In the guide F2 swings about the upright where its outer face meets F5's inside (641.63, z 1366.07), 20 degrees out, as published
(about 21); held 14 mm short of F5 its slit is at z 1327.34 and moves straight in along x, which is where the USB cable lies.

## 8. Wire routes, checked

`tools/wirecheck.py` (with the extra parts loaded) finds no wire in any view passing into a part or another wire (488 such points in
the first draft). The CAD's own routes are kept wherever they were clear; redrawn: the switch's three leads (each in a lane of its own
beside the base; seated, through the closed case), the potentiometer's (lying beside the base: raised over the lying buzzer and LCD
and their wires, crossing F9's plane at x < 689, the black lead crossing over the other two, whose pin is on the far side of them;
stood up in front of the case; seated: under the potentiometer, between the buzzer and F8, along the rails, black behind the LCD's
board), the dark red jumper (a low arch, 8 mm), and the USB cable (out through F2's slit, clear of the breadboard by 1.2 mm and of
the slit by 0.6 mm). The seated routes were found by a path search over a 1 mm grid of the closed case (clearance to every part's
surface and every other wire, A* preferring 3 mm of room) and smoothed into control points (`scripts/routing/`).
The CAD's jumper wires lie as tightly as the engineer drew them (some 0.02 mm apart), within the check's tolerance.
`tools/motioncheck.py` (wires during each move) still finds wires passing briefly through parts or each other mid-move, mostly where a
lead changes shape while its part is carried (README.txt, question 8).

