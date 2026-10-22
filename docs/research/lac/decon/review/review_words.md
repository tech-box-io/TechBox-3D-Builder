# LAC deconstruction, first draft: review of the words

21 Oct 2026. Lens: every caption, caution and pin label in `LAC Build Instructions/steps-deconstruction.json` against what the step
does (the strips in `pictures/`, the JSON: moving parts, paths, offsets, wires) and against the Full Build's own captions and names
(`steps.json`, `guide.py`); the README draft. Read-only: light Python on the two steps files, nothing run that loads the CAD.

## Checked and right

- **Every hole and colour.** All 20 wires (LCD 4, buzzer 2, potentiometer 3, switch 3, jumpers 8) and the RTC and both resistors:
  each caption's holes are the Full Build captions' holes for the step that plugged that part (Full Build Steps 3 - 39), and each
  step's eye anchor lies within 1 mm of the Full Build's label anchor for the hole it names (e.g. Step 18's eye [686.9, 899.8, 1325.1]
  on b8 [686.64, 897.11, 1324.256]; Step 35's [696.0, 900.4, 1269.4] on Step 17's (+) red [696.655, 897.11, 1269.675]). The ids each
  step removes are the ones the Full Build plugged (e.g. Step 16c takes `lcd purple`, NAUO82 / NAUO97, Full Build Step 36).
- **Pin labels** GND / VCC / SDA / SCL (Steps 16 - 19): the Full Build's labels of Steps 36 - 39, same anchors, header order
  GND, VCC, SDA, SCL; purple = GND, yellow = VCC, teal = SDA, blue = SCL as the Full Build.
- **Names**: "the potentiometer", "the rocker switch" / "the switch's ... wire", "the alarm buzzer", "the LCD screen", "the real time
  clock module", "12 kΩ resistor", "the Nano Board", "the USB cable's small end", "jumper wire" (M-M) against plain "wire" (M-F): all
  the Full Build's, lower case as it has them. Every caption is unique and none is a Full Build caption copied.
- Steps 1, 3, 4, 5, 9, 13, 15 - 26, 28 - 36, 38 - 43, 45, 46: wording matches what the strip shows.

## Findings (most important first)

### 1. Step 6 sends F1 the wrong way (medium)
- Caption: "Lay F1 face down in front of the case, toward the end where F6 was." (`deconstruction.py:168`)
- What it does: F1 stands at offset [76.7, 0.0, 1.1] (Step 5c) and is laid at t [135.97, -10.43, 14.63], turned about z (Step 6c):
  59 mm further out in front, and **13.5 mm toward F5**, not toward F6 (F6 is the -z end: Step 1's arrow tail z 1208.67, F5's
  1371.07). It is laid straight out in front of where it stood. The phrase is the Full Build's Step 47 ("along towards its other end"),
  which was relative to F1's earlier place by the breadboard's end; here F1 comes from standing in front of the case. From Step 6's
  camera the +x move draws to the right, where F6's end is, which hides the slip in the picture, but a student following the words
  lays F1 off towards the knob end.
- Fix: `g.lift('Lay F1 face down on the table, out in front of the case.', ...)`.

### 2. Step 12 does not say to keep F9 tipped while it comes out (medium)
- Caption: "Tip the top of F9 toward the front to lift its back foot out of F3. Then lift F9 up out of its front slot."
  (`deconstruction.py:194`)
- What it does: `path=[HOOKED, *TIPPED]`, the second pose "the same tilt, 33 mm higher" (line 191): F9 is lifted still tipped. The
  close-up (`step12_closeup.png`, red box) shows the front foot's hook under F3, and the Full Build hooks it in tipped (Step 45: "hook
  its front foot into its slot"). A student who straightens F9 before lifting catches the hook under F3; the words say "lift up", the
  close-up says "hook".
- Fix: "Tip the top of F9 toward the front to lift its back foot out of F3. Then, keeping it tipped, lift F9 to unhook its front foot
  from its slot."

### 3. Step 47 has no Pry Tool caution (medium: ask Lee)
- Caption: "Remove the Nano Board from the breadboard." No caution (`deconstruction.py:290`).
- The MRA (Step 55) and the LSM (Step 24) both carry "Use the Pry Tool to carefully remove the Nano Board." For the LSM Lee said "The
  kit does have a pry tool, although it's not shown" (`docs/research/lsm/lee_notes_2026-10-21.md:28`). Nothing in the LAC's files says
  whether its kit has one.
- Fix: if the LAC kit has the tool, `caution='Use the Pry Tool to carefully remove the Nano Board.'` on Step 47, word for word as the
  MRA's and LSM's. Add the question to the README (finding 10).

### 4. Step 14: "the case" is gone by now, and "past the end of the breadboard" does not say which end (low)
- Caption: "Lift the alarm buzzer out from between the two F7s and lay it beside the case, past the end of the breadboard. Leave its
  wires connected." (`deconstruction.py:204`)
- By Step 14 only F3 and the two F7s are left (F9 went at 12c): the Full Build says "beside the base" for this same spot (Steps 33,
  35). The buzzer starts beside one end of the breadboard (between the F7s, z about 1225) and is carried over the board to the other
  (Full Build Step 43's start, t z +176: about z 1401, past column 1 at z 1342, the Nano Board's USB end). "Past the end" reads as the
  end it is already at.
- Fix: "Lift the alarm buzzer out from between the two F7s, carry it over the breadboard, and lay it beside the base past the Nano
  Board's end. Leave its wires connected."

### 5. Step 11: "back" refers to the Full Build, and the end is not named (low)
- Caption: "Move F1, still face down, back in front of the end of the breadboard." (`deconstruction.py:188`)
- In this guide F1 has never lain there: "back" means "where the Full Build had it". The move is 85 mm along toward F5's end and
  57 mm in (Step 6c t [135.97, ., 14.63] to Step 11c [78.97, ., 99.63]). The step exists only to replay the Full Build's lead shapes
  (plan.md section 1); the words give the student no reason, so it at least needs to say plainly where.
- Fix: "Move F1, still face down, along to the end where F5 was, in front of the end of the breadboard."

### 6. Step 8: where the LCD screen is laid, and length (low)
- Caption: "Slide the LCD screen out of the slots in F8, bring it out through the front of the case, and lay it face down beside the
  case. Leave its wires connected." (31 words, three actions; `deconstruction.py:177`)
- It is laid (Full Build Step 51's start: t [-7.95, -38.61, 79.15]) at the F5 end, mostly past it, not alongside the case.
- Fix: "Slide the LCD screen out of the slots in F8 and out through the front of the case. Then, lay it face down past the end where F5
  was. Leave its wires connected."

### 7. Step 2: which end is "free" (low)
- Caption: "Swing the free end of F2 out from the case. Then slide F2 along to unhook it from F5, and pull it away, clear of the USB
  cable." (`deconstruction.py:152`). The free end is the one where F6 was (the slit end is still hooked in F5); the camera goes round
  to the back, which the Full Build announced ("Turn the case so its back faces you", its Step 56).
- Fix: "Turn the case so its back faces you. Swing the end of F2 where F6 was out from the case. Then, slide F2 along to unhook it from
  F5, and pull it away, clear of the USB cable."

### 8. The wire cautions (low)
- `PULL` ("Pull each wire out by its connector. Do not pull on the wires themselves.", line 147) is on Steps 16 and 32 only. The
  leads soldered to a part, which a student is most likely to yank (buzzer Step 21, potentiometer Step 24, switch Step 34), get none;
  the LSM puts its caution on each set's first step (12, 14, 17). On Step 16 the LCD wire's female end comes off a pin, not "out".
- Fix: Step 16's caution "Hold each wire by its black connectors to pull it off the pin and out of the breadboard. Do not pull on the
  wires themselves." (as the LSM's Step 14); `caution=PULL` also on Steps 21, 24 and 34 (or, if that is too many, on 24).

### 9. Small wording (low)
- Step 44: "out of row j, j19 to j24": the row is in the hole names. Fix: "Pull the real time clock module out of j19 to j24."
- Step 37: "Push the rocker switch up out of the square hole in F4." The Full Build pushes it in "until it clicks in"; if the switch is
  held by snap clips, the student has to squeeze them. Ask Lee; if so: "Squeeze the clips on the sides of the rocker switch, under F4,
  and push it up out of the square hole."
- Steps 2 and 12: "Then slide" / "Then lift": the MRA's and LSM's take-aparts write "Then," (comma), as the brief's house style.
- Steps 6, 7, 9, 12 say "toward"; the LAC Full Build says "towards" (10 times, none "toward"). One spelling per kit.

### 10. README draft (`review/readme_draft.txt`)
- **No questions for Lee, and a placeholder** (medium). Line 28 is still `Checked: CHECKED_LINE`. plan.md section 8 has ten questions
  (13 - 22) that the draft does not carry, and its question 13 says "The draft groups", which is no longer true: the draft is one wire
  per step (47), while Lee's instruction for the PMG and LSM the same day was groups. Fix: fill the Checked line after the checks;
  add the questions, 13 rewritten ("The draft is one wire per step, as published (47 steps); or in groups as the PMG's and LSM's
  (32)?"), plus the Pry Tool (finding 3) and the switch's clips (finding 9).
- **"each arrow the published one's size, one per stage, in turn (F9: the tip, then the lift)"** (line 5; also the
  `deconstruction.py` docstring, line 10) (low). Only F9 has an arrow per stage. F2 (Step 2), F4 (Step 10) and the buzzer (Step 14)
  have one arrow on one stage (`then=` is refused with `wire_via=`: plan.md question 20), and Step 15's F7s show only the up arrows.
  Fix: "each arrow the published one's size; an arrow per stage, in turn, for F9; one arrow where a lead changes shape on the way
  (F2, F4, the buzzer); the up arrows only for the F7s".
- **"Every step replays a state of the Full Build backwards"** (line 7) (low). From Step 4 to Step 15 the USB cable is out while the
  case is still on, which the Full Build never had (plan.md section 0: "the one new state"). Fix: "Every step after the USB cable's
  (Step 4, power first) replays ...".
