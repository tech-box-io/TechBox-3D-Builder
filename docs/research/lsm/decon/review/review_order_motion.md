# LSM deconstruction draft: review of order and motion (21 Oct 2026)

Scope: whether each step can really be done at that point, the way the draft moves it; groups; what stays or goes; riders; wires with
both ends; the LED matrix's round trip; the order against TechBox's published take-apart. Read: `LSM Build Instructions/deconstruction.py`,
`steps-deconstruction.json`, `guide.py`, `steps.json`, `assembly-report.json`, `README.txt`, `plan_final.md`, the published take-apart's
report, the pictures. Nothing was run but small Python reads of the JSON.

Checked and right (not repeated below): every paired state is the Full Build's exactly. Steps 6 - 16 and 21 - 24 (Step N against the
undone step's Nc, Step Nc against its hover) match `steps.json` in every part's pose and every wire route. The only differences are USB_A's
+Z 25, which is meant. Steps 17 - 18 are Full Build Steps 20 and 19 shifted by D2's 57.1 mm. Riders: D10 rides the matrix out (6) and
leaves (7). The sockets ride it until 19 (`let_go`). The button and nut ride D2 (14), and the pins ride the button from 16c. Every wire
leaves with both its ends (15, 18, 20, 21, 23). Nothing leaves or stays wrongly in the visible lists. The stems, D8 and D7 end clear of
D8 and the posts: stem bottoms 946.3 against D8's top 932.4, and D8 / D7 bottoms 984.2 / 978.5 against the post tops 935.8.

## 1. The middle of the guide rests on the b19 clash, which is still an open question to Lee (medium)

- **Steps 8 - 13 and 19 - 20.** The matrix is carried out over D4 (8). The box is turned over and back with it hanging outside (10 - 12).
  It is then carried back over the whole box (12) and unplugged only at 19 - 20. All of this follows from one premise: the purple
  wire's pin in b19 cannot come out while the USB plug is in.
- **Evidence.** That premise is the CAD clash in README question 2, which is open: "Is the kit's cable right-angle, and is b19 the purple
  wire's hole?" In the model, J_PURPLE_M (x 626.16 - 627.91, y 867.92 - 879.92, z 1212.76 - 1214.51) lies inside USB_B's box (x 619.29 -
  643.29, y 873.62 - 881.12, z 1204.60 - 1224.46). The README says the published model has the same clash. Yet TechBox's own take-apart
  pulls the three pins out of i2, b19 and i3 at its Steps 11 - 13, and the USB cable at its Step 20
  (`docs/research/guide_19075-laser_stem_matrix_lsm_-_deconstruction.md` lines 80 - 85 and 103). So its authors treat b19 as free.
- **The second link is weaker than the plan says.** The plan says the plug "runs into the button". The plug's tip is 7.0 mm inside the
  Nano (USB_B lo z 1204.60, NANO hi z 1211.63), and the button's back is 9.2 mm away (1233.65 - 1224.46). So the plug clears its socket
  before it reaches the button. Only the 25 mm hover way is blocked.
- **Plan question 1 to Lee does not give these facts** (`plan_final.md:399-402`). It does not say that the round trip exists only because
  of the clash, or that the published guide ignores the clash. It says only that the published order "needs new wire shapes", which is
  not true of the shorter order below.
- **The cost of the current order.** Step 12 is the four-beat walk-back with turns, the highest-risk motion. Two of motioncheck's three
  wire brushes are in it, and with it come the two turn-overs of finding 2.
- **Fix: put it to Lee with these facts.** If the real kit's b19 pin can come out with the plug in, correct the clash in the model (the
  Full Build's README question 2) and shorten the guide. After Step 9 (matrix outside D4; D9, D10 and D6 off), one step: "Disconnect the
  yellow, grey and purple wires from i2, i3 and b19 and lift the LED Matrix away with them." This is the plan's own fallback call
  (`plan_final.md:327-330`), applied at the OUTSIDE state. Every wire end and the matrix rise 30 together, so it is a rigid move and
  needs no new shape.
- **Why the rigid lift is clear.** Nothing lies above the OUTSIDE wires once D6, the D9s and D10 are off:
  - the in-box run is at y 881 - 885;
  - the run over D4's edge is at y 909.5 - 911.5;
  - the only part touching a wire is the USB plug under the purple run (y 881.45 against the plug's 881.12), which a +Y move leaves.
- **The rest of the shorter order:** D5, D3, D4, D2, USB, leads, nut, button, and the four breadboard parts. That is 22 steps, with no
  Step 12 and no Step 19.
- If the clash is real, keep the draft.

## 2. Steps 10 - 12: the box is turned over twice with the matrix hanging on wires that lie over D4's edge; the shapes allow an order without turning it over (medium)

- **What happens now.** Step 10 turns the box over and Step 12 turns it back while the LED matrix lies outside D4 on its three wires. Their
  pins are in the upturned breadboard.
- **Evidence.**
  - Where the wires cross D4 they run at y 909.4 - 910.6 (`guide.py:673`, `over_d4`). D4's top tabs reach 907.04 (`assembly-report.json`).
  - Turned over about y 881.6 (the camera pivot of Steps 10 - 11), the wires stand 2.3 - 3.6 mm proud of the plane on which the upturned
    box rests on the table. The box either rests on them or pushes them between the tabs.
  - The removals do not need the turn. D5 comes off sideways (+X 42), and TechBox's take-apart removes it upright (its Step 4).
  - The Full Build turned the box only to put D3 and D5 on (FB 27 - 28; README question 9 is still open on that).
  - The wording review (`review_wording.md` section 6) flags the same steps for the caption only.
- **Fix: ask Lee, offering this order.** It uses only moves and wire shapes the Full Build already has:
  1. Step 10: D5 off with the box upright, along the same +X 42.
  2. Step 11: the matrix carried back to the D5 end (today's Step 12, without "Turn the box the right way up"). That move needs only D5
     and the D9s off, not D3: the matrix passes at y +25 (underside 918, above D3's top at 907.03), and the BESIDE wires (z 1170 and up)
     do not reach D3 (z 1153.7 - 1156.7).
  3. Step 12: D4 off, today's move. D4's -X 8 slide also clears D3's end tabs: D3 lo x 590.58, D4's outer face goes to 586.41 - 589.41.
  4. Step 13: D3 pulled straight off D1's tabs (-Z, about 10 mm, then away), as TechBox's Step 16. Its end tabs are free once D4 and
     D5 are off, and D1's tabs through it reach only z 1150.
- **What it saves:** the same step count, no turning over, and no reversed 22-degree swing of D3 in D4's slots. It needs a new camera
  for D5 and for D3 (from above, for example DIAG). This applies only if finding 1 keeps the matrix wired. Otherwise D5, D3 and D4 come
  off with no matrix at all.

## 3. Step 18: the caption says "wires first", but the button leaves head first (medium; also `review_wording.md` section 1)

- **What is wrong.** The motion is BUTTON +Z 100 (Step 18c `paths`: [0, 0, 57.1] to [0, 0, 157.1]). The button's head is at +Z (BUTTON hi z
  1258.55, outside D2's outer face at 1254.93), and its leads leave its back at z 1233.65 (`guide.py:496`). So the head leads, and the
  wires follow it through the hole.
- **Why it matters.** A panel button cannot be pushed out wires first: its flange is bigger than the hole.
- **Fix:** "Push the Push Button out through the hole in D2, its wires following it through." This was the plan's own caption
  (`plan_final.md:293`).

## 4. Step 17: the nut stops on the wires, short of the pins, and fades there (low)

- **What is wrong.** `NUT_WAY` ends at FB Step 20's hover, -60 mm from D2 (Step 17c NUT [0, 0, -2.9] with D2 at +57.1). That puts the nut
  at world z 1247.5 - 1249.0, while the pins' housings, laid back from the button, are at z 1228.8 - 1240.8 (Step 17's pin poses). The nut
  fades 6.8 mm short of them, still threaded on the leads, under the caption "slide it off over the wires".
- **Fix:** add one more stop past the pins, as FB Step 18 took it (-95 from its seat). For example, append `slid([0.0, 0.0, -95.0], D2_AT)`
  as a stop. The pins are 3.7 mm either side of the axis, so they pass through the nut.

## 5. Step 4: the tabs are pushed up from under D1, but the box stands on the table (low; also `review_wording.md` section 2)

- **What is wrong.** The first stage (+6.4) has the student push the tabs up out of D1. The tabs end flush with the table: D11 lo y 856.02,
  with the walls' feet at 856.23. The step keeps D7's upright camera, and the Full Build did this joint with the box turned over (FB 36).
- **Fix: either wording or motion.**
  - Pull the posts up from above, as TechBox's take-apart does (its Steps 6 - 7: "Remove the four D11 posts from D6 and D1", one stage of
    85).
  - Or keep the two stages and say "Lift the box and push the tabs ... from underneath".

## 6. Step 16: both button pins swing sideways through the breadboard as they come out (low; the same in FB 21 - 22)

- **What is wrong.** Each pin goes from its hole to its laid-back pose in one stage, turning 90 degrees about X as it moves (Step 16c
  `paths`: seat to {t [-18.08, 7.69, 56.69], r 90 about X}). With no straight lift first, the bottom 4 mm of each pin (housing lo y
  867.92 under the board's top at 871.92) sweeps about 5 mm sideways through the board in the first tenth of the move, while still
  3 mm deep. Both pins do this
  at once.
- **Fix:** give the unplug a first stage straight up out of the hole, as the jumper pins have (+Y about 8), then the laid-back pose. Or
  accept it as the Full Build's.

## 7. After Step 19 the three connectors hang in the air; in Step 8 the matrix is "set down" 43 mm above the table (low)

- **What is wrong.** `let_go` leaves the sockets where the matrix held them in its BESIDE pose: y 871.8 - 873.6 against the table at
  856.23. That is about 16 mm up, with nothing holding them through Steps 19c - 20 (pictures 038, 039). This is inherited from the Full
  Build's BESIDE pose, in which the matrix's header is 15 mm above the table.
- In Step 8, "set it down outside the box" leaves the matrix at y 898.95 - 904, 43 mm above the table (README question 11, open).
- **Fix:** put it to Lee with README question 11 (both places come from the Full Build's poses). Meanwhile Step 8's caption can say "hold
  it outside D4". Finding 1's shorter order removes both.

## 8. Step 1 opens with a cut from the title page; the other kits' deconstructions glide (low)

- **What is wrong.** `g.put_away([BACKING])`, called straight after `take_apart()` (`deconstruction.py:96`), makes Step 1 a cut (Step 1
  `cut: true`). The first steps of the MRA's, RCC's and PMG's deconstructions are not cuts.
- **Why it happens.** BACKING is already out of sight on the title page, seated under the breadboard. It is put away only because
  `take_apart()` would otherwise bring it back 40 mm under D1.
- **Fix:** let `take_apart()` leave out a part that the Full Build put away and never showed again, or let a `put_away()` of parts not on
  screen skip the cut. Either way, Step 1 then glides from the title page.
