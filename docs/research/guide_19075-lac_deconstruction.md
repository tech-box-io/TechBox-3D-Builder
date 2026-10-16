# Guide report — `19075-lac_deconstruction`

Kit: LCD Alarm Clock (LAC) · role: deconstruction (take-apart) · 130 viewer steps (131 authored, 1 hidden baseline) · 47 numbered steps
Compared against: `19075-lac_full_build` (131 viewer steps, 57 numbered steps).

## 1. Summary

The student starts with the finished wooden LCD alarm clock and takes it apart down to the base panel F3 with the
breadboard still stuck to it. The guide is wordless (0 of 130 steps have a description or popup; the only text is the
title block and four pin-name labels). Every numbered step is an *instruct* frame `Step N` (model unchanged, one cue
drawn on it) followed by a *result* frame `Step Nc`; in 28 of the 47 steps one or two `Transition` frames (31 of 33 auto-advance)
sit between them and carry the removal motion. The cue vocabulary is tiny and strictly typed: a thick red
**arrow** means "pull this rigid part this way" (22 arrows, 20 steps), the black **eye icon** means "unplug / take away
this thing" (27 eyes, used for all 20 wires and for freed components), a thin red **lead line** appears only in the
three steps where something is put back *on* (washer, nut and knob re-fitted to the loose potentiometer for storage),
and a text **label** appears only to tell four adjacent LCD wires apart (GND, VCC, SDA, SCL). One wire per step, always
(20 of 20). The order is the build order reversed at the level of sub-assemblies, but it is **not** an exact reverse:
only steps 1–8 (the enclosure) mirror the build one-to-one, re-using its cameras and key poses; after that the author
works component group by component group, and inside six groups the items come off in the *same* order they went on
(LCD wires, buzzer leads, three jumper pairs, the two resistors).

> **Data caveat.** The `APPEAR / DISAPPEAR / MOVE` lines in `digest/19075-lac_deconstruction.md` (and in the Full Build
> digest) are unreliable for this kit. Checked against the raw payload and the renders:
> (1) visibility is decided by the leaf solid's own `visible` flag only. The digest also requires every ancestor to be
> visible and seeds that from `rootReference.hidden`, which is `true` for F2, F4-1, F4-3, F5, F6 and others — so it never
> sees those panels and misses their removal (e.g. digest [002] shows no move, the render shows F6 sliding out).
> Counter-examples that fix the rule: F1-2 has parent `visible:false`, leaves `true`, and is drawn at [012]; LAC Knob-3
> has parent `true`, leaves `false`, and is not drawn.
> (2) `position` on a top-level component is an absolute placement (equals the transform translation when seated), not
> an offset; the digest reports it as a 1.7 m displacement (resistors, wires).
> (3) `position` on a solid is in the parent's local frame; the digest prints it as if it were world axes.
> The part states below come from a corrected tracker (`reports/_work_lac_decon/state.py`: leaf-only visibility,
> top-level position minus transform translation, local offsets rotated to world). Annotation and camera lines in the
> digest are unaffected and were used as-is. All distances are mm (1 scene unit = 1.652 mm); Y is up.

## 2. Structure at a glance

| item | count |
|---|---|
| viewer steps | 130 (1 `Start`, 47 instruct, 47 result, 33 transition, 1 duplicate instruct frame, 1 `Completed View`) |
| numbered steps | 47 (`Step 1` … `Step 47`), no section cards, no sub-headings |
| behaviour | 99 pause, 31 play (all 31 are `Transition`); 128 steps at 800 ms, 2 at 1600 ms ([016], [017]) |
| steps with transitions | 28 of 47 (23 with one, 5 with two); 19 go straight from `Step N` to `Step Nc` |
| annotations shown | 22 arrows, 27 eye icons, 2 detail insets, 2 title images, 4 labels, 3 lead lines |
| camera | moves on 18 of 130 frames; never on a `Transition` or `Step Nc` frame |
| descriptions / popups | none |

What the 33 `Transition` frames contain: 11 single tweens of a part out to its offset pose; 6 frames forming three
two-stage moves (F2 tilt then slide [005–006], F9 unhook then shift [064–065], F7 pair straighten then lift [075–076]);
12 routed-wire to loose-wire cross-fades; 3 pose cross-fades ([016], [017], [023]); 1 no-op ([033]). None moves the
camera — in this guide a `Transition` is a motion frame, not a camera frame.

What the 47 `Step Nc` frames do: 28 fade the removed part out; 13 are a cross-fade to a new pose of a tethered part
(4c, 5c, 6c, 8c, 9c–11c, 27c, 29c, 30c, 32c–34c); 6 are a tween whose part stays on screen (15c pot out of panel,
26c F7 pair spread, 35c switch out of panel, 16c–18c re-assembly seats).

## 3. Step table (every viewer step)

Kinds: *instruct* = `Step N`, *result* = `Step Nc`, *transition (auto)* = plays and advances by itself.
Annotation positions are the icon/label position in % of the viewport (x, y); leaders end on the named feature.
Camera: `rot` = view rotation, `×` = zoom factor, `d` = distance in mm, `el` = elevation, `az` = azimuth.

| idx | name | kind | what is done / shown | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Title page: fully assembled clock at right | TechBox logo (2,6)% w=38.9; title block image "LCD Alarm Clock (LAC) / Deconstruction / (c) 2025 ..." (2,64)% w=42.1; no leaders | MOVES rot 70°, ×0.46 → d377 el37 az143 |
| 001 | Step 1 | instruct | Remove end panel F6 (knob/grille end). Model unchanged | 1 arrow 56 mm −Z, tail on F6 lower corner | MOVES rot 8°, ×0.86 → d439 el36 az133 |
| 002 | Transititon | transition (auto) | F6 tweens 67.5 mm out along −Z | arrow off | same |
| 003 | Step 1c | result | F6 faded out | — | same |
| 004 | Step 2 | instruct | Remove back panel F2 (USB-cable slot). Scene up-axis flipped to −X so F2 is "on top" | 1 arrow 80 mm −X (screen-up) on F2; eye (43,11)% → USB cable where it passes the F2 slot | MOVES rot 102°, ×1.0 → d439 el41 az-40 |
| 005 | Transition | transition (auto) | F2 tilts ~21° about one edge (opens like a lid) | arrow + eye off | same |
| 006 | Transition | transition (auto) | F2 slides away 78 mm (−X & −Z) | — | same |
| 007 | Step 2c | result | F2 faded out | — | same |
| 008 | Step 3 | instruct | Remove end panel F5. Up-axis back to +Y | 1 arrow 65 mm +Z at F5 lower edge | MOVES rot 66°, ×1.17 → d377 el30 az43 |
| 009 | Transition | transition (auto) | F5 tweens 56 mm out along +Z | arrow off | same |
| 010 | Step 3c | result | F5 faded out | — | same |
| 011 | Step 4 | instruct | Pull front panel F1 (LCD window + knob) forward | 1 arrow 79 mm +X at F1 lower edge | MOVES rot 66°, ×1.0 → d377 el42 az126 |
| 012 | Step 4c | result | Cross-fade swap (no tween): seated F1 + pot + knob + nut + 3 pot wires → "pulled-forward" pose copies (F1-2, wires stretched) | arrow off | same |
| 013 | Step 5 | instruct | Lay front panel aside. Model unchanged | eye (52,58)% → F1 panel | same |
| 014 | Step 5c | result | Cross-fade swap → "laid flat at the right" pose copies (F1-4 + pot + knob + 3 long wires) | eye off | same |
| 015 | Step 6 | instruct | Unclip LCD from bracket F9 | eye (31,58)% → LCD lower corner; inset detail image w=15% at (20,3)% → F9/LCD notch (2 red boxes on the retaining notches) | MOVES rot 58°, ×0.86 → d439 el30 az53 |
| 016 | Transition | transition (auto) | Cross-fade swap: LCD + its 4 wires → pose 2 (slid out of the notches). 1600 ms | eye + inset off | same |
| 017 | Transition | transition (auto) | Cross-fade swap → pose 3 (LCD swung out). 1600 ms | — | same |
| 018 | Step 6c | result | Cross-fade swap → pose 4: LCD lying face-down front-left of the base, 4 wires still attached | — | same |
| 019 | Step 7 | instruct | Remove strut F8 | 1 arrow 84 mm +X at F8 | MOVES rot 64°, ×1.36 → d323 el44 az134 |
| 020 | Transition | transition (auto) | F8 tweens 94 mm out along +X | arrow off | same |
| 021 | Step 7c | result | F8 faded out | — | same |
| 022 | Step 8 | instruct | Lift top panel F4 (carries rocker switch) | 1 arrow 73 mm +Y on F4 | MOVES rot 14°, ×1.0 → d323 el33 az123 |
| 023 | Transition | transition (auto) | Cross-fade swap: F4 + switch + 3 switch wires → "lifted" pose copies (F4-3) | arrow off | same |
| 024 | Step 8c | result | Cross-fade swap → "held above" pose copies (F4-2), wires still attached | — | same |
| 025 | Step 9 | instruct | Unplug pot wire 1 (black) from breadboard | eye (17,54)% → its plug on the breadboard | MOVES rot 16°, ×0.74 → d439 el44 az107 |
| 026 | Step 9c | result | Swap: black wire now hangs straight down from the pot under F1 | eye off | same |
| 027 | Step 10 | instruct | Unplug pot wire 2 (tan) | eye (26,54)% → plug | same |
| 028 | Step 10c | result | Swap: tan wire hangs from pot | eye off | same |
| 029 | Step 11 | instruct | Unplug pot wire 3 (red) | eye (25,58)% → plug | same |
| 030 | Step 11c | result | Swap: red wire hangs from pot | eye off | same |
| 031 | Step 12 | instruct | ISOLATION: only F1 + pot + knob + 3 hanging wires shown (the other 64 components hidden; loose nut + washer copies switched on); up-axis −X. Pull knob off | 1 arrow 41 mm along shaft axis, tail on knob | MOVES rot 81°, ×1.59 → d277 el38 az-134 |
| 032 | Transition | transition (auto) | Knob tweens 53 mm along shaft axis | arrow off | same |
| 033 | Transition | transition (PAUSE) | No change (duplicate frame; waits for click) | — | same |
| 034 | Step 12c | result | Knob faded out | — | same |
| 035 | Step 13 | instruct | Remove nut | 1 arrow 57 mm along shaft axis | same |
| 036 | Transition | transition (auto) | Nut tweens 59 mm off the shaft | arrow off | same |
| 037 | Step 13c | result | Nut faded out | — | same |
| 038 | Step 14 | instruct | Remove washer | 1 arrow 71 mm along shaft axis | same |
| 039 | Transition | transition (auto) | Washer tweens 55 mm off the shaft | arrow off | same |
| 040 | Step 14c | result | Washer faded out | — | same |
| 041 | Step 15 | instruct | Push pot out of the back of F1 (camera goes behind/below the panel) | 1 arrow 53 mm −Y, tail on pot body | MOVES rot 62°, ×1.0 → d277 el-24 az-142 |
| 042 | Step 15c | result | Pot + its 3 wires tween 67 mm out of the panel and stay visible | arrow off | same |
| 043 | Step 16 | instruct | F1 hidden. RE-ASSEMBLY for storage: washer fades in hovering 54 mm out on the shaft axis | 1 lead line 61 mm washer centre ⇄ pot bushing/shaft | MOVES rot 52°, ×1.0 → d277 el27 az-133 |
| 044 | Step 16c | result | Washer tweens 54 mm onto the shaft | lead line off | same |
| 045 | Step 17 | instruct | Nut fades in hovering 38 mm out | 1 lead line 39 mm nut ⇄ washer/shaft | same |
| 046 | Step 17c | result | Nut tweens 38 mm on | lead line off | same |
| 047 | Step 18 | instruct | Knob fades in hovering 43 mm out | 1 lead line 49 mm knob ⇄ shaft | same |
| 048 | Step 18c | result | Knob tweens 43 mm on | lead line off | same |
| 049 | Step 19 | instruct | Main assembly restored (pot group hidden), up-axis +Y. Unplug LCD wire GND (purple) | label "GND" (30,37)% → LCD header pin; eye (68,54)% → wire plug on breadboard | MOVES rot 102°, ×0.86 → d323 el47 az74 |
| 050 | Transition | transition (auto) | Routed purple wire cross-fades to a straight loose wire lying right of the base | label + eye off | same |
| 051 | Step 19c | result | Loose wire faded out | — | same |
| 052 | Step 20 | instruct | Unplug LCD wire VCC (yellow) | label "VCC" (30,37)% → header pin; eye (64,52)% → plug | same |
| 053 | Transition | transition (auto) | Routed yellow → straight loose wire right of base | label + eye off | same |
| 054 | Step 20c | result | Loose wire faded out | — | same |
| 055 | Step 21 | instruct | Unplug LCD wire SDA (teal) | label "SDA" (28,38)% → header pin; eye (53,58)% → plug | same |
| 056 | Transition | transition (auto) | Routed teal → straight loose wire | label + eye off | same |
| 057 | Step 21c | result | Loose wire faded out | — | same |
| 058 | Step 22 | instruct | Unplug LCD wire SCL (blue) | label "SCL" (28,39)% → header pin; eye (57,60)% → plug | same |
| 059 | Transition | transition (auto) | Routed blue → straight loose wire | label + eye off | same |
| 060 | Step 22c | result | Loose wire faded out | — | same |
| 061 | Step 23 | instruct | Take the (now free) LCD away | eye (16,26)% → LCD board | same |
| 062 | Step 23c | result | LCD faded out (no motion) | eye off | same |
| 063 | Step 24 | instruct | Remove LCD bracket F9 | 1 arrow 34 mm +Y on F9; inset detail image w=20% at (71,35)% → F9 foot hooked in F3 (1 red box) | MOVES rot 25°, ×1.0 → d323 el35 az44 |
| 064 | Transition | transition (auto) | F9 tilts about its foot to unhook (rotation; raw offset 65 mm) | arrow + inset off | same |
| 065 | Transition | transition (auto) | F9 shifts a further 33 mm, still tilted | — | same |
| 066 | Step 24c | result | F9 faded out | — | same |
| 067 | Step 25 | instruct | Unplug USB cable from the Nano | 1 arrow 64 mm +Z at the plug; eye (17,42)% → USB cable | same |
| 068 | Transition | transition (auto) | USB cable + right-angle adaptor tween 43 mm +Z | arrow + eye off | same |
| 069 | Step 25c | result | USB cable faded out | — | same |
| 070 | Step 26 | instruct | Spread the two F7 uprights apart | 2 opposed arrows (37 mm −X, 41 mm +X), one per upright | MOVES rot 14°, ×1.0 → d323 el35 az61 |
| 071 | Step 26c | result | Both F7 tilt outwards (rotation, ~3 mm) and stay | arrows off | same |
| 072 | Step 27 | instruct | Take buzzer out from between the F7 uprights | 1 arrow 58 mm +Z from buzzer; eye (64,12)% → buzzer | same |
| 073 | Step 27c | result | Cross-fade swap: buzzer + 2 leads → loose pose lying front-left on the table (still wired) | arrow + eye off | same |
| 074 | Step 28 | instruct | Lift out both F7 uprights | 2 arrows 37 / 34 mm +Y, one per upright | same |
| 075 | Transition | transition (auto) | Both F7 rotate back upright (seated) | arrows off | same |
| 076 | Transition | transition (auto) | Both F7 rise 44 mm together | — | same |
| 077 | Step 28c | result | Both F7 faded out | — | same |
| 078 | Step 29 | instruct | Unplug buzzer red lead | eye (34,31)% → plug on breadboard | same |
| 079 | Step 29c | result | Swap: red lead now free, sticking up from the buzzer | eye off | same |
| 080 | Step 30 | instruct | Unplug buzzer black lead | eye (36,33)% → plug | same |
| 081 | Step 30c | result | Swap: black lead free | eye off | same |
| 082 | Step 31 | instruct | Take buzzer away | eye (19,42)% → buzzer | same |
| 083 | Step 31c | result | Buzzer + 2 leads faded out (no motion) | eye off | same |
| 084 | Step 32 | instruct | Unplug switch wire 1 (black) | eye (59,27)% → plug on breadboard | same |
| 085 | Step 32c | result | Swap: black wire hangs straight below F4 | eye off | same |
| 086 | Step 33 | instruct | Unplug switch wire 2 (tan) | eye (64,29)% → plug | same |
| 087 | Step 33c | result | Swap: tan wire hangs below F4 | eye off | same |
| 088 | Step 34 | instruct | Unplug switch wire 3 (red) | eye (58,24)% → plug | same |
| 089 | Step 34c | result | Swap: red wire hangs below F4 | eye off | same |
| 090 | Step 35 | instruct | ISOLATION: only F4 + switch + 3 hanging wires shown (32 components hidden). Push switch out of F4 | 1 arrow 64 mm +Y on switch | MOVES rot 62°, ×1.17 → d277 el25 az133 |
| 091 | Step 35c | result | Switch + 3 wires tween 85 mm up out of the panel and stay visible | arrow off | same |
| 092 | Step 36 | instruct | Base F3 + breadboard restored (F4/switch hidden). Unplug jumper (white/light-grey) | eye (60,51)% → one plug of the jumper | MOVES rot 65°, ×1.0 → d277 el46 az54 |
| 093 | Transition | transition (auto) | Routed white jumper → straight loose wire right of base | eye off | same |
| 094 | Step 36c | result | Loose wire faded out | — | same |
| 095 | Step 37 | instruct | Unplug jumper (maroon) | eye (62,51)% → plug | same |
| 096 | Transition | transition (auto) | Routed maroon → loose wire | eye off | same |
| 097 | Step 37c | result | Loose wire faded out | — | same |
| 098 | Step 38 | instruct | Unplug jumper (purple) | eye (58,60)% → plug | same |
| 099 | Transition | transition (auto) | Routed purple → loose wire | eye off | same |
| 100 | Step 38c | result | Loose wire faded out | — | same |
| 101 | Step 39 | instruct | Unplug jumper (blue) | eye (59,56)% → plug | same |
| 102 | Transition | transition (auto) | Routed blue → loose wire | eye off | same |
| 103 | Step 39c | result | Loose wire faded out | — | same |
| 104 | Step 41 | instruct | Unplug jumper (green). MISNAMED: this is the Step 40 hover | eye (62,54)% → plug | same |
| 105 | Step 40 | instruct | No change (duplicate hover frame) | same eye still shown | same |
| 106 | Transition | transition (auto) | Routed green → loose wire | eye off | same |
| 107 | Step 40c | result | Loose wire faded out | — | same |
| 108 | Step 41 | instruct | Unplug jumper (black) | eye (60,55)% → plug | same |
| 109 | Transition | transition (auto) | Routed black → loose wire | eye off | same |
| 110 | Step 41c | result | Loose wire faded out | — | same |
| 111 | Step 42 | instruct | Unplug jumper (orange) | eye (24,24)% → plug | same |
| 112 | Transition | transition (auto) | Routed orange → loose wire | eye off | same |
| 113 | Step 42c | result | Loose wire faded out | — | same |
| 114 | Step 43 | instruct | Unplug jumper (yellow) | eye (29,15)% → plug | same |
| 115 | Transition | transition (auto) | Routed yellow → loose wire | eye off | same |
| 116 | Step 43c | result | Loose wire faded out | — | same |
| 117 | Step 44 | instruct | Pull RTC module (blue board + coin cell) out of breadboard | 1 arrow 30 mm +Y above RTC | same |
| 118 | Transition | transition (PAUSE) | RTC + coin cell tween 22 mm up (waits for click) | arrow off | same |
| 119 | Step 44c | result | RTC faded out | — | same |
| 120 | Step 45c | instruct (misnamed) | Pull resistor 1. MISNAMED: this is the Step 45 hover | 1 arrow 39 mm +Y above resistor | same |
| 121 | Transition | transition (auto) | Resistor 1 tweens 52 mm up | arrow off | same |
| 122 | Step 45c | result | Resistor 1 faded out | — | same |
| 123 | Step 46 | instruct | Pull resistor 2 | 1 arrow 47 mm +Y | same |
| 124 | Transition | transition (auto) | Resistor 2 tweens 51 mm up | arrow off | same |
| 125 | Step 46c | result | Resistor 2 faded out | — | same |
| 126 | Step 47 | instruct | Pull Arduino Nano | 1 arrow 64 mm +Y | same |
| 127 | Transition | transition (auto) | Nano tweens 55 mm up | arrow off | same |
| 128 | Step 47c | result | Nano faded out | — | same |
| 129 | Completed View | end | End state: base F3 with breadboard still stuck on | — | MOVES rot 5°, ×1.17 → d237 el50 az50 |

## 4. Conventions found

### 4.1 Structure and numbering
- **Triplet for a part that leaves the scene.** `Step N` (pause): nothing moves, cue drawn. `Transition` (play, 800 ms):
  cue fades out, part tweens out to an offset pose. `Step Nc` (pause): the part fades out. 26 of 47 steps are exactly
  this pattern (1, 2, 3, 7, 12, 13, 14, 19–22, 24, 25, 28, 36–47); 2, 24 and 28 use two transitions.
- **Pair when the part stays on screen afterwards.** No transition; the change happens on `Step Nc`. 19 of 47 steps
  (4, 5, 9–11, 15–18, 23, 26, 27, 29–35). Rule that separates the two: a transition is inserted only when three states
  must be seen (seated → out but visible → gone). Exceptions: steps 6 and 8 use transitions for intermediate *poses*
  although the part stays visible; 23 and 31 make a freed component vanish with no motion at all.
- **Transitions are hidden from navigation.** 31 of 33 have `behaviour: play`, `hideInStepPicker: true`,
  `overlayVisible: false`. The 2 that do not ([033], [118]) are also the 2 that are `pause` — see anomalies.
- **Annotations live only on instruct frames.** 47 of 47 instruct frames carry at least one cue; 0 of 33 transitions and
  0 of 47 true result frames carry any. The cue is switched off on the very next frame (the one frame that keeps it,
  [105], is a duplicate instruct frame).
- **Bookends.** `Start` = title page (model + logo + title block). `Completed View` = last state re-framed
  (rot 5°, zoom ×1.17). No section cards, unlike the build (5 cards).

### 4.2 Granularity
- **One wire per step: always** (20 wires, 20 steps: 9–11 pot, 19–22 LCD, 29–30 buzzer, 32–34 switch, 36–43 jumpers).
  Both ends of a jumper/LCD wire come off in the same step; only one end gets an eye.
- **One rigid part per step: usually.** Exceptions, each a physically inseparable or identical set: both F7 uprights
  together (26 spread, 28 lift, as in build 41/42); USB cable with its right-angle adaptor (25); RTC board with its
  coin cell (44); potentiometer with its 3 soldered leads (15); switch with its 3 leads (35); buzzer with its 2 leads (31).
- **Fasteners are separate steps:** knob, nut, washer are 12, 13, 14 and again 18, 17, 16 going back on.
- **A tethered panel gets two steps:** F1 front is "pull forward" (4) then "lay aside" (5); the LCD is "unclip" (6) and
  only removed 17 steps later (23) once its four wires are off; the buzzer is "release" (27) then "remove" (31).

### 4.3 Ordering
- Outside-in, top-down: enclosure panels (1–5), LCD unclipped (6), strut F8 (7), top F4 (8), then each wired
  component: unplug its wires, then remove it; breadboard jumpers (36–43), plug-in modules (44–46), Nano last (47).
- **Tethered component first, bare jumpers last.** Order of wire groups: pot (9–11) → LCD (19–22) → buzzer (29–30) →
  switch (32–34) → the 8 breadboard-to-breadboard jumpers (36–43).
- **No electrical rule inside a group.** Pot and switch: black, tan, red. Buzzer: red, black. LCD: GND, VCC, SDA, SCL.
  Jumpers: white, maroon, purple, blue, green, black, orange, yellow. Power is neither consistently first nor last.
- The breadboard is never removed from F3 (adhesive); the guide ends there.

### 4.4 Motion
- **Removal is a straight tween along one world axis**, 800 ms: 22–94 mm, median 55 mm (F6 67.5 −Z, F5 56 +Z,
  F8 94 +X, knob 53, nut 59, washer 55, pot 67, USB 43 +Z, F7 44 +Y, switch 85 +Y, RTC 22 +Y, resistors 52 / 51 +Y,
  Nano 55 +Y). Then the part fades (`animation_hide: fade`).
- **Two-stage moves where the real action has two stages:** F2 back panel tilts 21° about an edge then slides 78 mm
  ([005], [006]); F9 tilts to unhook then shifts 33 mm ([064], [065]); F7 pair straightens then lifts ([075], [076]).
- **Parts on wires are never tweened; they cross-fade between posed copies.** The model holds several instances of the
  same part in different poses, each with its own posed wires: F1 front ×3 (seated, pulled forward, laid flat), F4 top
  ×3, LCD ×4, buzzer ×2, and matching copies of the pot, knob, switch and every attached wire. 16 frames are such swaps.
- **Wire removal = routed model cross-fades to a straight loose model parked beside the base**, then the loose one
  fades out (12 wires: LCD ×4, jumpers ×8). The loose pose is the same one the build uses as its hover pose (identical
  raw offsets, e.g. green jumper 159.1 mm in both). Wires soldered to a component instead swap to a "hanging from the
  component" pose and stay (8 wires: pot ×3, buzzer ×2, switch ×3).
- **Re-assembly steps follow the construction pattern:** part fades in hovering on its axis (washer 54, nut 38,
  knob 43 mm out), `Step Nc` tweens it home, no transition.
- **Isolation scenes.** Steps 12–18 show only the front panel with the pot (64 other components hidden) and step 35
  only the top panel with the switch (32 hidden), then the main assembly is restored (19, 36).

### 4.5 Arrows
- One arrow per part being pulled; two only when two parts move (26, 28). 22 arrows on 20 of 47 instruct frames.
- **Identical style: 22 of 22** — `#ff0000`, straight, body width 5, head width 20, head length 17.
- **Always axis-aligned and equal to the removal direction:** +Y ×12, +X ×3, +Z ×3, −X ×2, −Y ×1, −Z ×1.
- **Tail sits on the part to remove, head points away.** In the data all 22 arrows are anchored to a neighbouring
  *static* part (F3 base ×7, breadboard ×3, F7 ×3, F1 ×3, F4 ×2, pot ×2, buzzer ×2), never to the part that moves.
- **Length is hand-set, not derived from travel:** 30–84 mm, median 56 mm; ratio to the tween that follows 0.75–1.47
  (e.g. F6 56 vs 67.5, USB 64 vs 43, RTC 30 vs 22).
- Exception in meaning: at 26 the two arrows mean "spread apart" (a 3 mm tilt), not removal.

### 4.6 Lead lines
- Only 3, only on the re-assembly steps 16, 17, 18: one thin `#ff0000` solid line per part, along the shaft axis from
  the centre of the hovering part to the mating feature (pot bushing/shaft). Lengths 61 / 39 / 49 mm against hover
  offsets 54 / 38 / 43 mm (ratio 1.04–1.15).
- No lead line is ever used for a removal. (43 other lead lines exist in the project but are never shown; see §6.)

### 4.7 Labels
- Only 4, on steps 19–22: `GND`, `VCC`, `SDA`, `SCL`. Arial bold 3em black, `#7fdbff` underline (thickness 5, shadow),
  `#7fdbff` leader ending in a dashed "life-saver" circle on the LCD backpack header pin of that wire.
- Position is held: (30,37), (30,37), (28,38), (28,39) % — upper-left of the header, same place for all four.
- No breadboard hole coordinates anywhere in this guide (41 such labels are inherited from the build and stay hidden).

### 4.8 Eye icon and image insets
- **Eye = the thing to act on when there is no single pull direction.** 27 uses: 20 wire plugs, the F1 panel (5), the
  LCD (6, 23), the buzzer (27, 31), the USB cable (25), the cable slot in F2 (2).
- Always the same asset, width 7.81 % of the viewport, no container, `#7fdbff` leader to a dashed life-saver circle.
- **On a wire it points at one plugged-in connector housing**, never at the wire body. For LCD wires the eye is on the
  breadboard end and the label on the LCD end.
- Placed in free space near the target (x 16–68 %, y 11–60 %); within a run of similar steps it barely moves
  (36–41: x 58–62 %, y 51–60 %).
- **Eye and arrow combine** when a rigid pull also needs attention on something: 2, 25, 27.
- **Detail inset = rounded light-blue framed close-up with a red rectangle on the catch**, leader to the spot: step 6
  (w=15 %, top-left, two red boxes on the LCD notches in F9) and step 24 (w=20 %, right, F9 foot hooked in F3).
  Both are the build's own inset images re-used.
- Title page: logo (w=38.9 %) at (2,6) % and title block image (w=42.1 %) at (2,64) %, model on the right half.

### 4.9 Camera
- **Moves only when an instruct frame starts a new work area** (16 of 47 instruct frames), plus `Start` and
  `Completed View`. Held runs: [025–030] 6 frames, [031–040] 10, [043–048] 6, [049–062] 14, [070–089] 20,
  [092–128] 37 (all jumpers, RTC, resistors and Nano from one view).
- Early enclosure steps re-aim almost every step (1–4, 6–9), by 8–102°, to face the panel coming off.
- **Distances come from a zoom ladder with ratio ≈1.166:** 237, 277, 323, 377, 439 mm (57 frames at 277, 47 at 323,
  17 at 439, 8 at 377, 1 at 237). Never closer than 277 mm while working — looser than the build (down to 110 mm).
- Three-quarter view from above: elevation 25–50°, azimuth near ±45° / ±135°. One exception: step 15 looks from
  below/behind (elevation −24°) to show the pot leaving the back of the panel.
- **Scene up-axis is flipped to −X twice** (step 2; steps 12–18) so that the part comes off "upwards" on screen or the
  isolated sub-assembly stands upright; it returns to +Y at steps 3 and 19.
- Perspective, fov 45; camera tween, `animation_speed 2`, no orbit animation.

### 4.10 Look
White background, toon-shaded parts with thin black edges (edge angle 40, width 1, no silhouette), matt scene style,
ambient 1.75 / directional 1, view cube on, bottom horizontal navigation overlay, font PublicSansMedium 20.

## 5. Part looks (from the renders)

| part | look |
|---|---|
| wooden panels F1–F9 | flat light tan/peach, thin black outline, part number engraved in black on the face ("F1", "F3", "F4", "F7", "F9") |
| breadboard | white body, grey hole grid, thin red and blue rail lines |
| Arduino Nano | dark navy board, black chip, silver pins and USB socket |
| RTC module | bright blue board standing upright, black chips, silver coin cell behind, silver pins |
| resistors | blue body, silver bent legs |
| LCD | green board, black bezel, light grey screen; back has a black I2C backpack with a blue trimmer and silver header |
| jumper / lead wires | saturated flat colours (black, green, purple, blue, light grey, maroon, orange, yellow, teal, red, tan) drawn as smooth arcs; black connector housings with silver pin tips at each end |
| potentiometer | brown round body, grey threaded bushing and splined shaft, three leads black / tan / red |
| knob, nut, washer | knob black with a silver ring; nut and washer silver |
| rocker switch | black, seen as a black square on F4; three leads black / tan / red |
| piezo buzzer | black disc with mounting ears; red and black leads |
| USB cable | black cable and right-angle plug, silver USB-A plug |
| arrows / lead lines | pure red `#ff0000`; arrows thick with a large head, lead lines hair-thin |
| eye icon, labels, insets | black eye glyph; black bold text; light blue `#7fdbff` underline, leader, dashed circular anchor and inset frame; red rectangle highlights inside insets |

## 6. Deconstruction vs Full Build

The deconstruction project is a clone of the Full Build project: same CAD id and version, identical 1776-node
assembly tree, 144 of the build's 150 annotation objects still present. Of the 60 annotations it actually shows, 55
were added for it (22 arrows, 26 eyes, 4 labels, 3 lead lines) and 5 images are re-used.

### 6.1 Is it the exact reverse? No.

| decon steps | what | build steps undone | order vs build |
|---|---|---|---|
| 1, 2, 3 | F6, F2, F5 panels | 57, 56, 55 | exact reverse |
| 4, 5 | F1 front: pull, lay aside | 54, 53 | exact reverse |
| 6 | LCD off bracket | 52 + 51 | reverse, two build steps merged |
| 7 | F8 strut | 50 | exact reverse |
| 8 | F4 top lifted | 49 + 48 | reverse, merged |
| 9, 10, 11 | pot wires black, tan, red | 32, 31, 30 | reversed, but **jumps over** build 33–47 |
| 12, 13, 14, 15 | knob, nut, washer, pot out of F1 | 28, 27, 26, 25 | reversed |
| 16, 17, 18 | washer, nut, knob back on the pot | 24, 23, 22 | reversed (restores the as-supplied pot) |
| 19–22 | LCD wires GND, VCC, SDA, SCL | 36, 37, 38, 39 | **same order as build** |
| 23 | LCD away | "LCD Screen" card | — |
| 24 | F9 bracket | 46 + 45 | reverse, merged |
| 25 | USB cable | 40 | reverse |
| 26, 27, 28 | spread F7 pair, buzzer out, F7 pair straightened and lifted out | 44, 43, 42 + 41 | exact reverse, last two merged |
| 29, 30 | buzzer leads red, black | 33, 34 | **same order as build** |
| 31 | buzzer away | "Alarm Buzzer" card | — |
| 32, 33, 34 | switch wires black, tan, red | 18, 17, 16 | reversed |
| 35 | switch out of F4 | 15 | reverse |
| 36, 37 | jumpers white, maroon | 13, 14 | **same order** inside the pair |
| 38, 39 | jumpers purple, blue | 11, 12 | **same order** inside the pair |
| 40, 41 | jumpers green, black | 10, 9 | reversed |
| 42, 43 | jumpers orange, yellow | 20, 21 | **same order**, and moved after the six above |
| 44 | RTC module | 7 | reverse |
| 45, 46 | resistor 1, resistor 2 | 5, 6 | **same order** |
| 47 | Nano | 3 | reverse |

- Mirrored one-to-one: steps 1–8 only. They re-use the build's cameras exactly (step 1 = build 57 at d439 el36 az133;
  2 = 56; 3 = 55; 4/5 = 54/53; 6 = 52; 7 = 50; 8 = 49) and its key poses (F6 67.5 mm, F5 56 mm, F8 94.2 mm, F2 tilt
  + 78 mm). From step 9 on every camera is new.
- Regrouped: the build order after the breadboard parts is 6 jumpers → switch → 2 jumpers → pot → buzzer leads → LCD
  wires → USB → F7/buzzer mount → F9. A strict reverse would be F9 → F7/buzzer mount → USB → LCD → buzzer → pot →
  2 jumpers → switch → 6 jumpers. The take-apart instead goes pot → LCD → F9 → USB → F7/buzzer mount → buzzer leads →
  switch → all 8 jumpers. The pot comes first because the loose front panel hangs on it; the LCD wires come before
  F9; the two late jumpers (build 20, 21) are pooled with the six early ones.
- Not undone: build 1–2 (peel backing, stick breadboard to F3). No counterpart: build 4 (bend resistor legs),
  8 / 19 / 35 (split ribbon wires), 29 (knob orientation check), 47 (front panel pre-positioned), the five section
  cards.
- Added: explicit "take it away" steps for the LCD (23) and buzzer (31), and the pot re-assembly (16–18).
- 57 build steps become 47: 8 have no counterpart (1, 2, 4, 8, 19, 29, 35, 47), four pairs are merged (52+51, 49+48,
  46+45, 42+41) and 2 take-away steps are added (57 − 8 − 4 + 2 = 47).

### 6.2 How a take-apart step differs from a construction step

| aspect | Full Build | Deconstruction |
|---|---|---|
| `Step N` shows | new part faded in at a hover offset | model unchanged, part still seated |
| cue on a rigid part | thin red lead lines, feature to feature (2–4 per panel: F6 4, F5 4, F1 4, F4 4, F8 2, F2 2) | one thick red arrow per part |
| same enclosure operations (build 48–57 = decon 1–8) | 22 lead lines, 5 eyes, 1 inset | 6 arrows, 3 eyes, 1 inset |
| cue length | lead line 0.86–1.26 × hover distance (panels 0.91–1.00) | arrow hand-set, 0.75–1.47 × travel |
| where the motion plays | on `Step Nc` (tween to seat) | on an auto `Transition` (tween out), `Step Nc` only fades |
| transitions | 10 of 131 frames | 33 of 130 frames |
| wire step | 2 frames: loose wire + eye on the wire body + 2 hole labels → routed | 3 frames: eye on one plug → loose wire → gone; no hole labels |
| labels shown | 41 (hole coordinates, rail names, pin names, "2x") | 4 (pin names only) |
| annotation show events | 48 images, 44 lead lines, 41 labels, 7 arrows | 31 images, 22 arrows, 4 labels, 3 lead lines |
| section cards | 5 | 0 |
| closest camera | 110 mm (10 distances, 110–513) | 277 mm while working (5 distances, 237–439) |
| camera moves | 38 of 131 frames | 18 of 130 frames |

The meaning of each cue is the same in both guides. The build also uses an arrow, not lead lines, wherever it
*removes* something (peel paper, pot strip-down 22–24, spread F7, USB) and the take-apart uses lead lines the moment
it *fits* something (16–18). Arrow = direction of a removal; lead line = where a part goes.

## 7. Anomalies

1. [002] is named `Transititon` (typo); the other 32 are `Transition`.
2. [104] is named `Step 41` but is the Step 40 instruct frame (green jumper); `Step 41` therefore appears twice
   ([104], [108]).
3. [105] `Step 40` is a duplicate of [104] with no change — the student clicks through two identical frames.
4. [120] is named `Step 45c` but is the Step 45 instruct frame (it carries the arrow); `Step 45c` appears twice
   ([120], [122]) and `Step 45` does not exist.
5. [033] `Transition` is `pause`, changes nothing, and is visible in the step picker — a dead click inside step 12.
6. [118] `Transition` is `pause` instead of `play` — the RTC lift needs an extra click, unlike the 11 other lifts.
7. [016] and [017] run 1600 ms; every other frame is 800 ms.
8. Wire order inside groups is inconsistent (reverse of the build for pot, switch and the green/black jumpers; same as
   the build for LCD, buzzer, three jumper pairs and the resistors).
9. Arrow lengths bear no fixed relation to travel (0.75–1.47), and arrows are anchored to neighbouring static parts.
10. Unused inherited annotations: 41 of 45 labels, 43 of 46 lead lines, 7 of 29 arrows and 48 of 79 images are never
    shown.
11. Data only, not visible to the student: on `Start` the model lacks F9 and five internal wires, which are switched on
    at Step 1 with the box still closed; one resistor sub-solid is switched on 21.5 mm off its seat from [015] to [030].
12. Note for readers of the study README, which describes `Transition` as a camera step: here none of the 33 moves
    the camera.

## 8. Relation to the other LAC guides

- `19075-lac_full_build` is the parent project (see §6). Parts 1–4 are its slices: their numbered steps total
  14 + 18 + 8 + 17 = 57, the Full Build's count, and they carry the same annotation inventory (53 images, 41 labels,
  7 arrows, 49 lead lines). The deconstruction is the only LAC guide with its own added annotations.
- `19075-lac_electronics` is a 2-card overview ("All Electronics", "All Wood"), not a procedure.
- The LSM deconstruction report in this folder records the same digest defect (`hidden: true` on top-level
  components); I did not compare its conventions with this guide.

## 9. What an in-house player needs in order to reproduce this guide

- Three frame kinds with different defaults: instruct (pause, cues on), transition (auto-advance, hidden from the step
  list, navigation overlay hidden), result (pause, cues off).
- Cross-fade between posed instances of the same part, including its wires, as a first-class operation.
- Routed-wire to loose-wire swap with a fixed parking pose beside the model.
- Leaf-level visibility, and temporary isolation of a sub-assembly.
- Per-step scene up-axis as well as camera position.
- Screen-space icons, labels and insets with a leader that follows a 3D anchor; world-space arrows and lead lines.

Working files: `reports/_work_lac_decon/` (`state.py` corrected tracker, `compact_decon.out`, `compact_full.out`,
`table.py`).
