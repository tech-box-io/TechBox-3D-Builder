# LAC deconstruction, first draft: review of the pictures and the motion

Review of `LAC Build Instructions/deconstruction.py` -> `steps-deconstruction.json` (47 steps), 21 Oct 2026. Read-only: the strips
`review/pictures/stepNN.png` (Step N as it opens, Step Nc half-way, Step Nc done), the two close-ups, `motioncheck_draft1.txt`,
`generator_log.txt`, the steps file and the published pictures (`published/pictures/19075-lac_deconstruction/NNN.jpg`). Nothing was
run that loads the CAD. Positions below are pixels in the strip's own 960 x 540 pane (strip x minus 960 / 1920 for the 2nd / 3rd
pane, y minus 30). The known Full Build replays (6c, 11c, 14c in motioncheck) are not reported again.

Most steps read well: the arrows are the published sizes and point the way the parts go, the half-way pictures show no part passing
through another, the LCD pin labels (16 - 19) are clear, and 38 - 47 share one tidy camera. What follows needs a change.

## High

**Step 13 (spread the F7s): neither arrow reads, and one is hidden under F4.** F4 still hovers where Step 10 left it
(`offsets.F4 = [-82.7, 17.3, -0.1]`: its underside about y 971, its front edge about x 642 - 645). The hand-set arrows are at y 968
(deconstruction.py:201-202; steps file "Step 13".arrows), so F7A's arrow (x 659 -> 622) lies 3 mm under F4: only a headless red stub
shows, at about (590 - 625, 225 - 240), under F4's corner. F7B's arrow (x 691.6 -> 732.1, towards the camera) projects out over the
breadboard and the RTC, at (465 - 540, 260 - 295), pointing into the wires; it touches no F7. A learner cannot tell that the tops are
to be pulled apart. The published Step 26 (070.jpg) has both arrows at mid-height, beside the uprights, across the screen.
Fix: the published arrows and camera for this step, where F4 is behind the F7s and clear of the arrows:
`arrows=[dict(tail=[660.74, 918.41, 1243.69], head=[623.84, 918.65, 1244.77], normal=[0, 0, 1], part=F3, width=3.75),
dict(tail=[691.77, 921.08, 1243.91], head=[732.26, 922.14, 1245.34], normal=[0, 0, 1], part=F3, width=3.8)]` with
`view_dir=[0.7131, 0.5802, 0.3935], frame=([644.2, 892.6, 1291.2], 114.5)` in place of `camera_of('Step 44')`
(published_geometry.md section 2, frame 070). (Keeping our camera instead, the arrows would have to come down to about y 945 on the
-z face, z 1222, to clear F4.)

**Step 9 (F8): F8 is hard to find, the arrow lies on the potentiometer's leads, and F8 looks threaded on them.** The camera (the
Full Build's Step 50, from the +z end) shows F8 almost edge-on behind F4's front tab, (530 - 555, 260 - 330), its code not visible.
The arrow (tail [722.35, 919.53, 1265.97], +x) starts beside the F3 code and runs along the red / tan / black leads to F1, covering
them over most of its length (zoom of 400 - 800 x 150 - 420). In 9c half-way F8, sliding out +x, crosses the three leads mid-height:
the leads are drawn across F8's face, so it reads as a strut slid along the wires. (In 3D the leads pass about 15 - 20 mm in front of
it, so motioncheck finds nothing; the trouble is what the picture says.) The published Step 7 (019.jpg) looks from the -z end: F8's
face and the arrow are clear of the leads. Fix: `g.remove(..., [F8], arrow_style={F8: size('f8', at=[706.38, 925.49, 1267.42])},
view_dir=[0.5117, 0.6969, -0.5024], frame=([689.6, 889.4, 1273.7], 114.5))` (the published camera and arrow tail), then look at
9c again.

## Medium

**Step 14 (buzzer out): the eye sits on the arrow.** `eye=[dict(id=BUZZER, ..., side='near-above', reach=0.05)]`
(deconstruction.py:207) puts the eye's white pad over the middle of the up arrow, (535 - 605, 225 - 265): the shaft shows below it
and the head above, and the head ends on F4's edge and engraved code. Two cues on one spot, neither clean. Fix: `side='near-right',
reach=0.07` (empty white to the right of the F7s), or drop the eye: the arrow already says "lift out" (the published eye is far
from its arrow, top right, 072.jpg).

**Step 3 (F5): F5 is seen nearly edge-on and the arrow's tail covers its code.** The Full Build's Step 55 camera
(dir [0.8164, 0.3983, 0.4182]) looks along F5's face; F5 is a sliver at the left end of the case, and the arrow's tail
(682.9, 919.53, 1371.07: F5's middle) sits on the engraved "F5". The published Step 3 (008.jpg) shows F5's face and its code, the
arrow at its lower edge. Fix: `arrow_style={F5: size('f5', at=[683.78, 881.40, 1368.15])}` (the published tail, F5's lower edge)
and `view_dir=[0.5964, 0.4991, 0.6287], frame=([683.0, 919.0, 1320.0], 115.0)` (the published direction, our framing).

**Step 10 (F4): the caption says "lay it behind the case", but F4 ends in mid-air.** Step 10c's path ends at
`[-82.7, 17.3, -0.1]`: 83 mm back and 17 mm higher than its seat, i.e. about 75 mm above the table, at the height of the case top
(10c done, F4 at (440 - 755, 1200 - 1310) of the stack: level with where it was). It stays there, floating with the switch hanging
under it, through Step 36, and is in the way of the cues in Steps 13 - 15. The pose is the Full Build's own (its Step 48 says "Lift F4,
with the switch, over the frame"; the published 8c "held above"). Fix, the wording: "Lift F4, with the rocker switch, off the tabs of
the F7s and F9, and move it behind the case. Leave the switch's wires connected." (or "hold it up behind the case"); a real fix
would lay it on the table (new switch-lead routes: Lee's call).

**Step 12 (F9): the "tip" arrow is not on F9's top, and its head lies on the potentiometer's leads.** The stage-0 arrow
(tail [728.39, 924.95, 1355.78] -> [761.34, 932.48, 1355.78]) starts 30 mm in front of F9, at mid-height, over the breadboard's end,
and its head ends on the black and tan leads (zoom of 330 - 700 x 170 - 380). The caption says "Tip the top of F9 toward the front":
the arrow should be on the top. Fix: `arrow_style={F9: size('f9', stage=0, at=[697.9, 953.7, 1358.1], then=[size('f9', stage=1)])}`
(the published tail, F9's top edge). The close-up's leader then also has a clear run (it crosses the leads and F1 at y 375 now).

**Step 7 (LCD out of F9's notches): the eye's leader and the close-up's leader cross.** The eye (225 - 295, 340 - 370) points to
the lower notch; the close-up's leader, starting just under the eye at about (293, 382), goes to the upper notch, and the two blue
lines cross over F3 and F9 (zoom of 200 - 500 x 250 - 430). The strip does not show the close-up box itself: check in the player that
it does not sit on the eye, since its leader starts beside it. Fix: `eye=[dict(id=LCD, anchor=[713.76, 895.78, 1358.05],
side='near-below', reach=0.05)]`, so that the eye hangs under the lower notch and its leader stays below the close-up's.

**Step 11 (F1 back in front of the breadboard): the eye covers the middle of the case.** `side='up-left', reach=0.05` puts the
eye's pad over the breadboard, the F7s' feet, the F3 code and where the potentiometer's leads leave the case
(430 - 500, 245 - 290). Fix: `side='right'` (the empty white right of F1) or `'down-right'`.

**Eyes that hide the wires or cross the board (Steps 16, 17, 34, 36, 38, 39, 42, 43).** Each is placed by default:
- 16 and 17: the pad covers exactly where the purple (16) and yellow (17) LCD wire arcs over the board to its breadboard end
  (410 - 485, 205 - 250), so the wire being taken off cannot be followed. Fix: `eye=[dict(id=male, side='up-right', reach=0.06)]`
  in the loop at deconstruction.py:222-224 (18 and 19 are already to the right).
- 34 and 36: the eye is at the frame's left edge (15 - 85, 370 - 400) and its leader runs about 350 px across the green and black
  jumpers, the Nano and the resistors to j29 / j27. unplug() passes `eye=` on: `eye=[dict(id=SWITCH_CAPS[colour], side='near-right',
  reach=0.05)]` at deconstruction.py:267-269.
- 38, 39, 42, 43: the eye is above the board and its leader runs down through the RTC module and the jumpers. The published puts
  these below and to the right ((60, 51) %, 092.jpg). Fix: `eye=[dict(id=eye_cap, side='down-right', reach=0.06)]` at
  deconstruction.py:280.

## Low

**Step 15 (F7s up): the arrows are where the F7s will be once closed, not on their spread tops; F7A's head is on F4.** Both
`stage=1` arrows (tails x 650.51 and 699.99) are drawn above the closed positions, 15 - 18 mm off the tilted tops: F7B's starts over
the jumper caps. F7A's head (y 979 - 992) is drawn over F4's edge and code. In 15c half-way F7A rises past F4's front edge with a few
mm to spare (top at (380, 320) of the zoom, touching F4's outline on screen). All three come from F4 hovering at x 554 - 645 (Step
10, above). No change needed if Step 10 stays; with F4 laid elsewhere they go away.

**Steps 28 - 31 (F1 alone): the nut and the washer are tiny and F1 is seen at a glancing angle.** The Full Build's Step 28 camera
(dir [0.3505, 0.4506, -0.8211], radius 98) is 69 degrees off F1's face: F1 is a thin parallelogram, and half-way through 29c and 30c
the nut and washer are specks of about 15 x 25 px. The published (031, 035, 038.jpg) shows F1's face and code. Fix:
`view_dir=[0.6112, 0.5658, -0.5535], frame=([799.9, 907.0, 1389.3], 98.2)` for Step 28 (published_geometry.md, the frame-031 camera in
F1's seated frame, moved by BUILD [100, 35, 100]), kept for 29 - 31; or, keeping the camera, a closer frame for 29 and 30 only,
e.g. `frame=([845.0, 950.0, 1335.0], 60.0)` on the shaft.

**Step 21c done: the freed red lead runs to the bottom edge of the frame.** The red lead lies straight out from the buzzer towards
the camera and its cap ends at (330, 545), on the pane's edge (the radius-47 camera of Steps 21 - 23). Fix: `frame=` radius about 55
on Step 21 (kept by 22, 23), or accept.

**Steps 24c - 26c done: the "hanging" leads stick straight out in mid-air.** After unplugging, each lead runs horizontally from the
potentiometer towards the breadboard and ends in the air (24c done, cap at (440, 1430) of the stack). The shape is the Full Build's
Step 29c, so it is consistent with the build, but it does not hang (the published 9c hangs them straight down). Lee's call.

**motioncheck, new contacts.** 24c: pot black passes through pot tan (centre lines 0.65 mm apart at 73 %, near [718.6, 916.5,
1334.1]); visible in the half-way picture as the black lead sliding under the tan one. It happens because `to_hanging()` blends the
black lead from its plugged shape (route 49) to the Step 29c hanging shape (46), a change the Full Build never animated (its Step 32
cut straight from 46 to 49). 35c: switch black and switch tan 1.04 mm apart at 88 %, near [603.1, 916.3, 1259.0], where the two leads
come to hang side by side under the switch: invisible. Fix for 24c, if wanted: a stop higher above the board first
(`paths={cap: [VIEW[step]['path'][0], [0, 30, 0], hanging]}` with a matching lifted route), or accept.

**Step 2 (F2): the arrow's head crosses the eye's leader at the slit.** The arrow (F2's middle, y 919.5) points down to the slit
where the eye points (zoom of 420 - 760 x 250 - 480). Fix: `arrow_style={F2: size('f2', stage=2, at=[645.22, 958.23, 1291.32])}`
(the published tail, near F2's top), clear of the slit at y 889.

**Steps 6 and 11: the camera is far, and F1 runs off the frame in Steps 7 - 10.** The Full Build's Step 47 camera (radius 166.9)
leaves the case and F1 at about a third of the frame's width, with wide margins; in Steps 7 - 10 (the Full Build's Steps 52 - 49
cameras) F1, lying aside, runs off the bottom and right (generator_log.txt's NOTE lines for Steps 7, 9, 14 and 16 - 19 name F1 or other parts lying aside that the copied cameras leave out). Both are
the Full Build's framings and the subject is clear, so this is optional: e.g. `frame=(..., 135)` on Step 6.
