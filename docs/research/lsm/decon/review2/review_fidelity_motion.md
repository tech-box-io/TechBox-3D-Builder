# LSM take-apart, rebuilt draft: review for fidelity to the published guide, and motion (21 Oct 2026)

Scope: `LSM Build Instructions/deconstruction.py` -> `steps-deconstruction.json` (52 views), against TechBox's published take-apart
(19075) as replayed in our ids and mm (`docs/research/lsm/decon/published/published_steps.json` / `.txt`), its feasibility tests
(`feasibility_log.txt`, `feasibility_verdicts.json`), the study (`docs/research/guide_19075-...deconstruction.md`), the pictures in
`LSM Build Instructions/pages/steps-deconstruction/` and part boxes read from `lsm.glb` (accessor min/max only). Nothing was run
but light JSON reading; nothing in the repository was changed except this file.

Our step -> published step: 1-8 -> 1-8; 9 + 10 -> 9; 11 -> 10; 12 -> 11 + 12 + 13; 13 -> 14; 14 -> 15; 15 -> 16; 16 + 17 -> 17;
18-24 -> 18-24.

What matches (checked number by number, so not repeated below): every step's camera is the published one to within 0.9 degrees and
0.1 mm of target, same radius (Steps 13 and 14 turned half round with the matrix, as intended); all 24 arrows are on the published
parts, in the published direction, at the published length and shaft width, tails within 1 mm of the published tails (Step 9's
moved onto the matrix, Steps 13, 14, 18, 19 carried with their sub-assembly); 16 of the 17 published eyes are on the same parts
(Steps 1 - 7 and 12 at the published rings, the others within 10 mm of them; the one dropped is the yellow pin's, which shares the
gray pin's eye); all 8 close-ups are on the published steps and parts. Every move is along the published axis and direction; distances
are sensible (stems 44 mm clear D8 by 14 mm; D8 55, D7 65, D5 42, D4 75, posts 6.4 + 78.6, D6 64, matrix 56.6, D9 65, D10 40,
connectors 30, D3 40, D2 57.1, nut 95, button 100, USB 25, R330 30, CAP 29, R12K 32, Nano 35). Riders go with the right part (D10
and the three sockets on the matrix; the button and nut on D2; the three pins on the matrix after Step 12; the button's pins on the
button after Step 17), every lead leaves with both its ends (Steps 14c, 19c, 20c, 21c, 23c), nothing removed stays on screen, and
nothing that stays vanishes. The published slips in the study's section 5 are not copied (D3 hidden, the posts' flicker at 4c, D5's
missing slide, the matrix never shown seated, Step 9's stale arrow, Step 20's motion-less fade, the matrix floating 5.9 mm up).

## Findings

### 1. Steps 6 and 7: the posts' barbs also catch under D6, and nothing says so (medium)

- What: each D11 post is pushed up out of D1 (6.4 mm) and then pulled straight up 78.6 mm more through D6's corner slot, D6 still on
  (it comes off at Step 8). The barb that held the post under D1 meets D6's underside on the way: feasibility_log.txt:54-55, "stage 2
  ... 78.6 mm: BLOCKED (D6 blocked) ... first met after 35.22 mm at [602.13, 900.98, 1248.24]"; feasibility_verdicts.json:11, "the same
  barb meets D6's corner slot, which is as long as D1's (10.32 mm against the barb's 11.06)". In the Full Build the barb went down
  through D6 ramp first (Steps 34 - 35); coming out, its flat top catches. The animation passes it through D6 (1.1 mm into the slot
  edge for 3 mm), the generator does not check hand-given ways, and the captions (deconstruction.py:195-198) say only "push the tabs
  ... up out of the slots in D1 from underneath. Then, remove the posts from D6." A learner doing exactly that finds each post stuck
  under D6 after about 35 mm. The published guide moves the posts the same way (86.5 / 88.8 / 84.5 / 70.5 mm straight up), so this is
  a published slip we inherit, not a departure.
- Fix: keep the published pairs and motion, and say it: Step 6 "... Then, squeeze each tab's prongs together again as you pull the
  posts up out of the corner slots in D6." (Step 7: "the same way"), or add a second red box at D6's corner slot to the close-up.
  Alternative to put to Lee (feasibility option a): once the four tabs are out of D1, lift D6 with the four posts on it (FREE),
  which merges published Steps 6 - 8.

### 2. Step 18: the nut "unscrews" over 60 mm, mostly on the wires (low)

- What: Step 18c's way is the Full Build's Step 20 reversed (deconstruction.py:253-255): eight quarter turns of 7.5 mm each
  (z 57.1 -> 49.6 -> ... -> 4.6 -> -2.9), stops [0, 4, 8, 9]. The button's thread inside D2 is about 18 mm (button z 1233.6 - 1258.5,
  nut 1250.4 - 1251.9, D2 1251.9 - 1254.9 in lsm.glb), so the nut leaves it during the third quarter turn and spins five more on the
  bare wires; the beat "after the first whole turn" comes with the nut already 11.7 mm past the button's end (1277.5 against 1290.7,
  D2 out). The published nut turns 176 degrees over its 84.8 mm. Visible in the player as a long spin along the leads.
- Fix: unscrew over the thread only (for example eight quarter turns of 2.1 mm, a stop after each whole turn), then the straight slide
  off over the wires and pins as now (-95 mm in all). The Full Build's Step 20 has the same spacing; changing it is Lee's call and
  outside this guide.

### 3. Completed View: not the published camera (low)

- What: ours is the generator's take-apart default, Step 24's direction closer in (stepgen.py:2100-2104): dir [0.6564, 0.6618, 0.3621],
  target [638.2, 865.7, 1204.3], radius 70.5 (049.png). The published Completed View has its own: view_dir (0.4098, 0.7518, 0.5166),
  target (639.5, 845.2, 1212.5), radius 67.1 (published_steps.txt:461; 23 degrees round from ours). The docstring says each step takes
  the published camera; this is the one view that does not. (The website card is the Full Build's either way.)
- Fix: `g.end_view = dict(dir=[0.4098, 0.7518, 0.5166], target=[639.5, 845.2, 1212.5], radius=67.1)` after `Guide(...)`, as guide.py:104
  sets the Full Build's (stepgen honours end_view for a take-apart: stepgen.py:2095-2101); or keep the house default and say so to Lee.

### 4. Title page without the USB cable; the cable appears at Step 1 (low)

- What: the take-apart opens on the Full Build's title page, which hides the cable (guide.py:103, `hide=[USB_A, USB_B]`, "as the MRA's
  title page"): the Start view has no USB_A, USB_B or 'usb cable'; Step 1 adds all three (000.png against 001.png), and they stay to
  Step 20. The published take-apart's Start shows the finished kit with its cable (published_steps.txt:30, 39-40). In the RCC's and
  MRA's take-aparts the cable is the first thing off, so its appearance there is the step's subject; here it pops in on the stems' step.
- Fix: put to Lee: show the cable on the take-apart's title page (Step 1's caution names it), or accept the pop-in.

### 5. Step 16: a third of D2's arrow is behind D2 (low)

- What: the published tail (637.93, 855.51, 1256.74), 86.5 mm along +Z at D2's foot, seen from the published camera (dir -0.4635,
  0.7743, -0.4309, from the box's side): a ray test against D2's box (x 590.6 - 685.9, y 856.2 - 907.0, z 1251.9 - 1254.9) puts 31% of
  the arrow behind D2; 031.png shows only its head and a short shaft above D2's top edge. Same tail and camera in the published guide.
  Lee's PMG second round asked for arrows their own plate does not cover.
- Fix: raise the tail to just above D2's top edge (y about 910), same length and direction; or put to Lee.

### 6. Step 5: D4 fades while still astride the USB cable (low)

- What: D4 slides 75 mm along the cable, as published, and fades with the cable still in the notch at its foot
  (feasibility_verdicts.json:10, "stays in the notch for the whole 75.2 mm; D4 then lifts off the cable"). The notch is open at the
  bottom (the Full Build lowered D4 over the cable, its Step 25), so in the kit D4 comes off the tabs in a few mm and is then lifted off
  the cable; the caption ("Slide D4 off the tabs of D1, D2, and D3, along the USB Cable.") and the fade leave that out.
- Fix: keep the published slide and add "then lift it up off the USB Cable"; or the Full Build's way reversed (-X 8, then up 65, FREE:
  feasibility_log.txt:37), which departs from the published.

### 7. Step 14 (and 13): the carried published framing centres below our content (low)

- What: the camera target is the published one carried to the laid matrix (deconstruction.py:133-135): Step 14 [543.4, 832.2, 1233.0],
  radius 57.5. The published target sat 36 mm under the held matrix because its loose wires hung there (published wires y 929.9 -
  949.8 under the matrix at 947 - 956: published_steps.json, Step 14 "moved"). Ours lie flat at the matrix's level and on the table
  (matrix y 866.3 - 871.3 laid, pins 856 - 858), so in 027.png the matrix runs along the top and the lower 40% is empty. Step 13 is
  the same (target 42 mm under the matrix; 025.png).
- Fix: keep the turned published direction and radius, aim at the middle of what the view shows (the matrix, sockets and pins; for
  Step 13 with D10's drop).

### 8. The rulebook and README still describe the superseded draft (low)

- What: docs/cadasio-patterns.md:285-292 ("The LSM's deconstruction (first draft ...): the Full Build in reverse ... the LED matrix,
  over D4 and back") is the draft Lee rejected; Lee's 21 Oct answers (lee_notes_2026-10-21.md: base it on the published take-apart,
  the pry tool, gray, eyes not hole labels) are not in the rulebook, though CLAUDE.md asks for a convention Lee states to go there;
  README.txt:156-171 keeps questions 20 - 25 open; CLAUDE.md documents `reappear=True` for `lift()` only, not for `unplug()` (Step 12),
  and motioncheck skips both fades (Steps 10c, 12c), so only wirecheck at rest covers them.
- Fix: replace the LSM paragraph of rulebook section 11 with the rebuilt draft's basis and Lee's words; close README 20 - 25; one line
  in CLAUDE.md for `unplug(..., reappear=True)`.

## Every departure from the published guide, judged

| Ours | Published | Departure | Judgement |
|---|---|---|---|
| Start | Start | The Full Build's title page (camera Lee chose 21 Oct, no USB cable) | Justified by the house rule; the missing cable is finding 4 |
| Step 1 | Step 1 | Caution: disconnect the USB cable first; stems 44 mm (published 62.5) | Justified (the cable cannot come out first; 44 clears D8 by 14 mm) |
| Steps 4 - 5 | 4 - 5 | Close-up on both of D2's tabs (published ring on one); eyes on D3's tabs, which we show (the published eyes pointed at a hidden D3) | Justified; D5 really slides (published did not) |
| Steps 6 - 7 | 6 - 7 | Posts pushed up 6.4 out of D1 first; close-up of the tab under D1 from below (published ring 15 - 20 mm above D1 on the post's foot) | Justified (the catch is under D1; the Full Build's Step 36c close-up); D6 catch is finding 1 |
| Step 9 | 9 | Arrow on the matrix's middle (published reused Step 8's); matrix rises with the Full Build's Step 32 wire shapes reversed; shown hovering at 9c | Justified (published slip 8; one brief wire touch, the Full Build's own Step 32c) |
| Step 10 | 9c | Setting the matrix down is a step of its own, a fade, an eye on it; laid on the table (published floats 5.9 mm up), 2.5 mm further toward D2 | Justified (the published swaps models; clear of the USB A end) |
| Step 11 | 10 | none | |
| Step 12 | 11 - 13 | Three wires in one step (Lee's group), in the build's order (published white, purple, gray: its slip 11); two eyes (i2/i3 share one) instead of three; a fade with the pins laid on the table beside the matrix | Justified (Lee; the MRA's one eye per cluster) |
| Step 13 | 14 | Matrix where it lies, turned half round, camera and arrow turned with it (published put it back at the hover: its slip) | Justified; framing is finding 7 |
| Step 14 | 15 | As 13 | Justified; framing is finding 7 |
| Steps 16 - 17 | 17 | D2 slid out with its leads still in (the Full Build's Steps 21 - 24 reversed), then the two pins unplugged with the published eyes, instead of both in one swap | Justified |
| Step 18 | 18 | Nut: the Full Build's eight quarter turns, then off over the wires and pins (published 176 degrees over 85 mm) | Finding 2 |
| Step 20 | 20 | The cable really slides 25 mm before fading (published: no motion) | Justified (published slip 10) |
| Step 24 | 24 | Caution: use the Pry Tool | Justified (Lee) |
| Completed View | Completed View | Generator's default camera, not the published | Finding 3 |
| Parts List pages | none | The Full Build's parts list after the Completed View | Justified (Lee's MRA ruling of 19 Oct, by analogy) |
| Arrows | | Published sizes copied, including the spread the study lists as a slip (section 5, item 9: Step 4's 7.1 mm, Step 23's 1.3 mm) | Justified by Lee's PMG ruling of 21 Oct ("Examine the Cadasio"; "Step 7 needs a wider arrow", the published 6.5 mm) |

Numbering: ours and the published both have 24 steps, but Steps 10 - 17 carry different numbers from the published steps they stand
for (the split of 9, the merge of 11 - 13, the split of 17). Only worth a word to Lee if TechBox's own material cites the published
step numbers.

## Motion, step by step (feasibility as tested in our model)

Stems FREE; D8 LATCH (the posts' latch heads: close-up); D7 FREE; D5 LATCH (D2's and D3's barbs: close-up and eye); D4 LATCH (same),
then astride the cable (finding 6); posts LATCH at D1 (close-up), then BLOCKED at D6 (finding 1); D6 FREE; matrix with D10 FREE (the
D9s 0.28 mm tight); laid pose clear of the cable and its A end; D9s LATCH (a detent lip at the top of each notch: no cue in either
guide, a firm pull); pins out of i2, i3, b19 FREE with the USB plug in (purple pin 3.4 mm clear of it); D10 down LATCH (its hooks over
the board's edges: eye) and clear of the wires in its notch; connectors FREE; D3 LATCH (close-up); D2 LATCH (close-up), clear of the
USB plug; nut FREE over the pins; button with its pins FREE through D2's hole; USB plug tight in the Nano's socket, FREE after; R330,
CAP, R12K, Nano FREE in that order (the Nano before R12K would catch on the resistor, 0.4 mm). motioncheck: one 0.48 mm centre-line
pass between the gray and purple wires in Step 9c (the Full Build's own Step 32c, played back); it skips Steps 10c and 12c (fades).
