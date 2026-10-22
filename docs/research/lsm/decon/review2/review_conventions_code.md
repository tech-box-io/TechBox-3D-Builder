# LSM deconstruction, rebuilt 21 Oct 2026: review of conventions and code

Scope: `LSM Build Instructions/deconstruction.py`, `wire_shapes.py` (kit copy), `steps-deconstruction.json` (52 views) and
`steps.json`, checked against rulebook section 11 (and Lee's dated paragraphs there), CLAUDE.md "A deconstruction guide", and the
MRA, RCC and PMG scripts. I ran nothing heavy: I only read JSON, the pictures in `pages/steps-deconstruction/` and the logs. Step
numbers are the player's (ours). The published guide's Step 10 onward is one number higher than ours from our Step 10 on.

## Findings, most severe first

### 1. HIGH: the gray breadboard wire is drawn pure white, in the Full Build and in the take-apart
- **What:** Lee asked for "gray", which changed `SHOWN['grey']` to `'gray'` (guide.py:37). guide.py:205 builds the wire's colour as
  the palette key `f'wire_{SHOWN[w]}'`, which is now `wire_gray`. materials.json:27 has only `"wire_grey": "#cad1ee"`. stepgen.py:764
  (`self.palette.get(colour, colour)`) passes the unknown name through unchanged, so both steps files now hold
  `wires['wire grey'].colour == 'wire_gray'` (in HEAD it was `#cad1ee`). The player calls `new THREE.Color('wire_gray')`
  (core.js:349). three.js does not know that name, so the colour stays white.
- **Evidence:** a scan of every kit's steps files: this is the only colour that is not `#rrggbb`. Pictures 019 - 028 (Steps 10 - 14)
  show a white wire beside the yellow and purple ones. runthrough.js compares the page with steps.json, so it cannot catch this.
  The test site still has `#cad1ee`.
- **Why it matters:** the wire is named "Gray Breadboard Wire" but drawn white. This brings back the "white next to light grey"
  confusion that made Lee turn the white wire yellow (rulebook section 9, 20 Oct).
- **Fix:** key the palette by the code id rather than by the shown word. In guide.py, for example,
  `COLOUR = dict(white='wire_yellow', grey='wire_grey', purple='wire_purple')`. Alternatively, add a `wire_gray` palette entry.
  Then run guide.py and deconstruction.py again, run runthrough on both guides, and redraw the pages. Worth adding: `Guide.wire()`
  should refuse a colour that is neither a palette key nor `#rrggbb` (stepgen.py:764).

### 2. MEDIUM: Steps 10 and 12 are fades (`reappear=True`). The stated reason does not hold, so this needs to go to Lee
- **What:** Step 10 sets the matrix down by a fade (deconstruction.py:216), and so does Step 12, the three pins unplugged
  (deconstruction.py:223). The docstring gives two reasons: the published guide's model swaps, and the rulebook's "Wires are
  unplugged by swapping the routed model for a loose one".
- **Evidence:**
  - CLAUDE.md:82-85 records `reappear` as "Lee, 21 Oct 2026, that step only" (the PMG's Step 42). CLAUDE.md:385-388 allows it in
    a take-apart only to undo "the Full Build's own reappear".
  - The Full Build moved both of these things: the matrix's lift over D4 (its Step 26) and the plug-ins.
  - Every in-house take-apart moves its plugs out on their way (`unplug()`: the MRA's Steps 5 - 7 and 53, the RCC's, the PMG's 21
    wires).
  - The rulebook line records how Cadasio does it, because Cadasio cannot animate a flexible lead. It is not a TechBox choice.
  - Nothing physical forces a fade. feasibility_log.txt P11-13: the three pins come straight up free with the USB plug in, and
    overlap 0.0 mm.
  - motioncheck skips both steps.
  - The LAID and LOOSE routes in wire_shapes.py carry no blending attributes (`tail_from`, `stretch`). They are end states only.
- **Fix:** ask Lee: "Steps 10 and 12 fade, as the published guide swaps models, where the MRA's, RCC's and PMG's take-aparts move
  the plug out. Keep the fades, or show the motion?"
  - If they keep them, record that as Lee's ruling for this kit in CLAUDE.md:82-85 and rulebook section 11.
  - If not: Step 12 takes each pin up out of its hole the Full Build's way, then to the table, with a stage route per wire. Step 10
    takes a path from held to laid, with `wire_via` (`tail_from` on the matrix-end runs, as the Full Build's matrix wires have).

### 3. MEDIUM: the guide script reads docs/research
- **What:** deconstruction.py:101 loads `docs/research/lsm/decon/published/published_steps.json` (330 KB) every time it runs.
  CLAUDE.md (Version control) says "nothing that regenerates or publishes a guide reads docs/research".
- **Fix:** put the numbers the script uses into the script as a table, as the PMG's `PUBLISHED` dict does (PMG
  deconstruction.py:118-122). That means, for 24 steps: the camera (view_dir, target, radius), each arrow's length, width and tail,
  each eye's part and ring, and each close-up's part and ring. Or write them once, with replay_decon.py, to a small JSON in the kit
  folder. docs/research stays as the evidence.

### 4. MEDIUM: wire_shapes.py exists twice, and the kit copy's docstring and output are the research copy's
- **What:** `LSM Build Instructions/wire_shapes.py` is untracked and byte-identical to `docs/research/lsm/decon/published/wire_shapes.py`.
  - The kit copy's docstring (lines 21-31) says to run the research copy, and to "copy this file into the kit folder".
  - `main()` writes `wire_shapes.json` "beside this file" (line 472). Run from the kit, it would drop a JSON into the kit folder,
    and the two copies would drift apart.
- **Fix:** keep the kit copy only, and commit it with the guide. Delete the research copy, or reduce it to a stub that imports the
  kit's. Send `main()`'s report to docs/research/lsm/decon/published/ and update the docstring's run command.
- Import side effects are benign: sys.path for tools/, `import wires` and `stepgen`, and LAID_POSE computed at import. `_root()`
  raises SystemExit at import outside the repository.

### 5. MEDIUM-LOW: Step 13 drops D10 straight off, against the build's hook-on
- **What:** D10 comes straight down 40 mm (deconstruction.py:228). The Full Build hooks it on by holding it under the matrix,
  sliding it along, then raising it (its Step 31: carry [0, -22, 40] -> via [0, 0, 40] -> [0, 0, 0]). Rulebook section 11 says
  "The part leaves along its build hover path, reversed".
- **Evidence:**
  - feasibility_log P14: straight down is LATCH, the hook catching the matrix by 1.0 mm or more after 0.63 mm.
  - The step has no close-up of the hooks, although section 11 wants one at a catch to release.
  - The first draft (still on the test site) had "Slide D10 toward D2 until its hooks come off ...". The rebuild copied the
    published straight drop, which happens in the published guide's glitched hover view (its section 5).
- **Fix:** use the Full Build's Step 31 reversed: slide 40 mm along the matrix (laid: -Z), then down 22. Suggested caption: "Slide
  D10 along the bottom of the LED Matrix until its hooks come free, then remove it." Check it against the LOOSE wires in D10's
  notch (a wire_shapes scene). Otherwise, put to Lee whether D10 simply pulls off downward.

### 6. LOW-MEDIUM: rules broken without saying so (CLAUDE.md: "say which one and why")
- **a. One camera per sub-assembly in the hand.** "Two steps on one sub-assembly in the hand keep one camera" (rulebook section 11,
  Lee 18 Oct). Steps 13 -> 14 change camera (`laid_cam('Step 14')` to `laid_cam('Step 15')`), and so do Steps 18 -> 19
  (`cam('Step 18')` to `cam('Step 19')`). Both follow the published guide. Step 19's reason is sound: the button comes out on D2's
  engraved side. The draft states neither change.
- **b. USB cable seen whole.** The RCC ruling: a USB cable taken off is "seen a little wider so that the cable shows". Step 20's
  published camera puts the A end at the left edge of picture 039 (about x 25 of 2000 at aspect 1.72), so any narrower window cuts
  it off.
- **Fix:** name both in the docstring and README as departures made to follow the published guide. Or give Step 20 a camera a
  little wider (as the PMG's Step 1, "the cable shows whole"), and Step 14 Step 13's camera.

### 7. LOW: Steps 10c and 11 may cut off the laid matrix in square or portrait windows
- **Evidence:** the camera's fit sphere (target (616.3, 882.2, 1206.6), radius 91.3) does not contain the laid matrix, whose far
  corner is about 105 - 110 mm from the target. A projection estimate puts that corner at 0.61 - 0.68 of the half-width at aspect
  1.72, but 1.05 - 1.17 at aspect 1.0. The 768 px check covered arrows and close-ups, not parts.
- **Fix:** look at Steps 10c and 11 at 768 px portrait and in the LMS frame. If the matrix is cut, give Step 10 a frame that holds
  it (Step 12's camera holds it: 0.45 at aspect 1.0).

### 8. LOW: the Completed View is not the published one
- **What:** it uses Step 24's direction at radius 70.5, which is wider than Step 24's 67.1. The published Completed View is
  view_dir (0.4098, 0.7518, 0.5166), target (639.5, 845.2, 1212.5), radius 67.1. The docstring claims the published cameras
  throughout, and CLAUDE.md says the take-apart ends "closer in".
- **Fix:** `Guide(..., end_view=dict(dir=..., target=..., radius=67.1))`, using PUB['Completed View'], in the format of
  guide.py:103-104.

### 9. LOW: a wire touch in Step 9c, inherited from the Full Build
- **What:** motioncheck reports the gray and purple centre lines 0.48 mm apart (an overlap of 0.76 mm) at 0.55 of the lift. This
  is the Full Build's Step 32c played backwards. Rulebook section 9 says wires never touch, even in motion.
- **Fix:** note it in the README with the Full Build's own touches, or fix it once in the Full Build's Step 32c `wire_via`.

### 10. LOW: code that is right only by accident
- **Half-turn assumption.** `wire_shapes._socket_run` (line 157) turns laid z into seated z using a point at x = y = 0. That is
  right only because LAID_POSE is exactly a half turn about Y. Convert whole points instead, or assert the angle.
- **Default pose.** `socket_pose` and `pin_pose` default to `pose=LAID_POSE`. Step 14's paths (deconstruction.py:232) rely on that
  default instead of passing `where(MATRIX)`, so they would be silently wrong if the laid pose changed. Pass the pose.
- **D11 poses relative to D1.** `D11_SHORT` and `D11_UP` (deconstruction.py:193) are carry poses relative to D1, used as absolute
  poses. That is right only because D1 never moves. Say so in a comment.
- **D2 offset.** Steps 18 and 19 take their published camera targets as published (D2 0.6 mm off ours), while their arrows are
  carried by `to_ours`. The difference is under 1 mm. Carry the targets too, for consistency.
- **Checked and correct:** `cam`, `arrow`, `eye`, `ring`, `to_laid`, `laid_cam` (Step 13's target and direction reproduced by
  hand), `tab_ends` (boxes at y 861.04 / 902.21 on tabs spanning 858.4 - 861.8 / 901.5 - 904.9), `tab_under_d1`,
  `full_way_back`, `slid` (a `via` is a dict, so it survives) and `NUT_WAY` (stops 0, 4, 8, 9: one whole turn, then the second
  turn, then the slide). Published arrow k is matched to the right post or D9 in Steps 6, 7 and 11, and the close-up's post belongs
  to its step's pair.

## Before this ships
1. Fix finding 1. Run guide.py and deconstruction.py again, run runthrough on both guides, and redraw `pages/` (the PDF if one is
   wanted).
2. **README.txt.**
   - Line 7 still says "DECONSTRUCTION, FIRST DRAFT".
   - THE DECONSTRUCTION (lines 93-123) describes the first draft: the matrix carried over D4 and back, the box turned over,
     `let_go`. Rewrite it for Steps 1 - 24 as rebuilt, with Lee's four answers word for word.
   - Mark questions 21 (eyes), 22 (Pry Tool), 23 (sizes; posts two and two, as published), 24 (D10 taken off with the matrix on its
     own) and 25 (gray) answered. Question 20 is answered by "base the deconstruction process off of this guide".
   - Correct question 2 and the premise of question 20: feasibility P11-13 shows the b19 pin comes up free with the plug in, and
     the purple wire's overlap is 0.0 mm.
   - Add the new questions (findings 2, 5, 6b) and re-point the research links (plan_final.md and review/ are the first draft's).
3. **CLAUDE.md.**
   - The LSM paragraph at lines 422-428 describes the first draft (`carried_back`, the box turned over, `let_go`, the matrix wired
     until Step 19). Rewrite it.
   - The `reappear` line (82-85, "that step only") needs the LSM's Steps 10 and 12 if Lee keeps them.
   - Add the LSM's (and the PMG's) `deconstruction.py` run line under Commands.
   - The Layout entry for the LSM lists neither `deconstruction.py` nor `wire_shapes.py`.
4. **Rulebook section 11** (lines 285-292): the LSM paragraph is the first draft's. Replace it with Lee's 21 Oct rulings for this
   kit:
   - the take-apart follows TechBox's published one in order and manner (unlike the PMG, where Lee kept the in-house order);
   - eyes instead of hole labels for this kit (against the MRA's Row labels);
   - the Pry Tool caution, though the tool is not drawn;
   - "gray";
   - the fades, if Lee keeps them.
5. **git:** wire_shapes.py is untracked. Commit the sources and generated files together once checked.
6. **Card:** `cards/steps-deconstruction.webp` is the Full Build's card byte for byte (its .json names `cards/steps.webp` and model
   0a7267f2bc49, the current one). Nothing to do unless the Full Build's Completed View changes.
7. **Test site:** `share/Test guides preview` still has the first draft ("Slide D10 toward D2 ...", "Carry the LED Matrix over
   D4 ...") and a Full Build from before "gray". After the fixes, publish both LSM guides `--to "share/Test guides preview"`, run
   check_site on it, and run runthrough on 8799. Nothing goes live without Lee's word.
8. guides.json already has `laser-stem-matrix-deconstruction` (script deconstruction.py): nothing to do.
