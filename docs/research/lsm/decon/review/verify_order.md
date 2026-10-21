# LSM deconstruction: verification of the order and motion review (21 Oct 2026)

Each finding in `review_order_motion.md` checked against `steps-deconstruction.json`, `steps.json`, `assembly-report.json`,
`deconstruction.py`, `guide.py`, `README.txt`, `plan_final.md`, `tools/stepgen.py`, `player/js/player.js`, the published take-apart's
report and the pictures. Nothing was run except small Python reads of the JSON (scratch scripts, not in the repository).
Summary: 4 confirmed (3, 4, 5, 8), 4 uncertain, which means they are Lee's call (1, 2, 6, 7). None refuted outright. Two severities are
lowered, and finding 1 is corrected in one detail.

## 1. Steps 8 - 13 and 19 - 20 rest on the b19 clash: UNCERTAIN (Lee's call), medium

- **The facts hold.** J_PURPLE_M (x 626.16 - 627.91, y 867.92 - 879.92, z 1212.76 - 1214.51) lies inside USB_B's box (x 619.29 - 643.29,
  y 873.62 - 881.12, z 1204.60 - 1224.46). README question 2 is open.
- The published take-apart pulls the three pins at its Steps 11 - 13 and the USB cable only at its Step 20 (report lines 80 - 85, 103).
- The plug is 7.03 mm into the Nano (1211.63 - 1204.60). The button's box is 9.19 mm above the plug (1233.65 - 1224.46).
- **The shorter order is clear except for the clash.** I swept every OUTSIDE wire (Step 9c routes 16 - 18) and its ends 30 mm up against
  every part on screen. The only part in the way is USB_B, under the purple run, which is the clash itself. Every wire end and the matrix
  move by the same shift, so the move is rigid and needs no new wire shape.
- **Correction.** Plan question 1 (`plan_final.md:399-402`) does give the reason: the purple pin is under the plug. "None of these facts"
  overstates it. What the question leaves out:
  - that the clash is README question 2, still unresolved;
  - that TechBox's own take-apart treats b19 as free;
  - the 7.0 / 9.2 mm numbers.
- **Fix: ask Lee, with those facts.** If the real pin comes out with the plug in:
  1. Resolve the clash in the model first. This is a Full Build change (the plug's leg or the b19 pin), then wirecheck.
  2. After Step 9, one step: the three pins and the matrix (sockets riding) go up 30 together. This is the plan's fallback
     (`plan_final.md:327-330`).
  3. Drop Steps 12 and 19. That gives 22 steps.
  - Optional: the published guide then shows the cable pulled off the matrix on its own (its Step 15, isolated). An `alone=[MATRIX] +
    SOCKETS` step with today's Step 19 move would keep that, for 23 steps.

## 2. Steps 10 - 12, the box turned over with the matrix outside: UNCERTAIN (Lee's call), low (reviewer: medium)

- **The numbers hold.** Over D4 (x 594.4 - 597.4) the OUTSIDE wires run at y 909.24 - 910.62, with a maximum of 913.13. D4's top is at
  907.04. Turned over, the box would rest on its wires.
- **But it is Full Build Steps 27 - 28 exactly.** In those steps the box is turned over with the matrix outside on the same routes 53 - 55.
  Lee has reviewed them over three rounds, and README question 9 (turned over, or on its side) is open about that very turn. No floor is
  drawn: in 019.png and 021.png nothing passes into anything.
- **The alternative order checks out.**
  - The Full Build Step 26 walk-back works with D3 on. All three stage routes and BESIDE have wire z ≥ 1169.6; D3 ends at z 1156.68.
    No point of any route lies in D3's box.
  - The matrix passes at y ≥ 918.06, above D3's 907.03, and never below z 1185.15.
  - D4's −X 8 slide clears D3's end tab by 1.17 mm (589.41 against 590.58).
  - D3 is free of D1's tabs after −Z 3.7 mm.
  - D5's +X 42 slide meets nothing (the OUTSIDE wires stay at x ≤ 650).
- **Fix:** offer the reviewer's order to Lee together with README question 9: D5 upright, the matrix carried back, D4, then D3 straight
  off. This is the published guide's way for D5 and D3. If finding 1's shorter order is taken, the question is moot.

## 3. Step 18, "wires first": CONFIRMED, medium (the same point is `verify_words.md` 1, rated high there)

- In Step 18c the BUTTON moves from [0, 0, 57.1] to [0, 0, 157.1], which is +Z, the side its head is on. The head is at z ≤ 1258.55,
  outside D2's outer face at 1254.93. The nut is on the inside, at 1250.43 - 1251.93.
- The phrase is copied from Full Build Step 19, where the button goes in and "wires first" is true.
- **Fix:** "Push the Push Button out through the hole in D2, its wires following it through."

## 4. Step 17, the nut fades on the wires: CONFIRMED, low

- **The numbers hold.** The nut ends at offset [0, 0, -2.9], world z 1247.53 - 1249.03. The pins' ends are at z 1240.76 (Step 17 poses),
  6.8 mm short. The leads run straight from z 1240.76 to 1290.76, at x 634.5 and 641.9, 3.7 mm either side of the button's axis at x 638.23.
- **Why.** The pins ride in Full Build Step 21's hover pose, 6 mm nearer the button than in Full Build Step 20. So Full Build Step 20's −60
  now ends on the leads. `plan_final.md` ruling 8 foresaw this ("-95 only if the nut looks wrong fading on the wires").
- **Fix:** append a stop at `slid([0.0, 0.0, -95.0], D2_AT)`, which is [0, 0, -37.9]. The nut then lies at z 1212.5 - 1214.0, 14.7 mm past
  the pins. The pins' corners are at most 4.7 mm from the axis.

## 5. Step 4, push from under D1 while the box stands: CONFIRMED, low (the same point is `verify_words.md` 2, rated medium there)

- D11 lo y 856.02 is below the walls' feet at 856.23. The camera is D7's, upright (007.png). Only the close-up hints at underneath.
- **Fix:** `verify_words.md`'s caption, "Lift the box and push the tabs ... from underneath. Then, remove the posts from D6."

## 6. Step 16, the button pins swing out of j5 and j16: UNCERTAIN, low

- **The numbers hold.** `player.js` `mixPose` blends t linearly and turns about the pose's pivot. At 10% of the move the red pin's tip has
  moved 4.73 mm along Z while still 3.16 mm below the board's top.
- **But it is Full Build Steps 21 - 22's single-stage way, reversed.** In those steps the path runs from hover to seat with no stop between,
  as CLAUDE.md's `unplug()` rule ("comes out the way it went in") specifies. Lee has seen it. The tip is hidden inside the breadboard.
- **Fix, if Lee wants it:** in guide.py, a `via()` straight above each hole in Full Build Steps 21 - 22. The deconstruction follows. Do not
  fix it in the deconstruction alone.

## 7. Connectors in the air (Steps 19c - 20) and the matrix "set down" 43 mm up (Step 8): UNCERTAIN, low

- **The numbers hold.**
  - Sockets: y 871.80 - 873.55, 15.6 mm above the table (856.23).
  - Step 8 matrix: y 898.96 - 904.00, 42.7 mm above the table.
- **Both come from the Full Build's poses.**
  - The BESIDE matrix itself floats 15.2 mm up (y 871.4) in Full Build Steps 21 - 26 and in Steps 12c - 19 here.
  - Full Build Step 26's caption says "lay it down outside" for the same pose that Step 8 shows.
  - No floor is drawn: in 038.png the connectors read as wire ends, not as floating.
- **Fix:** put both to Lee with README question 11. If the poses or wording change, change Full Build Step 26 and Step 8 here together.
  Finding 1's shorter order removes both.

## 8. Step 1 cuts from the title page: CONFIRMED, low

- Step 1 is `cut: true`. Among the MRA's, RCC's, PMG's and LSM's deconstructions, only the LSM's Step 1 is a cut.
- `player.js:717` turns animation off for a cut. The title page's camera (dir [0.60, 0.53, 0.60]) then jumps to Step 1's opposite corner.
- **Cause.** `take_apart()` (`stepgen.py:874-880`) brings back every part any Full Build view showed. BACKING was put away for good in
  guide.py:286, so the script has to put it away again.
- **Fix, either of these:**
  - The reviewer's: `take_apart()` skips a part that the Full Build put away and never showed again.
  - Script-only, with no shared-tool change: in place of `g.put_away([BACKING])`, drop it from `g.placed`, `g.riding` and `g.parked`
    straight after `take_apart()` (the script already reads `g.riding` and `g.resting`). It lies under the breadboard and does not show.
