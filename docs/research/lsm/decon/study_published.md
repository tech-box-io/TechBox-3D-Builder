# LSM deconstruction: TechBox's published take-apart mapped onto our Full Build

Study for the LSM Deconstruction guide (21 Oct 2026). Lee's request, word for word: "Alright, now take this LSM Full Build guide and
create a Deconstruction Guide based on it. Same principles as you used for the MRA. Remembering some things can be removed in groups
(like the 3 breadboard wires, etc.)"

Read: `docs/research/guide_19075-laser_stem_matrix_lsm_-_deconstruction.md` (the published take-apart, 24 steps; its raw data and
thumbnails are not on this Mac, so everything published below is from that report), `docs/research/guide_19075-laser_stem_matrix_lsm_-_full_build.md`,
`LSM Build Instructions/guide.py`, `steps.json` (82 views), `assembly-report.json`, `README.txt`, `docs/research/lsm/lee_notes_2026-10-19.md`,
`-19b.md`, `-20.md`, `-21.md`, `docs/cadasio-patterns.md` section 11, `MRA Build Instructions Prototype/deconstruction.py`,
`RCC Build Instructions/deconstruction.py`, `tools/stepgen.py` (take_apart / remove / unplug / lift, lines 828 - 1200, and the takeoff
views, 1713 - 1790). No meshes were loaded (this Mac had 60 MB free and 650 MB of swap left): "what blocks what" below is from the
parts' boxes in `assembly-report.json`, the build's ways in, and the research notes. Nothing was run.

Camera numbers: published = distance mm / elevation / azimuth as the report gives them. Ours = the Full Build step's camera, with its
frame radius turned into a distance as the player does in a landscape window (`player/js/core.js:265`: radius / sin(22.5 deg) x 1.08,
i.e. x 2.82). The azimuth convention is the same in both (atan2(x, z) of the view direction): our Step 36 and the published build's
Step 34 are both el -57 az 49, our Steps 34 / 35 and the published build's 32 / 33 both az 36 / -55, and the Completed Views agree
within 1 mm (321 / 322). Corners, in assembly space: D2 at +Z, D3 at -Z, D4 at -X, D5 at +X; az 45 = D5/D2 corner, az 135 = D5/D3,
az -135 = D4/D3 (our usual DIAG), az -45 = D4/D2.

## 1. Our 40 steps against the published 38

| published build | ours | what |
|---|---|---|
| 1 - 5 | 1 - 5 | backing; breadboard on D1; Nano; 12 kOhm legs; 12 kOhm in h3 / h16 |
| Capacitor card | 6 | (ours a 3D step, single view) |
| 6 - 8 | 7 - 9 | capacitor j2 / j3; 330 Ohm legs; 330 Ohm in a11 / a19 |
| 9 - 12 | 10 - 13 | ribbon split; white (ours yellow, code 'white') i2; grey i3; purple b19 |
| LED Matrix Diagram card | 14 | (ours a 3D step of the matrix's back, flipped, single) |
| 13 - 15 | 15 - 17 | sockets onto V+, IN, V- (ours: matrix held upright over the breadboard, P_UP) |
| 16 - 18 | 18 - 20 | nut off; button through D2; nut on (ours turn) |
| 19 | 21 + 22 | button leads: ours one per step, red j5, black j16 (D2 standing 57 mm out) |
| Mini USB card | - | |
| 20 | 23 | USB Mini-B plug (ours slides in -Z from +25; published fades in plugged) |
| 21 | 24 | D2 stood on D1 (ours slides -Z 57.11) |
| 22 | 25 | D4 (ours from above, then pushed 8 mm +X: guide.py:632) |
| 23 | 26 | matrix carried over D4 and laid outside (ours lifted and turned, 4 beats, wires over D4's top edge; published wires through D4's notch) |
| 24 + 25 | 27 | D3 hooked into D4 tilted, swung shut (ours one step, two stages, flipped) |
| 26 | 28 | D5 (ours flipped) |
| 27 - 30 | 29 - 32 | D9 x2; matrix held over the box; D10 hooked on (two beats); matrix lowered in |
| 31 - 33 | 33 - 35 | D6; D11 pair at the D5 end (A, B); pair at the D4 end (C, D), each short of home |
| 34 | 36 | all four D11 home from below (flipped, D1 / D5 ghosted) |
| 35 - 36 | 37 - 38 | D7; D8 |
| LED Stems card, 37 - 38 | 39 - 40 | one stem; the other 63 |

## 2. The published take-apart, step by step, on our model

Ids are guide.py's (lines 27 - 40). "Undoes" is in our numbering. "In our model" says whether our build allows that removal at that
point of the published order.

| pub | what it does (arrows, eye, inset) | our ids | undoes (ours) | in our model at that point | pub camera | ours (build step undone) |
|---|---|---|---|---|---|---|
| 1 | 64 stems up together; 1 arrow, eye on a middle stem | STEM_01 - STEM_64 | 40 + 39 | yes: up 44 (build hover, guide.py:819 - 823) | 374/24/32 | Step 40: ~254/35/-135 (120 deg apart) |
| 2 | D8 up; arrow, eye on plate, inset of a D11 corner latch (red box) | D8 | 38 | yes, up 55 (D8 sits just under the D11 top latches: Lee 20 Oct; 0.19 / 1.2 mm into ledges and posts, README Q17) | 300/34/123 | Step 38: ~254/35/-135 |
| 3 | D7 up; arrow, eye, inset of a D11 notch | D7 | 37 | yes, up 65 | 300/34/123 | Step 37: same |
| 4 | D5 out +X (but no visible slide: glitch) ; arrow, framed eye, inset D5/D3 corner tabs | D5 | 28 | yes: D5 slides +X off D1's tabs, D2's and D3's end tabs and D10's end tab, all along X; D6 stops at D5's inner face (x 679.51), D11_A/B are inside (x 673.3 - 676.3) | 300/37/139 | Step 28: ~383/-35/135 FLIPPED (72 deg) |
| 5 | D4 out -X 75; arrow, eye, inset D4/D2 corner | D4 | 25 | yes physically (straight -X, or -8 then up 65 as our build reversed); but in our build the matrix later lies outside D4 with its wires over D4's top edge (Steps 26 - 29), so D4 early rules out that route | 300/37/-145 | Step 25: ~353/35/-135 (8 deg) |
| 6 | two D11 (the build's second pair: D4 end), up 70 - 89; 2 arrows, eye on a foot, inset of the foot / lock slot | D11_C, D11_D | 35 (+ 36's last 6.38 mm) | yes once D7 / D8 are off: tabs up out of D1 (6.38), then up through D6's corner slots (to 85: guide.py:802) | 350/25/-120 | Step 35: ~282/23/-55 (59 deg) |
| 7 | the other two D11 (D5 end); 2 arrows, eye, same inset | D11_A, D11_B | 34 (+ 36) | yes | 350/24/58 | Step 34: ~282/21/36 (21 deg) |
| 8 | D6 up 45; arrow only | D6 | 33 | yes after the D11s (they pass through its corner slots) | 300/24/58 | Step 33: ~237/35/-135 (120 deg) |
| 9 | matrix + D10 lifted off the D9s (two model swaps: hovering 29 mm, then lying on the table beside the box, still wired); arrow reused from Step 8 | MATRIX (+ D10, J_WHITE_F, J_GREY_F, J_PURPLE_F ride on it) | 32 + 30 | lifting straight up to P_HELD (56.6 up, guide.py:223) is our build reversed and clear (D9s stay); "beside the box" has no route in our record with D4 off: our record has it outside D4 (P_OUTSIDE, guide.py:222), wires over D4's top edge, which needs D4 on | 258/35/-145 | Step 32: ~186/35/-135; Step 30: ~324/35/-135 (8 deg) |
| 10 | both D9 up 54; 2 arrows | D9_A, D9_B | 29 | yes once the matrix is no longer over the box (held at P_HELD it is in their way: matrix bottom y ~949.7, D9 top 900.7 + 65 = 965.7). The wires lie under D9_A's engraved end (open at the bottom: the build lowered it over them), so D9_A lifts off over them | 258/46/-133 | Step 29: ~324/35/-135 (11 deg) |
| 11 - 13 | wires out of the breadboard one per step, white i2, purple b19, grey i3 (eye only, no arrow; routed wire swapped for one dangling from the matrix) | J_WHITE_M, J_PURPLE_M, J_GREY_M | 11, 13, 12 | pins come up 30 (build hover) clear of everything once D6 / D9 / matrix are off; but see section 4: unplug() would put each lead back on the route drawn for the matrix upright over the breadboard | 258/49/122 | Steps 11/12: ~108/39/-155; 13: ~96/35/-45 |
| 14 | isolated: matrix + D10 + loose wires; D10 unclipped downward 48 mm; arrow down, eye on D10 | D10 | 31 | ours hooked D10 on with the matrix held over the box: up under it 22, then slid 40 along -Z (guide.py:751 - 760); reversed: +Z 40 then down 22 | 221/36/-140 | Step 31: ~179/29/-128 (12 deg) |
| 15 | isolated: the 3-wire cable (3 wires, 6 plugs) pulled off the header in one pull, 30.5 mm; fat arrow, eye on the connector | J_WHITE_F, J_PURPLE_F, J_GREY_F (+ wires) | 15 + 16 + 17 | ours has three separate sockets (one per pin, one per step in the build), pulled off along the pin axis, +Z 15 in the matrix's frame (SOCKET_OFF, guide.py:224) | 162/24/-60 | Steps 15 - 17: ~135/27/-156 (matrix upright then, not comparable) |
| 16 | D3 straight out -Z 38; arrow at its bottom tab, large inset of D3's face with a red box on the bottom tab | D3 | 27 | with D4 already off (published order): straight -Z works (D1's tabs and D9's ends run along Z). With D4 on (our build reversed): D3's end tabs are hooked in D4's slots, so it must swing open 22 deg about the hinge at D4 and then slide out along its tilted length: the build's two stages reversed (guide.py:708 - 714). D5 must be off first (D3's other end tabs are in D5's slots) | 258/31/-124 | Step 27: ~333/-35/-135 FLIPPED (67 deg) |
| 17 | D2 with the button off, both button wires unplugged, in one step (no Transition: swap to D2 standing clear, wires straight); 1 arrow 86.5 mm, 2 eyes on the plugs, large inset of D2's outer face, red box on its bottom tab | D2 (+ BUTTON, NUT ride on it), BTN_RED_PIN (j5), BTN_BLACK_PIN (j16) | 24 + 21 + 22 | D2's end tabs pass through D4's and D5's slots (D2 x 590.58 - 685.89), so D2 comes off only after both; then +Z 57.11 (the build's way reversed) slides it off D1's tabs (D1 reaches z 1258.61, 3.7 mm past D2's outer face: D1's tabs through D2's slots, round4/review_B.md:88). The leads were plugged in with D2 standing out at D2_OUT (guide.py:559, 585 - 590), so lifting D2 out first and unplugging after matches the build's routes exactly | 300/51/-133 | Step 24: ~353/35/-135 (16 deg); 21: ~113/35/135; 22: ~100/44/115 |
| 18 | isolated D2 + button: nut unscrewed 85 mm along the axis, turning; fat arrow, eye on the nut | NUT | 20 | yes (alone); the nut is on D2's inner face (-Z side) and comes off over the leads | 189/42/-137 | Step 20: ~196/35/135 (66 deg; both from inside D2) |
| 19 | isolated: button + wires pushed out of D2, 95 mm; arrow from the cap, eye on the button; camera to the outer face | BUTTON (+ pins once unplugged) | 19 | yes: +Z 100 (the reverse of Step 19, guide.py:550), leads following through the hole | 221/48/-54 | Step 19: ~305/35/45 (70 deg) |
| 20 | USB cable unplugged; arrow 63 mm, eye on the right-angle plug; cable just fades (no motion: glitch) | USB_B, USB_A, wire 'usb cable' | 23 | only after D2 is out: with D2 (and the button) seated, the plug's way out +Z 25 runs into the back of the button after about 9 mm (USB_B x 619.3 - 643.3, y 873.6 - 881.1, z to 1224.46; BUTTON x 629.8 - 646.7, y 873.2 - 890.1, back at z 1233.65). Also the plug's leg overlaps the purple pin in b19 by 0.3 mm (README Q2), so the jumper pins are best out before it | 300/48/-28 | Step 23: ~353/35/-135 (75 deg) |
| 21 | 330 Ohm up 30 | R330 (legs '330 leg 1/2' go with it) | 9 | yes | 189/32/-137 | Step 9: ~85/35/-135 (3 deg) |
| 22 | capacitor up 29 | CAP | 7 | yes | 189/41/61 | Step 7: ~79/35/35 (21 deg) |
| 23 | 12 kOhm up 31.5 | R12K (legs go with it) | 5 | yes; and before the Nano: R12K's box overlaps the Nano's (x 645.1 - 646.3, y 874.7 - 879.6, z 1183.8 - 1194.8) | 189/41/61 | Step 5: ~85/35/135 (57 deg) |
| 24 | Nano up 31 | NANO | 3 | yes, last | 189/41/61 | Step 3: ~141/35/-135 (103 deg) |
| end | breadboard on D1 only | BREADBOARD, D1 | (1, 2 stay) | | 189/49/38 | generator's own, closer in |

Build steps of ours with no counterpart in a take-apart: 1 (backing), 2 (breadboard on D1: stays), 4 and 8 (bending legs), 6 and 14
(the capacitor's and the matrix's look-steps), 10 (ribbon split), 18 (nut off a new button), 26 (matrix carried over D4: has none
if the wires come off before the walls, section 5), 36 (absorbed as the first stage of the D11 removal), 39 + 40 merged.

Our build's ways in that the generator will read (steps.json 'moving' records): BREADBOARD, NANO, R12K, CAP, R330 and the three
J_*_M pins straight up; BUTTON (18, 19, 20); NUT (20, with BUTTON); BTN_RED_PIN (21), BTN_BLACK_PIN (22); USB_B (23); D2 (24); D4
(25, and again 26, 30, 31 with stay-put paths, as the host of the matrix's ride); D3 (27); D5 (28); D9_A + D9_B (29); MATRIX (32 only,
[P_HELD, via P_HALF, 0]); D6 (33); D7 (37); D8 (38); STEM_01 (39); the other 63 (40). Never 'moving' (they rode): D10, the three
J_*_F sockets, the four D11, USB_A. At the end of the build (Completed View 'carry'): BUTTON and NUT ride on D2; D10 and the three
sockets on MATRIX; D11_A - D11_D on D1 (all at pose 0). MATRIX itself is not riding at the end.

## 3. What blocks what in our model (boxes from assembly-report.json)

- The walls are held by D1's tabs through closed slots in each wall (D1: x 593.78 - 682.68, z 1150.0 - 1258.61, i.e. through D4 by
  0.6, D5 by 0.2, D3 by 3.7, D2 by 3.7 mm) and by D2's and D3's end tabs through D4 and D5 (D2 / D3 x 590.58 - 685.89). So D4 and D5
  (sliding along X) must come off before D2 and D3 can move along Z; D3 can also come off by its hinge (swing, then slide out of
  D4's slots) with D4 still on, once D5 is off. D10's end tabs sit in open-topped slots in D4 and D5 (D10 x 594.01 - 682.91), D9's
  in notches in D2 and D3 (D9 z 1153.68 - 1254.93): both run along the wall's normal, so they do not stop a wall sliding off.
- D4's own way in (guide.py:632): down from above, then +8 X over the tabs of D1 and D2 (closed slots). Reversed: -8 X (its inner
  face then at 589.4, clear of D2's / D3's end tabs at 590.58 and D10 at 594.01), then up 65 over the USB cable in its open notch.
- D6 (y 900.98 - 903.98) is over the matrix (top 898.1) and D10 (top 900.68): D6 before the matrix. The D11 posts run through D6's
  corner slots: the D11s before D6. D7, D8 are on the posts: before the D11s. The stems run through D8, D7, D6: first.
- The matrix held at P_HELD (over the box) is in the D9s' way up: the D9s come out once the matrix has gone outside D4 (as the
  build put them in, Step 29, with the matrix outside) or away.
- USB_B's way out (+Z 25) is blocked by the seated button: D2 out first (the build plugged the USB in with D2 57 mm out).
- R12K over the edge of the Nano: R12K first. The purple pin and the USB plug's leg overlap 0.3 mm (the build plugs the USB in
  through the pin; no worse in reverse, and the generator will not warn since the build had the same).
- The three jumper wires: from i2 / i3 (x ~650, z 1170 - 1174) along -X at y ~885 under D9_A's engraved end (open-bottomed), along
  the floor beside D4, up at the D2 end into D10's slot and back under the matrix to the sockets on the header (guide.py:645 - 656,
  762 - 766). The purple runs from b19 under D9_A's lower edge (0.1 mm clear). Held over the box (P_HELD), the wires go up from the
  floor at the D2 end, over D2's top (loop at z 1256 - 1259, y 942 - 951) and back along under the matrix's edge (guide.py:735 - 742).
  Outside D4 (P_OUTSIDE), they go up at the D2 end and over D4's top edge (guide.py:662 - 676).
- Visibility of the breadboard pins from the usual DIAG (D4/D3 corner, el 35): i2 / i3 are hidden behind D3's top edge (a sight line
  from x 650, z 1171.7 rises only about 15 mm before reaching D3's inner face, which stands 27 mm above the pins); b19 is behind D9_A
  while the D9s are in, and once they are out its sight line just clears D4's top (909 against 907).
  From above (Step 26's camera, el 85) all three show. The sockets are on the header on the matrix's underside: hidden from above
  wherever the matrix lies LEDs up (held, outside D4, beside the base).

## 4. Generator behaviour that will misfire on this kit (stepgen.py)

- remove(D4): came[D4] has four records (Steps 25, 26, 30, 31) and the generator takes the last that fits (stepgen.py:1000 - 1004),
  Step 31's stay-put way: D4 would not move, and Step 31's camera would be used. Give the way by hand (path=[[-8, 0, 0], [-8, 65, 0]])
  and Step 25's camera (BASE_CAMERA, guide.py:615: DIAG, [630, 880, 1228], 125).
- BUTTON: last record Step 20 (stay-put TWO_BEATS): would not move. Hand path +Z 100 (reverse of Step 19), D2 then at D2_OUT, so the
  absolute pose is [0, 0, 57.11 + 100]; camera by hand (Step 19's or 20's, shifted by D2_OUT, as the MRA's camera_of(step, moved)).
- NUT: rides on D2; its only record (Step 20) was with BUTTON, which stays, so it does not fit: lifted straight up with a review note
  (stepgen.py:1030). Hand path: the reverse of NUT_ON (guide.py:552), i.e. nut_turns(0, -60, -1) composed with D2_OUT (two turns,
  unscrewing clockwise seen from the head, as Lee asked for Step 18, 19 Oct). With in_turn=[[NUT], [BUTTON]] in one step the nut's
  record fits, but the button still needs its hand path.
- D11_A - D11_D ride on D1 and never 'moved': lifted straight up "unchecked" with a review note. Give paths={i: [[0, 6.38, 0],
  [0, 85, 0]]} (the two stages: tabs out of D1, then up through D6; Step 36 and Steps 34 / 35 reversed). An arrow each (two of a kind
  that do not touch); four in one step logs the "more than 2 arrows" NOTE (stepgen.py:1134), as the MRA's six base screws did.
- D10 and the three sockets ride on MATRIX and never 'moved': hand paths. D10 from P_HELD: [[-0.2, 56.64, 39.68], [-0.2, 34.64,
  39.68]] (slide +Z 40, then down 22: Step 31's record, offsets D10 [-0.2, 34.6, 39.7] and via [0, 0, 40]). Sockets: +15 Z in the
  matrix's frame (compose(matrix pose, [0, 0, 15], socket centre)).
- lift() does not put leads back on earlier routes by itself (only unplug() does, stepgen.py:1090 - 1094): lifting the matrix needs
  wires= and wire_via= from the build's record, as the MRA's walked_back() does. Step 32 hover wires = HELD (routes 59 - 61), 32c
  wire_via = HALF (62 - 64); Step 30 hover wires = OUTSIDE (53 - 55), 30c wire_via = LIFT (56 - 58), 30c carry MATRIX via [P_LIFT].
  Step 26's record (BESIDE 33 - 35; via P_UP_BESIDE, P_MID, P_UP_OUTSIDE; wire_via 44 - 52) exists too, if the matrix is ever carried
  back over D4.
- unplug() of the jumper pins puts each wire back on its route before Steps 11 - 13: drawn with the matrix upright over the
  breadboard and the sockets 15 mm off its pins (f_pose(P_UP, SOCKET_OFF), guide.py:436 - 443). Wrong anywhere else. Either take each
  wire off whole (both ends in one step: no route needed, the leads go with their ends) or draw dangling routes by hand.
- unplug() of BTN_RED_PIN / BTN_BLACK_PIN is right as it stands once D2 is at D2_OUT: the routes before Steps 21 / 22 are
  hand_lead(c, D2_OUT), and the pins then ride on BUTTON (their 'rode' in Steps 20c / 21c). Unplugged with D2 seated, the routes would
  be 57 mm off.
- Cameras copied from flipped build steps: D5 (Step 28), D3 (Step 27). The decon would turn the box upside down for them unless a
  view_dir is given. Upright versions from the same corners match the published: D5 [0.5792, 0.5736, -0.5792] (az 135 el 35; published
  37/139), D3 DIAG [-0.5792, 0.5736, -0.5792] (published 31/-124).
- Stems: two build records (STEM_01 alone in 39, 63 in 40) make two arrows; units=[STEMS] gives one, on the stem nearest the middle.
- Close-ups on a take-off step keep only target, dir, radius, hide, mark, alt, caption and arrows (stepgen.py:1778): no `marks`
  (several red boxes), `ghost`, `side` or `image`. One red box (mark=half-width) per close-up; a see-through D1 would need a stepgen
  change. Build Step 36c's close-up of a D11 tab through D1 (target [674.83, 857.0, 1166.2], dir [0.4109, -0.8401, 0.3541], radius 6)
  works as it is, from below, with mark= added.
- USB_A was never moved in the build: give it a path (lifted with the plug), units=[[USB_B]] for one arrow on the plug, as the MRA
  (deconstruction.py, 'Unplug the power cable') and RCC (arrow_style at= clear of the cable) do.

## 5. Where ours should differ from the published one, and why

House rules (rulebook section 11, CLAUDE.md "A deconstruction guide"): the build in reverse as a rule; groups where Lee says; one
arrow per unit (smaller: 15 - 40 mm, never at the camera); eyes on plugs, several ends an eye each; hidden part: close-up from the
other side; leads unplugged before the structure round them; wired modules lifted off still wired, unplugged after; sub-assemblies
taken apart on their own (alone=), then back; two steps on one sub-assembly keep one camera; every step its own words; once off,
gone; ends on the base; title page and card the Full Build's; (MRA) the Full Build's parts list after the Completed View.

1. Wall order. The published takes D5 and D4 off early (its Steps 4 - 5, before the posts). Physically fine in our model, but our
   build lays the matrix outside D4 with its wires over D4's top edge (Steps 26 - 29), the only "laid aside" place with routes in our
   record while the walls stand. Keep the build's reverse: D5, D3 (unhook: swing and slide), D4, D2, after the matrix and its wires.
   The published's straight pull of D3 is possible only because its D4 is already off.
2. The matrix. Published: lifted off with D10, laid on the table still wired (two model swaps), D9s, wires out of the breadboard one
   by one, then on its own D10 off and the cable off. Ours (build reversed): lifted out with D10 to P_HELD (Step 32 reversed, wires
   HELD via HALF), D10 slid off and dropped over the box (31 reversed, as the build hooked it on there), the matrix laid outside D4
   (30 reversed: via P_LIFT to P_OUTSIDE, wires LIFT then OUTSIDE), then the two D9s (29). That uses only routes already in the record.
3. The three breadboard wires (Lee's group): one step, both ends, like the MRA's eight breadboard wires (remove(all six caps,
   arrows=[], eye=[...]): the leads go with their ends). Natural place: with the matrix outside D4 and the D9s out, from above
   (Step 26's camera, view_dir [0, 0.996, 0.088], frame ([638.5, 880, 1205], 82), where the pins in i2, i3, b19 show); eyes on the
   i2 / i3 pair, on b19, and on the header, with the header (under the matrix) in a close-up from below (target about the purple
   socket at P_OUTSIDE, [520.0, 900.2, 1212.4]). The published unplugs at the breadboard one per step (11 - 13, in neither build order
   nor its reverse) and pulls a single 3-way connector off the header later; ours has three separate sockets. Then the bare matrix
   goes in a step of its own (direction by hand: it is not in its seat). Option for Lee: the build's hole labels (i2, i3, b19)
   instead of eyes, as the MRA's row labels on its servo unplugs (Lee, 19 Oct 2026); the published shows no labels.
   Alternative: take the wires off with the matrix still held over the box (no walk back of Step 30), but there b19 is under the
   matrix, i2 / i3 at its edge and the header underneath: two close-ups would be needed.
4. The button panel. Published merges D2 off with unplugging both leads (one step, then a swap). Ours: D2 lifted out still wired
   (24 reversed, to D2_OUT, BASE_CAMERA), then the USB cable (23: now clear of the button), then both leads unplugged in one step (22 +
   21: Lee's "wires that went on one at a time may come off together"), eyes on both pins; then D2 + button on their own: the nut off
   (turning, 20 reversed), the button out (+Z 100, 19 reversed). The published's order of USB after the button block also works; ours
   is the strict reverse (USB before the leads). The nut and the button could go in one step in turn (the MRA's "screw, then its
   part"), but the nut is on the inner face and the button leaves by the outer face: one camera would have to see both; or keep two
   steps with one camera (Lee's rule for a run in the hand) or two (the published and our build use two sides).
5. The D11 posts: published two pairs (D4 end first, then D5 end: its build's order reversed). Ours: all four at once (one camera,
   four arrows) or the pairs in our build's reverse (C + D from Step 35's side, then A + B from Step 34's), each a two-stage pull. The
   catch to release is the tab through D1: a close-up from below with one red box (published: an eye on a foot and an inset of the
   lock slot from the side, possible there only because D4 / D5 were off).
6. Latches worth a close-up (published habit, rulebook "a latch or tab that must be released"): D8 under the D11 top latches (pub
   Step 2); D7 on the post notches (pub Step 3); the D11 tabs through D1; D3's latches (Lee's new D3 has spring cuts, README). No eye on
   a plate that simply lifts (in-house eyes are for plugs and for arrows that would point at the camera).
7. Cameras: reuse the build step's (the published reuses five build poses bit for bit) except the flipped ones (D5, D3; the D11 home
   step is not a removal of its own), the isolated button steps (the button is then 57 mm out with D2), and D4 (see section 4). Ours
   are closer than the published throughout (Lee's punch-ins); the published never goes below 24 deg of elevation.
8. Small parts: R330, CAP, R12K, Nano one per step, as both guides (exact reverse of the build). Grouping the two resistors and the
   capacitor in one step is possible (all straight up) but neither guide does it: Lee's call.
9. D8 and D7: one per step (published and build); they could go in one step in turn, but each has its own catch.

## 6. What the published does with the USB cable, the button panel and the matrix

- USB cable: its Step 20, after the button block and before the small parts, from the Full Build Step 20 camera (300/48/-28): one
  63 mm arrow at the plug and an eye on the right-angle Mini-B plug; Next fades the whole cable (no Transition, no motion, though the
  arrow says pull). Ours: +Z 25 slide of the plug then fade, A end lifted with it, one arrow on the plug (RCC rule: on the plug pulled,
  clear of the cable, none on the far end). Our title page (and so the decon's Start) hides the USB cable (guide.py:103); the
  published decon's Start shows it.
- Button panel: Step 17 takes D2 off (one arrow 86.5 mm), unplugs both leads (two eyes) and shows a large close-up of D2's outer face
  with its bottom tab boxed, then swaps to D2 + button standing clear with the leads straight. Steps 18 - 19 on their own: the nut
  turned off 85 mm along the axis (seen from inside D2), the button pushed out of D2 95 mm (seen from the outer face). Then back to the
  main model.
- LED matrix: Step 9 lifts it with D10 off the D9s (two swaps: hovering, then lying beside the box, still wired; the matrix is not
  drawn at all before this step); Step 10 the D9s; Steps 11 - 13 its three wires out of the breadboard (dangling from it); Steps
  14 - 15 on their own: D10 dropped off downward, then the 3-wire cable pulled off the header in one pull. The matrix itself is never
  removed (the guide ends on the breadboard).

## 7. Published glitches not to copy (its section 5)

Typo "Transiton"; D5's step with no visible slide (offset applied as it fades); the four D11 hidden at Step 4c and back at 5; D3
invisible from Step 1 to 9c while the eyes of Steps 4 - 5 point at its empty corner; the matrix not drawn until it pops in hovering;
a framed eye icon (Step 4); a clipped close-up frame (Step 16); Step 9 reusing Step 8's arrow (starting above the supports, not on the
matrix); arrows of uneven size and weight; the USB arrow with no motion; the wires unplugged in neither build order nor reverse;
leftover hidden lead lines, labels and a hidden "Step 51"; the breadboard backing ("Paper") shown under the breadboard and parts of
the Nano toggling. Ours avoids these by construction (every part on screen until removed; BACKING is put away at build Step 1,
guide.py:286, and is not in the Completed View), but watch close-up sizes in narrow windows and arrow sizes (15 - 40 mm).

## 8. A sketch of the order this points to (for the planner; 23 steps, 24 with the posts in pairs)

1 all 64 stems (40 + 39; units=[STEMS]) - 2 D8 (38; close-up of a D11 top latch) - 3 D7 (37) - 4 the four D11 (36 + 35 + 34; two
stages; close-up from below of a tab through D1) - 5 D6 (33) - 6 lift the matrix with D10 out of the box, still wired (32) - 7 D10
off the matrix (31; hand path, Step 31's camera, arrow by hand on D10's face outside the matrix as the build's had to be) - 8 lay the
matrix outside D4 (30 walked back) - 9 both D9 (29) - 10 the three breadboard wires, both ends (17 - 15, 13 - 11; Lee's group) - 11
the LED matrix away - 12 D5 (28, upright) - 13 D3 (27, swing and slide, upright; close-up of its latch) - 14 D4 (25, by hand) - 15 D2
with the button, lifted out still wired (24) - 16 the USB cable (23) - 17 both button leads unplugged (22 + 21) - 18 (D2 alone) the
nut (20) - 19 (D2 alone) the button out of D2 (19) - 20 R330 (9) - 21 CAP (7) - 22 R12K (5) - 23 Nano (3). Ends on the breadboard on
D1 (2, 1 stay), as the published.

## 9. Questions for Lee this raises

1. The three breadboard wires: off both ends in one step (as the MRA's eight), with the matrix laid outside D4? Eyes, or the build's
   hole labels (i2, i3, b19), as the MRA's row labels?
2. The D11 posts: all four in one step, or in the published pairs?
3. The walls after the matrix (our build reversed) rather than D5 / D4 first (published)?
4. The Full Build's parts list after the Completed View, as the MRA's?
5. Other groups: the two resistors and the capacitor together? D8 and D7 together? The nut and the button in one step?
