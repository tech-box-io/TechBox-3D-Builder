> One of three independent designs for the extension wire's resting route (Steps 97c - 100), 15 Oct 2026; the one taken is on_b2_front_of_r6. Its design is in the .json file beside this one. The scripts, pictures and harness it mentions were working files in the session's scratch folder and are not kept.

# low_drape: working notes (servo extension resting route, Steps 97c - 100)

## What is where (assembly mm, Y up)
- P0 (slot exit) [131.69, 133.54, 145.03], heading -x. Lead after P0 must be ~92.4 mm (100.6 total incl. 8.2 mm pocket).
- R6 is NOT a plain plate with its front edge at x 117.6: only its top part (y > 142: the ear with the shoulder
  lead's hook) reaches forward to x 117.6. Below y 142 its front edge is set back to x 131.9 - 135.7 (127.6 at the foot).
  So the lead can pass under R6's forward ear, in front of its lower edge, at any height below ~140.
- B6 right wall (NAUO6): a tab at x 95.5 - 107.5, z 150 - 153 rises to y 118.53 (the rest of the wall is at y 102.1).
- Module (NAUO82) x 43 - 96.7, z 116 - 175, y 102.9 - 117.4 (board top 106.4 at its corner; jack up to 117.4).
- Screw NAUO51 head on B2 at x 101.3 - 106.8, z 179.2 - 184.7 (3 mm tall). B2 edge z 188.3.
- Shoulder motor lead: from the motor it loops outside R6 (x 123 - 194, y 148 - 165, z 175 - 207) up to the hook in
  R6's ear (~[123.5, 163, 170-175]); in 97c-98c it then runs -x at y 160, z 165.7 to the hooked plug; from 99 it drops
  from the ear to y 154.7 at z 157 and climbs over the module to row 9.
- Visible B2 in Step 97c: x 102 - ~146 at z 173 - 188 (R6's cut-back lower edge hides x > ~146 at z ~182);
  x < 102 near z 175 - 180 is hidden by the module. In Step 100 all of x 100 - 130, z 173 - 188 shows.

## Reading Lee's words
On the Step 97 camera "right" is plan direction (-0.56, +0.83) and B2 is seen steeply from above, so a lead that ends on
B2 beyond R6's plane, just in front of R6's foot, shows only a little below the slot (plug ~230 px right, ~50 px down
of P0) - and it sits directly under the shoulder motor's lead (both its loop outside R6, ~55 mm above, and, on screen,
its hooked lead/plug). "Past R6" = the lead passes R6's front (under its forward ear) to the outer side of R6's plane.

## The length problem
92 mm of loose lead must lie in the visible pocket x 100 - 135, z 145 - 188. A monotone curve from the slot to the
B2 corner beyond R6 is only ~55 - 65 mm (total 75 - 85). The ways to absorb the rest:
(a) a U on B2 (bulge toward -x to x ~101, then back +x along R6's outside, plug pointing +x) - gives 98 - 99 mm;
(b) plug further back along R6's outside - hidden by R6 in 97c beyond x ~140 (t4a: plug not seen);
(c) over the module corner - looks like it is going into the module, and leaves R6 behind; rejected;
(d) J-curve with the plug pointing +z - only ~74 mm; rejected (would need Lee's length dropped).

## Tries
- t1: U on B2, crest free in air, plug +x at x 120-134; len 91.2 (short).
- t2: U draped over the B6 tab, len 98.7, but the conductor twisted 40 deg (wrong end_across sign) and went 1.26 mm
  into the tab. Using end_across -z (sign -1, the way the ribbon naturally arrives after a 180 deg turn) keeps it within
  ~17 deg of flat.
- t3: corners [[119,131.8,146.3],[104,121,152.5],[100.8,106,164.5],[102.5,96.5,173.5],[113,94.6,181.5],[126,95.3,182.6]],
  radius 8, end_across [0,0,-1]: len 98.5; B6 0.31, B2 0.48, screw 1.58, base lead 1.25, plug on B2 0.24; seen 1.0 / plug
  seen in 97c and 100; screen 97c (1282, 635), 100 (1408, 663); frames 98-100 all clear. Meets every number.
  Look: Step 100 view reads as a loose curl lying on the base. Step 97c view: the U reads as a narrow loop (its legs
  overlap on that camera) - the weak point.
- t4a-c: smaller bulge (x >= 106, clear of the tab), plug further back: len 93.7 - 103.5 but the plug hides behind R6's
  foot in 97c. Rejected.
- t5, t7: plug overhangs B2's edge (z max 188.4 / 188.9). Rejected.
- t6b-d: len 100.1 - 102.3 but only 55 % of the plug's surface shows in 97c (rear half behind R6's foot).
- t8a-c, t9a-c: trade length for plug visibility: plug further forward -> more shows, less length; t9 grazes the screw.
- s1 (smooth Hermite plan path + PCHIP heights): no better than hand corners (tighter bend at the landing). Dropped.
- Sweep of the U's turn past the screw -> L1 (final).

## Final: L1 (design.json)
corners [[118,131.5,146.6],[105.5,121.0,152.6],[101.2,108,163.0],[101.2,97.5,172.0],[109.2,94.6,179.0],[117,94.6,183.0],
[126,95.25,183.4]], radius 8, end_across [0.0444, 0, -0.999] (flat; the -z sign is the way the ribbon arrives after its
180 deg turn, so it stays within 17 deg of flat all along), fan_mm 10.
Shape: out of the slot heading -x, a shallow sag (133.5 -> 121) onto the top edge of the B6 wall's tab (rests 0.36 mm
over it), down past the module's corner (x 101, clear of it) onto B2 beyond R6's plane, a U round on B2 (1.4 mm past
the screw head), plug lying flat on B2 at R6's foot pointing +x (x 124.7 - 139.2, z 179.4 - 187.8, 0.5 mm in from
B2's edge), right under the shoulder motor's lead where it loops outside R6 (~55 mm above).
Numbers (full H.report): length 98.3 (wanted 100.6, -2.3); worst wire-part B2 0.31 (B6 tab 0.36, screw 1.41) in every
view; worst wire-wire base orange 1.25; plug: nearest B2 0.17, nothing inside, >= 31.5 mm from every wire; frames
97c->100: no moving part near, wire gap 1.25, plug-wire 31.55; seen 97c wire 1.0, plug yes (82 % of its surface;
its rear end is behind R6's foot), 100 wire 1.0, plug 100 %; plug on screen 97c (1286, 632), 98 - 100 (1413, 667).
Smoothed bend radius >= 8 mm everywhere after the slot.

Weak points (honest):
- A 92 mm loose lead cannot stay "a little down" in 3D: it rests at mid height on the B6 tab for its first third and
  then reaches B2. It is "a little down" on screen only: the plug ends ~240 px right and ~45 px below the slot in 97c,
  but the bottom of the U is ~215 px below it.
- In the Step 97c camera the U's two legs line up, so it reads as a loop of lead (it reads as a loose curl lying on
  the base in the Steps 98 - 100 camera). The length is what forces the U: without it the lead would be ~75 - 85 mm.

## Step 100 from here (contact point of the plug, checked against Step 100's parts and wires)
rest [126, 95.25, 183.4] -> straight up [126, 112, 181] (stay below ~145: the shoulder lead's loop is overhead at
y 150 - 155) -> under R6's ear and the shoulder lead [112, 128, 168] -> over the B6 tab and module [96, 148, 158] ->
between the joystick wires and the shoulder lead [78, 164, 155], [60, 163, 155] (the 100c route of the extension
passes [72, 165.7, 151]) -> above row 10 upright [52.5, 140, 154.8] -> seat. Turn the plug from flat to upright over the
last two stops. Clearances along that path >= 2.6 mm (closest: shoulder lead beside row 9 on the final drop).
