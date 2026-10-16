> One of three independent designs for the extension wire's resting route (Steps 97c - 100), 15 Oct 2026; the one taken is on_b2_front_of_r6. Its design is in the .json file beside this one. The scripts, pictures and harness it mentions were working files in the session's scratch folder and are not kept.

# own_reading: resting route for the servo extension, Steps 97c to 100

## How I read Lee's words
In the Step 97c picture, R4 is the front plate holding the slot, and R6 is the plate to its right with the hook-shaped
slot in its ear. The shoulder motor's lead hangs from that ear, down to its plug at about (1378, 581) on screen. On
screen, "a little down and rightward, past R6, under the shoulder motor's wires" points at the floor of B2 just in
front of R6's front corner, under the ear and the hanging shoulder lead. So the reading is: the lead comes out of the
slot, turns right, drops onto B2 in front of R6, and lies there in one easy curl. Its plug lies flat on B2 just past
R6's front edge, on R6's outer side, under the loop the shoulder lead makes outside R6.

Geometry found on the way:
- R6's lower front edge is at x 127.6. Only the ear (y >= 150) reaches x 117.6.
- The I/O module overhangs B2 up to z 175. From the 97c camera it hides the B2 strip beside it (x < ~97). Something
  on the module's edge also hides x 63-95 at z 178-185.
- The 6 mm screw NAUO51 (centre x 104.05, z 181.97, r 2.78, top y 96.5) sits in the front-right corner of B2.
- The floor that shows in 97c is x >= ~98 (x >= 110 at z 153-160, behind the end of B6's wall). On R6's outer side,
  only x < ~132-137 shows.
- 92.4 mm of lead has to go somewhere after the slot (the pocket takes 8.2 mm). The drop to B2 takes about 50 mm.
  The other ~40 mm, plus the 14 mm plug, can only fit the visible floor if the lead curls once.

## Shapes compared (all through H.rest_design, numbers from tool.quick / H.report)
| shape | idea | length | worst wire-part | 97c wire / plug seen | verdict |
|---|---|---|---|---|---|
| hookA | spline: S-drop, curl on B2, plug +x by R6 corner | 92.5 | B2 -0.56 (lead tilted 13 deg on floor, spline dips) | 0.88 / yes | too short, into B2, not flat |
| T1 | level turn, cosine drop, hook r9 | 89.7 | B2 0.16, screw 0.41 | 1.0 / yes | too short, kinks at drop ends (r ~3) |
| B1 | round R6's front edge to its OUTER side, lying along it under the shoulder loop | 102.6 | B2 0.26 | 0.91 / **no (hidden behind R6)**, plug overhangs B2 edge (z 188.8) | looks good in Step 100, fails 97c |
| strip | along B2 strip beside the module | (~103 for a plug at x 56-70) | - | plug hidden (x 63-95 hidden) | needs ~120 mm for a visible plug |
| T2 | level turn, arc-straight-arc drop, hook r8 | 100.9 | B2 0.21 | 1.0 / yes (64% of plug surface) | plug too far behind R6 |
| **final (T3)** | level turn r13 / drop r9-84deg-r9 / hook r10.5 / plug +x | **100.4** | **B2 0.26** | **0.97 / yes (~0.9 of plug surface)** | chosen |

A small search (72 combinations) picked the final turn, drop and hook radii, by plug visibility in 97c and the
clearances.

The ribbon stays flat by construction. It turns only where it is level (about the vertical) and drops only where it
runs straight in plan (about its own width). Parallel transport therefore keeps its width horizontal. end_across
[0, 0, -1] matches the untwisted lead (no roll needed); the other sign would roll it 180 deg along its length.

## Final design (design.json)
- corners: 49 points every 2 mm from tool.turtle; radius 50 (only smooths between the dense points); end_across
  [0, 0, -1]; fan_mm 10.
- Shape: out of the slot level, turning 46 deg towards +z (r 13). Then it drops 39.2 mm onto B2 along heading 130
  deg (bend r 9, 84 deg slope, bend r 9). It lands at about [109.5, 94.3, 165]. Next a level hook r 10.5 round to
  +x, passing 2.1 mm from the screw. Then 8.6 mm straight and up 0.8 mm into the plug's middle contact.
- The plug lies flat on B2 (box x 125.1-139.1, y 93.6-96.4, z 178.5-186.4), 2.9 mm outside R4's edge (z 175.6) and
  6 mm outside R6. It points +x along R6's outer face, under the shoulder lead's loop (y ~149-155 above it).

### Numbers (H.report, all of 97c, 98, 98c, 99, 99c, 100)
- length 100.4 (wanted 100.6 +- 4)
- worst wire-part: B2 0.26 mm (lying on it); screw NAUO51 2.12
- worst wire-wire: base orange 1.21 (where both leads leave R4's pocket)
- plug: no corners inside, no part points inside, nearest B2 0.09; nearest wire 31.6
- frames 97c->98 ... 99c->100: wire gap 1.21, plug-wire 31.6, no moving part near (99)
- seen 97c: wire 0.97, plug yes (~0.86-0.92 of its surface); Step 100: wire 1.0, plug yes
- plug contact on screen: 97c (1281, 635), Step 100 (1408, 663): in frame, away from the edges
- In Steps 98-99, wire_seen is 0.81, because the hanging shoulder plug hides part of the drop from the module-side
  camera. In other words, it really is under the shoulder motor's wires.
- smallest bend radius 6.4 mm (the hook); no kinks; across-y ~0 everywhere (flat)

### Step 100 lift (checked for the plug only)
REST -> via(REST + [0, 10, 0], same turn) -> via(upright at t [71.48, -6.97, 27.24], contact [124, 114, 182], still
beside R6's corner and under the shoulder loop) -> via(T_UNDER) -> T_RISEN -> via(T_ACROSS) -> T_OVER -> seat.

At 10 poses, rotation interpolated about `at`: no part intersection, nearest wire 11.9. Turning upright straight from
the flat rest, without the 10 mm lift, dips a corner into B2. Not trapped: the plug starts below everything (shoulder
loop >= 149) and stays under the shoulder motor's wire until T_UNDER, as the route does today. A route for the lead at
each new stop is still needed.

### Honest caveats
- In 97c the lead's curl reads as a loop that hangs down from the slot and comes back up to the plug at R6's corner.
  From the Step 98-100 camera it reads as a lead dropped onto B2 with a J-curl. Keeping Lee's length in the visible
  floor area needs that curl. Without it the plug goes behind R6 or under the module, hidden in 97c.
- A flat lead bending in its own plane at r 10.5 (on B2) is stiffer than this in reality. At guide scale it reads as
  a curl.
- The base lead's tube crosses in front of the curl on screen in 97c (wire, not part, so not in wire_seen).
