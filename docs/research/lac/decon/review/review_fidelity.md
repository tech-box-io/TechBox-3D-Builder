# LAC deconstruction, first draft: fidelity review

21 Oct 2026. Read-only review of `LAC Build Instructions/deconstruction.py` -> `steps-deconstruction.json` (47 numbered steps) against
TechBox's published take-apart (19075-lac_deconstruction, 47 steps: `docs/research/guide_19075-lac_deconstruction.md`, its pictures in
`published/pictures/19075-lac_deconstruction/`, its geometry in `published_geometry.md`) and the rulebook's section 11. Nothing was run
but light Python on the JSON and crops of the review strips (`review/pictures/stepNN.png`). The known Full Build replays (contacts in
6c, 11c, 14c) are not reported.

## 1. Step by step: ours against the published

| ours | published | same / different | justified and said? |
|---|---|---|---|
| 1 F6 | 1 | same cue (arrow 56.1 x 4.87, -z); Full Build 57's camera; caution POWER added | yes |
| 2 F2 | 2 | same arrow size and direction, eye at the slit; not rolled; cable walked back out of the slit | yes; but see F3 (arrow placement) |
| 3 F5 | 3 | same | yes |
| 4 USB cable | 25 | moved up (power first, the LSM's rule); arrow on the plug, no eye on the A end (RCC rule) | yes (README "published: Step 25") |
| 5 F1 forward | 4 | same arrow | yes |
| 6 F1 aside | 5 | eye; ours face down in front, published face up beyond the -z end | yes (plan) |
| 7 LCD out of F9's notches | 6, first half | eye at the published spot, close-up with two red boxes (Full Build 52c) | yes |
| 8 LCD laid down | 6, second half | split in two, as the Full Build brought it in | yes (README) |
| 9 F8 | 7 | same arrow; Full Build 50's camera | yes; see F7 (arrow on the pot leads) |
| 10 F4 lifted aside | 8 | same arrow, on the lift; ends at the Full Build's FLAT_F4 (published F4-2, the same idea) | yes; see F9 (wording) |
| 11 F1 back | none | added (F1 back where its leads were plugged) | plan only, not README (F5) |
| 12 F9 | 24 | published one +Y arrow; ours tip then lift, in turn (Lee's PMG rule); same close-up | yes; see F8 (stage-0 arrow) |
| 13 F7s spread | 26 | two arrows, published lengths | see F1 (arrows do not read) |
| 14 buzzer out, wired | 27 | ours up 75 mm and over (Full Build 43); published slid out +Z; arrow + eye | plan only (F5); see F4 (eye on arrow) |
| 15 F7s out | 28 | up arrows only, as published | breaks Lee's per-stage rule, not in README (F2) |
| 16-19 LCD wires | 19-22 | same order (GND first), label on the pin, eye on the breadboard end, at the published spots | yes |
| 20 LCD away | 23 | ours lifts 30 mm, then fades (published fades in place) | in-house rule; README silent (F5) |
| 21-22 buzzer leads | 29-30 | same order (red, black), eye each | yes |
| 23 buzzer away | 31 | as 20 | as 20 |
| 24-26 pot leads | 9-11 | same order (black, tan, red), eye each, caps hang from the pot | moved after the buzzer: README yes; see F6 (24c contact) |
| 27 F1 picked up | none (12's isolation) | added (ours lies face down) | plan only (F5) |
| 28-31 knob, nut, washer, pot | 12-15 | same arrows; nut unscrewed (published slides); not rolled | yes |
| none | 16-18 refit | dropped (Lee: nothing refitted) | yes |
| 32-33 yellow, orange | 43, 42 (last) | moved before the switch leads and the other six; yellow first (published orange first) | README says orange last is not taken; yellow-first not said (F5) |
| 34-36 switch leads | 32-34 | same order, caps hang below F4 | yes; see F6 (35c contact) |
| 37 switch out of F4 | 35 | same arrow, alone | yes |
| 38-43 six jumpers | 36-41 | same order, eye on the same end of each (ours within 2 mm of the published rings), the published camera | yes |
| 44-47 RTC, resistors, Nano | 44-47 | same arrows, same camera | yes |
| Completed View, parts list | Completed View | F3 + breadboard; Full Build's parts list after it (MRA, PMG, LSM) | yes |

Every published step has a counterpart or a stated reason (16 - 18). Ours adds Steps 8, 11 and 27 (47 - 3 + 3 = 47). Checked and
clean: no part comes back once it has left (`leaving` vs every later `visible`); F1 and F4 are put away after their isolated runs, as
the published hides them; every removal moves before it fades; the USB cable is out at the first step its plug can come out; every
caption is its own and names the Full Build's holes correctly (checked against steps.json Steps 3 - 39); arrow sizes are the
published ones; no arrow is over 0.77 towards the camera. The log's two Step 5 WARNINGs (F4 and the LCD "plugged into" F1) look
false (F1 slides forward off F4's tabs and away from the LCD's face) but are not mentioned in the README draft's Checked line.

## 2. Findings

**F1. Step 13 (high): the two "spread" arrows do not read.** `deconstruction.py:201-202` draws them flat (`normal=[0, 1, 0]`) 10 mm
above the tops (y 968). From Step 44's camera (33 deg up) F7B's arrow runs from its top out over the RTC module and the jumpers, and
F7A's is a thin sliver at F4's front edge, its head not visible (`review/pictures/step13.png`, left panel, about x 330 - 440, y 130 -
180). The published Step 26 (`070.jpg`) has two standing arrows at mid-height on the F7s (y 918 - 922, `published_geometry.md` section
3), each plainly on its F7. Lee has twice asked for arrows that are not occluded (PMG rounds 1 and 2). Fix: the published's arrows
mirrored to our camera's side and turned to face it, e.g. `dict(tail=[660.7, 920.0, 1222.7], head=[623.8, 920.0, 1222.7],
normal=[0.0, 0.658, -0.753], part=F3, width=3.75)` and `dict(tail=[691.8, 920.0, 1222.7], head=[732.3, 920.0, 1222.7], ...width=3.8)`
(z 1222.7 = 1233.2 less the published's 10.5 mm offset, since our camera is at the -z end; the planks are x 657 - 660 and 690 - 693,
`cad_study.md`; check their extent in z and keep the arrows a few mm on the camera's side of it). If F7B's
still lands on the breadboard, give Steps 13 - 15 the published's camera for this run (dir (0.7131, 0.5802, 0.3935), radius about
110), as Steps 38 - 47 already take the published's camera for the same reason.

**F2. Step 15 (medium): one stage without an arrow, the other's arrows off the parts, and not in the README.** The F7s close, then
rise (`paths={i: [ZERO, UP]}`, two stages); only the up arrows are drawn (`deconstruction.py:209-211`). Lee's 21 Oct rulings (rulebook
lines 301 - 315): a part that comes off in stages shows an arrow for each, in turn, "for every part that comes off in stages". The
code says why (14 mm inward arrows in a 30 mm gap were too short to read), but the README draft does not, so Lee is not asked. Also, as
Step 15 opens the up arrows stand where the F7s will be once closed (tails x 650.5 and 700.0), about 10 mm inside the spread tops: in
`step15.png` (left) F7B's stands over the RTC module and F7A's head lies on F4's edge; the published Step 28 puts them on the spread
tops (tails F7A (640.3, 955.5), F7B (711.4, 953.0)). Fix, in Lee's rule: inward arrows from outside the tops, so that they never meet,
then the up arrows in turn: `arrow_style={F7A: dict(dims=(20.0, 3.75), stage=0, at=[620.0, 958.0, 1233.2], then=[size('f7a_up',
stage=1)]), F7B: dict(dims=(20.0, 3.8), stage=0, at=[731.0, 958.0, 1233.2], then=[size('f7b_up', stage=1)])}` (each about the 18 mm a
top travels). If Lee prefers the published (up arrows only): drop `stage=1` and give `at=` the published tails above, and add the
exception to the README's questions.

**F3. Step 2 (medium): F2's arrow lands on the USB cable and the eye.** The arrow (stage 2, the pull, -x 79.8 mm, tail at F2's
mid-height, z 1289.9) points 45 deg towards the camera; seen from Step 56's camera a -x arrow runs right and down the screen, and from
that tail its head lands just below the slit (z 1339, y 889), so in `step02.png` (left) it crosses the cable where it leaves the slit
and ends on the eye's leader. The published Step 2 arrow (`004.jpg`) sits on the middle of F2, clear of the cable. Rulebook (Lee, 18
Oct): an arrow "sits where it reads", clear of leads; RCC: "clear of the cable". Fix: move the tail to F2's free end, near its top
edge, e.g. `arrow_style={F2: size('f2', stage=2, at=[640.0, 955.0, 1225.0])}`: by projection its head then lands about 45 mm left of the
slit at the slit's height, clear of the cable and of the eye below the slit, and it sits on the end the caption says to swing out first
(check that the tail is on F2: the case's -z end is near z 1213).

**F4. Step 14 (medium): the eye covers the arrow.** `eye=[dict(id=BUZZER, ..., side='near-above', reach=0.05)]` puts the eye picture on
the up arrow's shaft (`step14.png`, left; the arrow head pokes out above the eye). The published Step 27 (`072.jpg`) has the eye well
up and to the right of the arrow. Fix: `side='up-right', reach=0.1` (or `side='right'`).

**F5. README draft (medium): it overstates and leaves out what Lee must rule on.** (a) Line 5 (and the docstring, line 10) says "each
arrow ... one per stage, in turn (F9: the tip, then the lift)": only Step 12 has that; Steps 2, 10 and 14 have one arrow for a move in
2 - 3 stages (`then=` is refused with `wire_via=`: plan question 20) and Step 15 only its second stage's (F2). (b) Line 7 says every
step replays a Full Build state backwards: Step 4 is a new state (the plan says so), and Steps 16 - 19, 21 - 22, 38 - 43 and 45 - 46
follow the published order, which is the build's order, not its reverse (the shapes are the Full Build's; the states between are new).
(c) Not said: Steps 11 and 27 are additions, and why (our F1 lies face down; unplugged where Step 6 left it the pot's tan lead passes
through three other leads); the buzzer leaves upward over the board (Full Build Step 43) where the published slides it out +Z; the LCD
and buzzer lift 30 mm before fading (published: fade in place; plan question 21); yellow before orange (published: orange first). (d)
None of plan section 8's questions is carried over; most are still open (USB at Step 4, the order after F4, F1's two extra steps, a
storage note card instead of the refit, the LCD in two steps, keeping the pin labels, `then=` with `wire_via=`, the 30 mm lift, the
website name), plus Step 15's arrows. Fix: correct (a) and (b), add (c) to the "Not taken from the published guide" list as "Added /
changed", and add the open questions under QUESTIONS FOR LEE (13 is settled: one wire per step).

**F6. Steps 24 and 35 (medium): two wire-through-wire moments not in the known list.** `review/motioncheck_draft1.txt` lines 18 - 19:
24c pot black and pot tan 0.65 mm apart at 0.73 of the move; 35c switch black and switch tan 1.04 mm at 0.88 (touching is 1.25). Both
come from the published order (black first) meeting the hang stage that `to_hanging()` adds: the black caps went in from 5 mm up,
under the tan lead's hump (Full Build Steps 32 and 18). Fix: give the black cap a stop that brings it out from under the tan lead,
towards the part, before it drops to hang (a via in `to_hanging()`'s path for the black ones), or unplug tan before black in both runs
(a departure from the published order, to be said in the README); rerun motioncheck on Steps 24c and 35c.

**F7. Step 9 (low): F8's arrow lies on the potentiometer's leads.** Tail y 919.5, along +x, exactly where the three leads run out to
F1 lying in front (`step09.png`, left: the arrow covers the red and black leads). It reads as "pull the wires". The published's F8
arrow had no leads beside it. Lee (MRA, 18 Oct): arrows "above wires". Fix: `arrow_style={F8: size('f8', shift=[0.0, 25.0, 0.0])}`.

**F8. Step 12 (low): the tip arrow is low, beside F9, over the pot leads.** The stage-0 arrow's tail is at y 925 in front of F9
(`step12.png`, left: it points right across the pot's leads, F9's top above it). The tip moves F9's top most, and the published's
arrow sits at the top (y 953.7). Fix: `size('f9', stage=0, at=[722.0, 950.0, 1355.8], then=[size('f9', stage=1)])`.

**F9. Step 10 (low): "lay it behind the case" against a picture of F4 in the air.** F4 ends at the Full Build's FLAT_F4 pose
`[-82.7, 17.3, -0.1]`, 17 mm above its seated height, its switch leads hanging (`step10.png`, right panel); the published's F4 is held
the same way, but has no words. Fix: "... and hold it behind the case" or "move it behind the case", or a pose on the table if the
leads reach.

**F10. Step 7 (low): the eye's leader crosses the close-up's.** In `step07.png` (left) the eye's leader to the LCD's low corner and
the close-up's leader to F9's upper notch cross (the published Step 6 keeps the close-up top left, the eye bottom left). Fix: put the
eye below (`side='down-left'`) or ask for the close-up above it (`inset=dict(..., side='left')` and check).

## 3. Not findings (looked at)

- Step 4's arrow (0.77 towards the camera) reads as a pull towards the viewer, clear of the cable (RCC rule); no eye on the A end, by
  the RCC rule rather than the published.
- Steps 6, 8, 11, 27: eyes, as the published uses for parts laid aside; Step 6's camera swings 68 deg from Step 5's, where the published
  held one, but the code gives the reason (Step 53's camera leaves F1 out).
- Steps 16 - 19: labels on the LCD's pins and eyes on the breadboard ends, as published; the published's one camera is matched by
  `keep_camera`.
- Steps 38 - 47: the published camera, said in the README and the code.
