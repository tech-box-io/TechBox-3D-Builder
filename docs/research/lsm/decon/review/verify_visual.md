# LSM deconstruction: verification of review_visual.md (21 Oct 2026)

Skeptic's pass over the 12 visual findings. Basis: the draft the reviewer saw (deconstruction.py of 197 lines; the arrows quoted in
review_visual.md). Screen positions were computed with the player's own camera (core.js `cameraPose`: fov 45, padding 1.08, the flip
of Steps 10 - 11 included) at the pictures' 2000 x 1163; the projection reproduces the pictures to a few pixels (Step 4's four arrows
and ring, Step 11's arrow). Part boxes: assembly-report.json. Nothing was run but light JSON reading.

**The draft changed while this check ran.** deconstruction.py was rewritten at 18:10:55 and 18:13:27 (TechBox's published arrow sizes,
`dims=`, and `then=` stages for D10, the matrix over D4, D3, D4 and the matrix off its connectors: docs/research/lsm/decon/arrows/),
steps-deconstruction.json regenerated at 18:11:42 and 18:13:47, and the pictures redrawn at 18:11:51 - 18:12:30 from the 18:11:42 file.
The pictures on disk therefore match neither the reviewed draft nor the current steps file (025.png shows D4's slide arrow about 80 mm
long; the 18:13 file has 30 mm, `d4_slide`). Redraw them before anyone reviews from them again. Each verdict below says what the
revision changes.

## Summary

| # | Step | Verdict | Severity |
|---|---|---|---|
| pre | commit dependencies | refuted | low |
| 1a | Step 4, close-up in the player | refuted | low |
| 1b | Steps 4 and 19, close-up in the PDF pictures (pages.js) | confirmed | low |
| 2 | Step 11, D3 | confirmed (fixed in the revision) | medium |
| 3 | Step 13, D4 | confirmed; the fix's lift arrow moves onto the button's leads | medium |
| 4 | Step 7, D10 | confirmed; worse in the revision | medium |
| 5 | Step 8, matrix | uncertain; the fix does not clear the wires | low |
| 6 | Steps 2 - 4, stacked arrows | uncertain (cosmetic); Step 4 worse in the revision | low |
| 7 | Step 9, D9_A | confirmed; the fix collides with D9_B's arrow | low |
| 8 | Steps 21, 23, resistor arrows | refuted | low |
| 9 | Steps 16, 20, eyes | uncertain; the fix puts an eye on R12K | low |
| 10a | Steps 19 - 20c, framing | confirmed | low |
| 10b | Step 19, close-up in the player | refuted | low |
| 11 | Step 16c, pins | refuted | low |
| 12 | Step 17, nut arrow | confirmed; `scale` would misfire in the revision | low |

## Preamble: "then= and let_go are only in the working tree": refuted

`git grep` on HEAD: `let_go` is at tools/stepgen.py:930, 959, 980 and `then=` at 1091 - 1099, 1802 - 1805 (commit f6c9063, the PMG's
staged arrows). `git diff` shows only two uncommitted hunks in stepgen.py (a take-apart close-up's `side=`, `marks=` and `ghost=`, which
Step 19 already uses through `ghost=`) and one in player.js (a close-up keeps clear of arrows). The reviewer is right that `side=` on a
take-apart close-up needs the uncommitted change. review/code_changes.diff is stale: written at 17:50 against player.js 5778d63, it
still shows the `then=` / `staged_arrows` hunks that f6c9063 has since committed.

## 1a. Step 4: "the player would probably also put the close-up on the right": refuted

screenRect counts every visible part and wire (player.js:349-366). In Step 4 the USB cable and its A end run off the right of the frame,
so the room on the right is negative at every window shape: 2000 x 1163: left 621, right -16; 1440 x 800: 459 / 21; 1000 x 600: 304 / -24;
760 x 570: 194 / -118. The player picks the left, level with the ring (player.js:524-530): a short leader, and the box (x 12 - 312 at
1000 px) is clear of D11_B's arrow. `side='left'` is harmless but changes nothing. The ring on D3's face marks where the hidden tab is,
which is what a close-up of a hidden joint does; not a fault.

## 1b. Steps 4 and 19: the PDF pictures put the close-up in the far corner: confirmed (low)

pages.js:31-34 always uses the corner farthest from the spot and knows nothing of arrows, eyes, labels or `side`. That hides D11_C's
arrow in 007.png and runs Step 19's leader across the breadboard and the matrix in 037.png. It only matters for the 2D PDF, which is not
made yet, and it affects every guide's PDF, not only this one. **Fix:** in pages.js, before making the LSM PDFs, place the close-up the
way player.js's `buildInset` does for a W x H frame (sides by room, `side=` first, clear of arrows and callouts). Do not just scale the
on-screen `#inset` rectangle, because the window's shape differs from the picture's. `side=` in deconstruction.py would not change the
PDF.

## 2. Step 11: D3's arrow floats and shows only the slide: confirmed (medium); fixed in the revision

The tail `[681.58, 881.63, 1137.67]` is the generator's default: from the seated D3's middle, along the slide, 2 mm past the part
(stepgen.py:1443-1445). Because the slide runs 22 degrees off D3's plane, that is 16 mm off its face, about 57 px past the free end
(tail (1347, 578); free end (1302, 544)). The rulebook (section 11, Lee 21 Oct 2026, cadasio-patterns.md:292-297) asks for an arrow per
stage. The 18:13 revision does exactly the reviewer's fix (`size('d3', stage=0, then=[size('d3', stage=1)])`): the swing arrow now starts
on D3's face, and the slide arrow starts on the swung free end (`[680.74, 881.63, 1121.4]`). Nothing left to do.

## 3. Step 13: no cue for D4's slide, and the lift arrow reads as the button's: confirmed (medium)

The cue for the first stage is missing, against the same rule. The old arrow (screen (1034, 580) up to (1037, 415)) is drawn straight
over the push button (projected box x 970 - 1084, y 479 - 595). **The reviewer's `at=` for the lift is wrong:** `[587.9, 909.0, 1172.0]`
rises from (951, 662) and crosses the red lead and the black lead at (948, 551 - 554) and the purple wire at (947, 504), and passes
10 px from the 330 ohm resistor's leg. **Better:** the D2 end of D4's top edge, `at=[587.9, 909.0, 1245.0]` for the lift (screen
(1182, 522) up), clear of the button, the leads and the wires (check it in the player). The stage-0 slide arrow can stay where the 18:13
revision puts it, on D4's outer face. In that revision the lift arrow (`[587.91, 909.04, 1204.25]`, 80.1 mm, screen x 1061 - 1072)
still runs up the button's right edge, so the `at=` is still needed.

## 4. Step 7: D10's arrow points into the wires: confirmed (medium in the revision; low as reviewed)

The old arrow's centre line crosses the grey wire (drawn white) and comes within 7 px of the purple one, with a head about 88 px wide.
The reviewer's fix (`at_now(D10, [599.5, 886.0, 1207.0])`, `scale=0.7`) works at the old size: the head stops about 39 px from the
nearest wire against a half-width of about 29 px. The tail lies 1 mm behind D10's far face, but only its first 0.3 mm is hidden, so that
is fine. **The 18:13 revision makes this worse:** the slide arrow is the published 50.8 x 4.4 mm from the same tail, and it crosses all
three wires (screen (1104, 700) to (1408, 559)). At 4.4 mm wide even a 20 mm arrow's head reaches the wires. Its drop arrow (stage 1,
`[638.26, 929.72, 1244.17]`) sits behind D10 in the still (013.png). **Fix in the revision:** the reviewer's `at=` with dims of their own
for the slide, about `(20, 2.5)`, not the published D10 size, which belongs to the published *drop* (its Step 14: "1 arrow down 51 mm");
then check the still and the player.

## 5. Step 8: the matrix arrow crosses the wires: uncertain (low)

The crossing is real: the old arrow's centre line crosses all three wires at screen (1096 - 1116, 425 - 431). **The fix does not work:**
`shift=[0, 10, 0]` still crosses all three, and now twice each, over the arch. Only +25 to +30 mm clears them, and the arrow then floats
well above the matrix. Placements along the edge (z +12 to -30) or on the top face cross them too, because the wires hang from that
edge across the whole space the arrow points into. The wires go with the matrix in the arrow's direction, so the crossing does not
mislead. Leave it, or put it to Lee. The 18:13 revision (70.6 mm, then a drop) is the same.

## 6. Steps 2 - 4: arrows on the exact diagonal: uncertain (low, cosmetic)

The geometry is right: D11_D, the target and D11_A lie on the camera's diagonal. Steps 2 - 3: the plate's arrow plainly starts on D8 /
D7 and only crosses the far post's latch head. Step 4 as reviewed: the front post's head stops at the back post's foot (screen y 489),
and the back post's own arrow starts at 372, so there are two distinct heads, not one long arrow. **The 18:13 revision's 45 mm post
arrows put the front head over the back post's middle** (007.png, current), which makes the point stronger. Fixes: the reviewer's
`at=[650.0, 934.4, 1180.0]` (and y 918.5 for D7) works (screen (851, 553) to (835, 343), about 150 px from the nearest post). For Step 4,
prefer a `view_dir` about 15 degrees off the diagonal to `arrow_scale=0.6`, which would undo the published sizes.

## 7. Step 9: D9_A's arrow rises out of the USB plug: confirmed (low)

The tail (947, 580) is inside the plug's projected box (x 885 - 1004, y 578 - 673). In 017.png it sits on the plug's black body.
**The reviewer's fix collides with D9_B's arrow:** `at=[618.6, 902.7, 1178.0]` gives (864, 626) to (855, 490), and D9_B's tail
(844, 519) falls inside the new head (about 55 px wide). **Better:** `at=[618.6, 902.7, 1190.0]`, which gives (903, 605) to (897, 470):
left of the plug's visible body and about 20 px clear of D9_B's arrow. That holds at the revision's published lengths (61.2 / 69.2 mm)
too. The D2 end (z 1232 - 1245) runs into the button and nut instead.

## 8. Steps 21 and 23: resistor arrows "read as the Nano's": refuted

Both arrows start on the resistor's body, and the caption names the resistor and its two holes. The overlap is partial. Step 23's
shaft (x 988 - 1015) runs along the chip's left edge, not "wholly over" it. Step 21's shaft runs along the socket's right edge (socket
box x 813 - 1006). TechBox's published take-apart has the same thing: arrows straight up from each resistor body, 32 and 31.5 mm, which
the 18:13 revision now copies, so "already at the 15 mm minimum" no longer applies either. The fix cites "review_wording.md item 6",
but the hole-label item is **item 9**, and verify_words.md left it UNCERTAIN: TechBox's published LSM take-apart shows no hole labels,
the PMG's take-apart has eyes without labels, and it is plan question 5 for Lee. No change on visual grounds.

## 9. Steps 16 and 20: the eyes: uncertain (low)

Step 16: the upper eye's white box does cover the wire crossing and about 90 px of the red lead's run to j5, which is one of the two
leads being unplugged (031.png). The eyes "float" (player.js:399) because no side has room. **The reviewer's fix misfires:**
`side='up-right'` at the default reach (0.07 of the width) puts the black pin's eye at about (1107 - 1247, 505 - 583), on the 12 kOhm
resistor (about 1150 - 1260, 535 - 615). `side='right'` clamps to the frame's edge over D1. Reaching the empty top-right needs about
`reach=0.2`. Step 20: the eyes are in white space, as rulebook line 129 asks, and their leaders do not cross; "they read as a face" is
taste. Labels instead of eyes is Lee's open question 5 (see 8).

## 10a. Steps 19 - 20c: the camera crops D1 and leaves the top empty: confirmed (low)

D1's near corner `[593.8, 859.4, 1258.6]` is 108 mm from the target `[688, 878, 1210]`, outside the 82 mm frame sphere, so it is cut at
any window shape. The model's top is at screen y 394 / 477 / 477 / 528 (34 - 45% of 1163 empty). The reviewer's target
`[684, 870, 1214]` fits everything (projected y 346 - 1140, x 306 - 1426). The four views share it (`keep_camera`). After the change,
check Step 19's two matrix arrows.

## 10b. Step 19: "in the player the left side has the most room": refuted

The right has more room at every shape, because the matrix lies on the right: 2000 x 1163: left 306, right 574; 1440 x 800: 243 / 427;
1000 x 600: 142 / 280; 760 x 570: 40 / 171. The player already puts the close-up on the connectors' side, moving it up past the arrows
with the uncommitted player.js change. Only pages.js puts it bottom-left (1b). `side='right'` is harmless and changes nothing.

## 11. Step 16c: the pins hover over row 30: refuted

The pose is the Full Build's own: steps.json Step 21 has BTN_RED_PIN at `{t: [-18.08, 7.69, 56.69], r: [1, 0, 0, 90]}`, which is what
`unplug()` returns to by design (CLAUDE.md, "g.unplug": each plug goes back the way it came in and dangles from the part it rode on). The
pins lie flat, turned 90 degrees, with their tips along -z rather than down into a hole, so they do not read as "about to go in". The
reviewer calls it acceptable themselves. No change.

## 12. Step 17: the nut's arrow covers the nut's rim and the black lead: confirmed (low)

The tail is on the nut's lower rim, and the old 30 x 3.2 mm arrow's head (about 92 px wide) lies over the black lead by the button. The
arrow runs parallel to the leads, so the reviewer's `shift=[3, 0, -2]` (about 15 px down the screen and 2 mm past the nut) with
`scale=1.5` should clear the lead: about 44 px offset against a 34 px half-width. Check it in the player. **In the 18:13 revision** the
arrow is the published 56.3 x 5.0 mm and covers more of the nut and the lead (033.png). There, `scale` multiplies `dims`, so
`scale=1.5` would give an 84 mm arrow. Use `at=` / `shift=` only, or dims of its own.
