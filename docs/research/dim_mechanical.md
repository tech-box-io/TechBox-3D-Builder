# Dimension report: Mechanical (wood, fasteners, enclosure) assembly conventions

Scope: every non-wiring assembly action in TechBox's 20 published Cadasio guides - laser-cut plywood panels and frames,
tab-and-slot joints, panel nuts / washers / knobs, components mounted in panels, modules mounted on wood, LED stems,
cables through notches, sub-assemblies, turning the kit over, engraved part IDs, and what is hidden while the case is built.

## 0. Data, method, caveats

- **Source of numbers.** A corrected state walk over the raw payloads (`reports/_work_dim_mechanical/walk.py`, one
  `state_<guide>.json` per guide): step properties replayed as deltas, visibility per leaf solid, part offsets resolved to
  world millimetres. The published digests under-report wood panels (parent nodes flagged hidden), so the digest JSONs were
  used only for cross-checks; every count below comes from the corrected walk and was spot-checked against the saved renders.
- **Per-step table.** `mech.py` reduces every numbered step of the 19 step-bearing guides to one row (parts that tween,
  pose swaps, lead lines, arrows, eye icons, insets, camera, up-axis); `geom.py` gives each panel's thickness axis so a
  move can be classed as *edge-first* (in the panel's own plane) or *face-on* (along the panel normal).
- **Masters vs clones.** The three Full Builds contain all build content; the Part guides are trimmed copies
  (PMG Part 3 = PMG Full Steps 26-51 with identical line counts; LAC Parts = LAC Full verbatim; LSM Parts differ in
  small ways). Statistics are given for **the 3 master builds (75 mechanical steps)** so nothing is double-counted, and
  again for **all 16 build guides (173 mechanical steps)** to show the clones agree. Take-apart guides are treated in section 4.
- **Renders inspected.** 17 contact sheets (about 135 frames) plus 5 single frames at full size, across all three kits:
  LSM Full [032]-[079], LSM Part 3 [010], LAC Part 4 [000]-[023] and [032]-[039], LAC Full [048]-[063],
  PMG Part 3 [000]-[047].
- **What the corpus does not contain.** There is **no screw, bolt, standoff, threaded insert, glue or tool anywhere** in
  the 20 guides (component inventory of all three CAD models checked: 195 / 188 / 415 top-level components, none of
  these kinds). The only fasteners are one hex panel nut (LSM push button) and a washer + hex nut + push-on knob (LAC
  potentiometer). Every wood-to-wood joint is a press-fit tab-and-slot. Section 5 says which robot-arm rules are
  observed and which are extrapolated.
- **Step classes used below.** *wood-tween* (a plywood part travels), *pose-swap* (a wire-tethered sub-assembly is
  cross-faded between posed copies), *fastener*, *panel-mount* (button / switch / pot pushed through a panel),
  *module-tween* (breadboard onto base), *stem*, *repeat* (remaining identical parts fade in seated).

### Table 1 - mechanical content per guide

| guide | numbered steps | mechanical steps | wood-tween | pose-swap (tethered) | fastener | panel-mount | lead lines on mech steps | max lines on one frame | arrows on mech steps | text labels on mech steps | Transition frames inside mech steps | up-axis changes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LSM P1 | 8 | 1 | 0 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 |
| LSM P2 | 13 | 4 | 0 | 1 | 2 | 1 | 2 | 1 | 2 | 0 | 1 | 0 |
| LSM P1+2 | 21 | 5 | 0 | 1 | 2 | 1 | 7 | 4 | 2 | 0 | 1 | 0 |
| LSM P3 | 5 | 5 | 4 | 1 | 0 | 0 | 14 | 6 | 1 | 0 | 0 | 3 |
| LSM P4 | 12 | 12 | 8 | 2 | 0 | 0 | 29 | 4 | 0 | 0 | 1 | 2 |
| LSM P3+4 | 18 | 18 | 12 | 4 | 0 | 0 | 43 | 6 | 2 | 0 | 1 | 5 |
| **LSM FULL** | 38 | 22 | 12 | 4 | 2 | 1 | 47 | 4 | 3 | 0 | 2 | 5 |
| LSM DECON | 24 | 14 | 9 | 2 | 1 | 1 | 0 | 0 | 17 | 0 | 13 | 0 |
| LAC P1 | 14 | 1 | 0 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 |
| LAC P2 | 18 | 9 | 0 | 0 | 7 | 2 | 5 | 1 | 3 | 0 | 3 | 2 |
| LAC P3 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| LAC P4 | 17 | 17 | 9 | 8 | 0 | 0 | 27 | 4 | 3 | 0 | 5 | 2 |
| **LAC FULL** | 57 | 27 | 9 | 8 | 7 | 2 | 36 | 4 | 6 | 0 | 8 | 7 |
| LAC DECON | 47 | 20 | 7 | 5 | 6 | 2 | 3 | 1 | 17 | 0 | 16 | 4 |
| PMG P1 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PMG P2 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PMG P3 | 26 | 26 | 17 | 8 | 0 | 0 | 43 | 4 | 1 | 0 | 5 | 2 |
| **PMG FULL** | 51 | 26 | 17 | 8 | 0 | 0 | 43 | 4 | 1 | 0 | 5 | 2 |
| PMG DECON | 23 | 11 | 7 | 4 | 0 | 0 | 0 | 0 | 18 | 0 | 14 | 2 |

(LAC Electronics has no steps. "Mechanical steps" in the take-apart rows are approximate: scene swaps blur the classes there.)

Wood inventory: LSM 11 kinds D1-D11 (15 pieces) + 64 stems; LAC 9 kinds F1-F9 (10 pieces); PMG 14 kinds H1-H14
(17 pieces, four H9 keys). 34 kinds, 42 pieces. Stock is 3.0 mm (3.2 mm on LSM D3, D8 and the stems).

---

## 1. Rules

### MECH-1 - Hover the part back along its real joint axis, then seat it with one straight tween

A new rigid part fades in on `Step N` already displaced along the axis it will be pushed in on, in its final orientation,
and tweens home in one straight 800 ms move on `Step Nc`. The camera does not move after `Step N`.

- **Always true.** 0 of 173 mechanical steps (16 build guides) move the camera on a Transition or `Step Nc`. No colour,
  highlight or style change is ever applied to an incoming wood panel (0 colour / style property changes on any wood
  panel in a visible step of the three masters; the only opacity change is the one ghosting step in MECH-9). All moves are 800 ms tweens.
- **The axis is the joint axis, not "up".** 36 unique wood part-moves in the masters, direction relative to the
  declared up-axis: straight down 15, sideways 14, diagonal 4, up 3.
- **Two insertion modes** (panel normal from the CAD bounding box):
  - *edge-first* - the moving part carries the tabs and travels in its own plane (posts, brackets, braces, keys, the
    PMG side walls): 16 new parts, travel 43-139 mm, median 82.
  - *face-on* - the moving panel carries the slots and is pushed along its normal onto tabs of two fixed neighbours
    (walls, lids, shelves): 9 new parts, travel 22-69 mm, median 64.
  - *oblique* - a hinge panel arrives tilted: 3 new parts (46, 78, 117 mm). See MECH-4.
- **Hover distance is hand-picked per part, not a constant.** 28 unique new wood parts in the masters: min 22,
  q1 55, median 69, q3 94, max 139 mm. Per kit medians: LSM 64, LAC 79, PMG 87. As a share of the part's longest
  dimension: 0.2-1.4, median 0.7. Identical parts differ (D11 posts 82 / 82 / 83 / 77 mm).
- **Exceptions.** A part that was visible on the title page slides out to hover instead of fading in (first step of
  LSM P3, LSM P4, LAC P4, PMG P3). Repeat instances fade in already seated (MECH-3). Wire-tethered parts do not tween
  at all (MECH-6).

Evidence: LSM Full [048] D4 69 mm sideways, [060] 2x D9 65 mm down, [069] D6 64 mm down; LAC Full [090] F7 80 mm down,
[111] F8 94 mm sideways, [123] F5 56 mm; PMG Full [059] H2 40 mm, [063] H4 65 mm, [081] H8 94 mm, [083] key 108 mm.

### MECH-2 - One thin red lead line per tab-and-slot pair, tab tip to slot mouth; draw 1, 2 or 4 and never more than 4

On the hover frame draw thin, straight, pure-red lines parallel to the travel, each from a tab tip to the slot that
receives it. Remove them all when the part starts to move.

- **Counts.** Lead lines on `Step N`, all 425 numbered steps of the 19 guides: 0 lines 276, **1 line 37, 2 lines 69,
  4 lines 41**, 6 lines 2. Never 3, never 5. Wood-tween steps in the masters (38): 0 lines 2, 1 line 6, 2 lines 19,
  4 lines 11. All 16 build guides (88 wood-tween steps): 0 x4, 1 x12, 2 x43, 4 x27, 6 x2.
- **What 1 / 2 / 4 mean.**
  - 1 line: a part located by one hook or one tab (PMG H2, H3, key H9, brackets H11 and H12; LAC F9 second stage; stem).
  - 2 lines: a part with two tabs or one mating edge (posts, braces, every hinge panel, D10).
  - 4 lines: a panel closing onto two neighbours, **2 lines per neighbour**. Of the 13 four-line panel steps in the
    masters (11 wood-tween + the 2 tethered panels F4 and F1), 8 are 2 + 2 on two neighbours (D4 onto D1+D2, D5 onto
    D3+D2, the D9 pair onto D3+D2, F4 onto F9+F7, F1 onto F4+F3, F5 onto F1+F3, F6 onto F1+F2, H4 onto H2+H3) and D6
    probably is too (one anchor id is missing). The rest are four posts (D7, D8 and the D11 push-home) and H13 (1 + 1 + 2).
- **Not every tab gets a line.** LAC end panel F6 has slots on all four edges (8 visible in Part 4 [039] = Full
  [128]) and gets 4 lines, to the corner tabs of its two upright neighbours; its mirror part F5 also gets 4. PMG H8 gets 2 lines for its bottom tabs
  only. LSM Full gives D5 4 lines where the older Part 3 copy gives the same panel 6 (one per tab, Part 3 [010]) - the
  only frames in the corpus with more than 4.
- **Which end is which.** For face-on panels the tabs are on the fixed neighbours and the slots in the moving panel;
  for edge-first parts the tabs are on the moving part. Authors usually click the tab first (the fixed part is the
  first anchor in 30 of 42 face-on lines, the moving part in 37 of 39 edge-first lines, masters), but not always, so
  treat lines as undirected. In the renders a red dot is visible inside each target slot ([048], Part 3 [010]).
- **Length.** Line length / stage travel for wood parts that travel 10 mm or more: masters n = 81, q1 0.93,
  median 0.98, q3 1.01; 63 of 81 within 0.85-1.10 (all build guides: n = 201, median 0.97, 151 within). Six PMG
  single-stage lines are travel minus 3.0-3.5 mm, i.e. they stop at the near face of the 3 mm receiving panel
  (36.6 / 40.0, 39.8 / 43.2, 61.5 / 65.0, 104.3 / 107.7, 50.1 / 53.1, 41.0 / 44.5).
- **Exceptions to length.** Shorter when the part passes through something: D11 posts 37-44 mm lines for 77-83 mm
  travel, D7 49 for 68. Longer when anchored beyond the mating face: D8 59-63 for 54. Marker-only lines where little
  or nothing translates: F9 upright 7.3 mm, D3 swing 12.5 / 15.6 mm, H7 hinge 28.5 mm, H10 drop 8.7 mm, D11 push-home
  17 mm for a 7 mm push.
- **Bent paths.** A two-leg approach gets a multi-point polyline tracing the path: D10 (3-point L, LSM [064]) and
  F9 (3- and 5-point L, LAC [098]) - 4 lines on 2 steps in the masters (10 of 363 line showings in all guides).
  Everything else is a 2-point segment.
- **Lines when nothing tweens.** A tethered sub-assembly shown at a hover pose still gets its lines (6 pose-swap
  steps in the masters: 2, 4, 2, 4, 2, 2 lines), and so does a pure second stage (MECH-4).

### MECH-3 - One kind of wooden part per numbered step; identical parts only in pairs that share one motion

- **Counts (masters, 37 steps that introduce wood or stems).** One part: 31. Two identical parts moving together: 4
  (2x D9 [060], D11 2 + 2 across [071] and [073], 2x F7 [090]). "The rest of an identical set" appearing seated after
  one was shown in full: 2 (3 keys at PMG [086] after one at [083]; 63 stems at LSM [086] after one at [083]).
  Two different kinds in one step: 0 of 37.
- **Four identical posts are split 2 + 2** with an 82 degree camera turn between (LSM Steps 32 / 33), not shown as four.
- **The datum panel never moves.** The base of each kit (D1, F3, H1) fades in seated; the first mover hovers against
  it (3 of 3 kits). PMG Step 26 [059] is the only frame where two different panels appear together: datum H1 seated
  and H2 hovering.
- **The hand-held piece is the one that moves.** When a loose component meets a loose panel, the *panel* fades in
  seated and the component already on screen travels: breadboard onto D1 [004] and onto F3 [004], button into D2
  [037], switch into F4 [032], pot into F1 [055] - 5 of 5.
- **Bulk parts** get a named card with a quantity label ("LED Stems", `64x`, Arial bold 6em, #7fdbff), one exemplar
  animated with 1 line, then an eye icon on the seated exemplar and the rest fading in ([082]-[086]).

### MECH-4 - A joint that needs two motions is shown as two stages, each with its own lead lines

Hook-and-swing panels arrive tilted, slide until one edge's tabs are home, then rotate down. Drop-and-slide brackets
drop, then lock sideways. Press-fit posts are left short and pushed home later.

- **How common.** 13 of the 34 wood kinds need more than one motion: LSM D3, D10, D11; LAC F7, F9, F2; PMG H5, H6,
  H7, H10, H11, H12, H14.
- **Two ways to split, both in use.**
  - *Two numbered steps* (stage 2 has its own `Step N` / `Step Nc`): D3 (24 / 25), D11 (32-33 / 34), F7 (41 insert,
    42 spread, 44 close), F9 (45 / 46), H5 (29 / 30), H6 (31 / 32), H7 (35 / 36), H10 (40 / 41) - 8 parts. The
    camera is re-aimed for stage 2 in 5 of 8 (PMG 62-85 degrees on all four; D11 117 degrees to the underside) and
    held in 3 (D3, F7, F9).
  - *An auto-advancing Transition between `Step N` and `Step Nc`* (one press of Next plays both stages): D10 [065],
    F9 first two legs [099]-[100], F2 [126], H11 [092], H12 [095], H14 [114] - 6 parts, 7 Transition frames, camera
    held in all of them.
- **Stage geometry.** Tilt on arrival 7.9-25.8 degrees (7.9, 11.7, 12.6, 18.1, 21.4, 21.6, 23.6, 25.8), rotation
  recorded on the seating stage. Second-stage travel 0-65 mm. Lock slide 6.7 / 7.6 mm (H11 / H12). Push-home 7.0 mm
  (D11). Clamp splay 15.1 / 16.0 degrees (F7).
- **Stage-2 cues.** 7 of the 9 second-stage numbered steps in the masters carry fresh lead lines (1, 2 or 4 short
  ones); the other two are the F7 spread (2 opposed red arrows, [092]) and the F7 close (2 eye icons, [096]). In PMG the second-stage lines appear on the Transition
  frame itself (H14 [114]).
- **Exceptions.** The H11 / H12 lock slide has no line or arrow at all. D10's two legs share one L-shaped line.

### MECH-5 - Fasteners: one per step, off with an arrow, on with a single axial lead line, on the loose panel in isolation

- **Corpus.** 27 fastener steps in 7 guides (LSM P2, P1+2, Full, Decon; LAC P2, Full, Decon): 13 removals, 12 fits,
  2 knob-setting steps. Plus 7 panel-mount insertions (button x3 copies, switch x2, pot x2).
- **One fastener per step: 27 of 27.** Washer, nut and knob each get their own step coming off and going back on, in
  exact reverse order (LAC Full 22-24 off: knob, nut, washer; 26-28 on: washer, nut, knob).
- **Removal (13 of 13):** `Step N` shows one fat red arrow along the axis, no lead line; an auto Transition slides the
  fastener off (38 mm in the LAC build, 99-101 mm in the LSM builds where it must clear the leads; 53-59 and 85 mm
  in the take-apart guides); `Step Nc` hides it.
- **Fitting (12 of 12):** the fastener fades in on the axis (56-61 mm away in the LAC build, 80-83 mm in LSM, 38-54 mm in the LAC take-apart
  refit), exactly **one**
  thin red lead line from its centre to the shaft, no arrow, no Transition; `Step Nc` tweens it home.
- **Panel-mount component (7 of 7):** pushed through its hole along the axis, leads first, from 79-103 mm away with
  exactly one lead line from the body to the hole. The hover is at least the full length of body plus leads (button
  102 mm for a 75 mm part). Axial line / hover ratio over the 19 fits and insertions: 0.86-1.26, median 1.16 (the
  line is anchored on the bodies, not the mating faces).
- **No text.** 0 labels on 27 fastener steps; no size, thread or part name is ever shown. No tool is drawn.
- **Spin.** The LSM nut rotates about half a turn while travelling and that frame runs 1600 ms instead of 800 (5 of
  the 7 frames in the whole corpus that are not 800 ms). LAC's nut and washer spin on removal (176 and 124 degrees)
  but at 800 ms, and nothing spins on refit. Spin on 8 of 13 removals and 3 of 12 fits - usual in LSM, not a kit-wide rule.
- **Isolation.** Every fastener and panel-mount step shows only the component and its panel: 3-11 parts on screen
  against 20-51 when the assembly returns. Camera fixed for the whole run (LAC [055]-[062], 8 frames).
- **Result check.** One inset on the c-step with a red box on the anti-rotation tab in its slot (LAC [056]); one
  straight-on close-up with an eye icon to set the knob pointer ([063]).

### MECH-6 - Build sub-assemblies on the loose panel, join them later; anything on wires is pose-swapped, "pick up" then "attach"

- **Sub-assemble first.** Button into D2 (LSM Steps 16-18), switch into F4 (LAC 15), pot into F1 (LAC 22-29) are all
  done on the loose panel in isolation, wired next, and joined to the box later: 4, 34 and 29 steps later. D10 is
  clipped onto the lifted LED matrix in mid-air (LSM 29) before both are lowered in (30).
- **Tethered parts never tween.** 20 pose-swap steps in the masters (45 across the build guides), each a cross-fade
  between pre-posed copies of the part with its own re-routed wires: LSM matrix (5 poses), D2 + button; LAC F1 (4
  copies), F4 (3), LCD (4), buzzer (2); PMG buttons, shield, display, dot matrix.
- **Two numbered steps per tethered part** in 7 cases: *pick up* (eye icon on the part; c-step shows it re-posed at
  hover next to its mount) then *attach* (lead lines or arrow; c-step shows it seated) - LSM matrix 28 / 30; LAC F4
  48 / 49, LCD 51 / 52, F1 53 / 54; PMG shield 45 / 46, display 47 / 48, matrix 49 / 50. Single-step in 6 (D2 onto
  base, matrix carry, buzzer, F1 moved aside, the two button steps).
- **Cue by case (20 steps):** eye only 10; lead lines 6 (2 or 4, tab or bracket notch to the part edge); red arrow 4
  (with an eye in 2) where there is no single mating pair - D2 slid onto the base (45 mm), matrix carried over the
  wall (103 mm), F1 carried aside (102 mm), shield lowered onto H4 (80 mm).
- **Modules onto wood.** Breadboard onto the base: 4 lines from its corners to the base plate (LSM [004], LAC [004];
  LAC adds an eye icon on the breadboard's orientation corner). Display and dot matrix into the H11 / H12 brackets: 2 lines per
  stage from PCB edge to bracket notch, stage 2 on an auto Transition ([105]-[107], [110]-[112]). LCD onto the F9
  hooks: 2 lines of 25 mm plus an inset ([115]). Buzzer between the spread F7 posts: eyes only.

### MECH-7 - To work on another face, turn the kit over by re-declaring "up" and swinging the camera; never rotate the model, never look up at it

- **Mechanism.** The scene up-axis is switched and the camera moves in the same step, so the kit appears standing on
  a different face. No part transform changes: 0 frames in 20 guides rotate the assembly; the only rotations are
  hinge panels, nuts / washers and the knob.
- **Counts.** 39 up-axis changes in 12 of 20 guides, every one with a camera move of 43-167 degrees. They happen on
  a `Step N` in 28, on an auto Transition in 8 (all LSM), on a section card in 2, on a Completed View in 1.
  Masters: 14 changes (LSM 5, LAC 7, PMG 2).
- **Six mechanical episodes in the masters, 22 of 75 mechanical steps:** LSM Step 23 (plan view to carry the matrix
  over the wall), LSM 24-26 (box stood on its rear wall so D3 hinges in and D5 goes on like a lid), LSM 34 (upside
  down to push the posts through the base), LAC 22-29 (the loose front panel shown upright instead of face-down),
  LAC 56 (box stood on its front so the back panel hinges on from above), PMG 29-36 (kit upside down for the two
  deck plates, the buttons and the bottom cover).
- **Entered on `Step N` in 5 of 6, via an auto Transition in 1** (LSM [052]); left via an auto Transition in 3 (LSM
  [052], [059], [077]) and via the next `Step N` in 3 (LAC, PMG). So a Transition is optional, and only LSM uses one.
- **The camera stays above the working horizon.** Measured against the declared up-axis, 73 of 75 master mechanical
  steps are viewed from 10-60 degrees above (median 34). The two exceptions are the plan view (LSM Step 23) and the
  straight-on knob close-up (LAC Step 29). Underside work is therefore "kit turned over, seen from above", never
  "camera underneath".
- **No flip cue.** No arrow, icon, label or dedicated step tells the student to turn the kit over. Engraved IDs
  simply render upside-down (PMG Part 3 [007]-[022]).
- **Group underside work.** PMG does all of it in one block of 8 numbered steps (16 frames) and turns back once.
  LSM turns the kit three separate times.

### MECH-8 - Engraved part IDs live on the model and in the tooltip, never in a label

- **On the model.** Every wooden part carries its ID as black engraved geometry (D1-D11, F1-F9, H1-H14; each panel
  is one tan solid plus black surface solids). It is what identifies the part in every hover frame.
- **Never in a callout.** 221 text-label showings in the 20 guides: breadboard holes 104, module pins 54, shield
  pins 30, rails 24, quantities 5, other 4. **0 contain an engraved ID, a part name or a fastener size.** 0 text
  labels on any of the 173 mechanical steps of the 16 build guides.
- **One appearance inside a picture.** PMG Step 39 inset [085]: outline of a key with its engraved "H9" and "3x".
- **Tooltip naming.** All three kits bind the hover tooltip to a per-part description of the form
  `<Role> - Part <ID>`: "Housing Rear Side - Part D4", "Top Side - Part F4", "Right Display Bracket - Part H11".
  34 of 34 wood kinds have one. (Read from the data; the live viewer was not opened.)
- **ID order vs build order.** Equal only in PMG (H1 to H14 in sequence). LSM installs D1, D2, D4, D3, D5, D9, D10,
  D6, D11, D7, D8; LAC F3, F4, F1 (sub-assemblies), F7, F9, F4, F8, F1, F5, F2, F6.
- The camera is not chosen to keep the ID readable.

### MECH-9 - Keep the whole build on screen while the case goes on; hide only for bench work and for a harness not yet involved

- **Wires stay visible during case assembly.** LSM Steps 21-38 (18 of 18) and LAC Steps 41-57 (17 of 17) show every
  wire and module already installed while walls, lids and shelves are added (25-40 and 73-78 parts on screen).
- **PMG hides the whole harness while the bare frame is built**: all 74 electronics components are off for Steps 26-32
  (7 steps, 2-6 parts on screen) and fade back at Step 33 [073], the first step that needs them; they then stay to
  the end (19 of 19).
- **Bench work is isolated.** Fastener and panel-mount steps hide everything except the component and its panel
  (MECH-5); the build fades back on the first wiring step that follows.
- **Ghosting is used once.** LSM Step 34 [075]: base D1 and front wall D5 at 50 % opacity so the post tips can be
  seen through them, restored at 34c and the following Transition. No other opacity change in 20 guides.
- **Not observed in any build guide:** hiding individual wires that are in the way, cut-aways, or a highlight colour
  on the new part.
- Consequence visible in the renders: dangling electronics are often cropped by the frame edge in PMG case steps.

### MECH-10 - Confirm hidden or small results with an eye icon or a framed close-up on the c-step

- 66 of 75 master mechanical c-steps are clean; 6 carry an inset, 3 an eye icon (all build guides: 152 clean, 14
  inset, 7 eye).
- **Insets** (white rounded rectangle, cyan border, cyan leader to the feature, a thin red box on the detail,
  13-22 % of the viewport wide): 9 on mechanical steps in the masters. On the c-step as "check this" in 6 - close-up
  of the wire path inside the box (LSM 30c), post tips through the base (34c), anti-rotation tab (LAC 25c), F9 foot in
  its slot (45c), button module on its ledge (PMG 33c), key tip through H4 (38c). On the hover step as orientation
  or quantity aid in 3 - top view with four corner boxes (LSM 31), LCD on the hooks (LAC 52), "H9 3x" (PMG 39).
- **Cables through notches** are not animated. The cable is pose-swapped and an eye icon on the c-step points at the
  notch: matrix wires through D4 (LSM 23c), USB lead through F2 (LAC 56c). The USB lead through D4's U-notch
  (LSM 22) has no cue.

### MECH-11 - Red arrows are for hand moves with no mating feature; arrows and lead lines never share a step

- 12 arrows on 11 steps in the masters (10 on mechanical steps plus the two peel-the-backing steps): peel the
  backing (2), pull a fastener off (4), spread two posts (2 opposed arrows on one step), carry or slide a tethered
  sub-assembly (4). 0 of 75 master mechanical steps carry both an arrow and a lead line (one stray case in LSM P1+2 Step 20 is a leftover).
- Style: #ff0000, straight, body 5, head 20 x 15-17 in 7 of 12; length 25-103 mm. The other 5 are hand-scaled
  variants (body 3-6, head 9-24).

### MECH-12 - Re-aim the camera at the joint for most mechanical steps

- Camera moves on entering 47 of 61 wood / tethered steps in the masters (108 of 141 in all build guides), median
  65 degrees, 32 of 47 by 45 degrees or more. It is held when the next step works at the same place or follows a
  camera-only Transition.
- The travel is kept roughly across the screen, so the hover gap and its lead lines are seen side-on.

---

## 2. Numeric defaults

| default | value | basis |
|---|---|---|
| plywood thickness | 3.0 mm (3.2 on D3, D8, stems) | CAD bounding boxes, 34 kinds |
| hover distance, new wood part | median 69 mm; q1 55, q3 94; range 22-139 | 28 unique new parts, masters |
| hover, edge-first parts | median 82 mm (43-139) | 16 parts |
| hover, face-on panels | median 64 mm (22-69) | 9 parts |
| hover as share of longest dimension | median 0.7 (0.2-1.4) | 28 parts |
| hover, breadboard onto base | 47 mm (LAC), 49 mm (LSM Full); 39 mm in LSM P1 and P1+2 | 5 guides |
| hover, panel-mount component | 79-103 mm, at least body + lead length | 7 insertions |
| hover, nut / washer / knob | 56-61 mm (LAC), 80-83 mm (LSM) | 12 fits |
| fastener removal travel | 38 mm (LAC), 99-101 mm (LSM) | 13 removals |
| hover, LED stem | 44 / 50 / 55 mm | LSM Full, P4, P3+4 |
| lead lines per frame | 1, 2 or 4; hard maximum 4 | 425 steps; 2 frames with 6 |
| lead-line length, wood | 0.98 x stage travel (IQR 0.93-1.01); PMG = travel - 3.4 mm | 81 lines, masters |
| lead-line length, axial part | 1.16 x hover (0.86-1.26) | 19 fits |
| lead-line style | #ff0000, thin constant screen width (scale 5), no arrowhead; renders solid | 363 of 363 showings are #ff0000 scale 5; 36 stored 'dashed' |
| hinge tilt on arrival | 8-26 degrees, typically about 20 | 8 angles |
| lock slide / push-home / clamp splay | 6.7-7.6 mm / 7.0 mm / 15-16 degrees | H11, H12 / D11 / F7 |
| step duration | 800 ms; 1600 ms for a spinning nut | 1030 of 1037 frames; 5 nut frames |
| nut spin while travelling | about half a turn (171-180 degrees recorded) | 6 LSM nut moves |
| ghost opacity | 0.5 | 1 use |
| arrow | #ff0000, body 5, head 20 x 15-17, length 25-103 mm | 12 arrows, masters |
| eye icon width | 7.8 % of viewport (8.2 % in PMG) | 25 on mechanical steps |
| inset width | 13-22 % of viewport, cyan #7fdbff border 5 px | 9 insets |
| camera turn on entering a mechanical step | median 65 degrees; moves on 77 % of steps | 47 of 61 |
| view height over the working orientation | 10-60 degrees, median 34 | 73 of 75 steps |
| camera turn when "up" is re-declared | 43-167 degrees | 39 changes |
| wooden parts per step | 1 (84 %); 2 identical at most in motion | 31 of 37 |
| parts needing two motions | 38 % of wood kinds | 13 of 34 |
| text labels on mechanical steps | 0 | 173 steps |

---

## 3. What a mechanical step looks like, by case

| case | Step N shows | between | Step Nc shows |
|---|---|---|---|
| panel, single motion | part hovering on the joint axis + 1 / 2 / 4 lines | - | part seated, clean |
| hinge or lock panel (one view) | tilted part + lines for stage 1 | auto Transition plays stage 1 (PMG: new lines for stage 2) | stage 2 played, clean |
| hinge or push-home (new view needed) | stage 1 as a normal step | next numbered step: 2 short lines, camera re-aimed | part seated |
| fastener off | part alone + red arrow on the axis | auto Transition slides it off | fastener hidden |
| fastener on | fastener on the axis + 1 line | - | seated |
| component through panel | panel fades in, component hovers leads-first + 1 line | - | seated (inset if a tab must align) |
| tethered sub-assembly | eye on it (pick up), then lines or arrow (attach) | pose copies cross-fade | seated copy, clean |
| remaining identical parts | eye on the exemplar or "Nx" inset | - | all fade in seated |
| work on the underside | kit shown turned over (new up-axis, camera swing) | optional auto Transition | same view |

---

## 4. Take-apart guides (mechanical side only)

- Wood comes off with **arrows, not lead lines**: arrows on LSM 24, LAC 22, PMG 31 showings; lead lines 0, 3, 0
  (the 3 are LAC Steps 16-18, which refit washer, nut and knob for storage and so follow the build pattern exactly:
  one fastener per step, one axial line each).
- The part is still seated on `Step N`; it travels on an auto Transition or on the c-step and is then hidden.
- A tab or latch that must be released gets a framed close-up with a red box: LSM 8 steps, LAC 2, PMG 0.
- Two-stage removals mirror the two-stage fits (unhook, then pull), one arrow per stage.
- The kit is turned over the same way (PMG Steps 11-14, LAC Steps 2 and 12-18); LSM's take-apart never does.
- Details and counts are in the deconstruction dimension report; nothing there contradicts the rules above.

---

## 5. Rules for a wood robot-arm kit with servos and screws

**Directly supported by the corpus**

1. Base plate is the datum: it fades in seated and never hovers. Build bottom-up from it.
2. One wooden part per numbered step. Two identical parts may share a step only if they go in with the same motion
   and both are clear in one view; four identical parts are 2 + 2 with a camera turn.
3. Hover each part back along its true joint axis by roughly 0.7 x its longest dimension (40-140 mm), in final
   orientation; seat with one straight 800 ms tween on the c-step.
4. Lead lines tab tip to slot mouth, parallel to travel, 1 / 2 / 4 per frame: 1 for a single hook, 2 for a two-tab
   part, 4 (2 per neighbour) for a plate closing onto two neighbours. Do not draw every tab of a many-tab plate.
5. A part that hooks and swings, drops and slides, or is pushed home later is two stages with separate lines. Use an
   auto Transition if both stages read from one view; use a second numbered step with a re-aimed camera if not.
6. A servo is a pre-wired panel-mount component: when it meets a loose bracket, the bracket fades in seated and the
   servo travels, lead first through the cut-out, from at least body + lead length away, with exactly one axial
   lead line. Do this on the loose bracket in isolation, then bring the build back.
7. A servo horn or knob pressed onto a shaft: its own step, hover on the shaft axis, one line.
8. Once a servo is in a bracket and its lead is plugged in, that bracket is tethered: never tween it. Pose-swap it,
   with a "pick up" step (eye icon) and an "attach" step (lead lines to the tabs).
9. Arm segments are sub-assemblies: build each on the bench with everything else hidden, join later.
10. To reach an underside, re-declare up and swing the camera so the work is seen from 10-60 degrees above. Group all
    underside steps into one block. Do not rotate the model and do not add a "flip" graphic.
11. Leave all wiring visible while the frame is closed. Hide the electronics only while a bare frame is being built
    before they are involved.
12. No text on mechanical steps. Parts are identified by engraved IDs; give every part a tooltip
    `<Role> - Part <ID>`.
13. Where a joint ends up hidden (horn spline, tab through a plate, cable in a notch), add an eye icon or a framed
    close-up with a red box on the c-step.
14. A servo lead through a slot is shown by the result (eye on the notch), not by animating the cable.

**Extrapolated - the corpus has no screws** (nearest evidence: panel nut, washer, repeated stems and keys)

15. One screw per step for the first screw of each size and joint: hover on its axis, one axial lead line, no arrow;
    spin it while it travels and give that frame 1600 ms (LSM nut precedent).
16. Remaining identical screws of the same joint: follow the "one in full, then the rest" pattern - a following step
    with an eye icon on the seated screw or an "Nx" inset, the rest fading in seated. Pairs may share a step.
17. Screw size has no precedent in any label. The closest authored device is the quantity card ("LED Stems",
    `64x`): the part alone, enlarged, with a bare quantity label. Whether to print "M3 x 6 mm" there is a TechBox
    decision, not an observed convention.
18. A nut or standoff behind a plate: fit it from the side it goes on, with the camera swung to that side first
    (LSM Step 18 turns 114 degrees to the inside face before the nut goes on).
19. No tool is ever drawn in the corpus.

---

## 6. Anomalies and inconsistencies (not conventions)

- LSM Full Step 26 [057]: two of the four D5 lines are stored 133 mm long but render about 40 mm; the same panel has
  6 lines in Part 3 and Part 3+4.
- LSM Part 4 Step 5 [010]: one lid-plate line mis-anchored (103 mm against 62-68); LSM Full Step 31 [069] has a line
  anchored to an object id that no longer exists.
- LSM Steps 35 / 36: 8 lines stored as "dashed" but render solid.
- Identical D11 posts hover 82, 82, 83 and 77 mm with lines of 44, 44, 43 and 37 mm.
- LSM Part 4 names one pair "Step 8" / "Step 9c".
- LSM nut refit: 1600 ms and 179 degrees in Part 2 and Part 1+2, 800 ms and 115 degrees in the Full Build.
- LAC: the nut and the (unthreaded) washer spin on removal but nothing spins on refit.
- LAC Steps 22-24: three removal arrows in three sizes (body 5 / 6 / 5, heads 20x17, 24x22, 15x10).
- LAC Step 42 arrows are anchored to the base F3 rather than the F7 posts; Step 47's arrow to USB-lead parts.
- LAC [053] step name "Ttansition". LAC Step 45: one polyline has 5 points, three coincident (click artefact).
- LAC: the washer is hidden from Step 30 onward and never shown again; the nut gets an unannounced 21 degree twist.
- LAC [108] is the only camera-only Transition between two mechanical steps.
- PMG Step 51c [115] still has 2 lead lines on, and H14 moves a further 1.4 mm on the Completed View.
- PMG H11 / H12 lock slide has no cue.
- PMG "do the rest": keys get a "3x" inset, buttons only an eye icon on one of three.
- PMG tooltip descriptions are inconsistent inside one part: H8 is "Key Passthrough - Part H2" on some solids; H4 is
  "Front Baseplate", "Backplate" and "Rear Baseplate"; H10 has three variants; H5 has a double space; H5 and H6
  share one role name. LSM mixes "Part D9" with "Parts D11".
- Quantity label is `64x` in LSM Full and `64X` in Part 4 and Part 3+4.
- Engraved IDs read upside-down in every turned-over view.
- PMG case frames often crop the dangling electronics at the frame edge.
- Arrow heads and lead-line anchor order are hand-set and vary; neither encodes meaning.

## 7. Open questions

1. Screws, standoffs and tools: no evidence. Rules 15-19 need a TechBox decision.
2. Lead-line cap: 4 per frame in 41 steps, 6 in two older LSM copies. Is "all tabs" or "at most 4" intended?
3. Two-stage joints: when to use an auto Transition and when a second numbered step. The camera explains PMG but not
   LSM D3 or LAC F9.
4. Turning the kit over: auto Transition (LSM only) or hard cut on the step (LAC, PMG, and LSM twice)?
5. Should threaded parts spin and take 1600 ms everywhere, or was that an LSM experiment?
6. Hide the harness while the bare frame is built (PMG) or keep it visible (LSM, LAC)?
7. Is ghosting a convention (one use) or a one-off?
8. Hover distance is hand-picked. Is "0.7 x longest dimension, clamped 40-140 mm" acceptable as an auto default?
9. Are the tooltip names shown to students in the live viewer? Read from data only.
10. No cue tells the student to turn the kit over. Should the in-house player add one?

---

## Appendix A - files

All under `reports/_work_dim_mechanical/`:
`walk.py` (state walk), `state_<guide>.json`, `mech.py` -> `mech_rows.json` (one row per numbered step),
`geom.py` -> `geom_<master>.json` (panel normals), `tab2.py` -> `wood_moves.json`, `stats1.py` ... `stats9.py`,
`final_nums.py`, `gen_tables.py` -> `tbl_masters.md`, `tbl_guides.md`, `out_fasteners.txt`.

## Appendix B - per-step tables for the three master builds

Reading the tables: `Nc49` = travels 49 mm on the c-step; `T22+Nc40` = 22 mm on an auto Transition then 40 mm on the
c-step; `/rot22°` = rotation recorded in that stage; direction is relative to the declared up-axis. "class" adds
edge-first / face-on / oblique for wood. `*` after the up-axis = it changed on this step. "eff.elev" is camera
elevation measured against the declared up-axis. "held" = camera not moved on entering the step.

#### LSM Full Build - mechanical steps

| Step | frames | what moves / swaps | class | lead lines N (mm) | lines on T | arrow (mm) | eye N | inset N/c | eye c | cam on entry | up / eff.elev | parts on screen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | [004]+[005] | tween: breadboard Nc49 down; target fades in seated: D1 | module-tween | 4: 50, 50, 50, 50 |  |  |  | / |  | 11° | +y / 34° | 2 |
| 16 | [034]+T+[036] | tween: nut T101/rot180° sideways | fastener |  |  | 69 |  | / |  | 78° | +y / 38° | 5 |
| 17 | [037]+[038] | tween: button Nc102 sideways; target fades in seated: D2 | panelmount | 1: 106 |  |  |  | / |  | 3° | +y / 35° | 6 |
| 18 | [039]+[040] | tween: nut Nc83/rot115° sideways | fastener | 1: 92 |  |  |  | / |  | 114° | +y / 30° | 6 |
| 21 | [046]+[047] | pose swap: D2(Nc), button(Nc) | pose-swap |  |  | 45 |  | / |  | 62° | +y / 51° | 25 |
| 22 | [048]+[049] | tween: D4 Nc69 sideways | wood-tween / face-on | 4: 65, 66, 69, 69 |  |  |  | / |  | 57° | +y / 43° | 26 |
| 23 | [050]+[051] | pose swap: LED matrix(Nc) | pose-swap |  |  | 103 | 1 | / | 1 | 43° | -z* / -5° | 26 |
| 24 | [053]+[054] | tween: D3 Nc46 diagonal | wood-tween / oblique | 2: 42, 43 |  |  |  | / |  | held | +x / 31° | 27 |
| 25 | [055]+[056] | tween: D3 Nc32/rot22° sideways | wood-tween / face-on | 2: 16, 12 |  |  |  | / |  | held | +x / 31° | 27 |
| 26 | [057]+[058] | tween: D5 Nc42 down | wood-tween / face-on | 4: 133, 134, 39, 43 |  |  |  | / |  | 76° | +x / 36° | 28 |
| 27 | [060]+[061] | tween: 2x D9 Nc65 down | wood-tween / edge-first | 4: 65, 65, 65, 65 |  |  |  | / |  | held | +y / 31° | 30 |
| 28 | [062]+[063] | pose swap: LED matrix(Nc) | pose-swap |  |  |  | 1 | / |  | 32° | +y / 24° | 30 |
| 29 | [064]+T+[066] | tween: D10 T22+Nc40 up | wood-tween / face-on | 2: 44, 44 |  |  |  | / |  | 14° | +y / 18° | 32 |
| 30 | [067]+[068] | pose swap: D10(Nc), LED matrix(Nc) | pose-swap | 2: 57, 56 |  |  |  | /1 |  | 77° | +y / 24° | 32 |
| 31 | [069]+[070] | tween: D6 Nc64 down | wood-tween / face-on | 4: 63, 62, 68, 70 |  |  |  | 1/ |  | 69° | +y / 31° | 33 |
| 32 | [071]+[072] | tween: 2x D11 Nc82 down | wood-tween / edge-first | 2: 44, 44 |  |  |  | / |  | 14° | +y / 21° | 35 |
| 33 | [073]+[074] | tween: D11 Nc83 down; D11 Nc77 down | wood-tween / edge-first | 2: 43, 37 |  |  |  | / |  | 82° | +y / 23° | 37 |
| 34 | [075]+[076] | tween: 4x D11 Nc7 up | wood-tween / edge-first | 4: 17, 18, 17, 17 |  |  | 1 | /1 |  | 117° | -y* / 57° | 37 |
| 35 | [078]+[079] | tween: D7 Nc68 down | wood-tween / face-on | 4: 49, 49, 49, 49 |  |  |  | / |  | held | +y / 34° | 38 |
| 36 | [080]+[081] | tween: D8 Nc54 down | wood-tween / face-on | 4: 63, 63, 62, 59 |  |  |  | / |  | held | +y / 34° | 39 |
| 37 | [083]+[084] | tween: stem Nc44 down | stem / edge-first | 1: 44 |  |  |  | / |  | 0° | +y / 31° | 40 |
| 38 | [085]+[086] | appear seated: 63x stem | repeat |  |  |  | 1 | / |  | held | +y / 31° | 40 |

#### LAC Full Build - mechanical steps

| Step | frames | what moves / swaps | class | lead lines N (mm) | lines on T | arrow (mm) | eye N | inset N/c | eye c | cam on entry | up / eff.elev | parts on screen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | [004]+[005] | tween: breadboard Nc47 down; target fades in seated: F3 | module-tween | 4: 48, 48, 48, 48 |  |  | 1 | / |  | 5° | +y / 31° | 2 |
| 15 | [032]+[033] | tween: switch Nc81 down; target fades in seated: F4 | panelmount | 1: 70 |  |  |  | / |  | 28° | +y / 17° | 8 |
| 22 | [046]+T+[048] | tween: knob T38 sideways | fastener |  |  | 42 |  | / |  | 119° | -x* / 38° | 10 |
| 23 | [049]+T+[051] | tween: nut T38/rot176° sideways | fastener |  |  | 41 |  | / |  | held | -x / 38° | 9 |
| 24 | [052]+T+[054] | tween: washer T38/rot124° sideways | fastener |  |  | 33 |  | / |  | held | -x / 38° | 8 |
| 25 | [055]+[056] | tween: pot Nc79 sideways; target fades in seated: F1 | panelmount | 1: 92 |  |  |  | /1 |  | 6° | -x / 33° | 8 |
| 26 | [057]+[058] | tween: washer Nc61 sideways | fastener | 1: 75 |  |  |  | / |  | held | -x / 33° | 9 |
| 27 | [059]+[060] | tween: nut Nc56 sideways | fastener | 1: 67 |  |  |  | / |  | held | -x / 33° | 10 |
| 28 | [061]+[062] | tween: knob Nc60 sideways | fastener | 1: 76 |  |  |  | / |  | held | -x / 33° | 11 |
| 29 | [063]+[064] | tween: knob Nc57/rot50° down | fastener |  |  |  | 1 | / |  | 53° | -x / 8° | 11 |
| 41 | [090]+[091] | tween: 2x F7 Nc80 down | wood-tween / edge-first | 2: 77, 75 |  |  |  | / |  | 73° | +y / 22° | 73 |
| 42 | [092]+[093] | tween: F7 Nc0/rot15° ; F7 Nc0/rot16°  | wood-tween |  |  | 38, 48 |  | / |  | held | +y / 22° | 73 |
| 43 | [094]+[095] | pose swap: buzzer(Nc) | pose-swap |  |  |  | 2 | / |  | 106° | +y / 50° | 73 |
| 44 | [096]+[097] | tween: F7 Nc0/rot15° ; F7 Nc0/rot16°  | wood-tween |  |  |  | 2 | / |  | held | +y / 50° | 73 |
| 45 | [098]+T+T+[101] | tween: F9 T104+T68/rot26°+Nc33 sideways | wood-tween / edge-first | 2: 108, 112 |  |  |  | /1 |  | 11° | +y / 42° | 74 |
| 46 | [102]+[103] | tween: F9 Nc65/rot26° up | wood-tween / edge-first | 1: 7 |  |  | 1 | / |  | held | +y / 42° | 74 |
| 47 | [104]+[105] | pose swap: F1(Nc), pot(Nc) | pose-swap |  |  | 102 | 1 | / |  | 39° | +y / 48° | 74 |
| 48 | [106]+[107] | pose swap: F4(Nc), switch(Nc) | pose-swap |  |  |  | 1 | / | 1 | 15° | +y / 46° | 73 |
| 49 | [109]+[110] | pose swap: F4(Nc), switch(Nc) | pose-swap | 4: 50, 46, 46, 46 |  |  |  | / |  | held | +y / 33° | 73 |
| 50 | [111]+[112] | tween: F8 Nc94 sideways | wood-tween / edge-first | 2: 94, 94 |  |  |  | / |  | 14° | +y / 44° | 74 |
| 51 | [113]+[114] | pose swap: LCD(Nc) | pose-swap |  |  |  | 1 | / |  | 64° | +y / 30° | 74 |
| 52 | [115]+T+T+[118] | pose swap: LCD(Nc), LCD(T) | pose-swap | 2: 25, 25 |  |  |  | 1/ |  | held | +y / 30° | 74 |
| 53 | [119]+[120] | pose swap: F1(Nc), pot(Nc) | pose-swap |  |  |  | 1 | / |  | 58° | +y / 42° | 74 |
| 54 | [121]+[122] | pose swap: F1(Nc), pot(Nc) | pose-swap | 4: 73, 73, 73, 73 |  |  |  | / |  | held | +y / 42° | 74 |
| 55 | [123]+[124] | tween: F5 Nc56 sideways | wood-tween / face-on | 4: 51, 55, 56, 52 |  |  |  | / |  | 66° | +y / 30° | 76 |
| 56 | [125]+T+[127] | tween: F2 T78+Nc0/rot21° diagonal | wood-tween / oblique | 2: 76, 76 |  |  |  | / | 1 | 66° | -x* / 29° | 77 |
| 57 | [128]+[129] | tween: F6 Nc68 sideways | wood-tween / face-on | 4: 63, 64, 64, 64 |  |  |  | / |  | 102° | +y* / 36° | 78 |

#### PMG Full Build - mechanical steps

| Step | frames | what moves / swaps | class | lead lines N (mm) | lines on T | arrow (mm) | eye N | inset N/c | eye c | cam on entry | up / eff.elev | parts on screen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 26 | [059]+[060] | tween: H2 Nc40 sideways | wood-tween / edge-first | 1: 37 |  |  |  | / |  | 110° | +y / 36° | 2 |
| 27 | [061]+[062] | tween: H3 Nc43 sideways | wood-tween / edge-first | 1: 40 |  |  |  | / |  | 65° | +y / 40° | 3 |
| 28 | [063]+[064] | tween: H4 Nc65 sideways | wood-tween / face-on | 4: 62, 62, 62, 62 |  |  |  | / |  | 103° | +y / 36° | 4 |
| 29 | [065]+[066] | tween: H5 Nc117 sideways | wood-tween / oblique | 2: 118, 118 |  |  |  | / |  | 100° | -y* / 34° | 5 |
| 30 | [067]+[068] | tween: H5 Nc56/rot24° down | wood-tween / face-on | 2: 57, 57 |  |  |  | / |  | 68° | -y / 45° | 5 |
| 31 | [069]+[070] | tween: H6 Nc122 sideways | wood-tween / edge-first | 2: 122, 122 |  |  |  | / |  | 71° | -y / 28° | 6 |
| 32 | [071]+[072] | tween: H6 Nc43/rot18° down | wood-tween / face-on | 2: 44, 44 |  |  |  | / |  | 67° | -y / 23° | 6 |
| 33 | [073]+[074] | pose swap: button module(Nc) | pose-swap |  |  |  | 2 | /1 |  | 55° | -y / 40° | 80 |
| 34 | [075]+[076] | pose swap: button module(Nc) | pose-swap |  |  |  | 1 | / |  | held | -y / 40° | 80 |
| 35 | [077]+[078] | tween: H7 Nc139 sideways | wood-tween / edge-first | 2: 139, 139 |  |  |  | / |  | 102° | -y / 24° | 81 |
| 36 | [079]+[080] | tween: H7 Nc0/rot12°  | wood-tween | 2: 29, 28 |  |  |  | / |  | 85° | -y / 35° | 81 |
| 37 | [081]+[082] | tween: H8 Nc94 down | wood-tween / edge-first | 2: 95, 95 |  |  |  | / |  | 122° | +y* / 30° | 82 |
| 38 | [083]+[084] | tween: H9 Nc108 sideways | wood-tween / edge-first | 1: 104 |  |  |  | /1 |  | 17° | +y / 36° | 83 |
| 39 | [085]+[086] | appear seated: 3x H9 | repeat |  |  |  |  | 1/ |  | held | +y / 36° | 83 |
| 40 | [087]+[088] | tween: H10 Nc126 sideways | wood-tween / edge-first | 2: 116, 116 |  |  |  | / |  | 51° | +y / 26° | 87 |
| 41 | [089]+[090] | tween: H10 Nc9/rot8° down | wood-tween / face-on | 2: 9, 9 |  |  |  | / |  | 62° | +y / 13° | 87 |
| 42 | [091]+T+[093] | tween: H11 T53+Nc7 down | wood-tween / edge-first | 1: 50 |  |  |  | / |  | 31° | +y / 40° | 88 |
| 43 | [094]+T+[096] | tween: H12 T44+Nc8 down | wood-tween / edge-first | 1: 41 |  |  |  | / |  | 99° | +y / 37° | 89 |
| 44 | [097]+[098] | tween: H13 Nc80 diagonal | wood-tween / edge-first | 4: 82, 82, 68, 68 |  |  |  | / |  | 48° | +y / 40° | 90 |
| 45 | [099]+[100] | pose swap: Nano shield(Nc) | pose-swap |  |  |  | 1 | / |  | 13° | +y / 28° | 90 |
| 46 | [101]+[102] | pose swap: Nano shield(Nc) | pose-swap |  |  | 80 |  | / |  | 76° | +y / 29° | 89 |
| 47 | [103]+[104] | pose swap: 4-digit display(Nc) | pose-swap |  |  |  | 1 | / |  | 37° | +y / 41° | 90 |
| 48 | [105]+T+[107] | pose swap: 4-digit display(Nc), 4-digit display(T) | pose-swap | 2: 12, 12 | 10, 9 |  |  | / |  | 83° | +y / 34° | 90 |
| 49 | [108]+[109] | pose swap: dot matrix(Nc) | pose-swap |  |  |  | 1 | / |  | 35° | +y / 38° | 90 |
| 50 | [110]+T+[112] | pose swap: dot matrix(Nc), dot matrix(T) | pose-swap | 2: 21, 20 | 11, 11 |  |  | / |  | 96° | +y / 14° | 86 |
| 51 | [113]+T+[115] | tween: H14 T58+Nc0/rot13° diagonal | wood-tween / edge-first | 2: 58, 59 | 8, 8 |  | 1 | / |  | 22° | +y / 36° | 91 |

## Appendix C - every fastener and panel-mount step

Columns: guide, step, hover frame, CAD component (the LSM nut is one solid of "Push button"), class, stage and travel
(`T` = on an auto Transition, `Nc` = on the c-step, `rot` = degrees recorded), frame durations in ms, lead-line lengths,
arrow lengths, eye icons on Step N, insets on Step Nc, parts on screen, declared up-axis, raw camera elevation against
world +Y (not the effective elevation used in the text), camera turn on entering the step.

```
fastener / panel-mount steps, every guide
  LAC DECON S12 [031] LAC Knob           fastener   T 53mm                   durs['800', '800', '800', '800'] LL[] AR[41.2] eye0 insetC0 tops11 up-x el38 cam81
  LAC DECON S13 [035] LAC Nut            fastener   T 59mm                   durs['800', '800', '800'] LL[] AR[56.5] eye0 insetC0 tops10 up-x el38 cam-
  LAC DECON S14 [038] Washer             fastener   T 55mm                   durs['800', '800', '800'] LL[] AR[70.6] eye0 insetC0 tops9 up-x el38 cam-
  LAC DECON S15 [041] LAC Potentiometer  panelmount Nc 67mm                  durs['800', '800'] LL[] AR[52.7] eye0 insetC0 tops8 up-x el-24 cam62
  LAC DECON S16 [043] Washer             fastener   Nc 54mm                  durs['800', '800'] LL[60.7] AR[] eye0 insetC0 tops8 up-x el27 cam52
  LAC DECON S17 [045] LAC Nut            fastener   Nc 38mm                  durs['800', '800'] LL[39.2] AR[] eye0 insetC0 tops9 up-x el27 cam-
  LAC DECON S18 [047] LAC Knob           fastener   Nc 43mm                  durs['800', '800'] LL[48.9] AR[] eye0 insetC0 tops10 up-x el27 cam-
  LAC DECON S35 [090] Rocker Switch      panelmount Nc 85mm                  durs['800', '800'] LL[] AR[63.6] eye0 insetC0 tops8 up+y el25 cam62
  LAC FULL  S15 [032] Rocker Switch      panelmount Nc 81mm                  durs['800', '800'] LL[69.5] AR[] eye0 insetC0 tops8 up+y el17 cam28
  LAC FULL  S22 [046] LAC Knob           fastener   T 38mm                   durs['800', '800', '800'] LL[] AR[41.8] eye0 insetC0 tops10 up-x el-28 cam119
  LAC FULL  S23 [049] LAC Nut            fastener   T 38mm rot176            durs['800', '800', '800'] LL[] AR[41.3] eye0 insetC0 tops9 up-x el-28 cam-
  LAC FULL  S24 [052] Washer             fastener   T 38mm rot124            durs['800', '800', '800'] LL[] AR[32.6] eye0 insetC0 tops8 up-x el-28 cam-
  LAC FULL  S25 [055] LAC Potentiometer  panelmount Nc 79mm                  durs['800', '800'] LL[91.7] AR[] eye0 insetC1 tops8 up-x el-32 cam6
  LAC FULL  S26 [057] Washer             fastener   Nc 61mm                  durs['800', '800'] LL[75.4] AR[] eye0 insetC0 tops9 up-x el-32 cam-
  LAC FULL  S27 [059] LAC Nut            fastener   Nc 56mm                  durs['800', '800'] LL[66.7] AR[] eye0 insetC0 tops10 up-x el-32 cam-
  LAC FULL  S28 [061] LAC Knob           fastener   Nc 60mm                  durs['800', '800'] LL[76.5] AR[] eye0 insetC0 tops11 up-x el-32 cam-
  LAC FULL  S29 [063] LAC Knob           fastener   Nc 57mm rot50            durs['800', '800'] LL[] AR[] eye1 insetC0 tops11 up-x el-82 cam53
  LSM DECON S18 [048] Push button        fastener   T 85mm rot176            durs['800', '800', '800'] LL[] AR[56.3] eye1 insetC0 tops6 up+y el42 cam9
  LSM DECON S19 [051] Push button        panelmount T 95mm                   durs['800', '800', '800'] LL[] AR[38.4] eye1 insetC0 tops6 up+y el48 cam56
  LSM FULL  S16 [034] Push button        fastener   T 101mm rot180           durs['800', '1600', '800'] LL[] AR[68.7] eye0 insetC0 tops5 up+y el38 cam78
  LSM FULL  S17 [037] Push button        panelmount Nc 102mm                 durs['800', '800'] LL[106.1] AR[] eye0 insetC0 tops6 up+y el35 cam3
  LSM FULL  S18 [039] Push button        fastener   Nc 83mm rot115           durs['800', '800'] LL[92.4] AR[] eye0 insetC0 tops6 up+y el30 cam114
  LSM P2    S 8 [016] Push button no wires fastener   T 99mm rot171            durs['800', '1600', '800'] LL[] AR[63.4] eye0 insetC0 tops3 up+y el39 cam82
  LSM P2    S 9 [019] Push button no wires panelmount Nc 103mm                 durs['800', '800'] LL[106.7] AR[] eye0 insetC0 tops4 up+y el36 cam3
  LSM P2    S10 [021] Push button no wires fastener   Nc 80mm rot179           durs['800', '1600'] LL[92.9] AR[] eye0 insetC0 tops4 up+y el26 cam118
  LSM P1+2  S16 [032] Push button no wires fastener   T 99mm rot171            durs['800', '1600', '800'] LL[] AR[63.4] eye0 insetC0 tops3 up+y el39 cam82
  LSM P1+2  S17 [035] Push button no wires panelmount Nc 103mm                 durs['800', '800'] LL[106.7] AR[] eye0 insetC0 tops4 up+y el36 cam3
  LSM P1+2  S18 [037] Push button no wires fastener   Nc 80mm rot179           durs['800', '1600'] LL[92.9] AR[] eye0 insetC0 tops4 up+y el26 cam118
  LAC P2    S 1 [002] Rocker Switch      panelmount Nc 81mm                  durs['800', '800'] LL[69.5] AR[] eye0 insetC0 tops8 up+y el17 cam28
  LAC P2    S 8 [016] LAC Knob           fastener   T 38mm                   durs['800', '800', '800'] LL[] AR[41.8] eye0 insetC0 tops10 up-x el-28 cam119
  LAC P2    S 9 [019] LAC Nut            fastener   T 38mm rot176            durs['800', '800', '800'] LL[] AR[41.3] eye0 insetC0 tops9 up-x el-28 cam-
  LAC P2    S10 [022] Washer             fastener   T 38mm rot124            durs['800', '800', '800'] LL[] AR[32.6] eye0 insetC0 tops8 up-x el-28 cam-
  LAC P2    S11 [025] LAC Potentiometer  panelmount Nc 79mm                  durs['800', '800'] LL[91.7] AR[] eye0 insetC1 tops8 up-x el-32 cam6
  LAC P2    S12 [027] Washer             fastener   Nc 61mm                  durs['800', '800'] LL[75.4] AR[] eye0 insetC0 tops9 up-x el-32 cam-
  LAC P2    S13 [029] LAC Nut            fastener   Nc 56mm                  durs['800', '800'] LL[66.7] AR[] eye0 insetC0 tops10 up-x el-32 cam-
  LAC P2    S14 [031] LAC Knob           fastener   Nc 60mm                  durs['800', '800'] LL[76.5] AR[] eye0 insetC0 tops11 up-x el-32 cam-
  LAC P2    S15 [033] LAC Knob           fastener   Nc 57mm rot50            durs['800', '800'] LL[] AR[] eye1 insetC0 tops11 up-x el-82 cam53
```
