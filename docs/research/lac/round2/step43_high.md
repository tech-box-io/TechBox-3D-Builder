# LAC Step 43: the buzzer carried high, its leads keeping their over/under order (design "high")

Lee, 21 Oct 2026, his second note on Step 43: "Pass the red and black wires over the black/green/purple/blue wires instead of clipping
through and under them." The seated leads already pass over the jumpers and the lowering was already clean. The carry beat was not:
`motioncheck --moments 39 "Step 43c"` on the guide as it stood listed 14 problems, and 16 at 199 moments.

This was a scratch study. Nothing in the kit was changed or regenerated. The scripts and outputs are in
`docs/research/lac/scripts/round2/step43_high/`. All numbers are assembly mm, Y up. "Crosses over/under" means in plan (x-z), with the
lead above or below the other wire there.

## 1. Result

| | the guide now | this design |
|---|---|---|
| Step 43c, 39 moments | 14 problems | **1** (black and the LCD teal wire, 0.70 mm centre to centre at 0.45) |
| Step 43c, 199 moments | 16 problems | **4**: black through the LCD's purple, yellow, teal and blue wires, once, at 0.44 - 0.46 |
| red lead, Step 43c, any moments | through the green, black, purple, blue, orange and yellow jumpers and the switch's tan lead | **nothing** |
| black lead, besides the four LCD wires | through the purple, green and black jumpers, the switch's tan lead and the potentiometer's tan lead | **nothing** |
| Steps 44c - 56c (39 moments) | 16 problems, none with a buzzer lead | the same 16, none with a buzzer lead |
| buzzer (the part) against other parts along its way | touches the F7s only in their slots at the end | the same |

The four LCD contacts are **forced**. As long as the LCD's wires stay laid as they are, no motion of the buzzer can avoid them
(section 2). The same reasoning showed that two more contacts were forced by the old seated red lead, which ran under the orange jumper
and under the switch's lying tan lead. The design therefore changes the red lead's seated way (section 3). Lee's
black/green/purple/blue jumpers are passed over, never through, in every view and at every moment.

## 2. Which contacts no carry can avoid

Take one buzzer lead L and another wire W, both seen in plan. Count the places where L passes **under** W, each with its sign (the
orientation of the crossing). Without the two wires passing through each other, that count changes in only three ways:

* L's free end (the buzzer) passes **under** W. A carry over the field never does this.
* W's end can be passed under. That happens at W's free end, or where W runs directly over L's own hole: the yellow jumper's centre
  line passes 0.21 mm from j4, 8 mm up. This is how red can turn under the yellow at j4.
* W's own end moves over L. This is the switch in Step 47, carried over the case on F4. Each switch lead's exit moves along z ~1258.3,
  from x 590 - 604 to x 672.5 (red), 679.5 (tan) and 686.5 (black). It passes over every buzzer lead that crosses that line further
  back (smaller x).

Comparing the counts before Step 43 (Step 42c) and after it (and after Steps 47 - 48) gives:

| pair | lying (Steps 33 - 42) | seated (old) | can it change in Step 43? | so |
|---|---|---|---|---|
| red / orange jumper | no crossing | under, at z 1318.9 (by 7.1) | no: the orange passes 4.3 mm from j4, not over it | **forced** by the old seat |
| red / yellow jumper | under at j4 only | under at j4 | yes, at j4 | free in principle. With the old seat, though, red's rise had to cross the yellow's line, which also touches |
| red / switch tan (lying) | no crossing | under, at z 1270 (8.9) | no: the buzzer goes over it | **forced** by the old seat. Red cannot simply go over the lying tan instead: in Step 47 the tan's exit passes over red at x 674.5, and the seated tan does not cross red, so red would have to be *under* the lying tan for Step 47 to be clean |
| black / LCD purple, yellow, teal, blue | under all four, at (684.5, 1358.7), 33 - 40 below | not under any | no: their ends are the holes and the LCD lying on the table, and none passes over (-) blue | **forced** |

How the LCD wires trap black: in Steps 36 - 39 they are laid in a C round (-) blue. Each goes from its hole back (-x) to x 677 - 688,
along to z ~1360 and forward to the LCD's header, and the loops pass 32 - 40 mm over the black lead lying under them. The seated black
lead leaves the C over the purple wire's end at the rail, which is the same as not crossing it at all. To get from one to the other the
black lead must pass through all four wires. The C is still there in the final shapes (Step 51c), so keeping black under the LCD wires
until the LCD moves (Steps 50 - 51) does not help. The LCD's header moves away from the black lead rather than over it, and the
contact only moves to Step 50 or 51.

**What would clear the black lead (outside the buzzer's own shapes):**

* Lay the LCD wires (Steps 35 - 51) so that they do not enclose (-) blue, for example forward of it, along the front. Then this design
  is clean with no other change.
* Or lay the black lead in Steps 34 - 42 over the LCD's loops. That makes a 45 mm arch over empty space in Lee's Step 33 - 34 camera.
  I would not recommend it.

## 3. The design

**Stops.** The path is `[BUZZER_LYING, BUZZER_LIFT, BUZZER_HIGH, ZERO]`, three beats as now. BUZZER_HIGH = [0, 75, 0] (75 mm over the
seat; was BUZZER_UP, 45 mm). The buzzer is carried over the spread F7s' tops (y 956.2) with its stub ends at y 969, then lowered
straight in. `partpath.py`: along the way it comes within 3 mm of no part except the F7s, and those only in their slots at the end.

**Red, seated (changed: BUZZER_SEAT_WAY['red']).** In order from j4:

* It comes into j4 from behind (-x), as it lies before the step, so it is under the yellow jumper's arch only at the hole.
* It climbs behind the j-side caps and crosses over the yellow (8.0) and orange (5.8) jumpers just past the clock module's end
  (z ~1300, 2.4 mm from the module).
* It passes over the row-i ends of the purple (11.8) and blue (12.5) jumpers.
* It passes over the black (4.9) and green (2.6) jumpers' arches.
* It passes over the switch's tan lead by the (+) red rail: over the lying tan (11.8), the tan lifted with F4 (Step 47, 4.9) and the
  seated tan (7.1).
* It comes down in front of the switch, at x 688 where the switch's leads pass z 1258.3, ahead of the switch black lead's exit at
  x 686.5. It passes round F7B's end to the stub.

Red crosses nothing under in any view from Step 43c on (`cross.py`). It is 158 mm long (was 130). The stub end is unchanged: 1 mm
straight on, then round under the stub.

**Black, seated:** the same way as now.

**Carried high (BUZZER_HIGH, new: `buzzer_high`).**

* Red: the seated way from j4 to BUZZER_KEEP (661.6, 923.8, 1303), behind the caps. From there it rises to 945 at (661.0, 1304.2) and
  arches over the board at y 948 - 960 to the buzzer.
* Black: straight up out of (-) blue to 945, through the open space between the potentiometer's leads and the LCD's loops. From there
  it runs along the front at y 950 - 960 to the buzzer.

**Lifted (BUZZER_LIFT):**

* Black: as now.
* Red: its run behind the board's end stays at y 906.5 - 908 for its first 32 mm and only then rises. That run does not follow the
  buzzer (`hold=32`). Its last controls are moved 3.5 mm back, so that it leaves j4 further from the j3 cap. At the lifted stop it is
  0.97 mm from the yellow jumper. The guide's lifted shape now passes 0.23 mm into it.

**How each beat is kept clean:**

* LYING to LIFT: as now (stretch).
* LIFT to HIGH: stretch. Red's low run swings round behind the j-side caps, under the yellow's arch at j4, to the riser behind the
  caps. Black rises out of the LCD's loops; this is the forced pass.
* HIGH to ZERO: `tail_from` is the same in both shapes: the run kept (red, 43.7 mm to BUZZER_KEEP) and black's 9 mm drop. That run stays
  put. Each riser folds down onto it, and the rest settles from above onto its seated way while the seated way is carried down with
  the buzzer: the seated route's `b_from` is now the same 43.7 / 9.0, so the whole lead after it follows the buzzer down by the
  player's ramp.

## 4. Paste-ready code for guide.py

Replace everything from the comment `# Each lead's way to its hole, the buzzer lying (Steps 33 - 42) and lifted 60 mm` down to the end
of `buzzer_clamped` (its `return W.route(line, a=cap, b=BUZZER, b_from=k, tail_from=k)`) with `step43_high/guide_patch.txt`. In that
file:

* BUZZER_WAY and black's BUZZER_LIFT_WAY are copied verbatim from the guide.
* BUZZER_UP, BUZZER_UP_WAY, BUZZER_J_Z and buzzer_over_seat are gone; nothing else uses them.
* The lying shapes (Steps 33 - 42) come out identical to the routes in steps.json (checked).

Replace the Step 43 comment line and `g.place('Lower the buzzer ...` call with `step43_high/guide_patch_step43.txt`. `build_final.py`
runs the patch with guide.py's own helpers and reproduces the checked routes exactly.

## 5. Checks (on `steps-final.json`, the steps copy the patch gives)

`motioncheck --moments 39 "Step 43c"`:

    Step 43c  buzzer black  and lcd teal      centre lines 0.70 mm apart at 0.45, near [682.1, 930.3, 1349.8]
    checked 1 views in motion; 1 problems

`--moments 199`: black and the LCD yellow 0.31, teal 0.53, blue 0.62 and purple 0.76 mm, at 0.44 - 0.46 (`mc43_199.txt`). There is
nothing else, and nothing with a part.

`motioncheck --moments 39 "Step 44c" ... "Step 56c"`: 16 problems, all of them the potentiometer's leads in 46c and 52c, as on the
current guide (`mc44_56.txt`). None involves a buzzer lead.

**At rest, every view from Step 43c to the Completed View** (`static.py`, as wirecheck samples: surface gaps, mm):

* Red:
  * black lead at the stubs 0.47 (they leave the buzzer 1.52 apart; 0.54 before)
  * green jumper 0.78
  * seated tan 0.99 (48c on)
  * j3 cap 1.60 and yellow 1.65 (at j4, unchanged)
  * black jumper 2.31
  * clock module 2.43
  * orange 3.66
  * switch black 4.83 (48c)
  * potentiometer tan 6.03 (52c)
  * switch 6.61 (48c)
* Black, unchanged:
  * potentiometer tan 0.41 (43c - 46)
  * green 0.72
  * LCD yellow 1.47
  * potentiometer red 2.07
  * switch tan 2.40 (47c)
  * F7B 2.91 (44c)

Nothing passes into a part. Steps 33 - 43: unchanged (lying shapes identical).

**The in-between shapes at their stops** (`stops.py`, parts as in Step 43c):

* LIFT:
  * red: black lead 0.24 by the buzzer (0.25 now), yellow 0.97 (now -0.23), j3 cap 0.99, USB cable 1.81
  * black: as now (red 0.24, LCD blue 6.69)
* HIGH:
  * red: black 0.77 by the buzzer, j3 cap 1.60, yellow 1.65, clock module 3.35, orange 3.66
  * black: red 0.79, potentiometer tan 5.66, LCD wires 11.5 and more

## 6. What it looks like (CASE_CAMERA, 3 beats)

1. **Lift.** The buzzer rises 60 mm straight up from where it lies past the breadboard's end. Red's lead stays low behind the board's
   end for its first few cm and rises to the buzzer. Black rises from under the LCD's wires toward it.
2. **Carry.** The buzzer swings over the board to 75 mm above its seat, turning upright.
   * Red's lead swings round behind the j-side caps. It rises behind them just past the clock module and arches high over the board to
     the buzzer.
   * Black's lead straightens up out of (-) blue and arches high along the front edge. On the way up it passes once through the
     LCD's four wires; this is the forced contact, at 0.44 - 0.46 of the motion, under 0.1 s of the step's 2.4 s.
3. **Lower.** The buzzer goes straight down into the F7s' slots. Each lead folds its rise down and settles from above onto its way.
   * Red ends over the yellow and orange jumpers, over the jumpers' row-i ends, and over the black and green jumpers' arches. It then
     comes over the switch's tan lead by the rail and down in front of the switch.
   * Black ends along the front rails as before.

Not viewed in the player. It has only been checked numerically, with the same blending the player uses (motioncheck), on a steps copy.

## 7. Notes

* The seated red lead is no longer "under the orange and yellow beside the Nano". That constraint was itself the cause of the forced
  contacts with the orange (and, in practice, the yellow). Red now goes over both, beside the clock module.
* Red now runs in front of the switch with black, about 2 - 5 mm from it, for z 1244 - 1275.
* If the LCD wires are re-laid as in section 2, rerun `build_final.py` and the motioncheck on Step 43c. The black lead's shapes need no
  change.
* The current guide's lifted red lead touches the yellow jumper at rest at its stop (-0.23). This design fixes that too.
