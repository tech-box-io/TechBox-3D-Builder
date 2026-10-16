# RCC: wire paths from the CAD

Written 15 Oct 2026 by the wire-path study. Data: `RCC Build Instructions/wire-paths.json`, in the same format as the MRA's (top-level
`NAUOn` tube lists, `chains`, `plugs`, `features`), plus `battery`, `colour_check` and `stub_colour_rules`.
All coordinates are mm in the assembly space of `rcc.glb` (Y up, as assembled). Ids are the CAD's top-level instances (`NAUOn`).
"Measured" means computed from the CAD geometry. Anything that is a guess says so.

STATUS: complete. Open points are in section 6.

## Short answers

- Every lead in the CAD is a round swept tube. The motor leads have conductors 1.00 mm across (r 0.5) lying 1.10 mm apart in a flat
  ribbon (the MRA's were 1.02 apart). The battery lead has two conductors 1.40 mm across (r 0.7). The USB cable is 3.5 mm across (r 1.75).
- Which conductor is which was traced tube by tube from the motor's stubs to the plug contacts. It agrees with the CAD's own names
  (`Fitec Right Wire Yellow 4` and so on) and with the colours in TechBox's Cadasio project. All 16 conductor centres land within 0.2 mm of
  the Cadasio solid of the same colour (`colour_check.all_agree = true`).
  - **Right motor (NAUO17):** yellow, red, brown from the bottom up where the lead leaves the motor (y 905.76 / 906.86 / 907.96).
  - **Left motor (NAUO18):** brown, red, yellow from the bottom up. It is the same motor turned over about X.
  - On both motors, yellow (signal) is on the motor's label side and brown is away from it, as on the MRA's MG90S.
  - Plugged on U1 / U2: brown on G (z 1318.43), red on V (1320.97), yellow on S (1323.51). The published guide and Lee's "S V G" agree.
- The lead lengths, middle (red) wire from the motor to the contact top:

  | Chain | Pieces | Length | Plug |
  |---|---|---|---|
  | `NAUO17`: right, loose | stub 1.5, then NAUO31 ribbon 55.2, then loose ends NAUO32-34 11.0 to the contact top | **67.7** (CAD wire 69.9) | NAUO21, loose |
  | `NAUO18`: left, loose | stub 1.5, then NAUO35 ribbon 55.1, then loose ends NAUO36-38 11.0 | **67.6** (69.8) | NAUO22, loose |
  | `NAUO17_plugged`: right, routed | stub 1.5, then NAUO39 160.7 | **162.2** (164.4) | NAUO19 on U2 (RWh) |
  | `NAUO18_plugged`: left, routed | stub 1.5, then NAUO40 105.9 | **107.4** (109.6) | NAUO20 on U1 (LWh) |

  One real lead is modelled three different lengths, 68, 107 and 162 mm (section 6). The in-progress `guide.py` uses 115 mm for both
  motors.
- In both poses the lead goes through the same two places. First, **L4's lead hole** (closed, 9.0 tall x 5.0 wide), 2.9 mm from where the
  lead leaves the motor. Second, **L1's lead notch** (10.0 x 5.0), 5-9 mm along, where it rises from below the deck to above it. The
  notch opens forwards into the motor's cut-out, which is open to L1's side edge. Each conductor clears the cut edges by about 0.9 mm.
- The battery lead runs from the clip's +z end down to the back of the barrel plug. **Red is the conductor from the clip stub at x 640.67;
  it ends on the +z side of the plug's axis.** Black runs from x 642.67 and ends on the -z side. The CAD draws this lead only 30-33 mm long
  plugged in and 25-27 mm out (section 6).

## 1. Centre lines (top-level `NAUOn` keys)

Method: the same as the MRA study (`docs/research/mra/cad_wire_paths.md`, section 1), with one change. Each wire instance was welded
(0.001 mm) and split into solids. Each tube was then measured like this:

- The two flat round end faces were found (coplanar faces whose rim fits a circle to 0.03 mm, area within 12% of pi r^2).
- Each side vertex was moved in by the radius along its normal. The change: the normal is averaged over side faces only.
- The points were ordered by distance over the mesh from end a, then binned at 0.4 mm and refined six times.
- The line was thinned to 2 mm spacing or closer, within 0.02 mm of the fine line.

`check` gives the distance of every side vertex from the final line. For every tube it lies within 0.032 mm of the radius, and
the spread is the facets of the CAD tube. In each list, end_a is the end nearer the motor (or the clip).

| Instance | What | Tubes |
|---|---|---|
| NAUO17 / NAUO18 | the motors' own lead stubs, x 716.04-717.54 (they stand 0.5 mm proud of the case face at x 716.54) | 3 x 1.5 mm |
| NAUO31 / NAUO35 | loose pose: ribbon straight back from the motor, through L4 and up out of L1's notch, back to x 662.12 | 3 x 55.1 |
| NAUO32-34 / NAUO36-38 | loose pose: the separated ends from x 662.12 into the plug, pitch 1.1 to 2.54 | 1 x 13.2-13.4 each |
| NAUO39 | right lead, routed: up behind L4 to y 981 at s = 103 mm, over and down onto U2 | 162.3 / 162.9 / 163.9 |
| NAUO40 | left lead, routed: up to y 970 at s = 77 mm, down onto U1 | 106.9 / 108.1 / 109.7 |
| NAUO15 | the battery clip's two lead stubs, z 1347.68-1353.68 (2.85 mm proud of the housing) | 2 x 6.0, r 0.7 |
| NAUO41 / NAUO42 | battery lead, plugged / out | red 32.7 / 26.8, black 30.5 / 25.4 |
| NAUO28 / NAUO29 | the barrel plug's own lead stubs, 3 mm behind the grip | 2 x 3.0, r 0.65 |

## 2. Chains (`chains`)

The fields are as on the MRA: `servo`, `pieces`, `piece_ranges_mm`, `middle`, `length_mm`, `across`, `leaves_servo_at`,
`leaves_servo_direction`, `plug`, `plug_position`, `plug_direction`, `plug_centre`, `plug_box`, `plug_cable_end`, `conductors[]`,
`passes`, `comes_near`. These are added:

- `lines`: `{brown, red, yellow}` centre lines keyed by colour.
- `g_towards`: what to pass to `W.plug()` for that plug.
- `ribbon_pitch_mm` (1.1) and `fan_mm`: about 10.5 mm, over which the conductors spread to the 2.54 pitch before the contact top.
- `ribbon_twist_deg`.
- `leaves_case_at`, `highest_point`.
- `check_loose_lead` / `check_plugged_lead`.
- `other_lead`: for the routed pair, they stay 11.6 mm apart.

- **`middle` ends on the contact top.** The CAD's wires run 2.2 mm deeper into each housing than the point `tools/wires.py` `plug()`
  calls the top (1 mm inside the cable-end face; the BLS-3's cavities stop 1.5 mm inside it). The middle is cut there
  (`middle_trimmed_mm` = 2.2). `conductors[]` keep the full CAD length, and `runs_past_contact_top_mm` says by how much. Cut this way:
  - `W.loose_lead(middle, across, W.plug(plug, g_towards), pitch=1.1, fan_mm=fan_mm)` puts the loose plug where the CAD has it: no
    shift, a 0.2-0.7 degree turn.
  - `W.plugged_lead(...)` ends the three wires on the three contact tops, and the drawn wires stay within 0.12 mm (red) and 0.5 mm (outer
    wires) of the CAD's routed lead.
- `across`: right motor (0, -1, 0), left motor (0, 1, 0). This is the unit vector from brown to yellow at the motor, so `W.ribbon()`
  returns [brown, red, yellow].
- `leaves_servo_at` is the inner end of the middle stub, (717.54, 906.86, z), as on the MRA (the chain starts at the stub). The lead leaves
  heading -x. z is 1384.63 on the right and 1292.33 on the left.
- The routed ribbon twists -124 degrees (right) and +140 degrees (left) between the motor and the plug. `plugged_lead`'s even spread of
  the twist reproduces the CAD to 0.5 mm.
- **Loose pose, as the CAD has it.** The lead comes out of L1's notch about 15 mm along and runs straight back 1.2-2.2 mm above L1's top
  face (it does not touch it) to x 662. The separated ends then go down into the plug, which lies on L1 (bottom at y 909.23) at x 638-652,
  mating face to the rear. The plug is at z 1385.7 on the right and z 1291.3 on the left, straight behind its motor.
- `comes_near`: only L4, at 0.9 mm in its hole, and L1, at 0.2-0.9 mm at the notch and under the loose ends. Within 2 mm, no CAD lead runs
  into the battery, the I/O module, the adapter board or the radio. Nothing in the CAD crosses a lead.

## 3. Plugs (`plugs`)

- **NAUO19 / NAUO20** (plugged on U2 / U1) and **NAUO21 / NAUO22** (loose) carry `mating_direction`, `cable_end_face_centre` and
  `contacts[]`. Each contact has `centre`, `lands_on` and `colour`. With each plug's `g_towards`, `W.plug()` gives G = brown:
  - plugged: [0, 0, 1];
  - right loose: [0, -1, 0];
  - left loose: [0, 1, 0].

  `w_plug` records what `W.plug()` returns (tops at y 945.68 on U1 / U2, and x 651.12 loose). The housing is slightly off-centre
  (0.05 mm, a rib on one face). The CAD's loose housing is the plugged one turned, with the same cavity carrying brown
  (`same_housing_way_round_as_plugged`). The 14.0 x 7.62 x 2.64 housing passes end-on through L4's 9.0 x 5.0 hole, with its 7.62 side
  along y (`features`).
- **NAUO29 / NAUO28** (barrel plug, in the jack / out of it) have no three contacts, so `W.plug()` does not apply (it would raise on
  `contacts`). They give instead:
  - `axis` [1, 0, 0] through (y 925.04, z 1354.06), and `mating_direction` +x;
  - the tip, `mating_face_centre`: x 696.29 plugged (7.0 mm past the jack mouth at x 689.29), x 687.34 out (1.95 mm short);
  - `cable_end_face_centre`: the back of the grip, x 659.74 / 650.79;
  - `cable_exits`: red at z +0.70 from the axis and black at -0.70, each with the plug's own stub;
  - the solids: grip 8.6, sleeve 5.5, insulator 5.25, inner contact 3.8 (diameters, mm);
  - the jack.

  The two poses are 8.95 mm apart along x and otherwise identical.
- **NAUO16** (USB Mini-B, on the controller only) gives:
  - `mating_direction` +x and its tip at (694.92, 933.05, 1112.91), 5.5 mm into the Nano's socket;
  - the shell, 7.0 wide along z and 3.2 thick, with its wider face up;
  - the overmould (x 670.2-687.9), and a strain relief 7.0 across (x 660.9-670.2);
  - 20 mm of 3.5 mm cable, straight along -x to its cut end at x 640.92.

  `cable_end_face_centre` is that cut end, where a drawn cable continues the model; the MRA guide's `USB_B_EXIT` sits the same way,
  54 mm from the tip. `cable_exit` is where the cable leaves the strain relief.

## 4. Battery lead (`battery`)

`battery[pose][colour]` is the centre line: pose `plugged` (NAUO41 + NAUO29) or `out` (NAUO42 + NAUO28), colour `red` or `black`. This
is the shape the in-progress `guide.py` reads. `battery[pose]['conductors'][colour]` has the details: pieces, lengths, ends, directions.
Each conductor starts inside the clip at the inner end of the clip's own stub (z 1347.68) and leaves the clip heading +z at z 1353.68.
It ends on the grip's back face heading +x, and runs over the plug's own 3 mm stub just before.

`middle`, `across` (black to red at the clip: (-1, 0, 0)), `pitch_at_clip_mm` 2.0, `end_across` (0, 0, 1) and `pitch_at_plug_mm` 1.5 let
`W.ribbon(middle, across, pitch=2.0, n=2, end_pitch=1.5, end_across=end_across)` redraw it as [black, red]. The lead passes 1.1-1.9 mm
from the battery's +z face and touches nothing else.

## 5. Features (`features`)

| Key | What | Where |
|---|---|---|
| `L4_lead_hole_right` / `_left` | closed hole in L4, 9.0 (y) x 5.0 (z) | y 902.36-911.36; z 1383.18-1388.18 / 1288.78-1293.78; L4 x 713.12-716.12 |
| `L1_lead_notch_right` / `_left` | open notch in L1, 10.0 (x) x 5.0 (z), opening +x into the motor cut-out (x 713.12-742.47), which opens to L1's side edge | x 703.12-713.12; same z as the L4 holes; L1 y 906.23-909.23 |

Outlines are given as 3D points at mid-thickness. Each chain's `passes` gives the crossing point, the stretch inside the plate and the
gap from each conductor to the cut edge.

## 6. Checks and open points

Checks:
- Tube fit: every vertex lies within 0.032 mm of the radius from its centre line.
- Conductor continuity: the pieces meet end to end with gaps of at most 0.001 mm.
- Colours: matched against the Cadasio project's solid centres of mass (`colour_check`).
- The plug data was driven through `tools/wires.py` (`check_loose_lead`, `check_plugged_lead`, `w_plug`).
- For `materials.json`: `stub_colour_rules` lists each part's lead stubs in the order `build_model.py`'s `order_leads()` sorts them,
  with the colour each must have:
  - the FS90R stubs, mesh x -1.1 / 0 / +1.1: yellow, red, brown (the same on both motors, which share one mesh);
  - the clip, own z -1 / +1: red, black;
  - the barrel plug's `Wires`, own z -0.7 / +0.7: black, red.

  These agree with the present `materials.json` (clip "own z < 0 red"; barrel stubs from the atlas).

Open points:
1. **Lead length.** The CAD's one real FS90R lead is 68 mm loose, 107 mm routed on the left and 162 mm routed on the right. Measure a
   kit motor's lead and draw every pose at that length (the in-progress guide uses 115 mm). The CAD's 68 mm loose lead could not reach
   U1 / U2 at all.
2. **Battery lead length.** It is 30-33 mm plugged and 25-27 mm out in the CAD, which is far shorter than a real 9 V clip lead. The
   plugged pose is also 5.8 mm longer than the out pose, while the plug moves 8.95 mm. Measure the kit's.
3. **Signal colour.** The CAD and Cadasio say yellow; the MRA's captions say orange (reuse_and_colours 2.4, question 2).
4. The CAD has no USB A end and no USB cable on the car (cad_study 4.7).
