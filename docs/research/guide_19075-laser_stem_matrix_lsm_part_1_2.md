# Guide report: `19075-laser_stem_matrix_lsm_part_1_2` — Laser Stem Matrix (LSM) Part 1 + 2 (combined)

Sources read: `digest/19075-laser_stem_matrix_lsm_part_1_2.md` (all 47 steps), all 6 contact sheets, 30+ individual thumbs,
`digest/…_-_part_1.json`, `digest/…_-_part_2.json` (field-by-field diff against the combined guide), and targeted queries of
`cadasio_raw/` for annotation visibility, annotation style, LED-matrix visibility and project dates.
Step indices are the digest's `[NNN]`.

## 1. Summary

The guide takes the student from a bare breadboard to a wired electronics core in 21 numbered actions (47 viewer steps):
peel the breadboard backing, stick it on the wooden base "D1", press in the Arduino Nano, a 12k resistor, a capacitor and a
330 Ω resistor (Part 1 content, [001]–[016]); then split a 3-wire jumper ribbon and connect its male ends to I2 / I3 / B19 and
its female ends to the LED matrix V+ / IN / V−, mount the push button in side panel "D2" with its nut, plug its two wires into
J5 / J16, slide the panel onto the base and plug in the USB cable (Part 2 content, [017]–[046]). It is authored as strict
"Step N" (how, with annotations) / "Step Nc" (result, no annotations) pairs, with exactly one title page, two un-numbered
section cards ("LED Matrix Diagram", "Mini USB Cable"), one auto-advancing "Transition" and one "Completed Build" end view.
The combined guide is not a re-edit of the two parts: project dates show it is the original project (created 2025-07-17) and
Part 1 / Part 2 are copies of it made on 2025-08-22 and trimmed; it plays Part 1 [001]–[017] and Part 2 [001]–[030] back to
back with Part 1's "Completed View", Part 2's "Start" and Part 1's "Capacitor" card absent and Part 2's steps numbered 9–21.

Counts: 47 steps = 1 Start + 21 "Step N" + 21 "Step Nc" (one is spelled "Step 20C") + 2 section cards + 1 Transition +
1 Completed Build. 46 pause, 1 play. 45 steps animate in 800 ms, 2 in 1600 ms. Camera moves on 21 steps, stays put on 26.
Annotations that are actually switched on by step data: 16 label showings, 17 lead-line showings (one a leftover), 3 arrows,
18 image showings.

## 2. Step table (every viewer step)

Camera column: `rot` = view rotation on entering the step, then distance change; `[d el az]` = resulting distance (mm),
elevation and azimuth (degrees). "fixed" = camera identical to previous step. Offsets are mm; Y is up.

| idx | name | kind | what is added or done | annotations switched on | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Finished Part-2 model (25 parts) on the right half; nothing to do | TechBox logo SVG (w 33 %, at 2 %,4 %); title block PNG "Laser Stem Matrix (LSM) / Part 1 + 2 / © 2025 TechBox…" (w 45.7 %, at 2 %,63 %) | rot 9°, 15→351 [d351 el37 az50] |
| 001 | Step 1 | hover | "Peel off the adhesive backing": breadboard alone, pre-lifted 39.3 mm; grey backing sheet under it | 1 red block arrow 39.4 mm straight down from the breadboard underside; framed photo-style inset "Protective Backing" (w 18.7 %, at 68 %,14 %) with leader to the breadboard's bottom corner | rot 74°, 351→190 [d190 el26 az−40] |
| 002 | Step 1c | completed | Backing sheet drops 48.3 mm clear of the breadboard | none | fixed |
| 003 | Step 2 | hover | Base "D1" fades in at its final place below the still-hovering breadboard; backing sheet removed | 4 red lead lines 39.3–39.4 mm, vertical, breadboard bottom corners → the L-shaped cut-outs in the base | rot 12°, 190→190 [d190 el27 az−53] |
| 004 | Step 2c | completed | Breadboard descends 39.3 mm → seated | none | fixed |
| 005 | Step 3 | hover | Arduino Nano fades in 35–37 mm above its seat | 4 red lead lines 38.8–39.2 mm (3 solid, 1 "dashed"), Nano pin tips → breadboard holes; labels "Pin d12" (→ Nano pin, at 55 %,7 %) and "c16" (→ breadboard hole, at 56 %,29 %) | fixed (same view as Step 2) |
| 006 | Step 3c | completed | Nano descends 35.3 mm → seated ("Make Sure the Nano Board Touches the Breadboard") | none | fixed |
| 007 | Step 4 | hover (inspect) | Everything hidden; 12k resistor alone with straight leads, fills the frame | eye icon → resistor colour bands (w 8.7 %) | rot 91°, 190→75 [d75 el51 az78] |
| 008 | Step 4c | completed | Straight leads fade out, bent (staple-shaped) leads fade in; no travel | none | fixed |
| 009 | Step 5 | hover | Assembly fades back in; bent resistor hovers 36.8 mm above its holes | 2 red lead lines 41.4 mm ("dashed"), lead tips → holes; labels "h3" (68 %,20 %) and "h16" (33 %,21 %) → the holes | rot 12°, 75→163 [d163 el40 az74] |
| 010 | Step 5c | completed | Resistor descends 36.8 mm → seated | none | fixed |
| 011 | Step 6 | hover | Capacitor fades in ≈33 mm above J2/J3 (no card before it, see §5) | 2 red lead lines 27.2–27.3 mm (solid), leg tips → holes; labels "j2" (66 %,22 %), "j3" (43 %,16 %) → holes; eye icon → capacitor body/stripe (w 6.3 %) | rot 12°, 163→163 [d163 el43 az58] |
| 012 | Step 6c | completed | Capacitor travels 32.9 mm → seated | none | fixed |
| 013 | Step 7 | hover (inspect) | Everything hidden; 330 Ω resistor alone, straight leads | eye icon → colour bands (w 9.4 %) | rot 103°, 163→65 [d65 el33 az−104] |
| 014 | Step 7c | completed | Leads swapped to bent | none | fixed |
| 015 | Step 8 | hover | Assembly back; resistor hovers 31.4 mm above its holes | 2 red lead lines 35.8 mm ("dashed"); labels "a11" (36 %,27 %), "a19" (63 %,29 %) → holes | rot 29°, 65→163 [d163 el27 az−138] |
| 016 | Step 8c | completed | Resistor descends 31.4 mm → seated. (Last Part 1 step.) | none | fixed |
| 017 | Step 9 | hover (inspect) | Everything hidden; 3-wire jumper ribbon (white / purple / grey) alone, wires still joined. (First Part 2 step.) | 2 eye icons: → male pin end, → female socket end (w 7.6–7.8 %) | rot 66°, 163→103 [d103 el46 az−55] |
| 018 | Step 9c | completed | Joined ribbon swapped for "split" ribbon: the three connectors fanned apart at both ends | none | fixed |
| 019 | Step 10 | hover | Assembly back; split ribbon floats above the board | label "i2" (27 %,15 %) → male connector of the white wire | rot 66°, 103→163 [d163 el27 az−138] |
| 020 | Step 10c | completed | White wire's loose end swapped for a routed wire whose pin sits in I2 (appear + disappear, no travel) | none | fixed |
| 021 | Step 11 | hover | Nothing changes except the label | label "i3" (33 %,18 %) → male connector of the grey wire | fixed |
| 022 | Step 11c | completed | Grey wire swapped for routed version seated in I3 | none | fixed |
| 023 | Step 12 | hover | Nothing changes except the label | label "b19" (33 %,18 %) → male connector of the purple wire | fixed |
| 024 | Step 12c | completed | Purple wire swapped for routed version seated in B19 | none | fixed |
| 025 | LED Matrix Diagram | section card | All 3D parts hidden; flat picture of the back of the LED matrix (black square, 6 holes, two red-framed 3-pad groups, one captioned "V- Out V+") | 1 image (w 62.8 %, at 18 %,5 %), no leader. Saved render also shows 2 eye icons (see anomalies) | fixed |
| 026 | Step 13 | hover | Assembly back; LED matrix shown floating above the board (second, staged instance) | label "i2" (65 %,40 %) → the white wire's seated end; blue-filled round badge "V+" → matrix pin; white round badge "V+" → the wire's free female end (both w 7.8 %) | rot 81°, 163→190 [d190 el27 az129] |
| 027 | Step 13c | completed | White wire swapped for a version routed up to the matrix V+ pin | none | fixed |
| 028 | Step 14 | hover | Label/badges only | label "b19" (33 %,35 %); blue badge "V-In" → matrix pin; white badge "V-In" → purple wire's female end | rot 130°, 190→190 [d190 el20 az−32] |
| 029 | Step 14c | completed | Purple wire swapped for version routed to the IN pin | none | fixed |
| 030 | Step 15 | hover | Label/badges only | label "i3" (28 %,35 %); blue badge "V-" → matrix pin; white badge "V-" → grey wire's female end (w 5.9–6.1 %) | rot 105°, 190→163 [d163 el19 az−147] |
| 031 | Step 15c | completed | Grey wire swapped for version routed to the V− pin | none | fixed |
| 032 | Step 16 | hover (inspect) | Everything hidden; push button with its red/black pigtail and hex nut, alone | 1 red block arrow 63.4 mm along the wires (direction the nut comes off) | rot 82°, 163→163, target shift 118 mm [d163 el39 az−52] |
| 033 | Transition | transition (auto, 1600 ms) | Nut slides 98.8 mm off along the wires while rotating; arrow removed | none | fixed |
| 034 | Step 16c | completed | Nut fades out | none | fixed |
| 035 | Step 17 | hover | Side panel "D2" fades in; button sits 103 mm from the hole, on its axis | 1 red lead line 106.7 mm (solid), button body → centre of the panel hole | rot 3°, 163→221 [d221 el36 az−53] |
| 036 | Step 17c | completed | Button + pigtail travel 103.2 mm through the hole | none | fixed |
| 037 | Step 18 | hover | Camera swings to the inside face; nut fades in 82.6 mm behind the panel, beyond the wire tips | 1 red lead line 92.9 mm ("dashed") along the button axis, nut centre → button back | rot 118°, 221→163 [d163 el26 az134] |
| 038 | Step 18c | completed (1600 ms) | Nut travels 80.4 mm along the axis and rotates → tight against the panel | none | fixed |
| 039 | Step 19 | hover | Main assembly back, LED matrix now lying flat beside the base with long re-routed wires; panel+button sub-assembly hovers beside the board, pigtail straight | labels "j16" (31 %,24 %) → black wire's pin connector, "j5" (64 %,25 %) → red wire's pin connector | rot 14°, 163→258 [d258 el38 az143] |
| 040 | Step 19c | completed | Button swapped for routed-wire version: black wire in J16, red wire in J5 | none | fixed |
| 041 | Step 20 | hover | Nothing moves | 1 red block arrow 55.3 mm from the panel toward the base; eye icon → the slot in the panel (w 7.8 %); plus one stray 8.8 mm lead line inside the button (anomaly) | rot 64°, 258→258 [d258 el41 az−131] |
| 042 | Step 20C | completed | Panel, button and its two wires swapped for seated instances (panel slotted onto the base) | none | fixed |
| 043 | Mini USB Cable | section card | Everything hidden; USB cable alone, straight | eye icon → cable (w 7.8 %, at 19 %,16 %) | rot 93°, 258→190, shift 133 mm [d190 el46 az51] |
| 044 | Step 21 | hover | Assembly back, nothing new | eye icon → the Nano's USB socket (at 25 %,19 %) | rot 73°, 190→258 [d258 el36 az−53] |
| 045 | Step 21c | completed | USB cable fades in already plugged into the Nano and routed out past the panel | none | fixed |
| 046 | Completed Build | end view | Nothing changes; camera orbits to a three-quarter hero view | none | rot 70°, 258→221 [d221 el39 az40] |

## 3. Conventions found (with evidence and exceptions)

### 3.1 Structure
- **Always:** one title page first ([000]) and one end view last ([046]); every numbered action is a pair `Step N` → `Step Nc`
  (21 of 21). Exception in spelling only: [042] is "Step 20C".
- **Always:** all annotations are switched on in the `Step N` view and switched off on entering `Step Nc`; the 21 `c` views
  carry zero annotations. `Step N` = "here is what to do", `Step Nc` = "this is what it looks like when done".
- **Always:** the camera never moves on a `c` step (21 of 21). The before/after pair is always seen from one viewpoint.
- **Section cards** are named after the part ("LED Matrix Diagram" [025], "Mini USB Cable" [043]), are not numbered, have no
  `c` partner, hide every other part, and sit immediately before the first step that uses that part (Step 13, Step 21).
  2 cards in this guide; Part 1's "Capacitor" card is absent here.
- **Title page layout:** logo top-left (2 %,4 %, 33 % wide), title/part/copyright block bottom-left (2 %,63 %, 45.7 % wide),
  finished model pushed to the right by a very distant camera (351 mm, 1.36–5.4× any working distance).
- **End view** repeats the title-page direction (azimuth 40° vs 50°, elevation 39° vs 37°) but 1.59× closer (221 vs 351 mm).
- **Descriptions** exist on 28 of 47 steps. They are numbered by physical instruction ("Step 1"–"Step 16"), not by viewer
  step name: the three inspect steps (Step 4, 7, 9) have no description and are not counted, so description "Step 4" sits on
  viewer step "Step 5" [009], "Step 7" on "Step 10" [019], "Step 13" on "Step 16" [032]. `c` steps mostly carry just
  "Step Nc". Steps 20, 21 and both cards have none.

### 3.2 Granularity
- **Never more than one rigid part per numbered step.** Of the 21 numbered steps: 8 install one rigid part
  (2, 3, 5, 6, 8, 17, 18, 21), 6 connect exactly one wire end (10–15), 5 are preparation/inspection with nothing installed
  (1 peel backing, 4 and 7 bend resistor leads, 9 separate the ribbon, 16 remove the nut), 1 mates a sub-assembly (20),
  and **1 connects two wire ends at once** (Step 19: red → J5 and black → J16, both wires of the push-button pigtail, same
  breadboard column, two labels).
- The 3-wire ribbon is introduced once as a single object ([017]) and then connected one end at a time (6 steps).
- Preparing a part (bend, split, unscrew) is its own numbered step, shown with the part isolated on a blank background,
  and is always separate from inserting it.
- When the new part is the stationary target (base D1 in Step 2, panel D2 in Step 17) it fades in at its final place and the
  already-visible part moves onto it.

### 3.3 Ordering
- Bottom-up and inside-out: backing → base → breadboard → controller → passives → jumper wires → off-board module (LED matrix)
  → mechanical sub-assembly (button in panel) → button wires → panel onto base → USB cable last.
- Breadboard components go in the order Nano, 12k resistor, capacitor, 330 Ω resistor.
- Wire order is not consistently power-before-signal. Male ends: I2 (V+), I3 (V−), then B19 (signal). Female ends:
  V+, IN (signal), V−, which is the physical pin order across the matrix connector.
- All three male ends are done before any female end; the "LED Matrix Diagram" card separates the two groups.

### 3.4 Motion
- Breadboard-level parts appear by fading in directly above their seat and drop straight down: breadboard 39.3 mm, Nano
  35.3–36.9 mm, 12k resistor 36.8 mm, capacitor 32.9 mm, 330 Ω resistor 31.4 mm (range 31–39 mm, always vertical).
- Axial parts hover along their insertion axis, far enough to clear the pigtail: button 103.2 mm from the panel hole, nut
  82.6 mm away (travels 80.4 mm).
- Only the two nut moves include a rotation ([033] unscrew, [038] screw on) and only those two steps take 1600 ms; every
  other step is 800 ms.
- Hover positions are set while the part is still hidden, so the part fades in at the hover pose with no fly-in (e.g. the
  capacitor is positioned in [010] and made visible in [011]).
- Shape changes are fade swaps between two models with no travel: straight → bent resistor leads ([008], [014]), joined →
  split ribbon ([018]), loose → routed wire for every wire end ([020], [022], [024], [027], [029], [031], [040]), hovering →
  seated panel sub-assembly ([042]). 11 swaps in total. Each jumper wire exists as up to 5 models (joined, split, male end
  seated, both ends seated to the floating matrix, final long routing to the matrix on the table).
- Wires and cables never translate into place: all 8 wire-end connections and the USB cable are swaps or fade-ins.
- Show/hide is a fade, moves are tweens, camera moves are tweens (speed 2, orbit animation off).

### 3.5 Red lead lines
- Colour #ff0000, thin, straight, 2 points, parallel to the travel direction, from the mating feature on the moving part to
  the exact target feature. Used only for rigid parts with a straight insertion (7 steps, 16 line showings; a 17th showing
  in [041] is a leftover, see anomalies).
- Count per part: 4 for the breadboard (one per bottom corner → the four L-shaped cut-outs), 4 for the Nano (four pins
  spread over both pin rows → their holes, one of them the labelled D12 → C16 pair), 2 for each two-legged component (one per lead tip → hole), 1 for
  the button (axis → hole centre), 1 for the nut (axis).
- Length ≈ hover distance: breadboard 39.3–39.4 vs 39.3 (1.00×), Nano 38.8–39.2 vs 35.3–36.9 (≈1.08×), 12k 41.4 vs 36.8
  (1.13×), capacitor 27.3 vs 32.9 (0.83×), 330 Ω 35.8 vs 31.4 (1.14×), button 106.7 vs 103.2 (1.03×), nut 92.9 vs 82.6
  (1.12×). Overall 0.83–1.14×.
- Never used for flexible wires or the USB cable (0 lead lines in Steps 10–15, 19, 21), and the panel-onto-base step uses
  an arrow instead.
- Six lines are stored as "dashed" (both resistors' lines, one Nano line, the nut line); in the saved renders they look
  identical to the solid ones.

### 3.6 Red arrows
- 3 fat block arrows (#ff0000, body width 5, head width 20, head length 15–17), each showing a direction of removal or
  sliding rather than a pin-to-hole insertion: peel backing down ([001], 39.4 mm), nut off along the wires ([032], 63.4 mm),
  panel toward the base ([041], 55.3 mm). An arrow step has no lead lines (the 8.8 mm line in [041] is a leftover).

### 3.7 Labels
- One style throughout: bold black Arial 2.5 em, centred, underlined with a light-blue rule (#7fdbff), light-blue leader
  ending in a dashed "life-saver" ring on the feature. No box, no fill.
- Text is a bare coordinate in lower case ("c16", "h3", "j2", "a11", "i2", "b19", "j16", "j5"); only one label has a word
  ("Pin d12"). Descriptions write the same coordinates in upper case ("H3", "J2").
- At most 2 labels on screen at once; they sit left and right of (or stacked beside) the model in the upper 7–40 % of the
  viewport, never over the part.
- Rigid components: labels point at the **breadboard holes** (7 labels: c16, h3, h16, j2, j3, a11, a19).
  Wires: labels point at the **wire's own connector** and name where it goes (i2, i3, b19 in Steps 10–12; j16, j5 in Step 19).
  Female-end steps reuse the slot label on the already-seated end to say which wire is meant (Steps 13–15).
- Only two things are named on the moving part itself: "Pin d12" and the wire-end slot names.

### 3.8 Eye icon and image callouts
- Black eye glyph, 6–9 % of viewport width (7.81 % in 4 of 8), no frame, light-blue leader with life-saver ring. 8 showings
  in step data: resistor bands [007] [013], capacitor [011], ribbon male end and female end [017], panel slot [041], USB
  cable [043], Nano USB socket [044]. It always marks a feature the student must look at before acting (value, polarity,
  connector gender, which slot, which port). It has no text and no popup. Only on hover steps and cards, never on `c` steps.
- Matching round badges for off-board pins (Steps 13–15): a blue-filled circle with the pin name points at the pin on the
  matrix, a white circle with the same text points at the free wire end that goes there. Always exactly one pair.
- One framed inset in the whole guide: "Protective Backing" picture in a rounded light-blue rectangle with leader ([001]).
- One full-frame flat diagram used as a card ([025], 62.8 % wide, no leader, no 3D parts).

### 3.9 Camera
- Moves on 18 of 21 `Step N` views, on 1 of 2 cards, on Start and on Completed Build; never on a `c` step or the Transition.
- The 3 `Step N` views that keep the camera: Step 3 (same view as Step 2) and Steps 11, 12 (same view as Step 10): consecutive
  actions in the same area share a viewpoint. The female-end steps do the opposite: the camera swings 81°, 130°, 105° to
  face each matrix pin.
- Large swings are normal: 14 of 21 camera moves rotate the view by more than 60°.
- Two framings alternate: whole current assembly plus hovering part (163–190 mm while only the breadboard exists, 221–258 mm
  once panel and matrix are present) and single part filling the frame (65, 75, 103 mm for resistor, resistor, ribbon).
- Distances fall on a zoom ladder with ×1.166 between notches (some values are 2–3 notches apart): 65, 75, 103, 163, 190,
  221, 258, 351 mm.
- Elevation stays between 19° and 51°: always looking down at an angle, never top-down, never from below.
- Perspective camera, field of view 45°.
- The single "Transition" ([033]) is not a camera move here: it is an auto-playing part animation (nut coming off) between a
  hover view and its `c` view.

### 3.10 Isolation
- Inspect/prepare steps and part cards hide the whole build and show the part alone on white: [007]–[008], [013]–[014],
  [017]–[018], [032]–[034], [043]. The button/panel sub-assembly is built in isolation for 7 consecutive steps
  ([032]–[038], 3–4 parts on screen) before the main assembly returns in [039].
- The build fades back in on the next insertion step together with the camera pull-back.

## 4. Part looks (from the renders)

Global: pure white background (#ffffff), flat "toon" shading on every part with thin black outline edges, matt, no shadows,
no floor. Annotation colours: red #ff0000 (lead lines, arrows), light blue #7fdbff (leaders, underlines, anchor rings,
inset frame, pin badges), black (label text, eye icon).

| part | look |
|---|---|
| Breadboard | White body with light-grey side faces; holes drawn as small black-outlined squares; red and blue power-rail lines; black printed row numbers and column letters |
| Backing sheet | Flat mid-grey rectangle (#aaaaaa) |
| Base "D1" | Pale peach/light wood (#deb887 material, renders very light), darker tan cut edges, black engraved "D1" |
| Side panel "D2" | Outer face mid-brown (#855e42), inner face and edges tan (#deb887), black engraved "D2" |
| Arduino Nano | Navy-blue board, silver pin rows, black pin-strip plastic, silver USB socket, black chip, pale gold 2×3 header pins |
| Resistors | Bright blue body (#0074d9) with coloured bands (12k: brown/red/black/red/brown; 330 Ω: orange/orange/black/black/brown), light silver-grey leads |
| Capacitor | Black cylinder with a grey stripe down one side, silver top and legs |
| Jumper ribbon | Three wires: white, purple (#4e008e), light grey (#b1b3b3); black rectangular connector housings; silver pins on male ends |
| LED matrix | Black square board; 8×8 light-grey/white square LEDs with round lenses; black 3-pin header underneath with silver pins |
| Push button | Black cylindrical body and cap; light-grey/silver hex nut; one red and one black wire, black pin housings, silver pins |
| USB cable | Black cable and moulded plugs, silver USB-A shell with white insert, small right-angle mini-USB plug |
| Pin badges | Circle, blue fill (#7fdbff-like) for the board pin, white fill with thin grey rim for the wire end; bold black text |

## 5. Combined guide versus Part 1 + Part 2 played back to back

Mapping (verified field by field): combined [000] = Part 2 [000] with a new title image; combined [001]–[010] = Part 1
[001]–[010]; combined [011]–[016] = Part 1 [012]–[017]; combined [017]–[046] = Part 2 [001]–[030].
19 + 31 = 50 part steps versus 47 combined steps.

**Dropped (3 steps):**
1. Part 1 [011] "Capacitor" section card (capacitor alone, close-up at 60 mm, framed photo inset "GND Strip / GND / VCC").
2. Part 1 [018] "Completed View".
3. Part 2 [000] "Start" (Part 1's Start is the one that is really gone: the combined Start uses Part 2's camera and model).

**Kept:** one Start, the "LED Matrix Diagram" and "Mini USB Cable" cards, the Transition, and Part 2's "Completed Build"
(same camera: 221 mm, el 39°, az 40°).

**Renumbering:** Part 1 Step 1–8 unchanged. Part 2 Step N → Step N+8 (Step 1 → 9 … Step 13 → 21), `c` partners likewise.
Part 2 "Step 12c" appears as "Step 20C" in the combined guide. Cards and Transition keep their names. Description texts are
identical to Part 2's: Part 2 already numbers its descriptions "Step 7"–"Step 16", continuing from Part 1's "Step 6".

**The seam ([016] → [017]):** no card, no transition, no pause view. Played separately the student sees Part 1 Step 8c →
Completed View (orbit 21°, 163→190 mm) → Part 2 title page (351 mm, whole finished model) → Step 1 (rot 74°, 351→103 mm,
25 parts fade out). Combined: Step 8c → Step 9 directly, one camera move (rot 66°, 163→103 mm, target shift 18 mm) while the
6 assembly parts fade out and the ribbon fades in. It is indistinguishable from any other "isolate the next part" step.

**Changed content:**

| where | combined | part guide |
|---|---|---|
| Start [000] | Title image reads "Part 1 + 2" (w 45.66 %, at 2 %,63 %) | Part 2: "Part 2" image (w 48.36 %, at 2 %,62 %). Part 1: own Start, camera 190 mm el 47° az −141°, 6-part model, title image w 58.28 % at 2 %,24 % |
| Step 1 [001] entry | camera 351→190 mm, rot 74°; 24 parts fade out | Part 1: 190→190 mm, rot 78°; 5 parts fade out |
| Step 2 [003] | description "Step 2 - Place Breadboard on the Housing Base, centered in the L-Shaped cutouts" | Part 1: empty |
| Step 5 [009], 5c [010] | descriptions "Step 4 - Bend the leads of the 12k Ω Resistor…", "Step 4c" | Part 1: empty |
| Step 6 [011] | description "Step 5 - Install the Capacitor … (with the grey-striped side in slot J3)"; entered from Step 5c with a 12° nudge at 163 mm; capacitor simply fades in at hover | Part 1 [012]: no description; entered from the Capacitor card with a 128° swing 60→163 mm, capacitor travels 69 mm and rotates from its card pose, field of view goes 50° → 45° |
| Step 6 annotations | j2 at 66 %,22 %; j3 at 43 %,16 %; eye at 53 %,−1 % | j2 at 68 %,22 %; j3 at 43 %,17 %; eye at −6 %,16 % |
| Step 3 [005] | "Pin d12" leader colour set to #7fdbff | Part 1: leader colour unset (no visible difference) |
| Step 19 / 19c [039]–[040] | camera 258 mm, el 38°, az 143°; labels j16 at 31 %,24 %, j5 at 64 %,25 % | Part 2 Step 11 / 11c: 221 mm, el 27°, az 135°; j16 at 28 %,20 %, j5 at 65 %,17 % |
| Step 20 / 20C [041]–[042] | camera 258 mm, el 41°, az −131°; arrow 55.3 mm; eye at 63 %,56 %; extra 8.8 mm lead line switched on | Part 2 Step 12 / 12c: 258 mm, el 48°, az −123°; arrow 50.1 mm; eye at 65 %,56 %; no lead line |
| Mini USB Cable [043] | eye at 19 %,16 %; entry rot 93° | Part 2: eye at 35 %,12 %; entry rot 86° |
| Step 9 [017] entry | rot 66°, 163→103 mm; 6 parts fade out | Part 2 Step 1: rot 74°, 351→103 mm; 25 parts and 2 title images fade out |
| Small nudges | Step 1 inset x 68 %; Step 11 "i3" at 33 %,18 %; Step 15 blue badge at 58 %,12 % | 67 %; 34 %,17 %; 56 %,12 % |
| Project settings | default font unset; scene field of view unset (camera 45°) | Part 1: default font PublicSansMedium #637381, scene fov 45. Part 2: same as combined |

Everything else is identical: part motions, offsets, swaps, lead-line anchors and lengths, label texts, durations
(Transition and nut step 1600 ms in both), and all descriptions from Step 10 onward including their typos.

**Provenance (raw project dates):** combined created 2025-07-17, last modified 2025-09-17, publish version 25. Part 2 created
2025-08-22 02:02 UTC, Part 1 created 2025-08-22 02:06 UTC (3 minutes apart), both publish version 12. All three share the
same CAD id and 55 of 61 annotation ids; each part still carries the other part's unused annotations (Part 1 contains the
"j5"/"j16" labels). Part 1 was last modified 2026-09-22, a year after the other two, which is consistent with the Capacitor
card being a later addition to Part 1 only. So the parts were cut from the combined project, not the reverse.

## 6. Anomalies and inconsistencies

Text:
- [032] description "Remove the srew attached to the Push Buttoim" (two typos; the part removed is a hex nut, not a screw).
- [039] description "Ste[ 15"; [037] is also "Step 15", so two different viewer steps carry instruction number 15, and
  [040] then says "Step 16c" with no "Step 16" hover text.
- [031] description "Step 12c 0 Connect the female side…" ("0" typed for "-"); it is also one of only two `c` steps that
  repeat a full instruction ([006] is the other).
- [021] description has no "Step 8 - " prefix; [022] says "Step 8c".
- [027] description "Step 10C" and step name [042] "Step 20C" use a capital C; the other 20 use lower case.
- [035] description covers two actions (insert button, tighten nut) although the nut is its own step [037]–[038].
- Step names and description numbers disagree from [009] onward (name "Step 5" / description "Step 4" … name "Step 19" /
  description 15–16), growing to an offset of 3.
- Pin badge in [028] reads "V-In"; the description calls the pin "IN"; the diagram card labels the other pad group
  "V- Out V+".
- Project name has a double space ("(LSM) -  Part 1 + 2"); the guide id omits the "_-_" used by the other LSM guides.
- End view is named "Completed Build" here and in Part 2 but "Completed View" in Part 1.

Data versus render:
- [025] the saved render shows two eye icons with leaders on the red-framed pad groups, but the step data only switches on
  the diagram image; those two eye-icon objects are never set visible in any step (only set hidden in [026]). Same in Part 2.
- [026]–[031] the LED matrix floating above the board is clearly rendered, but the digest's part counts omit it (the second
  matrix instance is flagged hidden at the top of the assembly tree while its 323 solids are switched visible in [026] and
  hidden in [032]). Counts for those six steps are one part / 323 solids low.
- [011]–[012] the digest reports the capacitor appearing 32.9 mm *below* its seat and moving *up*; the render shows it above
  the board coming down. Sign artefact of the part's local frame.
- Six lead lines are stored as "dashed" but render as continuous lines in every saved thumbnail.

Leftovers:
- [041] an 8.8 mm lead line (button body ↔ panel hole, the Step 17 line) is switched on again; it lies inside the button and
  is not visible. Not present in Part 2.
- 11 of 61 annotation objects are never shown: 4 solid lead lines, 4 labels ("I3", "In", "V-", "V+", superseded by the round
  image badges), 1 older title image, 2 eye icons (the [025] pair).
- [005] one of the four Nano lead lines is anchored in the opposite direction (breadboard → Nano, 38.8 mm) to the other three.
- Many parts report a permanent "still displaced" offset (Nano solids by 1.6–2.8 mm; resistor leads, capacitor legs, USB
  cable by ~1700 mm): these are models authored away from their CAD pose, not motion.

## 7. Relation to the other LSM guides (as far as checked)

- **Part 1** and **Part 2**: trimmed copies of this project (see §5). Part 1 additionally has the "Capacitor" card and a
  "Completed View"; Part 2 is step-for-step identical to [017]–[046] apart from the three camera/label differences listed.
- **Full Build** (88 steps, created 2025-08-28; step names, annotation kinds and contact sheet 040–047 checked): follows the
  same sequence through Step 19 with the same pair structure and the same cards, but is a separate re-authoring: it inserts
  an auto "Transition" between Step 1 and Step 1c, includes the "Capacitor" card, uses different camera distances
  (189/221/300 mm), has no descriptions at all (0 of 88), and puts the USB cable (its Step 20) before the panel-onto-base
  arrow step (its Step 21), the reverse of this guide's Steps 20–21. It then continues with Part 3 + 4 content to Step 38.
- **Part 3 + 4** (43 steps): same Start / Step N / Step Nc / Transition / card / end-view vocabulary; its end view is
  spelled "Copmleted View".
