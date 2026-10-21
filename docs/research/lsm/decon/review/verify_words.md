# LSM deconstruction draft: the wording review, checked (21 Oct 2026)

A skeptic's pass over `review_wording.md`. Each finding was checked against `LSM Build Instructions/steps-deconstruction.json`,
`deconstruction.py`, `guide.py`, `steps.json`, `assembly-report.json`, the pictures in `LSM Build Instructions/pages/steps-deconstruction/`,
TechBox's edited MRA wording (`MRA Build Instructions Prototype/step-text-deconstruction.json`, `step-text.json`, against the MRA script's
own strings) and the summary of TechBox's published LSM take-apart (`docs/research/guide_19075-..._deconstruction.md`). Nothing was run; this
is the only file written.

Verdicts: 5 confirmed (1, 2, 5, 7, 8) and 4 confirmed points of style (10a, 10b, 10d, 10f). Uncertain, for Lee: 3, 4, 6, 9 and 10g.
Refuted: 10c and 10e.

## 1. Step 18, "wires first": CONFIRMED, high

- The button's head points +Z (guide.py:493, "its head at +Z"). BUTTON z 1233.65 - 1258.55 and D2 z 1251.93 - 1254.93 (assembly-report.json),
  so the head stands 3.6 mm proud of D2's outer face and the leads leave the back at z 1233.65 (guide.py:496 `STUB`), inside the box.
- Step 18c: `paths.BUTTON` = [0,0,57.1] -> [0,0,157.1], +Z 100. The pins ride on the button. The button leaves head first and the
  wires come through the hole last. 035.png: seen from inside D2, the arrow runs from the wires' side out through the hole.
- "wires first" comes from Full Build Step 19 (guide.py:550), where it is true on the way in. On the way out it is backwards.
- Fix (the reviewer's, kept): "Remove the Push Button from D2, pulling its wires back through the hole." Or, to match the inside view:
  "Push the Push Button out through the hole in D2, then pull its wires through after it."

## 2. Step 4, tabs under the box: CONFIRMED, medium

- The D11 feet are at y 856.02, D1's underside at 859.4 (assembly-report.json) and the table at 856.23 (guide.py:108 `TABLE_Y`). The tabs
  sit in the 3 mm gap between D1 and the table, slightly below the walls' feet, so nobody can push them up with the box standing.
  007.png shows the box upright from above (`keep_camera=True`). Only the close-up ("Push each tab up out of D1", seen from below) hints
  at reaching underneath. The Full Build turned the box over for this joint (Step 36, guide.py:811).
- TechBox's published take-apart also points at the posts' feet: an eye and a close-up of the foot or lock slot (Steps 6 and 7 there).
- Fix (the reviewer's, kept): "Lift the box and push the tabs of the four D11 posts up out of the slots in D1 from underneath. Then, remove
  the posts from D6." The question for Lee (must the feet be pushed from below, or do the posts pull straight up?) stands.

## 3. Step 17, the Full Build's Step 18 caption word for word: UNCERTAIN, low (the reviewer said medium)

- True: deconstruction.py:165 matches guide.py:543 except for the capitals, and Lee's rule says every take-apart step has its own
  description (cadasio-patterns.md:249-250).
- Against: Full Build Step 18 is the same physical act (the nut off the button, over the wires), so the words are accurate. 033.png
  shows the nut against D2 plainly, so leaving out "inside D2" does not mislead. No student-facing error. Whether a verbatim match with
  the same act breaks the rule is Lee's judgement.
- Fix if reworded: "Unscrew the nut from the Push Button, on the inside of D2. Then, slide it off over the wires." (NUT z 1250.43 - 1251.93
  against D2's inner face, 1251.93.)

## 4. Step 24, no Nano Board caution: UNCERTAIN, low; a question for Lee that is already open

- Nothing in the repository says whether the LSM kit has a Pry Tool. This is plan_final.md:406, question 4, already listed for Lee.
- The MRA's caution was TechBox's own edit, for a Nano in the I/O module's sockets. Here the Nano sits in a breadboard. The PMG and RCC
  drafts have no Nano caution either (no `caution` in their deconstruction.py), so the LSM draft is consistent with them. Not a defect
  of the draft.
- Fix: put question 4 to Lee. If there is a Pry Tool, use TechBox's sentence. If not, the reviewer's sentence is fine: "Lift the Nano Board
  straight up, a little at each end in turn, so that its pins do not bend."

## 5. Step 2, D8 under the posts' latches: CONFIRMED, low

- Lee's own note: lee_notes_2026-10-20.md:24. D8 now sits 0.02 mm under the latch heads (README.txt:32). 003.png shows the split latch
  heads above D8. TechBox's form for the same catch: "Remove C9 from the latches of C1 and C2." (step-text-deconstruction.json:84).
- Fix (kept): "Remove D8 from the latches of the four D11 posts."

## 6. Step 10, the box turned over with the matrix outside: UNCERTAIN, low

- True: the matrix lies outside D4, wired over D4's top edge, and turns over with the box (019.png).
- Against: Full Build Step 27 is the same state with the same kind of caption ("Turn the box over. Hook the tabs ...", steps.json; the
  matrix at P_OUTSIDE [-90.8, 5.9, 25.1] in both). Lee has reviewed it over several rounds without asking for a mention, so the draft
  only mirrors the Full Build.
- Also, "holding the LED Matrix against D4" is not what the model shows. Turned over, the matrix is beside D4, level with D1.
- Fix if Lee wants it: "Turn the box over, taking the LED Matrix over with it so that its wires stay connected. Remove D5 from D1, D2,
  and D3." Per CLAUDE.md, also ask whether Full Build Step 27 gets the same clause.

## 7. Step 19, the caution repeats the caption: CONFIRMED, low

- The caption is "Pull the LED Matrix off the connectors ..." and the caution's first sentence is "Pull the LED Matrix away from the
  connectors." They say the same thing. TechBox's form for a device off its wires: MRA Step 9, step-text-deconstruction.json:47-49. The
  connectors are black (037.png close-up).
- Fix (kept): "Disconnect the LED Matrix from the yellow, grey, and purple breadboard wires." Caution: "Hold the three black connectors
  while you pull the LED Matrix off its pins. Do not pull on the wires themselves."

## 8. Step 12, "the D5 end" after D5 is gone: CONFIRMED, low

- D5 comes off at Step 10. The place itself is right: the matrix ends at x +91, beyond D5's old face (Step 12c offsets).
- Better fix than "the open end": D3 is off too, so the box is open on a side as well as an end, and "open end" could be read as either.
  Use "... set it down beside the box, at the end where D5 was."

## 9. Steps 16 and 20, holes in the caption, eyes on the picture: UNCERTAIN, low; already plan question 5

- Lee's ruling (cadasio-patterns.md:262-266) is about the MRA's servo rows ("Row 6" and the servo). It was not carried into the PMG's
  take-apart, made the same day on "same principles": its "Unplug all 21 breadboard wires" has eyes and no labels.
- TechBox's published LSM take-apart deliberately shows no hole labels, the eye on each plug standing in for them (guide report, section 3.6).
- The breadboard's own printed letters and numbers are visible in 031.png and 039.png.
- Step 20 would need three labels (i2, i3, b19), more than the "2 at most" per step (cadasio-patterns.md:323).
- Fix: keep the eyes and put plan question 5 to Lee. If Lee wants labels: j5 and j16 on Step 16. On Step 20, three labels exceed the
  default, so say so.

## 10. Style

- **10a. "Unplug" in Step 1's caution: CONFIRMED, low.** TechBox turned every take-apart "Unplug" into "Disconnect" (MRA deconstruction.py
  :125, 130-132, 233, 238 -> step-text-deconstruction.json Steps 4 - 7, 51, 53), and Step 15 already says "Disconnect". Fix: "Disconnect the
  USB Cable from the computer or power supply before you begin."
- **10b. Serial comma: CONFIRMED, low (kit-wide).** TechBox adds it everywhere in its MRA edits ("B5, B6, and B7", "brown to G, red to V,
  and orange to S"). Fix: Steps 1, 10, 19 and 20. Note that the LSM Full Build has none either ("D1, D2 and D3", guide.py:716), so this
  is a kit-wide change, best made in both guides at once.
- **10c. "Leave ... connected" -> "Keep ... connected": REFUTED.** The only evidence is one TechBox rewrite of a different construction
  ("stay connected") in a Full Build caution. No TechBox edit rejects "Leave". "Leave its wires connected" is plain and correct.
- **10d. Step 5, "the walls" -> "D2, D3, D4, and D5": CONFIRMED, low.** TechBox names the parts ("Remove B8 from B5, B6, and B7."). D6 sits
  inside all four walls (D6 x 596.96 - 679.51, z 1156.68 - 1251.93, matching the walls' inner faces).
- **10e. Step 7, "the matrix" -> "the LED Matrix": REFUTED.** It refers back to "the LED Matrix" named earlier in the same sentence.
- **10f. Step 20 (and 19), "breadboard wires": CONFIRMED, low.** The hover names are "Yellow / Grey / Purple Breadboard Wire" (steps.json
  `names`), Lee says "the 3 breadboard wires", and TechBox writes "all eight breadboard wires". Fix: "Disconnect the yellow, grey, and purple
  breadboard wires from i2, i3, and b19."
- **10g. "grey" vs "gray": UNCERTAIN, for Lee.** TechBox writes American English ("colours" -> "colors", step-text.json:493-494), but "grey" is in
  the LSM's hover names, captions and close-ups. Changing it is a kit-wide decision.
