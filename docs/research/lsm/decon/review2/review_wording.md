# LSM deconstruction, rebuilt draft: wording review (21 Oct 2026)

Angle: every caption, caution, close-up caption and alt text in `LSM Build Instructions/steps-deconstruction.json` (52 views), against
what each view shows (`LSM Build Instructions/pages/steps-deconstruction/NNN.png`), the Full Build (`guide.py` -> `steps.json`), the holes in
guide.py, and TechBox's own take-apart wording (`MRA Build Instructions Prototype/step-text-deconstruction.json`). Steps are named as the
player names them (the script's `cam('Step 11')` etc. are the published guide's numbers, which differ from Step 10 on). Nothing was run
but light JSON and GLB reading; no file but this one was written.

The hole names were checked against guide.py and are right: Step 12 yellow i2, gray i3, purple b19 (guide.py:202), Step 17 red j5 and
black j16 (:501), Step 21 a11 / a19 (:194), Step 22 j2 / j3, Step 23 h3 / h16 (:193). Step 1's power caution, the wire-pulling cautions on
Steps 12 and 17, and Step 24's Pry Tool caution (TechBox's MRA sentence word for word) are in place. Full Build "gray": no student-facing
"grey" is left (captions, caution, close-up caption and alt text, hover names of parts and wires in steps.json and steps-deconstruction.json;
parts.json has none). The findings, most serious first:

## 1. Step 13: D10 is hooked on, and the caption does not say how to unhook it (medium; motion question for Lee)

- **Wrong:** "Remove D10 from the bottom of the LED Matrix." (deconstruction.py:228). The Full Build hooks D10 on by sliding it along
  the matrix: "hold it under the matrix, then slide it along until its hooks hold both edges" (Full Build Step 31, guide.py:756; D10 rides
  up 22 mm at +40 mm along Z, then along to its seat). Step 9 of the take-apart itself says "with D10 hooked under it". A student told only
  to "remove" it will pull it straight down, as the animation shows (path straight down 40 mm, published-style; arrow head 50.8 mm below
  its tail, picture 025), against the hooks.
- **Evidence the hooks hold:** in lsm.glb, D10 rises to y 900.68, above the matrix's top (898.1), with vertices at x 607.3 and 669.6, that
  is 0.4 and 1.1 mm inside the matrix's edges (606.92 - 670.71), from y 897.5 up. The generator does not test a way given by hand
  (stepgen.py:1068-1084 tests only ways taken from the Full Build), so the clean log says nothing about this step.
- **Fix:** "Slide D10 along the LED Matrix, away from its three pins, until its hooks come off the edges. Then, remove it." (the pins
  are at z 1183 - 1189, guide.py:466; D10 came in from the other end). Ask Lee whether the animation should show the slide (as the Full
  Build's Step 31 and the first draft did) or keep the published straight drop with this wording.

## 2. Completed View: read aloud and announced as "The finished model." (medium; player-wide)

- **Wrong:** player/js/player.js:586 gives every `end` view the words "The finished model."; `announce()` (:605-608) tells a
  screen reader "Completed View, 50 of 52. The finished model." On the take-apart that view shows D1 and the Breadboard, the kit taken
  apart (picture 049). The same holds for every deconstruction, the published PMG Deconstruction r1 included.
- **Fix:** in `wordsOf`, for a guide made by `take_apart()` (`data.meta.taken_from` is set), say "The model, taken apart." (or what is
  left: "D1 with the Breadboard on it."). A player change: run the check on every kit, and the published guides keep the old words until
  they are published again.

## 3. Step 14: "the three black connectors" can be read as the wrong ones (low)

- **Unclear:** caution "Hold the three black connectors while you pull them off the pins. Do not pull on the wires themselves."
  (deconstruction.py:234-235). In picture 027 the black connectors the student sees are the three pin housings at the loose end, with the red
  arrow beside them; the sockets that come off are under the matrix's edge, marked only by the eye. Gripping the loose ends and pulling is
  pulling on the wires, which the caution forbids.
- **Fix:** caption "Disconnect the three breadboard wires from the V+, IN, and V- pins on the LED Matrix." (the Full Build's own names
  for them, Steps 14 - 17); caution "Hold the three black connectors on the LED Matrix's pins while you pull them off. Do not pull on the
  wires themselves."

## 4. Steps 6 and 7: "the D4 end" once D4 is gone, and "the same way" (low)

- **Unclear:** Step 6 "... the two D11 posts at the D4 end ..." (deconstruction.py:195-196). D4 came off at Step 5 and D5 at Step 4, so
  both ends are open and nothing marks "the D4 end". Picture 011: the USB Cable runs out of that end, between the two posts with arrows.
  Step 7 "Push the tabs of the other two D11 posts up out of D1 the same way." (:197) leans on Step 6 for "from underneath"; a step should
  read on its own (in the 2D PDF it is on a page of its own).
- **Fix:** Step 6 "Lift the box and push the tabs of the two D11 posts at the USB Cable end up out of the slots in D1 from underneath.
  Then, remove the posts from D6." Step 7 "Push the tabs of the other two D11 posts up out of the slots in D1 from underneath. Then,
  remove the posts from D6."

## 5. Step 5: D4 is left hanging on the USB Cable (low)

- **Incomplete:** "Slide D4 off the tabs of D1, D2, and D3, along the USB Cable." (deconstruction.py:182). The cable lies in the notch
  at D4's foot, which is open at the bottom: the Full Build lowered D4 onto it ("the USB cable in the notch at its foot", Full Build Step
  25, path down 65 mm then in 8 mm). After the 75 mm slide (picture 009) D4 is still on the cable; it has to be lifted off it.
- **Fix:** "Slide D4 off the tabs of D1, D2, and D3, along the USB Cable. Then, lift it up off the cable."

## 6. Steps 15 and 16: one kind of joint, two wordings; Step 16's caption leaves out the latch its close-up shows (low)

- **Inconsistent:** Step 15 "Remove D3 from the latch on D1." (deconstruction.py:239), close-up "The latch on D1 at the foot of D3";
  Step 16 "Slide D2, with the Push Button, out of the slots in D1. ..." (:243), close-up "The latch on D1 at the foot of D2". Both walls
  slide straight out (D3 -Z 40 mm, D2 +Z 57.1 mm: Steps 15c, 16c `paths`), both are held by a latch on D1 (pictures 029, 031).
- **Fix:** Step 16 "Slide D2, with the Push Button, off the latch on D1 and out of its slots. Leave the Push Button's wires connected."
  (or Step 15 "Slide D3 off the latch on D1." to match).

## 7. Step 19: "Push the Push Button out" (low)

- **Awkward:** "Push the Push Button out through the hole in D2, pulling its wires through after it." (deconstruction.py:259). The
  repeated "Push" reads badly, and the view is now from D2's engraved face (picture 037), where the student takes hold of the button's
  head and pulls it out towards them.
- **Fix:** TechBox's form, as proposed in round 1: "Remove the Push Button from D2, pulling its wires back through the hole."

## 8. Step 24: "the breadboard" in lower case (low)

- **Wrong:** "Remove the Nano Board from the breadboard." (deconstruction.py:272). The guide capitalises part names as the parts list
  does (LED Stems, LED Matrix, Push Button, USB Cable, Nano Board, Capacitor), and the parts list names this part "Breadboard". ("breadboard
  wires" in Steps 12 and 14 stays lower case, as TechBox wrote "all eight breadboard wires" for the MRA.)
- **Fix:** "Remove the Nano Board from the Breadboard."

## 9. Close-up texts (low)

- Steps 15 and 16: in the 2D-PDF pictures the close-up captions run past their frames (picture 029: "The latch on D1 at the foot of D3"
  starts left of the frame and ends right of it; picture 031 likewise). pages.js draws a caption on one line (player/js/pages.js:43-45);
  the player wraps it, so this shows only in the PDF. Fix: shorter captions, "D1's latch at D3's foot" / "D1's latch at D2's foot", or
  let pages.js wrap.
- Steps 6 and 7: the close-up caption "Push each tab up out of D1" (deconstruction.py:204) is an order; every other close-up caption
  names what it shows ("The latch on each D11 post", "D2's tabs through D5"). The Full Build's own for this joint: "The tab through D1".
  Fix: "The tab of a D11 post through D1".
- Steps 4 and 5: alt text "red boxes round the ends of D2's two tabs" (deconstruction.py:180, 186): American English is "around".

## 10. "330 Ω" and "12 kΩ" are not spelled out for reading aloud (low)

- Steps 21 and 23 (and Full Build Steps 4, 5, 8, 9): the words given to the speech engine are `sayable()`'s (player.js:590-592), which
  spells out "mm", "I/O" and "+5V" but leaves "Ω" (U+03A9, the Greek letter), so a browser voice may read "330 omega Resistor". Not
  heard here (no browser). Fix in the player: `.replace(/kΩ/g, ' kilohm').replace(/Ω/g, ' ohm')`; a player change, checked on every kit.

## 11. The kit's two guides now differ in style (low; for Lee)

- The take-apart follows TechBox's MRA style; the LSM Full Build does not, so one kit's two guides word the same things differently:
  - Serial comma: Full Build "D1, D2 and D3" (guide.py:716), "D8, D7 and D6" (:819), "V+, IN and V-" (:467, 472); take-apart "D1, D2, and
    D3", "D8, D7, and D6".
  - Capitals: Full Build "Push the 12 kΩ resistor into h3 and h16." (Step 5), "LED matrix", "push button", "USB cable", "capacitor", "LED
    stem"; take-apart "Remove the 12 kΩ Resistor from h3 and h16." and the parts list's capitals throughout.
  - American English: Full Build "towards the D4 end" (:616; TechBox writes "toward", MRA step-text-deconstruction.json:104), "turning it
    round" (:700), alt text "four red boxes round the slots in D1" (:797).
- **Fix:** ask Lee whether the Full Build should take the same style (rewording in guide.py gives those steps new text keys; no Part
  guides exist for the LSM yet). If yes, change it in guide.py and run deconstruction.py after it.
