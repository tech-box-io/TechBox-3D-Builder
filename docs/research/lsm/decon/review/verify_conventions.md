# Verification of review_conventions_code.md (skeptic pass, 21 Oct 2026, 18:15)

**The files changed while this pass ran.** `deconstruction.py` was saved at 18:10:55 and `steps-deconstruction.json` at 18:11:42. The
pictures in `pages/steps-deconstruction/` were redrawn between 18:11:51 and 18:12:30. The review was written at 18:09:44 against the
17:50 draft. A JSON dump taken before the regeneration matches the reviewer's numbers: Step 13's arrow is up 40 mm, Step 1's is
48.73 x 4.87, Step 12's is 105 x 5, Step 11's tail is [681.58, 881.63, 1137.67] and Step 18's head is at z 1307.99. The 18:10
revision has:

- `arrow_style then=` (arrows in turn) on Steps 7, 8, 11, 13 and 19;
- every arrow at the size of TechBox's published LSM take-apart (`PUBLISHED`, deconstruction.py:117-121);
- the same motions as before (the paths are unchanged).

The checks reported (runthrough 52/0, generator_log.txt, motioncheck, pictures.md) are for the 17:50 file. Run the generator log and
runthrough again on the 18:11 file before Lee's round. Runthrough checks staged arrows, and the motions did not change, so motioncheck
and wirecheck still hold. Snapshot of the 18:11 file used below:
`/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/bb7022d1-3161-45f3-afca-4098ae74fc48/scratchpad/decon_1811.json`.

## 1. Staged removals with one arrow (Steps 13, 11, 7): CONFIRMED, now fixed; one leftover point

- **Confirmed.** Rulebook docs/cadasio-patterns.md:292-296 states the rule in general terms ("a part that comes off in stages shows
  an arrow for each, in turn"). The 17:50 Step 13 arrow was the lift only, which is exactly Lee's H11/H12 complaint. Step 11 had no
  arrow for the swing. Step 7 had no arrow for the drop. The PMG used staged arrows for swings too (f6c9063: "H7, H6, H5 swung up,
  then out of H2's windows").
- **Now:** Step 13 has a stage-0 arrow along -X: tail [592.41, 881.64, 1204.25], 2 mm off D4's outer face at x 594.41. Step 13c's
  `staged_arrows` has the lift. Steps 7, 8, 11 and 19 are done the same way.
- **Leftover (low, for Lee).** Step 13's slide arrow is the published D4 size, 80.1 x 6.2 mm. It stands for an 8 mm slide, 10 times
  the travel. The published LSM ratios run 0.4 - 1.6 (guide_19075-...deconstruction.md:165), and rulebook :109 says "about as long
  as the travel". In 025.png it runs out over the USB cable's whole run from D4's notch, so it can read as "pull the cable". The
  script already shortens a stage the published guide has no arrow for (`d10_drop`, 30 mm for a 22 mm drop).
- **Fix:** give D4's stage 0 a short arrow, e.g. `dims=(25, 4.0)`. Check in 025.png that it clears the cable. Tell Lee that the
  published LSM flattens D3's and D10's two stages into one straight pull (guide md:291), so arrows in turn follow the PMG ruling,
  not the published LSM.

## 2. Arrow sizes and group arrows: UNCERTAIN (Lee's call), mostly overtaken

- **Facts at review time were correct.** Step 1 was ×2 (48.7 x 4.87 mm). Step 12 was 105 x 5 mm. Step 4 had four arrows. The
  rulebook does say both "each with its own arrow" (:287) and "groups have one arrow" (:298).
- **Overtaken:** the 18:10 revision uses the published LSM sizes throughout. Step 1 is now 69.4 x 4.6 with no ×2, and Step 12's arrow
  by hand is 70.6 x 3.8.
- **What is left is for Lee:**
  - The PMG ruling names only the PMG ("The PMG's arrows take the published guide's sizes"), so applying it to the LSM is the
    draft's choice and should be said in README.
  - Step 4 has four arrows. The published LSM gives each post its own arrow, but takes the posts two per step (its Steps 6 - 7). The
    generator's NOTE flags this.
  - Reconcile rulebook :287 and :298 as "as each kit's published take-apart does". This is housekeeping.

## 3. Step 11: D3's arrow 16 mm off the plate: CONFIRMED at review time, fixed by the then= change

- **Cause, verified.** `_arrow_out` puts the tail at `a + d * (max projection + 2)`, measured from the part's pose now. The slide's
  direction was tilted 22 degrees by the swing before it, so the tail landed 46.8 mm along a line out of D3's plane: z 1137.67,
  against D3's face at z 1153.68.
- **Now:** Step 11c's stage-1 arrow starts at D3's free end as the slide begins, [680.74, 881.63, 1121.4].
- **Stage-0 (swing) arrow.** Its tail is [635.0, 881.63, 1141.28], 12.4 mm off the face, by the same "just outside along d" rule:
  D3's 95 mm length sets where it starts. It runs towards the camera and reads as on D3 in 021.png.
- **In stills** (021.png) the stage-1 arrow floats to the right of the box, where D3 will be after the swing. The rule accepts this
  ("a still shows them all at once").
- **Generator fix (later, low):** draw a default arrow along a stage after a turn from the part as that stage begins.

## 4. The order rests on the b19 / USB-plug overlap: CONFIRMED (medium, for Lee)

- TechBox's take-apart unplugs the three matrix wires at the breadboard in its Steps 11 - 13 (eye only), and unplugs the USB cable
  only at its Step 20 (guide md:80-85, :103).
- README.txt:94 says "the published model has the same clash".
- plan_final.md question 1 (:399-402) gives the b19 block as fact. It does not say that TechBox's own guide unplugs b19 with the plug
  in.
- **Fix:** add that evidence to question 1 and to README. Change nothing unasked: it needs new loose-wire shapes.

## 5. 2D PDF: Step 4's close-up covers a post's arrow: CONFIRMED (medium once a PDF is made, low until then)

- pages.js:20-35 chooses the corner by distance alone.
- 007.png (redrawn at 18:11) shows only the tip of the right-hand post's arrow at the close-up's left edge, and the leader crosses
  the whole model.
- This is a weakness in the shared tool. The MRA deconstruction's Step 64 (its pages/127.png) came out clear by chance.
- **Fix:** place the close-up where the player does, or test the corners against the projected arrows, labels and eyes. Test
  against `stillArrows` (every stage's arrow), not only Step N's: Step 19 has a close-up and a stage-1 arrow, and the player's
  placement ignores the stage-1 arrow because the close-up is hidden while the step plays (player.js:747).

## 6. Step 4 upright instead of turned over: REFUTED as a convention breach (wording point only)

- TechBox's published LSM take-apart removes the D11 posts with the box upright (its Steps 6 - 7: arrows up, an eye, and a close-up
  of the post's foot in its lock slot; guide md:65-69).
- It gives no step to the build's "flip over, lock the supports": "its content is the eye + inset here" (md:250).
- Its cameras stay at 24 - 51 degrees and never turn the box over (md:289).
- Rulebook :155 and :353 are for work done with the kit upside down. Step 4 does not ask for that.
- **What remains:** the caption does not say the box must be lifted to reach the tabs (review_wording item 2). The tab tips are at y
  856.02, against walls to y 856.1 - 856.23. Fix with wording only. Note the opposite inconsistency: the draft does turn the box over
  for D5 and D3 (Steps 10 - 11), which the published guide does not (review_order_motion item 2).

## 7. Step 7 in place, not on its own: UNCERTAIN (Lee)

- The facts are right: the published guide removes D10 in an isolated view (its Step 14, md:86); the draft uses FB 31's camera with
  the box shown; the matrix is still wired.
- Lee's RCC rule (sub-assemblies taken apart on their own) and the MRA's (seen as the build showed it) pull different ways.
- **Fix:** a README question only.

## 8. Arrows placed by hand: Step 18 CONFIRMED (low); Step 14 REFUTED (nit)

- **Step 18.** The arrow is now 38.4 mm long (published size), with its head at z 1314.5.
  - It runs at x 649.23, 11 mm off the button's axis (centre x 638.2), beside the body, so it goes through D2's wood (z 1309.03 -
    1312.03), not the hole.
  - Its tail is 14.65 mm behind the button's back, among the wires.
  - In 035.png it points into D2 with its tip hidden.
  - From this camera, on D2's inner side, no arrow along +Z can end in free space.
  - **Fix, one of:**
    - start the tail on the button's back face (seated z about 1234), sized to stop at D2's inner face, about 18 mm;
    - an eye on the button;
    - ask Lee about the published cap-side view (its Step 19), which goes against keeping one camera per sub-assembly.
  - Also correct the comment at :187. The caption's "wires first" is backwards (review_wording item 1).
- **Step 14.** The tail at y 912.0 is 5 mm above D2's top edge on purpose (comment :171), as Lee's MRA rule allows ("an arrow sits
  where it reads"). In 027.png it starts at D2's top corner. Nothing to fix.

## 9. Code: CONFIRMED (low)

- **Typed copies of Full Build values.** None will follow a Full Build change:
  - :133 is guide.py:802's D11_SHORT / D11_UP;
  - :135 is FB Step 36c's close-up, exactly;
  - :162's tail is FB Step 26's arrow head, now resized.
- **Latent failures.** `camera_of` and `slid` would fail on a pose dict. D2_AT is a list today, and the MRA's `camera_of` handles a
  dict (MRA deconstruction.py:59). `carried_back` does not check where the walk-back starts.
- **The nut comment (:180).** FB Step 20 has NUT `path_stops` [0, 8] (two beats, no stop), while the draft has [0, 4, 8]. "Two beats"
  matches the Full Build; the stop does not. Trivial.
- **put_away([BACKING]).** Confirmed: Step 1 has `cut: true`, while the MRA's, RCC's and PMG's Step 1 do not. The impact is small:
  Start and Step 1 look from opposite corners.

## 10. player.js arrow-avoidance: CONFIRMED (low)

- Only three views have both a close-up and arrows: LSM Steps 4 and 19, and MRA deconstruction Step 64. This was checked by scanning
  every steps*.json.
- **The band is too narrow.** It is ±10 px, but core.js:309 makes the head's half-width 2 x the arrow's width. Step 4's published
  widths of 3.4 - 4.0 mm give heads 14 - 16 mm across, about 55 - 65 px at its frame, so about 20 px of each wing is not counted.
  **Fix:** pad by the head's width.
- **The stepgen hunk must be committed with this guide.** Without it, only mark, alt, caption and arrows are copied, and Step 19's
  `ghost` is dropped.
- **code_changes.diff is out of date.** Its player.js hunks for go, stepAnimation and renderThumb, and its stepgen hunks from line
  1774 on, are in f6c9063.
