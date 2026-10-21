# LSM deconstruction draft: wording review (21 Oct 2026)

Angle: every caption, caution and close-up caption in `LSM Build Instructions/steps-deconstruction.json` (52 views) and the strings in
`LSM Build Instructions/deconstruction.py`, checked against what each view shows (`LSM Build Instructions/pages/steps-deconstruction/NNN.png`),
guide.py's holes and part names, `assembly-report.json`, and TechBox's own take-apart wording (`MRA Build Instructions Prototype/step-text-deconstruction.json`,
compared with the MRA script's original strings to see what TechBox changes). Nothing was run; no file but this one was written.

Checked and right, not repeated below: every hole name (Step 16 j5 / j16 = guide.py:501; Step 20 yellow-i2, grey-i3, purple-b19 in that order =
guide.py:202; Step 21 a11 / a19 = :194; Step 22 j2 / j3 = :327; Step 23 h3 / h16 = :193); every direction except Step 18's; the wire-pulling
caution on Steps 16 and 20 (TechBox's own sentence); Step 15's caption (TechBox's MRA Step 4, word for word); the comments and docstring of
deconstruction.py. TechBox's published LSM take-apart has no step text at all, so the MRA's edited wording is the only TechBox model.

## 1. Step 18: "wires first" is backwards (high)

- **Wrong:** "Push the Push Button, wires first, out through the hole in D2." (deconstruction.py:168). The button leaves head first, its
  wires following. Step 18c moves it from z +57.1 to +157.1 (steps-deconstruction.json, `paths.BUTTON`), i.e. +Z 100, the side its head is on:
  its back, where both leads leave, is at z 1233.65 (guide.py:496) and its head at 1258.55, with D2 at 1251.93 - 1254.93
  (assembly-report.json), so the head is outside D2 and the wires trail inside. Picture 035.png: the arrow runs from the wires' side out
  through the hole. The phrase is carried over from Full Build Step 19 (guide.py:550, "Push the button, wires first, through the round hole
  in D2 ..."), true only on the way in. "Push the Push Button" also reads badly.
- **Fix:** "Remove the Push Button from D2, pulling its wires back through the hole." (TechBox's form: "Remove the Claw Servo (Blue Dot) from
  C3.", MRA step-text-deconstruction.json:119).

## 2. Step 4: the tabs to push are under the box, and nothing says so (medium; one point for Lee)

- **Wrong:** "Push the tabs of the four D11 posts up out of the slots in D1, then remove the posts from D6." (deconstruction.py:120), shown
  with the box standing upright (`keep_camera=True`, D7's camera; picture 007.png). The tabs end under D1, flush with the table: D11 foot
  y 856.02, D1's underside 859.4 (assembly-report.json), table 856.23 (guide.py:108). A student cannot push them up without lifting or turning
  the box, which is why the Full Build turned it over for this joint (Full Build Step 36, guide.py:811). Only the close-up from below
  ("Push each tab up out of D1") hints at it.
- **Fix:** "Lift the box and push the tabs of the four D11 posts up out of the slots in D1 from underneath. Then, remove the posts from D6."
  Ask Lee whether the posts' feet really need pushing from below or pull straight up from above once D7 and D8 are off; if the latter,
  "Remove the four D11 posts from D6 and D1." and the close-up's caption changes with it.

## 3. Step 17: the Full Build's Step 18 caption, word for word (medium)

- **Wrong:** "Unscrew the nut from the Push Button and slide it off over the wires." (deconstruction.py:165) is Full Build Step 18's caption
  (guide.py:543) with only "Push Button" capitalised. Lee's rule: every take-apart step has a description of its own, not the build's captions
  reworded (docs/cadasio-patterns.md:249-250). It also undoes a different build step (Step 20, the nut tight against D2), and leaves out where
  the nut now is: on the inside of D2, tight against it (NUT z 1250.43 - 1251.93 against D2's inner face at 1251.93; picture 033.png).
- **Fix:** "Unscrew the nut from the back of the Push Button, inside D2. Then, slide it off over the wires."

## 4. Step 24: no caution for the Nano Board; whether the kit has a Pry Tool is unknown (medium, for Lee)

- **Missing:** TechBox added a caution to the MRA's Nano Board removal, "Use the Pry Tool to carefully remove the Nano Board."
  (MRA step-text-deconstruction.json:277-280). The LSM's "Remove the Nano Board from the breadboard." (deconstruction.py:195) has none, and a
  Nano's 30 pins bend easily when it is levered out of a breadboard from one end. Nothing in the repository says whether the LSM kit has a Pry
  Tool (only the decon plans mention it; plan_final.md:406 leaves it open; the published LSM guides show no tool).
- **Fix:** ask Lee. If the kit has one: TechBox's caution as written. If not: "Lift the Nano Board straight up, a little at each end in turn,
  so that its pins do not bend."

## 5. Step 2: D8 is held by the posts' top latches; the caption does not say so (low)

- **Wrong:** "Remove D8 from the four D11 posts." (deconstruction.py:116). D8 sits just under the posts' top latches (Lee's own word:
  lee_notes_2026-10-20.md:24; README.txt:32); picture 003.png shows the split latch heads above D8, so it does not simply lift off. TechBox
  names latches in the same situation: "Remove C9 from the latches of C1 and C2." (MRA step-text-deconstruction.json:84). TechBox's published
  LSM take-apart gives this step a close-up of a corner latch.
- **Fix:** "Remove D8 from the latches of the four D11 posts."

## 6. Step 10: the box is turned over with the LED Matrix hanging from it (low)

- **Unclear:** "Turn the box over. Remove D5 from the tabs of D1, D2 and D3." (deconstruction.py:140). The LED Matrix lies outside D4, wired
  over D4's top edge (Step 8), and turns over with the box (picture 019.png: beside D4, its back up). Nothing tells the student to take it
  along; turned over on its own, the matrix pulls on its three wires.
- **Fix:** "Turn the box over, holding the LED Matrix against D4 so that its wires stay connected. Remove D5 from D1, D2, and D3."

## 7. Step 19: TechBox's form for a device off its wires, and a caution that repeats the caption (low)

- **Wrong:** "Pull the LED Matrix off the connectors of the yellow, grey and purple wires." with the caution "Pull the LED Matrix away from the
  connectors. Do not pull on the wires themselves." (deconstruction.py:181, 184). The caution's first sentence says again what the caption says.
  TechBox's wording for the same act on the MRA: "Disconnect the Servo Extension Wire from the Claw Servo's wires." with "When disconnecting
  the wires, pull apart the two black connectors. Do not pull on the wires themselves." (MRA step-text-deconstruction.json:47-49).
- **Fix:** "Disconnect the LED Matrix from the yellow, grey, and purple breadboard wires." Caution: "Hold the three black connectors while you
  pull the LED Matrix off its pins. Do not pull on the wires themselves."

## 8. Step 12: "the D5 end" after D5 has gone (low)

- **Unclear:** "... set it down beside the box at the D5 end." (deconstruction.py:144-145). D5 came off in Step 10, so the student has no D5
  to find the end by.
- **Fix:** "... beside the box at the open end, where D5 was."

## 9. Steps 16 and 20: holes named in the caption, not on the picture (low; plan question 5)

- **Wrong:** "Disconnect the Push Button's red wire from j5 and its black wire from j16." and "Disconnect the yellow, grey and purple wires
  from i2, i3 and b19." (deconstruction.py:158, 189) carry eyes and no labels (no view in steps-deconstruction.json has `labels`; pictures
  031.png, 039.png). Lee's ruling for the MRA: the take-apart's unplugging from a row carries the Full Build's labels for that row instead of an
  eye (docs/cadasio-patterns.md:263-264).
- **Fix:** carry the Full Build's hole labels (Steps 21 - 22: j5, j16; Steps 11 - 13: i2, i3, b19) on Steps 16 and 20, as the MRA's Steps
  5 - 7, and tell Lee; or ask whether the eyes should stay as well (plan_final.md:408).

## 10. TechBox's style, where the draft departs from it (low)

TechBox's rewrite of the MRA's take-apart (step-text-deconstruction.json against the MRA script's own strings) shows these habits; the draft
follows most of them but not these:

- **"Disconnect", never "Unplug":** TechBox changed every "Unplug" (MRA deconstruction.py:125, 238 -> step-text-deconstruction.json Steps 4,
  53). Step 1's caution, "Unplug the USB Cable from the computer or power supply before you begin." (deconstruction.py:113), and Step 15 now use
  both verbs for one cable: "Disconnect the USB Cable from the computer or power supply before you begin."
- **Serial comma:** TechBox writes "B5, B6, and B7", "A1, A2, and A3" (step-text-deconstruction.json:263, Step 42). The draft has none:
  Steps 1, 10, 19, 20 (twice) (deconstruction.py:114, 140, 181, 189).
- **"Keep ... connected":** TechBox's phrase is "Keep the breadboard wires connected to the Nano I/O Module." (MRA step-text.json:168, 185).
  Steps 6, 8, 12 and 14 say "Leave its wires connected." / "Leave the Push Button's wires connected." (deconstruction.py:127, 135, 145, 152).
- **Name the parts:** Step 5 "Remove D6 from the tabs at the top of the walls." (deconstruction.py:124) -> "Remove D6 from D2, D3, D4, and D5."
  (TechBox: "Remove B8 from B5, B6, and B7."); Step 7 "remove it from under the matrix" (deconstruction.py:130) -> "the LED Matrix"; Step 20
  "the yellow, grey and purple wires" -> "breadboard wires", as Lee named them ("the 3 breadboard wires") and as TechBox wrote "all eight
  breadboard wires" (step-text-deconstruction.json:268).
- **"grey":** TechBox's own text is American ("center", "colors": MRA step-text.json Steps 31, 96); the LSM's Full Build, hover names and this
  draft say "grey". A kit-wide change if TechBox wants "gray": Lee's call, not this guide's alone.
