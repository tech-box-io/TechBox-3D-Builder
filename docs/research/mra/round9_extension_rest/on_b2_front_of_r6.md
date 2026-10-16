> One of three independent designs for the extension wire's resting route (Steps 97c - 100), 15 Oct 2026; the one taken is on_b2_front_of_r6. Its design is in the .json file beside this one. The scripts, pictures and harness it mentions were working files in the session's scratch folder and are not kept.

# on_b2_front_of_r6: servo extension resting route (Steps 97c to 100 start)

Final design: `n9` in designs.json, written out in design.json. Pictures: pic_n9_Step97c.png, pic_n9_Step100.png. These are drawn over
the reference renders, which still show the old upright plug. Faint dots are wire hidden by parts. The plug outline is dark where it shows.

## What it is
- The extension leaves R4's slot heading -x, bends down and falls a little towards +z (z 147 to 156) onto B2 in front of R4 and R6,
  about 20 mm in front of R4.
- Its slack lies on B2 in one smooth curve, landing at about (107, 159), out to x 101.5 at z 166 and back past the R6 side of the
  hex screw NAUO51.
- The plug lies flat on B2 just past R6: x 119.9-134.1, y 93.64-96.39, z 179.4-187.5. Its mating end points +x, along R6's outer face.
  It sits directly under the shoulder motor's lead where that lead crosses R6 (x 124-135, y 150-156), and on screen in 97c it is right
  of R6's front edge, below the hooked shoulder plug.
- corners (after P0): [[124.5,133,147],[118.2,128.3,151.5],[113.8,111.5,154],[111.5,98,155.5],[106.9,94.5,159],[101.4,94.5,165.8],
  [101.9,94.5,173.6],[108.7,94.75,179.4],[113.5,95.12,183.25],[121,95.12,183.4]], radius 10, fan_mm 10,
  end_across [0.02, 0, -0.9998] (level, so the plug lies flat).
- plug_pose: {t: [68.476, -25.846, 28.641], r: [0.5850, -0.5735, -0.5735, -119.34], at: [52.524, 120.966, 154.759]}

## Numbers (H.report, frames on)
- Length 99.8 mm (wanted 100.6 +- 4).
- Wire to parts: the closest is 0.39 mm, to B2 (where it lies). Next: screw NAUO51 0.71, R4 1.64 just past the slot, B6 wall end
  NAUO6 2.82, R6 10.4, R1 13.7, module 10.6.
- Wire to wire: closest 1.23 mm, to the base motor's lead beside the slot. Shoulder lead 22.7 mm.
- Plug: no corners inside any part and no part points inside it. It rests 0.11 mm above B2. The plug to the nearest wire is 34.4 mm.
  It is 7.5 mm from R6, 8.5 mm from R1 and 0.8 mm inside B2's edge (z 188.3).
- Steps 98 to 100 frames: nothing negative. Wire gap 1.23, plug to wire 34.4, and no moving part comes near.
- Seen in 97c: 0.84 of the wire after the slot. What is hidden is the bottom of the curve, behind the B6 wall end. The plug shows:
  its centre, and every hull corner. In Step 100: wire 1.00 seen and the plug shows. The plug is on screen at 1394,689 in Steps 98
  to 100 and 1308,657 in 97c.
- Shape:
  - Tightest bend is 8.7 deg/mm, about a 6.6 mm radius. It is where the lead turns flat onto B2, an easy bend about its width.
  - Tightest bend in the plane of B2 is a 7.6 mm radius. The curve on B2 is 38 mm long and turns 133 degrees in all.
  - The roll that brings the lead level is 11.7 degrees, spread along it. The lead's tilt where it lies on B2 is at most 4.7 degrees.
  - The plug's tilt is 0.

## Why a curve on B2 and not a straight lay past R6 (what was tried)
- 92 mm of lead is left after the slot. A direct lay past R6 (down and +z, then -x along B2 between R6 and the screw) uses it all and
  ends with the plug at x 72-88, z 175-185, beside the I/O module's barrel jack.
  - In 97c the module's board edge and the jack hide B2 there (x < 101 at z < 179; x 84-96 at z < 180).
  - c5 is the best of these. It is 97.0 mm, but only 14 % of the plug shows in 97c and its centre is hidden; c2 / c4 had about 25 %.
  - It fails "the plug shows in 97c".
- 97c shows the plug fully only on B2 at x 101-127 (and up to x 134 near the edge, z 186), outside the screw.
  - The straight distance from the slot to there is about 55 mm, so about 35 mm of slack has to lie somewhere.
  - Options looked at:
    - a hairpin behind R6: folds on itself.
    - lying deeper towards the module (x < 101): hidden by the jack in Step 100 and runs into B6 (m9g: wire_seen 0.74 / 0.64,
      B6 -1.27).
    - via the bay towards R5: runs under the base lead, and goes left first on screen.
    - round the end of the B6 wall: goes down to the old plug spot first.
  - The curve in front of R6 (m9 and n family) was the only one that kept the length, the clearances and the views.
- Making the drop fall slightly towards +z (rather than straight down) cut the roll the flat lead needs from about 35 to 12 degrees,
  so it lies nearly flat on B2.

## How it reads against Lee's words
- "past R6" and "under the Shoulder Motor's wires": yes, for the plug and the end of the lead, both on screen in 97c and in 3D.
- "a little down and rightward": overall, yes. But in 97c the lead first drops onto B2 in front of R4 and then curves right to the plug.
  It dips to about the height of the B6 wall end on screen before it comes back up to the plug, so it is a U on screen, not a shallow
  diagonal. This is the cost of keeping all 100 mm.
- It does not look plugged into B2: the lead and the plug lie flat on it.

## Step 100 from this rest (sampled, plug only, Step 100 scene: no part hit, nearest wire >= 4.7 mm until the existing last legs)
1. Lift straight up 35 mm, still lying flat. The plug's contacts reach y 130 at z 183, under the shoulder lead over R6 (y >= 150).
2. Glide -x/-z while turning upright to seat + [50, 21, 10] (abs about [102.5, 142, 164.8]).
   - This passes in front of R6's ear (x < 117.6 at z 169-172) and below the shoulder lead.
   - It ends on the +z side of the shoulder lead's run down to row 9.
3. Then the existing T_RISEN [43.5, 52, 3.4], via T_ACROSS [0, 52, 3.4], T_OVER [0, 52, 0], [0, 0, 0].
   - It goes over the jumper and joystick wires, with gaps 3.7 mm or more until it is over row 10.
   - It no longer needs T_LIFT or T_UNDER: the plug is already on the +z side of the shoulder lead, and its lead already runs under it.
- The extension's own wire routes for these stages are still to be made. EXTENSION_LEAD['risen'] / ['over_row'] can serve from
  T_RISEN on.

## Not met / caveats
- All the numeric requirements are met.
- The one judgement call is the U seen in 97c (see above). If Lee wants a shallow diagonal, the plug has to rest beside the jack,
  where 97c hides it, or the lead has to be shorter.
