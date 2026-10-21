# LSM deconstruction, first draft: the independent review and what was done (21 Oct 2026)

Four reviewers (order and motion, wording, visual cues, conventions and code), each finding then challenged by a skeptic: the
`review_*.md` and `verify_*.md` files here. 50 findings, 7 refuted. The review saw the draft before the published arrow sizes
(docs/research/lsm/decon/arrows/) were put in; its arrow findings were checked again on the revised draft. (`generator_log.txt`,
`motioncheck.txt` and `pictures.md` are the evidence it was given, as of that draft.)

## Done

- Wording, in TechBox's take-apart style (the MRA's step text): Step 1 caution "Disconnect ..."; serial commas; Step 2 "from the
  latches of the four D11 posts"; Step 4 "Lift the box and push the tabs ... from underneath. Then, remove the posts from D6."; Step 5
  names the walls; Step 10 says to turn the box over with the LED Matrix, its wires connected; Step 12 "at the end where D5 was" (D5 is
  off by then); Step 17 a description of its own ("on the inside of D2"); Step 18 no longer says "wires first" (the button leaves head
  first); Step 19 "Disconnect the LED Matrix from the ... breadboard wires", its caution to hold the connectors; Step 20 "breadboard
  wires".
- Step 17: the nut slid on past the pins' ends before it goes (it faded out on the wires), its arrow beside the nut, clear of the
  button and its wires.
- Arrows (with the published sizes): an arrow per stage, in turn (D10, D3, D4, the matrix off its connectors), as Lee had the PMG's;
  D10's slide short of the wires, its drop in front of D10; D4's lift from its D2 end, clear of the button; D9's left of the USB plug;
  Step 1 framed so that its arrow is on screen; every arrow on screen at 1280, 1000 and 768 px.
- Steps 19 - 20 framed higher (D1 was cut at the bottom).
- Step 1 glides from the title page: the breadboard's backing (put away in the Full Build's Step 1) is left out of the take-apart from
  the start (`take_apart(leave_out=)`), not put away, which had made Step 1 cut in.
- The script reads the Full Build's own records where it had typed values (the D11 posts' poses, Step 36c's close-up), asserts that a
  shift is a shift and that a matrix walk-back starts where the matrix is.
- The player: a close-up keeps clear of the arrows' heads too, not only their shafts.

## Put to Lee (README questions 20 - 25)

The order's dependence on the b19 / USB plug overlap (a shorter order if b19 is free in the real kit); hole labels instead of eyes on
Steps 16 and 20; a Pry Tool caution for the Nano Board; the published arrow sizes and the four D11 arrows; D10 off in place or on its
own; "grey" or "gray".

## Left as they are (inherited from the Full Build, or cosmetic)

The box turned over with the matrix outside (the Full Build's Steps 27 - 28); the button's pins swinging out of j5 / j16 in one stage
(the Full Build's Steps 21 - 22 reversed); the matrix and connectors lying a little above the table (the Full Build's poses, README
question 11); Step 8's matrix arrow crossing the wires (they go with it); the arrows of Steps 2 - 4 on the exact diagonal. The 2D PDF
tool (player/js/pages.js) places a close-up in the corner farthest from its spot without regard to arrows (Step 4): to be put right
before an LSM PDF is made.
