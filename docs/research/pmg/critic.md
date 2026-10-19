# PMG: completeness check of the four research reports (critic)

Written 19 Oct 2026, before anyone writes the PMG's `materials.json` and `guide.py`.

Read: `cadasio_map.md` (+ `.json`), `cad_study.md` (+ `.json`), `cad_wire_paths.md` (+ `wire-paths-draft.json`), `reuse_plan.md`
(+ `reuse_poses.json`, `materials.proposed.json`, `colour-atlas-pmg.proposed.json`, `scripts/trim.example.json`), checked against
`cad_tree.md`, the earlier study `../guide_19075-piano_memory_game_pmg-full_build.md`, the step pictures and the rulebook.

My own checks (all in `scripts/`, each one small process, under 150 MB, the whole `pmg.glb` never loaded):
- `critic_checks.py`: the JSON files against each other (classification of all 296 instances, the 21 wires, the poses).
- `critic_fit.py`: pins from the MRA's measured pins; the I/O module turned the published way up, tested against the wood
  (trimesh on single plates); the published bench matrix as a pose.
- `critic_poses.py`: exact poses from the Cadasio and GLB matrices; where the 8 caps the STEP lacks would go; bench poses
  re-expressed if the module is turned.

Millimetres, assembly space of `pmg.glb` (Y up; front = -X, the student's right = +Z), as `stepgen.Model` reads it.

STATUS: complete.

## 0. In short

- **The four reports agree on almost every number.** Frame (Cadasio = GLB, 23.6076 mm per unit), built copies, wood ids and
  engraved codes, pin positions (module, buttons, display, matrix, to 0.02 mm), button colours and rows, the 21 wire colours, and
  the main poses. I re-derived the D4, D7 and D13 pins from the MRA's measured pins and found the G4 cap NAUO97 centred on
  its pin (602.51, 941.06, 1310.44 against the pin at y 941.06, z 1310.42).
- **Everything is classified.** All 296 instances have a role (`cadasio_map.json`), all 114 flexible bodies have a centre line
  (`wire-paths-draft.json`), and all 17 wood parts have an engraved-code position (`cad_study.md` 2.2).
- **Three real contradictions** (section 1.1-1.3):
  1. The two wire JSON files file the same 16 STEP bodies under different wires. One calls them the button VCC wires, the other the
     GND wires, so they get different colours.
  2. `reuse_plan` keeps the bench copy of the USB A end as if it were the built one.
  3. `reuse_plan` calls the STEP "the new CAD", while the other two call it an older save than the published guide's.
- **Three decisions block the guide**, and only Lee (or TechBox's engineer) can make them (section 3):
  - whether the STEP is the current CAD;
  - which way up the I/O module goes on H4;
  - two or three wires per button.

  The jumper length comes next. Section 2.1 shows what each answer changes.
- **What nobody had produced yet, now in this report:**
  - the exact published module pose;
  - the module, Nano, plug and pin poses if the module is turned;
  - a fit test of the turned module against the case;
  - the published bench matrix as a pose of the built matrix;
  - where the 8 caps the STEP lacks would sit, and two ways to make them.

## 1. Contradictions, and how to settle them

### 1.1 The STEP's wire from a button's pin 0 to the G row: "VCC wire" or "GND wire"? (matters: colour and step)

- In the STEP each button has two wires: pin 1 -> S (OUT, as published) and pin 0 -> G. In the published guide pin 0 is VCC and
  pin 2 is GND.
- **`cadasio_map.json`** files these bodies (bench NAUO24, 26, 28, 30; case NAUO144, 150, 156, 162; held NAUO146, 155, 160, 166; built
  NAUO148, 152, 158, 164) under the **VCC** wires of Steps 3, 6, 9, 12 (colours #b70101, #21f17a, #85144b, #a75294). It gives the GND
  wires no body.
- **`wire-paths-draft.json` `wires`** files the same 16 bodies under the **GND** wires of Steps 5, 8, 11, 14 (colours #343232,
  #ffdc00, #3876ac, #3d9970). It gives the VCC wires no body (checked entry by entry, `critic_checks.py`).
- **Settled by the evidence:**
  - Physically, each body runs from pin 0 to the G row.
  - Pin 0 really is VCC. The published card "Push Buttons" ([006], `cadasio/thumbs/.../006.jpg`) shows a photo of the real board,
    cap towards the viewer, pins down, printed **VCC - OUT - GND from left to right**. Seen from the cap side (-X) the left is -Z,
    and pin 0 is the lowest z (black bench button: VCC z 1273.28, OUT 1275.78, GND 1278.28). That also answers the pin question in
    `cad_wire_paths.md` (its question 2).
  - The naming backs `cadasio_map`'s reading: TechBox's later CAD kept Part55, 57, 59, 61, 65, 67, 69, 71, 73, 75 as the
    **VCC** wires, re-routed to V, and added new GND bodies (Part169-189).
  - So the STEP's wire is the VCC wire landing on G. It is **not usable as it stands for either published wire**: under the
    published 3-wire wiring, every VCC route and every GND route must be drawn anew. The STEP body can serve as a shape to start
    from, moved one pin at one end: V is 2.48 mm from G on the module, and GND is 2.5 mm from VCC on the button.
- **Action:** the guide author ignores both JSONs' body mapping for these 16 bodies. If Lee chooses the STEP's two wires per button
  (question 3), the bodies are used as they are, and the wire is the VCC pin -> G wire (colour then Lee's choice).

### 1.2 The built USB A end is NAUO283, not NAUO278

- `cad_study` (3.1, 4.4), `cadasio_map` (4.1) and `cad_wire_paths` (8) agree:
  - NAUO283 is the built A end. The built lead NAUO285 meets it; it is Cadasio's USB Cable end-3; centre (655.8, 884.6, 1315.7),
    behind the case.
  - NAUO278 is the bench one. The bench lead NAUO277 meets it at z 1374.07; it is Cadasio's USB Cable end-1; box x 588.7-604.6,
    y 872.6-881.1, z 1374.1-1423.8.
- `reuse_plan.md` (section 1 table), `reuse_poses.json` (group 9, `"built": "NAUO278"`, NAUO283 "on the bench"),
  `materials.proposed.json` (rule `_about`) and `scripts/trim.example.json` (`keep`) have the two the other way round.
- **Settle:** keep **NAUO283** in `trim.json`, and take the A-end poses from `cad_study.md` 3.1 / 4.4. The mesh is the same, so the
  colours are unaffected.
- Either way the A end needs a resting pose set in the guide. Every copy lies partly below the table: NAUO283 y 880.3-888.8, the
  table at 887.8. Cadasio's built one is just as low (centre y 884.6, height 8.6).

### 1.3 Is the STEP older or newer than the published guide?

- `cadasio_map` and `cad_wire_paths` say older. Their evidence:
  - SolidWorks numbers new bodies upwards. The published CAD has Part168-207, which the STEP lacks. The STEP has Part36-53, which
    the published CAD no longer has.
  - Every difference is something the published guide has right (the mirrored bench matrix wiring, the missing GND caps, the slips
    of NAUO177 and NAUO274).
- `reuse_plan` reads the STEP as "the new CAD" and treats its 2-wire buttons and USB-down module as the engineer's latest choices.
- The STEP's header date (19 Oct 2026, 00:14) is the export date, not the save it came from. The Cadasio project's CAD is version 7,
  4 Aug 2026.
- **Settle:** treat the STEP as the older state (the evidence is good, but it is inferred). Ask Lee whether TechBox's engineer can
  re-export the assembly the Cadasio guide was made from (question 1). That one file would settle questions 2 and 3, the bench
  matrix and the missing caps.

### 1.4 Smaller disagreements (no decision needed; stated so nobody trips on them)

- **How much lower the published module sits.** `cad_study` says 1.9 mm lower, measured on the box centre. `reuse_plan` says
  3.7 mm, measured on the board's edge. Both are right.
  - Exact, from the two projects' matrices (`critic_poses.py`): the published module is NAUO78 turned 180 deg about the X-parallel
    line through **y 931.545, z 1290.510**. In stepgen form: `turned([1, 0, 0], 180, at=[605.78, 932.5, 1290.47], t=[0, -1.91, 0.081])`.
  - The published held copy is the published built one plus **[0, 102.33, 0.159]**. The STEP's NAUO94 is 104.68 above NAUO78.
- **Different `at` points.** `cad_study` and `reuse_poses.json` turn about different points:
  - module: 605.78 against 600.73 in x;
  - buttons, display and A end: other box centres.

  Each pair (t, at) is right for itself: I checked the display, and t differs by exactly the (I - R)(at1 - at2) term, to 0.01 mm.
  **Never take `t` from one report and `at` from the other.**
- **H14's end pose in Cadasio** has three readings, none verified:
  - `cadasio_map.json`: an offset of 13.3 mm with a turn;
  - `cadasio_map.md`: "turned about 14 deg";
  - `cad_study`: "about 7 deg; about 26 mm and 1 deg".

  The Completed View picture (`thumbs/.../116.jpg`) shows H14 seated: the display window over the digits and the bracket tops
  through its two slots. So all agree in practice: **use NAUO74 as it is**. Its way in is hand-set (no clean path in the CAD,
  `cad_study` 2.4).
- **The Nano.** `cad_study` 8 suggests `cut_part.py --like pmg.glb NAUO3`, then moving it by [0, -15.24, 0]. Use `reuse_plan`'s way
  instead (graft in the trimmed source, or `cut_part` **without** `--like` plus the `extra_parts` pose), for two reasons:
  - `--like` reads all 167 MB;
  - it leaves the part's own place above the bench, where a part's own place must be where it sits when built.
- **Counts.**
  - `cad_wire_paths.md` says "109 jumper-wire bodies"; its own table and the draft have 111 (91 routed + 20 loose; plus 3 USB = 114,
    as `reuse_plan`).
  - `cadasio_map`'s "29 rigid electronics" includes the 3 USB lead bodies.
  - "159" (`cadasio_map`, exact match) against "167" (`reuse_plan`, boxes to 0.5 mm) matched Cadasio components: different
    tolerances.
- **Colour of the matrix sockets.** `reuse_plan` gives Cadasio's as #232323, but #232323 is the MAX7219 chips. The 128
  "8x female rounded header" solids are #e4e4e4 in the Cadasio (counted from `colour-atlas-pmg-draft.json`). They are hidden
  between board and blocks, so the house `header_black` is fine.
- **"Behind the module."** `cad_study` 3.1, `cadasio_map` and `reuse_poses.json` say the bench buttons stand "behind" the bench
  module. They stand at x 641, on the student's side (-X) of the module (x 646.9-700.3), so they are **in front** of it. This
  matters only for captions.
- **USB cable thickness.** The CAD's cable is 4.6 mm across (radius 2.30), and the right-angle plug's exit is 4.5 mm across.
  `reuse_plan` proposes the MRA's radius 1.75. Either works; pick one.
- **Two colour atlases.** Use `colour-atlas-pmg.proposed.json`, which is keyed by our mesh names (the form `build_model.py` reads,
  like `colour-atlas-rcc.json`). `colour-atlas-pmg-draft.json` is keyed by Cadasio component names: a reference only, never the
  kit's `"atlas"`.
- **Engraved codes.** `reuse_plan` 4 lists the engraved codes as "not done", but `cad_study` 2.2 has all 17 in the RCC's `CODES`
  form (no `engraved-codes.json` needed). `cad_study` found no code engraved in the wrong place, so no `move_engraving`.

## 2. Gaps

### 2.1 What each of Lee's answers changes

| Decision | If the STEP's way | If the published way |
|---|---|---|
| Module on H4 | NAUO78 as it is. STEP routes usable for the module-on-H4 and held-above poses. Silkscreen and Nano pose as drafted. | Turn NAUO78 and everything on it (section 2.3). None of the STEP's in-case module-end routes, cap places or USB plug poses fit: about 50 routes to draw. |
| Wires per button | 17 wires; the 16 pin-0 bodies used as they are; no new caps. | 21 wires; 8 caps to add (2.2); 32 routes to draw (VCC and GND of 4 buttons, in 4 poses each). |
| Bench matrix | NAUO44 as it is: its 5 bench wires land on the mirrored pins (V11 -> CLK ... S13 -> VCC), the opposite of the case, so the wires would have to cross over when it is seated. Not a usable choice. | The published bench pose (2.4): 5 bench routes + 10 (to the held and mounted module) to draw. |

The published bench matrix is not a real choice: the STEP's bench wiring is simply wrong (DIN aside). So I have not put it to Lee
as a question; the guide should follow the published pose.

Not gaps for our player (the reports list them as "missing from the STEP"):
- **The four loose wires of Steps 11-14 (and every "token").** Our player lays the wire itself straight at the parking spot, between
  its own caps, then re-routes it. No CAD body is needed. The parking spots are in `cad_wire_paths.md` 5 and `cadasio_map.md` 4.5.
- **Cadasio's held and half-way poses of the display and the matrix.** They are in `cad_study.md` 3.3 as `turned()` poses; only
  their wires need drawing.

### 2.2 The 8 caps the STEP lacks (only if three wires per button)

No pose of the STEP has a cap on V4-V7 or on a button's GND pin, and our player needs one cap part per wire end: 42 for 21
wires, against the 34 the trimmed source keeps. Where they go, from the caps the STEP has (`critic_poses.py`):

| New cap | Centre (STEP way up) | Centre (published way up) | Made from |
|---|---|---|---|
| V4 | 602.51, 941.03, 1307.96 | 602.51, 922.06, 1273.06 | G4 cap NAUO97 moved (0, -0.023, -2.475) |
| V5 | 602.51, 938.49, 1307.95 | 602.51, 924.60, 1273.07 | G5 cap NAUO95, same move |
| V6 | 602.51, 935.94, 1307.93 | 602.51, 927.15, 1273.09 | G6 cap NAUO98, same move |
| V7 | 602.51, 933.41, 1307.95 | 602.51, 929.68, 1273.07 | G7 cap NAUO102, same move |
| GND black | 516.3, 906.4, 1239.1 | (buttons are not turned) | OUT cap NAUO87 moved by its pin step |
| GND yellow | 516.8, 906.4, 1271.7 | | OUT cap NAUO89 |
| GND white | 516.4, 906.8, 1304.3 | | OUT cap NAUO91 |
| GND blue | 516.0, 905.5, 1336.8 | | OUT cap NAUO92 |

- The (0, -0.023, -2.475) move is the V9 cap minus the G9 cap, measured.
- The button caps are not seated alike: their centres scatter about 0.2 mm in X. So a GND cap is good to about 0.2 mm. The pin tips
  themselves are in `cad_study.md` 5.2: black GND tip (520.26, 906.86, 1239.12).

Two ways to make the caps:
- **(a) Spare caps moved with `adjust_mm`.** This needs no tool change. Keep 8 caps the guide does not otherwise use in `trim.json`.
  The held-module caps NAUO103-110 and 120-128 are ideal for V4-V7: they are the built ones moved 104.68 mm up, so the move is
  plain. For example, NAUO106 (held G4) onto V4 is `adjust_mm` [0, -104.694, -2.558]. A button GND cap needs a turn as well: for
  example, NAUO130 onto the black button's GND is `{"t": [-48.292, -79.589, -155.519], "r": [0.4396, -0.8268, -0.3508, 98.067],
  "at": [564.575, 985.975, 1394.565]}`. The drawback: the parts keep misleading CAD ids.
- **(b) A `"copy"` entry in `trim.json`.** `scripts/trim_source.py` is our own proposal, so this is not a tools change. It would
  clone a kept cap's subtree under a new name (`CAP_V4` ...) with a moved matrix. Cleaner names. Not written.

### 2.3 If the module goes on H4 the published way up: nothing was planned for it

Every part on the module turns with it:
- NAUO78;
- its 17 caps (NAUO95-102, 111-119);
- the USB plug NAUO282;
- the Nano (NANO);
- the silkscreen decals.

Decals are "seated assembly mm" in `build_model.py`, so `silkscreen.py` must write them already turned. The turn is
`D` = 180 deg about the X line through y 931.545, z 1290.510, i.e. **y' = 1863.090 - y, z' = 2581.020 - z, x unchanged**.

Numbers, from `critic_poses.py` (exact, from the matrices) and `critic_fit.py`:
- **MRA module -> published built**:
  - x' = y + 490.546, y' = z + 785.108, z' = x + 1220.520;
  - as a pose: `{"t": [490.546, 785.108, 1220.52], "r": [-0.57735, -0.57735, -0.57735, 120.0], "at": [0, 0, 0]}`;
  - this is the NANO graft or `extra_parts` pose, and the transform for `silkscreen.py`.
- **Module pins, published built** (x 604.34 throughout):
  - columns: G z 1270.60, V 1273.09, S 1275.58;
  - rows (y): D4 922.03, D5 924.57, D6 927.11, D7 929.65, D8 934.58, D9 937.12, D11 942.20, D12 947.13, D13 949.67;
  - the USB end is at the top.
- **USB plug, published built**:
  - the cable leaves at about (611.2, 969.8, 1272.0) heading -Z (the STEP's exit at [611.2, 893.3, 1309.0], turned);
  - Cadasio's USB Right Angle-3 has its centre at (611.2, 962.9, 1284.0).
- **Poses from the turned built copies** (what `rest_at` / `carry` / `path` need):
  - Bench module (NAUO1): `{"t": [72.848, -46.234, 8.781], "r": [0.57735, 0.57735, 0.57735, 120.0], "at": [600.73, 930.586, 1290.552]}`.
  - Nano, bench seat: `{"t": [64.226, -45.07, 16.24], "r": [0.57735, 0.57735, 0.57735, 120.0], "at": [608.781, 937.473, 1289.981]}`.
    It lands on Cadasio's nano-3 centre (673.0, 892.4, 1306.2).
  - Bench USB plug (NAUO279): `{"t": [55.862, -68.076, 47.662], "r": [0.57735, 0.57735, 0.57735, 120.0], "at": [611.181, 962.942, 1284.044]}`.
  - Module held above H4: [0, 102.33, 0.159].
- **Fit test** (module vertices inside the wood; each plate tested as a closed mesh, trimesh):

  | Module | H2 | H3 | H4 | H5 | H10 | H11 | H12 | H13 | H14 |
  |---|---|---|---|---|---|---|---|---|---|
  | STEP way up | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
  | published way up | 0 | 0 | 0 | **116 vertices, deepest 1.09 mm** | 0 | 0 | 0 | 0 | 0 |

  - The board's bottom edge comes down to y 901.08, against the top of H5's rear tongue at y 902.98: the board sinks up to 1.9 mm
    into the tongue (x 595.3-598.5, z 1279.4-1312.2).
  - In the STEP's way up, the barrel jack's underside (y 902.99) sits exactly on that tongue (902.98). That looks like the case was
    designed for it.
  - Turned, the jack goes to y 945.7-960.1, z 1301.7-1310.7, clear of H13 and H10.
  - So the published way up fits too if the module sits about 1.9 mm higher than Cadasio put it. This is evidence for question 2,
    not an answer.

### 2.4 The published bench matrix as a pose (new)

Cadasio's bench matrix is NAUO44 turned 180 deg about the X line through y 923.8, z 1420.3. As a pose of the built NAUO81 (two
half-turns make one 40 deg turn):

    turned([0, 0, 1], 40.0, at=[532.477, 955.89, 1289.103], t=[114.717, -32.105, 145.911])

This was checked on all the matrix's vertices: the box lands on Cadasio's LED Matrix-1 exactly (centre 649.4, 923.8, 1435.0; size
17.7 x 32.0 x 131.9).
- Its input header then points -Z, towards the module: the header end is the module end.
- Its pins are the built pins carried by this pose.
- Its five bench routes, and the ten to the held and mounted module, must be drawn.

### 2.5 Other things the guide author will need that nobody produced

1. **One jumper length.** The CAD's poses need 47-329 mm and the finished game up to 184 mm. Holding the module above H4 needs up to
   288 mm in the STEP (its held copy is 104.7 mm up; the published one 102.3 mm). Without the real length no route can be drawn
   (question 4).
2. **Wire routes still to draw.** These are not in `wire-paths-draft.json`:
   - the VCC and GND routes (if 3 wires);
   - every in-case route (if the module is turned);
   - the published bench matrix routes;
   - the display and matrix approach legs.

   The published shapes exist as Draco files on Cadasio's server (`cadasio_map.md` 10); fetching them means downloading files
   (Lee's permission). They would be reference shapes only: house rules want smooth `W.smooth` curves at one length.
3. **Pin names for students.** The published guide names the pins on photo section cards of the real boards (I/O module, button,
   display, matrix: [001], [006], [034], [045]). Our player has no photo cards yet (rulebook 14). The I/O module carries its
   printed names (decals), but the button, display and matrix boards in the CAD are blank. Labels will name the pins; printed names
   on those three boards would need photos (question 5).
4. **The trimmed source is still to be made.** Before trimming, everything needing the full `pmg.glb` must be measured: centre lines
   (done, all 114) and pose copies (done). Also needed:
   - add the spare caps of 2.2 to `keep` if option (a) is chosen;
   - keep NAUO283 rather than NAUO278 (1.2).
5. **The Nano's sockets may be solid blocks** (`cad_study` 7.13: not checked). It is the RCC's module model (70 meshes to 0.004 mm),
   where they were. Expect to set the Nano's and the USB plug's `direction=` by hand, as on the RCC.
6. **Parts list.** Names are proposed (`cadasio_map.md` 6). Still to write: the grouping function, and the counts:
   - H9 x4;
   - Push Button x4 (with hover names Black / Yellow / White / Blue Push Button);
   - Breadboard Wire (F-F) x21 or x17;
   - the USB cable (pictured by its right-angle end).
7. **Website entries.** These are not research items, but the guide cannot be published without them:
   - a `guides.json` kit entry (PMG, folder `PMG Build Instructions`);
   - a guide entry (by the house pattern, `piano-memory-game-full-build`).

   The published PMG is also cut into three Parts: Steps 1-14 (buttons), 15-25 (display, matrix, USB) and 26-51 (case). So
   `g.chapter()` lines can follow later if Lee wants Part guides (question 9).
8. **The bench is not one level.** The bench module's board underside is at y 879.0, 8.8 mm below the case's table (887.8), and
   every A end lies partly under the table. No floor is drawn, so this only matters for the A end's resting pose and for cameras
   that look along the table.

## 3. Questions for Lee (deduplicated, most important first)

1. Is the STEP file the latest version of the PMG model? It looks like an older save than the one TechBox's published Cadasio guide
   was made from (August 2026); could your 3D engineer export that later version?
2. Does the I/O module go on the back panel with the Nano's USB end at the bottom (as in the STEP) or at the top (as in the
   published guide)?
3. Does each push button get three wires (VCC to V, OUT to S, GND to G, as in the published guide), or the STEP's two (OUT to S, and
   the VCC pin to G)?
4. How long are the kit's jumper wires, and are they all female-to-female?
5. The published guide shows photos of the real button, display and matrix boards to name their pins, which our player cannot show
   yet; would you like those boards to carry their printed pin names, as the I/O module does, and could you send a photo of each
   board?
6. May we keep the PMG's own right-angle Mini-B end of the USB cable? The MRA's is straight, and on this case a straight plug would
   not fit.
7. Should the jumper-wire caps be grey like the MRA's or black like the published PMG guide?
8. May `pmg.glb` (167 MB, over GitHub's 100 MB limit) stay on this Mac only, with the much smaller trimmed copy committed instead?
9. Should the Full Build also be cut into the published Parts 1-3 (buttons; display, matrix and USB; the case)?
10. Should the guide include an electronics check before the case, like the MRA's test card, or follow the published guide, which
    has none?
11. Should the jumpers be called "Breadboard Wire (F-F)" in the parts list, as on the MRA?
12. Are black, yellow, white and blue button caps on D4, D5, D6 and D7, as published, correct for the kit?
13. Should the LED matrix blocks look as published: white sides, a black face and white dots?
