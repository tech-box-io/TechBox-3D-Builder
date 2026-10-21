# LAC round 1: what the published Cadasio guide does in the steps Lee commented on

Written 20 Oct 2026 for Lee's first round of notes on the LAC guide. Read only: no project file changed.

Sources: `docs/research/lac/cadasio/raw/19075-lac_full_build.json` (one line; cited below as `raw:1`, with the step name and the
component/solid the property sits on), the digest `docs/research/lac/cadasio/19075-lac_full_build.md` (cited `digest:<line>`), its step
pictures `docs/research/lac/cadasio/thumbs/19075-lac_full_build/NNN.jpg`, `LAC Build Instructions/wire-paths.json` (`poses`, `lines`,
`caps`), and our `LAC Build Instructions/guide.py` as committed (HEAD 5253a44; the working copy is being edited by another round-1
job, so `guide.py:N` below means the HEAD line) and `steps.json`.

Numbering: ours = published up to Step 44 (published also has unnumbered cards: Real Time Clock [014], Rocker Switch [031], Alarm
Buzzer [071], LCD Screen [078], USB Cable [087]); our 45 = published 45 + 46; from our 46 on, ours N = published N + 1. `[NNN]` is
the published viewer index, as in the digest.

## 0. How this was read, and four things that matter for every step

Method (scratch scripts, not kept): replay `orderedSteps` (hidden steps included), per solid; a ref's local matrix is its CAD
`transform` with the rotation replaced by the step's `rotation` quaternion and the translation by its `position`; world = product down
the tree; mm = scene units / `scaleFactor` (0.6054633641936558). Each published part's pose is then written relative to the copy
that is our seated part, in our pose form (`[x, y, z]` or `turned(axis, degrees, at, t)`, tools/stepgen.py:122-124). Check: the
published pose copies reproduce `wire-paths.json` `poses` to 0.01 mm and 0.01 degree (F1_flat_beside, F1_flat_other_end,
F1_hover_front, pot_flat_beside/other_end, nut/washer_flat_beside, switch_flat_F4, switch_hover, buzzer_lying, lcd_lying,
lcd_standing_out). Mapping: F1-1 = NAUO10 seated, F1-2 front (= NAUO35), F1-3 face down beside the +z end (= NAUO125), F1-4 face up
beyond the -z end (= NAUO154); LAC Potentiometer-1/Knob-1/Nut-2/Washer-2 seated, -3/-3/-4/-3 the face-down set; F4-1 seated, F4-2
flat (NAUO50), F4-3 hovering; Piezo Buzzer-2 clamped (NAUO62), -1 lying (NAUO61); LCD V1-1 seated, V1-2 lying, V1-3 angled (no STEP
copy), V1-5 = NAUO96; F7-1 = F7A NAUO42, F7-2 = F7B NAUO43; LAC Resistor 1.SLDPRT-1 = RES1 NAUO6 (h27), -2 = RES2 NAUO7 (h29).

Cameras: target (orbit target), dir (unit vector target -> eye), dist (mm), all assembly mm. **Our equivalent radius** = dist x
sin 22.5 deg / 1.08 = **0.3543 x dist** (player/js/core.js:267-269, frame_padding 1.08 in steps.json): `view_dir=dir,
frame=(target, radius)` puts our eye exactly where Cadasio's was (same vertical framing; Cadasio authored at 2.07:1, raw:1
`cameraProperties.default_camera.aspect_ratio` 2.066, so at 16:9 our sides are cut ~14 %). "Frame height at P" = 2 x depth x tan
22.5 = 0.828 x depth, the height of the picture at that point; "on screen (x %, y %)" is in the 2.07:1 frame from the top left. Our
own numbers are computed from steps.json at 16:9. Published distances come in fixed zoom steps (110, 125.3, 149.7, 174.6, 237.5, 277,
323.1, 376.8, 439.5, 512.6), and every camera has world-up (roll 0) except where the scene's up axis is switched (Steps 22-29, 35, 56).

1. **The digest's MOVE vectors are in each part's own CAD frame, not assembly axes.** The published overrides sit on the solids
   (depth 2), in the part's frame (e.g. raw:1, Step 42c, `F7-1/F7-Cut-Extrude1` position (0, 2.63, -0.64) mm, rotation (0.1311, 0,
   0, 0.9914)), and tools/cadasio/digest.py:79-85 only subtracts translations. Magnitudes are right; directions are wrong for every
   part whose frame is turned: F7 hover is +80.3 **Y** (digest -Z, digest:850), F9 at Step 45 is (+103.9 X, +35.3 **Y**) (digest
   (103.9, 0, -35.3), digest:906), F5 +56 **Z** (digest +Y, digest:1078), F6 -67.5 **Z**, RTC +33.6 **Y** (digest +X), the pot's
   "-79 Z" is along its shaft, and the F7 spread's "[0, 2.6, -0.6]" is not a lift (section 41-44).
2. **Many published "moves" are cross-fades, not motion**: one CAD copy fades out while a differently posed copy fades in (800 ms).
   Buzzer into the F7s (43c), F1 round to the other end (47c), F4 lifted and lowered (48c, 49c), the LCD (51c, [117], 52c), F1 stood
   up and pushed on (53c, 54c), the USB plug (40c), and every lead and wire plugged in (each Nc fades in the plugged copy).
3. **Arrows**: their authored `points` are sometimes stale (Step 23's lie 230 mm away); the step pictures are the reference.
4. **Turns** are tweened by slerp (three.js), i.e. the shorter way round; spin directions below assume that.

## Our Step 3 = published Step 3 ([006], [007]; digest:173)

- Motion: Nano at `[0.0, 39.8, 0.0]` -> ZERO (straight down). (The published Nano sits 2.6 mm +Z of the CAD's throughout: a quirk.)
- Lead lines (2, vertical, from the corner pins' tips riding on the Nano, 7 mm into the holes): c15 (684.21, 931.27, 1306.52) ->
  (684.21, 890.11, 1306.52); g1 (668.75, 931.27, 1342.15) -> (668.75, 890.11, 1342.15). Ours: pin tip to hole top (guide.py:235).
- Labels: "c15" box (top-left corner) at (35.1 %, 20.0 %), 175 px wide, leader to (49.5 %, 45.3 %), anchor (684.20, 896.76, 1306.02);
  "g1" box at (61.7 %, 32.9 %), leader to (55.9 %, 56.3 %), anchor (669.08, 896.26, 1341.93). The hovering Nano spans (46-59 %,
  21-27 %): one label each side of it, level with it, leaders down to the holes, neither on the Nano. No part label.
- Camera (same as Step 2): target (701.0, 875.5, 1296.1), dir (-0.693, 0.517, 0.503), dist 237.5 -> **radius 84.2**. From behind
  (-x, the j-row side) at the breadboard end (+z), 31 deg up. Frame height at the board 168 mm; board middle at (47.8 %, 47.4 %), c15
  (49.6 %, 45.2 %), g1 (55.9 %, 56.0 %). Ours (guide.py:222, 235; radius 96, from the front at the buzzer end): 246 mm at the board,
  i.e. **published is 1.46x closer**.

## Our Steps 5-7 = published 5-7 ([010]-[016]; digest:206, 223, 240, 248)

- Motion: RES1 `[0.0, 37.1, 0.0]` -> ZERO; RES2 `[0.0, 40.0, 0.0]` -> ZERO; RTC + coin `[0.0, 33.6, 0.0]` -> ZERO (straight down).
- Lead lines (vertical, part end riding, to 7 mm into the hole):
  - 5: h27 leg (666.11, 930.53, 1275.87) -> (666.11, 890.11, 1275.87); rail leg (699.19, 930.26, 1277.44) -> (699.19, 890.11, 1277.44).
  - 6: (666.21, 933.28, 1271.09) -> (666.21, 890.11, 1271.09); (699.16, 933.28, 1272.33) -> (699.16, 890.11, 1272.33).
  - 7: j24 pin (661.06, 927.31, 1283.75) -> (661.06, 890.11, 1283.75); j19 pin (661.15, 927.31, 1296.00) -> (661.15, 890.11, 1296.33).
- Labels (box top-left / leader tip / anchor):
  - 5: "(-) blue" (32.2 %, 30.2 %) / (45.4 %, 43.8 %) / (699.24, 896.76, 1276.80); "h27" (57.0 %, 58.3 %) / (50.8 %, 50.1 %) / (666.31, 896.70, 1275.60).
  - 6: "(-) blue" (33.1 %, 30.9 %) / (44.6 %, 44.8 %) / (699.55, 896.01, 1272.42); "h29" (57.8 %, 54.9 %) / (49.9 %, 51.4 %) / (666.55, 895.63, 1271.26).
  - 7: "j24" (39.3 %, 27.1 %) / (53.3 %, 49.6 %) / (661.46, 896.58, 1283.96); "j19" (63.8 %, 25.8 %) / (55.6 %, 47.6 %) / (661.46, 896.16, 1296.71).
  - The hovering parts are at (48 %, 27 %) (RES1), (47 %, 26 %) (RES2), (57 %, 20 %) (RTC): the rail label sits left of the part,
    the h-row label below-right of the board, the two j labels left and right below the module. None on a part.
- Camera (one for 5-7): target (708.5, 866.6, 1310.4), dir (-0.644, 0.486, -0.591), dist 277 -> **radius 98.2**. From behind (-x)
  at the buzzer end, 29 deg up: the h-row legs and j pins are on the camera's side. Frame height at the board 197 mm; h27 at (50.9 %,
  49.8 %), h29 (49.9 %, 50.8 %), j24/j19 (53.3/55.7 %, 49.4/47.2 %): the target holes are at the frame's centre. Ours (from the front,
  radius 94.5-100.6): 241-263 mm at the board, **published ~1.25x closer**.
- (Step 4, not asked: the resistor alone at dist 110, straight legs on Step 4, bent on 4c by swapping solids; label "2x" in black
  6em, no underline, (54.4 %, 11.9 %).)

## Our Steps 9-21: cameras only (how close on the holes)

| ours | published | target | dir | dist (radius) | frame height at the holes, published / ours | holes on screen |
|---|---|---|---|---|---|---|
| 9-14 | [019]-[030] (digest:289) | (665.5, 826.6, 1302.1) | (0.462, 0.813, -0.355) | 277 (98.2) | i21-i24 178-180, a8-a14 175-179 / 189-195 (ours radius 74) | i-row (53-54 %, 29-31 %), a-row (41-44 %, 29-33 %); board middle (48 %, 29 %) |
| 16-18 | [034]-[039] (digest:415) | (629.2, 904.7, 1304.1) | (-0.340, 0.413, -0.845) | 277 (98.2) | j27 221, j29 218 / 182, 180 | j27 (41 %, 56 %), j29 (41 %, 57 %) |
| 20-21 | [042]-[045] (digest:478) | (660.0, 841.3, 1287.9) | (0.449, 0.838, 0.309) | 277 (98.2) | j1 176, i27 192, j3 178, i29 194 / 217, 189, 215, 187 | j1/j3 (38-39 %, 47-48 %), i27/i29 (53-54 %, 32 %) |

- 9-14: from the front, 54 deg up, a little from the buzzer end; the target is 70 mm under the board, so the board sits in the top
  third and the loose wires (in front) fill the lower half. 16-18: from the buzzer end (-z), a little from behind, 24 deg up (the
  switch and its hanging leads to the left). 20-21: from the front, 57 deg up, from the breadboard end (+z).
- So the published is only ~1.1x closer than ours on 9-14 and 20-21, and farther on 16-18: Lee's "zoom" asks for more than published.

## Our Steps 22-28 = published 22-28 ([046]-[062]; digest:515-625): knob, nut, washer off and on

The published does all of this on the CAD's **face-down** copy beside the +z end (pot_flat_beside; F1-3 fades in at 25) and switches
the scene's up axis to -x (digest:522; raw:1 `scenes`), which under that pose is the potentiometer's own up: on screen it looks
upright, leads hanging down (pictures 046, 049, 052, 056). So everything below is in the **potentiometer's seated frame** (shaft along
+x out of F1's front), which is directly our BUILD/PULLED pose (pure translations, guide.py:396, 400): add the translation.
Poses are relative to each part's seat (= our `DELIVERED` / `ride` poses on POT).

| stop | knob | nut | washer | pot |
|---|---|---|---|---|
| [046] Step 22 | `[-2.9, 0, 0]` | `[-2.2, 0, 0]` | `[-2.5, 0, 0]` | seat (ours: PULLED+BUILD) |
| [047] auto | `[34.7, 0, 0]` (slides 37.6, no turn) | | | |
| [048] 22c | fades out | | | |
| [050] auto | | `[35.7, 0, 0]`, slides 37.9 and **turns +176.0 deg about +x** | | |
| [051] 23c | | fades out | | |
| [053] auto | | | `[35.4, 0, 0]`, slides 37.9, turns +123.6 deg about +x | |
| [054] 24c | | | fades out | |
| [055] Step 25 | | | | `[-79.1, 0, 0]` (behind F1); F1 fades in seated |
| [056] 25c | | | | ZERO |
| [057] / [058] 26 / 26c | | | `[61.2, 0, 0]` -> `[-0.1, 0, 0]`, no turn | |
| [059] / [060] 27 / 27c | | `[55.8, 0, 0]` -> `[-0.1, 0, 0]`, **no turn** | | |
| [061] / [062] 28 / 28c | `[59.3, 0, 0]` -> `[-1.2, 0, 0]`, no turn | | | |

- **The nut is spun off, not on.** At [050] its turn relative to the potentiometer goes from -53.3 to +122.7 deg about +x: +176.0 deg,
  i.e. **counter-clockwise seen from the shaft's tip** (looking back at F1's front), almost half a turn while it slides 37.9 mm off
  (raw:1, Transition [050], `LAC Nut-4` rotation (0.9752, 0, -0.2215, 0) -> (-0.2561, 0, -0.9667, 0)). Putting it back (27 -> 27c) it
  only slides. The washer's +123.6 deg turn coming off ([053], `Washer-3` rotation (0, 0.8813, 0, -0.4725)) looks like an authoring
  accident. In our ride form (nut on the shaft axis y 919.53, z 1235.26):
  `turned([1, 0, 0], 176.0, [725.24, 919.53, 1235.26], [34.9, 0.0, 0.0])` for "unscrewed and off" from our DELIVERED `[-3.0, 0, 0]`
  (guide.py:403); for Lee's clockwise spin on (27), the same with -176 (a turn over 180 deg needs `via()` stops).
- **Arrows** (one red straight arrow per step, along the shaft, pointing away from F1; authored lengths 41.8 / 41.3 / 32.6 mm,
  digest:520, 538, 556): tail anchored on the potentiometer's body (`LAC Potentiometer-Fillet2`), head on the shaft/knob. Step 22's
  authored points, in the seated frame, run (727.0, 920.1, 1226.2) -> (768.7, 922.7, 1227.7): from inside the knob at the nut, 9 mm to
  the -z side of the axis, to 28 mm past the knob's face (x 741). Steps 23 and 24 (pictures 049, 052): from the threaded bushing,
  just below the shaft, to about one shaft length past the tip. **Not from the tip.** Ours: guide.py:445 (tail 4 mm, head 34 mm out
  from the part's middle).
- **Lead lines** (25-28): along the shaft axis (y 919.5, z 1235.3 seated), from the moving part to the potentiometer's back face
  (x 709.8): 25: 91.8 mm, from the pulled-back pot (x 630.7) to F1's hole (x 722.5); 26: washer (x 785.2) -> 709.8, 75.4 mm; 27: nut
  (780.9) -> 709.8, 71.1 mm; 28: knob (786.3) -> 709.8, 76.5 mm.
- **Labels: none** in 22-28 (no "Potentiometer", no "F1"; docs/research/guide_19075-lac_full_build.md:100-115).
- **Step 25: yes, there is a close-up of the tab** - on **25c only** ([056], digest:586; picture 056.jpg). An image callout
  (`ASS530bc61b-bf8a-a988-136c-2864cef41b09.png`, on Cadasio's S3: raw:1 toolbox `Mdb879366`), box at (19.0 %, 19.1 %), 17.7 % of the
  frame wide, light-blue rounded border, a light-blue leader to the cutout at seated **(722.52, 919.70, 1243.89)** (on F1, 8.6 mm from
  the shaft axis towards +z). The picture: F1's front around the shaft, shaft end-on, the potentiometer's little tab in F1's small
  rectangular cutout outlined in red. Ours as a model close-up: `inset=dict(target=posed_line(BUILD, [[722.5, 919.7, 1243.9]])[0],
  dir=[1, 0, 0], radius=10, mark=3)`: from straight in front, the cutout is left of the shaft, as in the picture. Removed at 26.
- **Cameras** (in the seated frame; roll about 1-2 deg, i.e. world-up for us):
  - 22-24 ([046]): dir **(0.471, 0.607, -0.640)**, dist 512.6, but the eye is only 118 mm from the shaft tip (target 250 mm past
    the part); frame height at the shaft tip **97 mm**, tip at (45 %, 42 %). Ours (guide.py:436-437): dir (0.35, 0.45, -0.82), radius
    42 = 98 mm: same zoom, published more from the front and higher.
  - 25-28 ([055]-[062]): dir **(0.528, 0.532, -0.662)**, dist 439.5; at 25c frame height at the shaft tip **182 mm**, tip at (52 %,
    49 %) (at 25, pot pulled back: 217 mm). Ours (guide.py:438): radius 98 = 229 mm at its target.

## Our Step 29 (lay F1 face down) - published 29 is something else ([063], [064]; digest:631)

- Published Step 29 checks the knob: camera square to the knob's face (seated dir (0.991, 0.131, -0.018), dist 125.3, frame height
  91 mm at the shaft), eye icon on the knob; 29c turns the knob +49.7 deg about +x (counter-clockwise seen from the front), no slide.
- **Published never flips F1**: 22-29 already happen on the face-down copy, so between 29c and 30 only the camera moves (turns 132
  deg, 125 -> 439 mm) and the up axis returns to +y (digest:643-655). F1 then lies at exactly our FLAT_BESIDE
  (`turned([0.707, -0.707, 0], 180, [722.43, 918.11, 1277.49], [-92.30, -9.13, 243.60])`), its middle at (628.7, 909.1, 1508.7);
  the potentiometer at pot_flat_beside (0.8 deg off F1's, as the CAD). No published camera frames F1 alone face down; the first
  layout view (Step 30) has F1 at (34.6 %, 26.2 %), 342 mm frame height at F1 (ours, radius 185: 465 mm, F1 at (33 %, 48 %)).

## Our Steps 30-34 = published 30-34 ([065]-[075]; digest:643-723): where F1 and the buzzer lie

- F1 + pot + knob + nut lie face down beside the +z end (above) from 25 to 47c. The washer is hidden from [065] on (a published slip).
- Buzzer from the "Alarm Buzzer" card [071]: at exactly our BUZZER_LYING (`turned([0.577, 0.577, -0.577], 120, [675.26, 918.29,
  1224.70], [-0.38, -12.76, 176.10])`), its middle at (670.9, 902.4, 1400.8): behind and beyond the +z end.
- Leads: the straight leads lie as the CAD has them; Nc fades in the plugged copy (no wire moves at all). Eye icon on the lead's cap,
  one label on the hole.
- Camera 30-32 ([065]): target (596.6, 827.6, 1401.4), dir (0.706, 0.580, -0.407), dist 439.5 -> radius 155.7; 35 deg up from the
  front at the buzzer end, looking along the case to the +z end. F1 at (34.6 %, 26.2 %), red cap (21.2 %, 28.2 %), (+) red hole
  (52.2 %, 55.8 %), board middle (58.4 %, 54.0 %); frame height 253 mm at the board (ours 303), 342 mm at F1 (ours 241).
  Labels: "(+) red" (38.3 %, 42.3 %) -> (52.2 %, 55.8 %); "a5" (36.1 %, 41.6 %) -> (52.7 %, 54.5 %); "(-) blue" (35.6 %, 43.6 %) ->
  (52.0 %, 56.5 %); eye icons at (12.7-14.4 %, 10.4-12.7 %).
- Camera 33-34 ([072]): target (692.7, 831.5, 1320.4), dir (-0.412, 0.746, 0.523), dist 277 -> radius 98.2; 48 deg up from behind
  (-x) at the +z end. Buzzer (61 %, 57 %), red cap (44.8 %, 83.0 %), j4 (45.5 %, 38.0 %), (-) blue (54.7 %, 30.9 %); frame height
  189 mm at the board (ours 189: same zoom, but ours from the front).

## Our Steps 36-39 = published 36-39 ([079]-[086]; digest:758-820): camera

- LCD lying at exactly our LCD_LYING. The "loose" wire is the plugged wire's own shape (CAD body for the lying LCD) with both caps,
  moved +184.5 / +181.5 / +183.4 / +182.2 mm in x (in front of the case); at Nc it fades out and the plugged copy fades in.
- Camera: target (684.3, 869.6, 1335.7), dir (0.500, 0.779, -0.379), dist 323.1 -> radius 114.5; 51 deg up from the front at the
  buzzer end (ours from the breadboard end). Header pins (38-39 %, 34-36 %); rail holes at z 1280 (57.6-57.9 %, 57.4-58.1 %); b8/b9
  (51.5-51.9 %, 45.8-46.3 %); loose wire (42.7 %, 72.3 %). Frame height at the board 245 mm (ours 284: published 1.16x closer).
- Labels: pin labels GND/VCC/SDA/SCL at (19-21 %, 47-51 %), leaders up to (38-39 %, 34-36 %); rail labels at (69 %, 36-41 %); b8/b9 at
  (55-56 %, 17-19 %).

## Our Step 40 = published 40 ([087]-[089]; digest:828-848)

- [087] "USB Cable" card: the cable alone. [088] Step 40: no plug yet; eye icon on the Nano's mini-USB socket (anchor (675.83,
  903.87, 1346.91), box (34.4 %, 51.7 %)). [089] 40c: plug, cable and A end fade in, plugged (`[0.0, 0.0, 1.0]`, 1 mm proud). No hover.
- Camera: target (686.1, 858.7, 1345.9), dir (-0.768, 0.490, 0.413), dist 277 -> radius 98.2; from behind (-x), 29 deg up, from the +z
  end. Socket at (49.1 %, 33.0 %), frame height there 204 mm; the A end at (56.7 %, 76.3 %). Ours (guide.py:644): socket (58.3 %,
  35.8 %), 188 mm, from higher (37 deg).

## Our Steps 41-44 = published 41-44 ([090]-[097]; digest:850-904)

- 41: both F7s `[0.0, 80.3, 0.0]` -> ZERO (straight down). Lines from each tab's bottom (y 961.55 at hover) to F3's mid-thickness:
  F7B (691.93, 961.55, 1233.70) -> (691.93, 884.64, 1233.70), 76.9 mm; F7A (659.21, 961.55, 1233.55) -> (659.21, 886.15, 1233.55), 75.4.
- Camera 41-42 ([090]): target (683.1, 901.9, 1321.6), dir (-0.544, 0.371, -0.753), dist 376.8 -> radius 133.5; from behind (-x) at
  the buzzer end, 22 deg up. F7s seated at (41.1 %, 54.8 %), hovering (40.1 %, 22.0 %), case middle (46.8 %, 58.1 %); frame height
  at the F7s 248 mm (ours 242).
- 42: two arrows (authored), horizontal, 43 mm above F3, just off the F7s' -z edges, each from an F7's inner face outwards:
  (690.75, 930.73, 1222.17) -> (729.19, 931.59, 1220.65), 38.5 mm (+x); (660.97, 931.09, 1222.43) -> (613.04, 931.08, 1221.50), 47.9 (-x).
- **42c: the F7s do not lift.** Each turns about its own outer bottom edge where it meets F3's top:
  F7A `turned([0, 0, 1], 15.07, [656.60, 887.75, 1233.2])`, F7B `turned([0, 0, -1], 16.05, [693.18, 888.19, 1233.2])` (t = 0).
  That edge moves at most 0.2 mm; the tops go out 18.3 / 19.3 mm and down 2.2 / 2.7 mm. (HEAD guide.py:660-661 adds `[0.0, 2.6, 0.0]`
  from the digest's local-frame offset: drop it.)
- 43 ([094]): camera changes: target (654.6, 858.5, 1277.7), dir (0.524, 0.769, 0.365), dist 376.8 -> radius 133.5; 50 deg up from
  the front at the +z end. Lying buzzer (31.5 %, 65.2 %), its seat (59.0 %, 34.2 %); 278 mm at the F7s. Two eye icons: on the lying
  buzzer (665.70, 903.84, 1399.54) and on F7A's slot (650.35, 918.63, 1230.84).
- **43c: the buzzer is not lowered**: the lying buzzer and its leads fade out, the clamped copy fades in, F7s still spread.
- 44: eye on each F7; 44c: F7s turn back to ZERO (same camera as 43).

## Our Step 45 = published 45 + 46 ([098]-[103]; digest:906-944): F9, hooked and stood up

Stops (poses relative to F9's seat; pivot P = (720.13, 887.54, 1355.78) = F9's front edge on F3's top):

1. [098] Step 45: `[103.9, 35.3, 0.0]` (upright, 104 mm in front, 35 mm up). Two bent lead lines from the feet across and down into
   F3's slots (authored (800.25, 916.55, 1355.67) -> (696.48, 885.04, 1355.67), 108.5 mm; (818.62, 916.55, 1355.76) -> (711.08,
   885.72, 1355.65), 111.9 mm; 3 and 5 points).
2. [099] auto: `[0.0, 35.3, 0.0]` (slides back over its slots).
3. [100] auto: `turned([0, 0, -1], 25.79, [720.13, 887.54, 1355.78], [-0.45, 32.96, 0.0])` (top tipped 25.8 deg towards the front, still
   33 mm up, front foot over its slot).
4. [101] 45c: `turned([0, 0, -1], 25.79, [720.13, 887.54, 1355.78])` (drops 33.0 mm: front foot hooked in its slot, back foot 14 mm
   up). Inset picture (`ASSc25abb5a-8228-7084-f31b-a2596b5758de.png`, box (66.1 %, 37.4 %), 20.3 % wide, leader to (716.51, 884.89,
   1355.89)): the hooked foot in F3's slot, red box (picture 101.jpg).
5. [102] Step 46: same pose; lead line 7.3 mm at the back foot (696.67, 891.88, 1355.85) -> (696.67, 884.61, 1355.85); eye icon at
   (699.49, 897.24, 1357.28).
6. [103] 46c: ZERO: stands up by turning 25.79 deg about +z through P, the back foot dropping into its slot.

- Camera (all six): target (686.2, 875.0, 1312.0), dir **(0.529, 0.664, 0.530)**, dist 323.1 -> **radius 114.5**: from the front and
  the **breadboard end (+z), the side F9's engraved code faces** (guide.py CODES: F9 +z), 42 deg up. F9 hovering at (67.8 %, 62.1 %),
  seated F9 (46.0 %, 48.1 %), case middle (52.5 %, 42.8 %); frame height at F9 seated 216 mm. Ours (CASE_CAMERA guide.py:656, from
  the -z end): F9 hovering at (14.3 %, 38.7 %) at 16:9.

## Our Step 46 = published 47 ([104], [105]; digest:946-958): F1 "carried round"

- **Not carried**: at 47c the face-down set fades out and the face-up set beyond the -z end fades in: F1 = our FLAT_OTHER_END but
  0.9 mm lower (`turned([0, 0, 1], 90, [722.43, 918.11, 1277.49], [-31.61, -6.62, -187.81])`), pot = pot_flat_other_end, knob 2.1 mm
  higher than the CAD's knob_flat_other_end. No upright stage in between.
- Arrow (authored, 101.7 mm, anchored to the USB parts by mistake): (601.82, 912.59, 1441.00) -> (603.09, 912.67, 1339.34): behind the
  case (x 602, behind F2's plane x 641.6), 28 mm above the table, pointing -z along the back. Eye icon on the face-down F1 at (600.53,
  910.59, 1499.50).
- Leads: the plugged leads for that pose fade in (= CAD NAUO157-159, our POT_OTHER). They never cross F9's plane (wire-paths.json
  `lines` NAUO157-159 stay at z <= 1332), so nothing passes through F9 in the published.
- Camera: target (671.8, 911.8, 1271.1), dir (0.650, 0.750, -0.124), dist 376.8 -> radius 133.5; 49 deg up from the front, nearly square
  to the case's length. F1 face down (19.8 %, 32.5 %), F1 at the other end (77.6 %, 62.9 %); 323 mm at the case (ours radius 200: 495).

## Our Step 48 = published 49 ([108]-[110]; digest:974-993), with published 48 (= our 47) for context

- Published 48 ([106], [107]): eye icon on the flat F4 (587.81, 971.72, 1223.66); 48c: F4 + switch + leads fade from flat
  (`[-117.83, 17.26, -0.06]`) to hovering over the frame (`[0.0, 49.8, 0.0]`, switch `[0.0, 49.8, -0.2]`; leads = CAD NAUO147-149).
- [108] auto: camera only, to target (678.6, 923.4, 1294.9), dir (0.697, 0.551, -0.460), dist 323.1 -> radius 114.5 (33 deg up, front,
  buzzer end). F4 at (50.2 %, 22.6 %), frame height there 226 mm (ours 230, at (47.9 %, 13.7 %)).
- [109] Step 49: four vertical lead lines from the tab tops up to F4's top face at hover (y 1004.26 = 954.46 + 49.8):
  (712.08, 954.77, 1355.75) [F9, 49.5 mm], (694.35, 957.84, 1355.83) [F9, 46.4], (691.57, 957.84, 1233.03) [F7B, 46.4],
  (658.47, 957.84, 1233.23) [F7A, 46.4], each -> same x, z at y 1004.26. (The first is not one of the tab tops the CAD study lists,
  F9 at x 693.6 / 697.6: docs/research/lac/cad_study.md:83.) Ours (guide.py:684, 691): x 693.64, 697.62 (F9), (658.83, z 1238.01),
  (691.68, z 1228.36), from F4's underside y 951.46 to 957.84.
- [110] 49c: F4 fades from hover to seated: **no slide**.

## Our Steps 50-51 = published 51-52 ([113]-[118]; digest:1009-1046): the LCD, every stop

1. [113] Step 51: LCD lying face down (= our LCD_LYING), eye icon on it (728.53, 904.67, 1431.71).
2. [114] 51c (cross-fade, no motion): **angled** copy LCD V1-3 (no STEP copy of the LCD in this pose):
   `turned([0, 1, 0], 14.0, [723.37, 921.6, 1265.11], [0.0, 2.14, 0.0])`
   (= `turned([0, 1, 0], 14.0, [708.91, 946.54, 1331.16], [16.41, 2.14, 1.54])` about the LCD's own middle): upright, face to the
   front, turned 14.0 deg about the vertical through (x 723.37, z 1265.11) - 3 mm in front of F8 at its notch - and 2.14 mm up.
   Its F8 (-z) end sits in F8's notch (front corner (722.08, 921.6, 1262.45), board end at its seat); its F9 (+z) end is swung 23 mm
   out in front of F9 (front corner (745.79, 921.6, 1357.54), back corner (726.87, 921.6, 1362.26)). **Its wires are the CAD's
   NAUO109-112** (the "pose the STEP has no LCD for", docs/research/lac/cad_study.md:66): in this pose their female ends meet the header within 2.8-4.4 mm.
3. [115] Step 52: two lead lines from F9's two notches to the angled board's end: (712.14, 947.28, 1355.70) -> (737.15, 949.08,
   1357.45), 25.1 mm; (712.11, 892.56, 1356.04) -> (736.82, 894.14, 1357.17), 24.8 mm. Inset picture (`ASS5757488f-64de-e675-2e13-
   81d0b64f6b75.png`, box (19.9 %, 4.4 %), 15.0 % wide, leader to (720.29, 943.85, 1356.68)): F9's notches, two red boxes.
4. [116] auto: annotations off.
5. [117] auto (cross-fade): **straight, 14.88 mm towards -z** = our LCD_STANDING `[0.065, 0.376, -14.884]` (CAD NAUO96, wires
   NAUO117-120): the F8 end pushed 14.9 mm further through F8's notch, the F9 end now clear of F9.
6. [118] 52c (cross-fade): seated (= slid +14.88 along +z into F9's notches; wires NAUO101-104).

So the path is: lying -> F8 end into F8's notch with the F9 end angled 14 deg out -> straightened while pushed 14.9 mm further
through F8 -> slid 14.9 mm back into F9. Ours (guide.py:698-700): lying -> LCD_STANDING + 40 mm in x -> LCD_STANDING -> seated (no
angled stage). All published changes here are fades; as motion: rest each stop in turn.
- Camera (all): target (670.6, 875.2, 1275.4), dir (0.698, 0.495, 0.519), dist 439.5 -> radius 155.7; 30 deg up from the front at the
  breadboard end. Lying LCD (32.7 %, 67.3 %), seated LCD (49.5 %, 46.4 %), F9's notch (43.0 %, 41.9 %), F8's (56.2 %, 42.6 %); frame
  height at the seated LCD 306 mm (ours 254).
- (Published 50 = our 49: F8 `[94.2, 0.0, 0.0]` -> ZERO; lines (800.98, 953.50, 1266.27) -> (706.79, 953.50, 1266.27) and (800.98,
  885.03, 1266.28) -> (706.79, 885.03, 1266.28).)

## Our Step 53 = published 54 ([121], [122]; digest:1062-1076), with published 53 (= our 52)

- Published 53: eye on the face-up F1 (668.83, 912.90, 1103.91); 53c: F1 + pot + knob fade to standing in front (`[76.7, 0.0, 1.1]` =
  F1_hover_front; knob `[76.4, 0.0, 1.1]`).
- 54: four lead lines along +x, 73.3 mm, from the tab tips on F4's and F3's front edge (x 727.21) to F1's front face standing out
  (x 800.49 = 723.83 + 76.66): F4 (727.21, 952.77, 1320.47) and (727.21, 952.52, 1258.71); F3 (727.21, 885.37, 1319.88) and (727.21,
  885.59, 1257.51); each -> same y, z at x 800.49. 54c: F1 fades to seated (**no slide**).
- Camera (53-54): target (706.6, 874.3, 1253.3), dir (0.605, 0.664, -0.440), dist 376.8 -> radius 133.5; 42 deg up, front, buzzer end.
  F1 standing out at (33.9 %, 50.4 %), 255 mm there (ours radius 120: 248 mm, same zoom).

## Our Step 54 = published 55 ([123], [124]; digest:1078-1092): F5

- F5 `[0.0, 0.0, 56.0]` -> ZERO (slides -z).
- Four lead lines along +z from the tab tips to F5's outer face at hover (1369.07 + 56 = 1425.07): F1's hooks (722.43, 948.87,
  1372.45) -> (722.43, 948.87, 1423.12) and (722.28, 889.85, 1372.45) -> (722.28, 889.85, 1424.97); F3's tabs (663.88, 885.58,
  1369.24) -> (663.88, 885.58, 1424.42) and (702.29, 886.22, 1369.24) -> (702.29, 886.22, 1425.11). Ours (guide.py:725-727): the same
  tabs within 1.5 mm, but lines from F5's inner face (z 1366.07) to the tab tip.
- Camera: target (688.4, 888.4, 1297.7), dir (0.596, 0.499, 0.629), dist 376.8 -> radius 133.5; 30 deg up from the front at the +z end
  (more from the end than our END_CAMERA (0.82, 0.40, 0.42), guide.py:724). F5 hovering at (31.4 %, 57.1 %), F1's hook (44.4 %,
  44.1 %); frame height at F5 236 mm (ours 233).
