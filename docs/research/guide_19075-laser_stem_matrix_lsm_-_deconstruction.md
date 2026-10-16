# Guide report — `19075-laser_stem_matrix_lsm_-_deconstruction`

Kit: Laser STEM Matrix (LSM) · role: deconstruction (take-apart) · 69 viewer steps (70 authored, 1 hidden)
Compared against: `19075-laser_stem_matrix_lsm_-_full_build` (88 viewer steps, 38 numbered steps).

> **Data caveat (important for anyone re-using the digest of this guide).** The `APPEAR / DISAPPEAR / MOVE`
> lines in `digest/19075-laser_stem_matrix_lsm_-_deconstruction.md` are unreliable for this guide and for the
> Full Build. Two reasons, both verified against the raw payload and the renders:
> 1. 96 top-level components carry `hidden: true` in the assembly tree (all lens plates, lens supports, all four
>    side panels, 63 stems, 6 of 7 LED-matrix instances, several wires). The digest treats that flag as
>    "ancestor never visible", but the steps only ever set `visible` on leaf solids (0 step properties target a
>    node with children). Result: the digest never sees the lens plates, side panels or lens supports appear,
>    move or disappear (e.g. it reports nothing at [005], [008], [014], [017], [020] where the renders clearly
>    show parts lifting off).
> 2. `position` is the node's local position in its parent's frame (absolute for single-solid top-level parts,
>    an offset for solids inside a component), so the digest's direction words are in component-local axes
>    (it says "-Z" for long supports that visibly move straight up) and it reports absurd "displaced by
>    [607, 902, 1231] mm" for stems that are in fact seated.
>
> Everything quantitative below comes from a corrected walk (leaf-level visibility with the assembly flag as
> initial value only; world displacement = R(parent chain) x (position - own translation)), cross-checked
> frame by frame against the thumbnails. Script: `reports/_work_lsm_decon/state.py`.
> Annotation and camera data in the digest are fine and were used as-is.

## 1. Summary

The guide takes the finished Laser STEM Matrix apart in 24 numbered steps, from the 64 light-pipe stems down
to a bare breadboard stuck on base plate D1. It is authored as a strict three-beat loop that never varies in
kind: **`Step N`** (pause) shows the model still assembled with a thick red 3D arrow giving the pull direction,
plus (optionally) a black eye icon and a framed close-up inset pointing at the tab, clip or plug that has to be
released; an auto-advancing **`Transition`** (800 ms) fades the annotations and slides the part out along the
arrow; **`Step Nc`** (pause) fades the removed part away, leaving the clean remainder. There are no section
cards, no text labels, no descriptions and — unlike the build — not a single red lead line: arrows replace lead
lines completely (24 arrows in 21 of 24 steps, 0 of the 69 lead-line objects in the project are ever shown).
The camera moves only on entering a `Step N` (19 of 24) and holds through Transition and `Nc`. The order is
"outside-in / top-down by physical access", which is close to but not the exact reverse of the Full Build:
two side panels come off early, three pairs/groups of build steps are merged, eight preparatory build steps
have no counterpart, and two sub-assemblies (LED matrix, button panel) are lifted off as a unit and then
dismantled in an isolated view. The project was clearly cloned from the Full Build project (same CAD, 94 of
180 annotation ids shared, 5 identical camera poses) and carries a handful of visibility glitches from that.

## 2. Step table (every viewer step)

Camera column: `d / el / az` = distance mm / elevation deg / azimuth deg; `=` means unchanged from previous step.
Travel distances are world-space, from the corrected walk. "eye" = black eye icon with light-blue leader.

| idx | name | kind | what is done / what changes | annotations | camera |
|---|---|---|---|---|---|
| 000 | Start | title | Complete LSM (box, 64 stems, USB cable) at right of frame | 2 images, no leaders: TechBox logo SVG (w 37.6 %, at 2 %,5 %) and title PNG "Laser Stem Matrix (LSM) / Deconstruction / (c) 2025 TechBox..." (w 42.9 %, at 2 %,61 %) | set 374 / 29 / 54 (identical to Full Build Start) |
| 001 | Step 1 | N | Remove all 64 stems. Stems still seated | 1 arrow up 69 mm from top of the stem block; eye -> one stem near the centre | moves 20 deg -> 374 / 24 / 32 |
| 002 | Transition | T auto | 64 stems rise together 62.5 mm | none (fade out) | = |
| 003 | Step 1c | Nc | Stems fade out | none | = |
| 004 | Step 2 | N | Lens top plate D8 | 1 arrow up 66 mm from plate; eye -> plate centre; framed inset (w 7.8 %) of corner latch with red rectangle -> leader to that latch | moves 78 deg, zoom x1.25 -> 300 / 34 / 123 (= Full Build Steps 35/36 pose) |
| 005 | Transition | T auto | D8 rises 54 mm | none | = |
| 006 | Step 2c | Nc | D8 fades out | none | = |
| 007 | Step 3 | N | Lens middle plate D7 | 1 arrow up 59 mm; eye -> plate centre; framed inset (w 9.9 %) of D11 upright notch with red rectangle -> leader to an upright | = |
| 008 | Transition | T auto | D7 rises 68 mm | none | = |
| 009 | Step 3c | Nc | D7 fades out | none | = |
| 010 | Step 4 | N | Side panel D5 (pull outward, +X) | 1 arrow 63 mm horizontal out of the panel face; eye **in a light-blue box** -> D5/D3 corner; framed inset (w 8.8 %) "D5 / D3" corner with 2 red rectangles on the tabs -> leader to the other end of D5 | moves 13 deg -> 300 / 37 / 139 |
| 011 | Transition | T auto | **No part motion** (annotations fade only) | none | = |
| 012 | Step 4c | Nc | D5 gone (its 54 mm +X offset is set in this same step, so at best it slides while fading; no hover frame exists). All four D11 uprights also vanish (glitch) | none | = |
| 013 | Step 5 | N | Side panel D4 (pull outward, -X). D11 uprights are back | 1 arrow 80 mm out of the panel face; eye -> bottom corner of D4; framed inset (w 9.7 %) "D4 / D2" corner with 2 red rectangles -> leader to top corner of D4 | moves 59 deg -> 300 / 37 / -145 |
| 014 | Transition | T auto | D4 slides out 75 mm | none | = |
| 015 | Step 5c | Nc | D4 fades out | none | = |
| 016 | Step 6 | N | Two D11 lens supports (pair 1 and 4) | 2 arrows up (46 and 47 mm), one per upright; eye -> foot of one upright; framed inset (w 8.6 %) of upright foot/lock slot with red rectangle -> leader to the other upright | moves 24 deg, zoom x0.86 -> 350 / 25 / -120 |
| 017 | Transition | T auto | Both rise 86.5 / 88.8 mm | none | = |
| 018 | Step 6c | Nc | Both fade out | none | = |
| 019 | Step 7 | N | Other two D11 lens supports (pair 2 and 3) | 2 arrows up (45 and 42 mm); eye -> foot of one; same inset image again (w 9.6 %) -> the other | moves 131 deg -> 350 / 24 / 58 |
| 020 | Transition | T auto | Both rise 84.5 / 70.5 mm | none | = |
| 021 | Step 7c | Nc | Both fade out | none | = |
| 022 | Step 8 | N | Lens bottom plate D6 | 1 arrow up 71 mm from plate centre. No eye, no inset | zoom only x1.17 -> 300 / 24 / 58 |
| 023 | Transition | T auto | D6 rises 45 mm | none | = |
| 024 | Step 8c | Nc | D6 fades out; D9/D10 supports exposed (LED matrix itself is missing from the render) | none | = |
| 025 | Step 9 | N | LED matrix with its clip-on support D10, to be lifted off the D9 supports | 1 arrow up 71 mm (same arrow object as Step 8, not moved) | moves 117 deg, zoom x1.17 -> 258 / 35 / -145 |
| 026 | Transition | T auto | Cross-fade to a second model: matrix + D10 + its 3 wires hovering about 29 mm above the supports | none | = |
| 027 | Step 9c | Nc | Cross-fade to a third model: matrix (+D10, still wired) lying on the table beside the box | none | = |
| 028 | Step 10 | N | Two long matrix supports D9 (D3 panel body reappears here) | 2 arrows up (69 and 61 mm), one per support | moves 14 deg -> 258 / 46 / -133 |
| 029 | Transition | T auto | Both rise 54 mm | none | = |
| 030 | Step 10c | Nc | Both fade out | none | = |
| 031 | Step 11 | N | Unplug matrix wire 1 (white) from the breadboard | eye only -> the wire's black plug on the breadboard. No arrow | moves 65 deg -> 258 / 49 / 122 |
| 032 | Step 11c | Nc | No Transition. Routed wire swapped for a loose one dangling from the matrix | none | = |
| 033 | Step 12 | N | Unplug matrix wire 2 (purple) | eye only -> plug | = |
| 034 | Step 12c | Nc | Swap to loose wire | none | = |
| 035 | Step 13 | N | Unplug matrix wire 3 (grey) | eye only -> plug | = |
| 036 | Step 13c | Nc | Swap to loose wire | none | = |
| 037 | Step 14 | N | **Isolated view**: only LED matrix + D10 + 3 loose wires. Unclip small support D10 downward | 1 arrow down 51 mm below D10; eye -> D10 | moves 68 deg, zoom x1.17 -> 221 / 36 / -140 |
| 038 | Transiton | T auto | D10 drops 48 mm (step name misspelt) | none | = |
| 039 | Step 14c | Nc | D10 fades out | none | = |
| 040 | Step 15 | N | Pull the 3-wire cable off the matrix header | 1 fat arrow 32 mm horizontal beside the wires; eye -> connector at the matrix header | moves 69 deg, zoom x1.36 -> 162 / 24 / -60 (closest view in the guide) |
| 041 | Transition | T auto | Cable (3 wires + 6 plugs) slides 30.5 mm away | none | = |
| 042 | Step 15c | Nc | Cable fades out; bare LED matrix left | none | = |
| 043 | Step 16 | N | Back to the main assembly (base, breadboard, D3, D2 + button, USB cable). Side panel D3, pull outward | 1 arrow 51 mm starting at D3's bottom tab; large framed inset (w 24.8 %) of the whole D3 face with red rectangle on its bottom tab -> leader to that tab. No eye | moves 57 deg, zoom x0.63 -> 258 / 31 / -124 |
| 044 | Transition | T auto | D3 slides out 38 mm | none | = |
| 045 | Step 16c | Nc | D3 fades out | none | = |
| 046 | Step 17 | N | Side panel D2 with the push button; also unplug its two wires | 1 arrow 86.5 mm out from the panel; **2 eyes** -> the two button-wire plugs on the breadboard; large framed inset (w 22.5 %) of D2's outer face with red rectangle on its bottom tab | moves 21 deg, zoom x0.86 -> 300 / 51 / -133 (= Full Build Step 21 pose) |
| 047 | Step 17c | Nc | No Transition. Swap: D2 + button now standing clear of the base, red/black wires straight and unplugged | none | = |
| 048 | Step 18 | N | **Isolated view**: D2 panel + button only. Unscrew the nut | 1 fat arrow 56 mm along the button axis; eye -> nut | moves 9 deg, zoom x1.59 -> 189 / 42 / -137 |
| 049 | Transition | T auto | Nut travels 85 mm along the axis while rotating | none | = |
| 050 | Step 18c | Nc | Nut fades out | none | = |
| 051 | Step 19 | N | Push the button (with its wires) out of D2 | 1 arrow 38 mm from the button cap; eye -> button | moves 56 deg to the other face, zoom x0.86 -> 221 / 48 / -54 |
| 052 | Transition | T auto | Button + wires slide out 95 mm | none | = |
| 053 | Step 19c | Nc | Button fades out; bare D2 panel | none | = |
| 054 | Step 20 | N | Back to base + breadboard + Nano + components + USB cable. Unplug the USB cable | 1 arrow 63 mm from the plug; eye -> right-angle mini-USB plug | moves 18 deg, zoom x0.74 -> 300 / 48 / -28 (= Full Build Step 20 pose) |
| 055 | Step 20c | Nc | No Transition. Cable simply fades out | none | = |
| 056 | Step 21 | N | Resistor 2 | 1 arrow up 32 mm from the resistor body | moves 78 deg, zoom x1.59 -> 189 / 32 / -137 (= Full Build Step 8 pose) |
| 057 | Transition | T auto | Rises 30 mm | none | = |
| 058 | Step 21c | Nc | Fades out | none | = |
| 059 | Step 22 | N | Capacitor | 1 arrow up 21 mm (smallest, thinnest arrow) | moves 105 deg -> 189 / 41 / 61 (= Full Build Steps 5/6 pose) |
| 060 | Transition | T auto | Rises 29 mm | none | = |
| 061 | Step 22c | Nc | Fades out | none | = |
| 062 | Step 23 | N | Resistor 1 | 1 arrow up 31.5 mm | = |
| 063 | Transition | T auto | Rises 31 mm | none | = |
| 064 | Step 23c | Nc | Fades out | none | = |
| 065 | Step 24 | N | Arduino Nano | 1 arrow up 40.5 mm from the board | = |
| 066 | Transition | T auto | Rises 31 mm | none | = |
| 067 | Step 24c | Nc | Fades out | none | = |
| 068 | Completed View | end | Breadboard on base D1, nothing else | none | moves 17.5 deg -> 189 / 49 / 38 |

Totals: 1 Start + 24 `Step N` + 19 Transitions + 24 `Step Nc` + 1 Completed View = 69.
Annotations shown: 24 arrows (22 distinct objects), 17 eye icons, 8 framed insets, 2 title-page images. 0 lead lines, 0 text labels.

## 3. Conventions

### 3.1 Structure

- **Always**: `Start` -> 24 x [`Step N` -> optional `Transition` -> `Step Nc`] -> `Completed View`. Numbering 1..24 is contiguous; every `Step N` has a `Step Nc` (24/24).
- **Always**: `Start`, `Step N`, `Step Nc`, `Completed View` are `pause` (student presses Next); every `Transition` is `play` (auto-advance). All 69 steps have duration 800 ms. Parts and annotations fade in/out; moves and camera are tweens (`animation_speed` 2, orbit animation off).
- **Always**: no section cards (Full Build has 4), no step descriptions, no popups, no text labels. The only words on screen are baked into the title-page PNG and engraved part numbers (D1..D11) on the wood.
- **Meaning of the three beats in a take-apart step** (differs from a build step, see section 6):
  - `Step N` = still assembled, annotated: "this is what comes off, this way, mind this catch".
  - `Transition` = annotations fade, the part tweens to its removed pose (the exploded frame).
  - `Step Nc` = the removed part fades out; clean remaining assembly.
- **Usually** (19/24) there is a Transition between N and Nc. Exceptions: Steps 11, 12, 13, 17, 20 — all wire/cable steps, where N goes straight to Nc by cross-fading a routed model to a loose one (11-13, 17) or just fading the cable (20).
- **Always**: annotations exist only on `Step N` (24/24 have at least one). Transitions (0/19), `Nc` (0/24) and Completed View carry none.
- Title page: logo top-left, title/subtitle/copyright block bottom-left (both plain images, no leader), full model on the right. Same layout and same camera as the Full Build title page; only the subtitle image differs ("Deconstruction" vs "Full Build").

### 3.2 Granularity

- **Usually** one removable unit per step (19/24 steps remove exactly one unit).
- Identical parts are removed together when they come off the same way: 64 stems in one step [001]; lens supports 2 + 2 [016], [019]; two long supports [028].
- A plug-in connection is one step per plug when the plugs are separate (three matrix wires at the breadboard: Steps 11, 12, 13) but one step when they share a housing (3-way connector at the matrix header: Step 15). Exception: Step 17 unplugs two button wires and removes the D2 panel in one step (2 eyes + 1 arrow).
- Sub-assemblies come off as a unit and are dismantled afterwards in an **isolated view** with everything else hidden: LED matrix (off in Step 9, dismantled in Steps 14-15), D2 panel + button (off in Step 17, dismantled in Steps 18-19). After each isolated block the next `Step N` cuts back to the main assembly with a camera move ([043], [054]).

### 3.3 Ordering

- Outside-in and top-down by physical access: stems -> lens stack (D8, D7) -> two side panels (D5, D4) -> lens supports -> lens bottom D6 -> LED matrix -> matrix supports -> matrix wiring -> remaining side panels (D3, D2) -> button -> USB cable -> small components (resistor, capacitor, resistor) -> Nano.
- Stops at breadboard-on-base; the breadboard is never lifted (build Steps 1-2 are not undone).
- Small components leave in exact reverse build order (R2, capacitor, R1, Nano).
- Not an exact reverse of the build; see section 6 for the mapping.

### 3.4 Motion

- **Always** one straight, world-axis-aligned translation per removed part, opposite to the direction it was seated in the build. 17 of 17 tweened removals match their arrow's direction.
- Travel by part type (Transition tween, 800 ms): plug-in components 29-31 mm up (R2 30.3, capacitor 29.1, R1 31.3, Nano 31.0); wood plates 45-68 mm up (D8 54.1, D7 67.8, D6 44.7); long supports 54.4; lens uprights 70.5-88.8 up; side panels 38-75 mm outward (D4 75.2, D3 38.4); stems 62.5; button 94.8; 3-wire cable 30.5; D10 clip 48.4 down. Median 54 mm.
- Only compound motion: the nut translates 85 mm and rotates in the same tween [049].
- Wires are never animated. Unplugging is a cross-fade from the routed/plugged wire model to a separate loose model (Steps 11c, 12c, 13c, 17c) — the mirror of the build's straight-to-routed swap.
- The LED matrix lift-off is two successive model swaps (hovering [026], then laid aside [027]) rather than a tween.
- **Usually** (19/24) the removed part is hidden at `Nc`; removed parts do not pile up beside the model. Exceptions are things still tethered: the matrix laid aside in 9c, the dangling wires in 11c-13c, the D2 panel standing clear in 17c.

### 3.5 Red arrows (replace lead lines)

- **Always** red `#ff0000`, straight 3D arrows with the head at the far end. 24 arrows in 21 of 24 steps. Steps without an arrow: 11, 12, 13 (wire unplug at the breadboard — eye only).
- One arrow per moving unit: 2 arrows for 2 parts (Steps 6, 7, 10), 1 arrow for the block of 64 stems, 1 for a 3-wire cable.
- Tail sits on or right beside the part to be removed (plate centre, panel face, tab, component body, plug); head points where it goes. 15 point up, 1 down, 8 horizontal.
- Length 21-87 mm, median 54 mm — same order as the travel that follows, but not tied to it (ratio arrow/travel ranges 0.4 to 1.6).
- Typical geometry: body width 5, head width 20, head length 15-17 (19 of 24). Each arrow has its own `scale` (0.12-0.68) so on-screen thickness varies a lot with zoom.
- Arrows are free world-space objects; the part ids stored on them are whatever surface was under the cursor (e.g. the stems arrow is "attached" to two lens plates), so they carry no target semantics.
- **Lead lines: never.** 69 line objects exist in the project (inherited); 0 are visible in any step.

### 3.6 Eye icon and insets

- Eye icon = "look here / this is what you release". 17 icons in 16 of 24 steps. Always the same PNG at 7.81 % of viewport width, placed in free white space 10-40 % of the viewport away from its target (no fixed side), with a light-blue `#7fdbff` leader ending in a dashed ring on the feature.
  - Targets: the part itself when it simply lifts (stem, plate centre: Steps 1-3), a corner/foot where a tab locks (Steps 4-7), the plug or connector to pull (Steps 11-13, 15, 17, 20), the clip (14), the nut (18), the button (19).
  - Absent on plain lift-offs with nothing to release: Steps 8, 9, 10, 21-24; and Step 16 (inset only).
  - Two eyes when two separate plugs must be pulled (Step 17).
- Framed inset = close-up of a wooden joint. 8 of 24 steps (2-7, 16, 17) — exactly the steps that release a laser-cut tab or latch. Each is a pre-rendered close-up in the same toon style with 1-2 thin red rectangles on the tab(s), inside a light-blue rounded frame (border 5), with a light-blue leader to a ring on the real feature. Small insets are 7.8-9.9 % of viewport width; whole-panel insets (D3, D2) are 22-25 %.
- When a step has both and there are two catches or two parts, the eye marks one and the inset the other (Steps 4, 5, 6, 7). In Steps 2-3 the eye marks the plate and the inset marks the latch that holds it.
- No text callouts at all: the breadboard hole labels used in the build (i2, i3, b19, j5, j16...) exist as objects but are never shown; the eye on the plug stands in for them.

### 3.7 Camera

- **Always** static through `Transition` and `Step Nc` (0 moves in 43 steps). Moves only on entering `Start`, a `Step N` (19/24) or `Completed View`.
- Stays put across consecutive steps that work on the same spot: Step 3 after 2 (lens plates), 12-13 after 11 (wire plugs), 23-24 after 22 (breadboard components).
- Always a three-quarter view from above: elevation 24-51 deg. Never top-down, side-on or from below (the build ranges -57 to +85 deg).
- Orbits freely to face whatever is being pulled (azimuth changes of 9-131 deg between steps), so the arrow reads clearly in screen space.
- Distance comes from a discrete ladder — 162, 189, 221, 258, 300, 350 mm, each x1.17 (plus 374 for Start/Step 1). Whole box: 300-374. Opened box: 258. Isolated sub-assembly or breadboard components: 162-221.
- The model sits in the middle third of a 2:1 frame with wide white margins; annotations are placed in that margin.

### 3.8 Look

- White background, no floor or shadow. Flat toon shading with thin black outlines on every part.
- Red is reserved for arrows and inset highlight rectangles (apart from real red parts: one wire, resistor bands, breadboard rail). Light blue `#7fdbff` is reserved for callout leaders, rings and inset frames. The eye icon is solid black.

## 4. Part looks (from the renders)

| part | look |
|---|---|
| Laser-cut wood (base D1, sides D3-D5, lens plates D6-D8, supports D9-D11) | Flat light tan (burlywood `#deb887`), slightly darker tan on shaded faces and cut edges, black outline, black engraved part number |
| Front panel D2 | Outer face mid-brown (`#855e42`), inner face and edges tan, engraved "D2" |
| LED stems (64) | Pure white square rods with black outlines |
| Breadboard | White block; holes drawn as small dark squares; thin red and blue rail lines; black row/column legends |
| Arduino Nano | Dark navy PCB, white/silver mini-USB socket, black IC, silver header pins, gold ICSP pins |
| Resistors | Blue body with coloured bands, silver-grey bent leads |
| Capacitor | Black can, grey top, two silver legs |
| 8x8 LED matrix | Black PCB, 64 LEDs as light-grey/white squares with silver detail, black pin header |
| Matrix jumper wires | One white, one purple (`#4e008e`), one light grey, side by side as a ribbon; black plug housings with silver pins |
| Button wires | One red, one black; black plug housings |
| Push button | Black body and cap; hex nut light grey/white |
| USB cable | Black cable and plug bodies, silver metal shells, black right-angle mini-USB plug |
| Arrows | Solid red, flat-shaded |
| Eye icon | Solid black eye glyph with white ring pupil |
| Callout leaders, rings, inset frames | Light blue `#7fdbff`; inset highlight rectangles thin red |
| Title page | Cyan rounded TechBox logo with white lettering; dark-grey condensed title; small serif copyright line |

## 5. Anomalies and inconsistencies

1. Step name typo: `Transiton` at [038].
2. Step 4 has no visible removal: its Transition [011] moves nothing, and panel D5 receives its 54 mm offset in the same step that hides it [012]. Every other tweened removal shows the part out at the Transition.
3. Step 4c [012] also hides all four D11 lens supports; they are back in Step 5 [013] and are really removed in Steps 6-7.
4. Side panel D3 is invisible from Step 1 [001] through Step 9c [027] although it is still attached (it is removed in Step 16). The box therefore looks open on that side in [004]-[024], and the eye icons of Step 4 [010] and Step 5 [013] are anchored to the missing panel, pointing at an empty corner. Its body returns at Step 10 [028]. Could be an intended cut-away, but the callouts and the Step 4 inset ("D5 / D3" corner) contradict that.
5. The LED matrix is not rendered from Start through Step 9 [000]-[025] (the seated instance is never switched on). After the lens bottom plate lifts ([023], [024]) the D9/D10 supports are bare, and the matrix pops in already hovering during the Step 9 Transition [026].
6. The eye icon in Step 4 [010] has a light-blue rectangular frame; the other 16 are unframed.
7. The Step 16 inset frame [043] is clipped — no bottom edge.
8. Step 9 [025] reuses Step 8's arrow object unchanged (same world position), so it starts above the supports rather than on the matrix (which is not shown anyway).
9. Arrow sizing is inconsistent: 5 of 24 depart from body 5 / head 20 (Step 6 has one fat and one normal arrow side by side; both Step 10 arrows and Step 21's have head 15; Step 22's is body 4 / head 12), and per-arrow scale makes [040] and [048] very heavy while [059] is thin.
10. Step 20 has an arrow but no motion: the USB cable just fades at 20c.
11. The three matrix wires are unplugged white, purple, grey (i2, b19, i3), which is neither the build order (i2, i3, b19) nor its reverse.
12. Leftovers from the cloned build project that never show: 69 lead lines, 10 text labels (i2, i3, b19, j5, j16, 64x...), 16 arrows, 36 images. A hidden authoring step named "Step 51" precedes Start.
13. Minor invisible flicker: lens supports 1, 3, 4 are off for Step 1 only; the breadboard's protective-backing sheet ("Paper") is switched on under the breadboard for most of the guide; parts of the Nano toggle at [001], [004], [065].
14. Digest caveat at the top of this report (part visibility and directions mis-read for this guide and the Full Build).

## 6. Relation to the Full Build

### 6.1 Same project, cloned

Same CAD id, 94 of 180 annotation ids shared with the Full Build, identical Start camera, and five `Step N`
cameras are bit-identical to the build step being undone: decon Step 2 = build Steps 35/36; 17 = build 21;
20 = build 20; 21 = build 8; 22 = build 5/6.

### 6.2 Order mapping (decon step <- build step)

| decon | undoes build | note |
|---|---|---|
| 1 | 37 + 38 | Build seats 1 stem then 63; decon pulls all 64 at once |
| 2 | 36 | Lens top D8 |
| 3 | 35 | Lens middle D7 |
| 4 | 26 | Side D5 — **moved earlier** (strict reverse would do it after the matrix supports) |
| 5 | 22 | Side D4 — **moved earlier** |
| 6 | 33 | Lens supports 1 + 4 (same pairing as the build) |
| 7 | 32 | Lens supports 2 + 3. Build Step 34 (flip over, lock the supports) has no step; its content is the eye + inset here |
| 8 | 31 | Lens bottom D6 |
| 9 | 30 + 28 | Matrix off the supports and laid aside — two build steps merged |
| 10 | 27 | Long supports D9 |
| 11, 12, 13 | 10, 12, 11 | Wire ends at the breadboard — **moved earlier** and in a different order |
| 14 | 29 | Clip-on support D10 |
| 15 | 13 + 14 + 15 | Three matrix-end plugs in the build; one connector pull here |
| 16 | 24 + 25 | Side D3: build tilts it in in two stages; decon is one straight pull |
| 17 | 21 + 19 | D2 panel off the base and button wires unplugged, merged |
| 18 | 18 | Nut |
| 19 | 17 | Button out of panel |
| 20 | 20 | USB cable — **later** than strict reverse (after the button block is finished) |
| 21 | 8 | Resistor 2 |
| 22 | 6 | Capacitor |
| 23 | 5 | Resistor 1 |
| 24 | 3 | Nano |
| — | 1, 2 | Breadboard stays on the base |

Build steps with no counterpart (8): 1 peel backing, 2 breadboard on base, 4 and 7 bend resistor legs,
9 split the ribbon cable, 16 take the nut off the new button, 23 slide the matrix across, 34 lock the supports.
38 build steps - 8 unmatched - 6 absorbed by merges = 24 decon steps.

So the take-apart order is driven by access (what is on top or outside) and by finishing a sub-assembly once
it has been touched, not by replaying the build script backwards.

### 6.3 How a take-apart step differs from a build step

| aspect | Full Build | Deconstruction |
|---|---|---|
| `Step N` shows | New part hovering at an offset, lead lines to its seat | Model still assembled, arrow on the part to pull |
| `Step Nc` shows | Part seated (tween in, 21/38) or wire swapped to routed (16/38) | Part gone (fade out) or wire swapped to loose |
| Transition | 6 total; 3 are pure camera repositioning between sections, 3 are an extra motion stage | 19 total; none moves the camera; 17 are the removal tween itself |
| Red lead lines | 57 lines in 21 of 38 steps (solid; dashed for the last two plates) | 0 |
| Red arrows | 4 (peel backing, unscrew nut, place D2, slide matrix) | 24 in 21 of 24 steps |
| Text labels | 14 hole labels in 10 steps + "64x" card | 0 |
| Eye icon | 9 `Step N` + 1 `Nc` + 1 card — orientation and "look closely" cues | 17 in 16 of 24 steps — release-point cues |
| Framed insets | 5 (Steps 1, 30c, 31, 34c and the Capacitor card), explanatory; plus 6 round pin-name badges in Steps 13-15 | 8 steps, all joint close-ups with red rectangles; no badges |
| Section cards | 4 (Capacitor, LED Matrix Diagram, Mini USB Cable, LED Stems) | 0 |
| Camera elevation | -57 to +85 deg (includes underside and top-down) | 24 to 51 deg only |
| Camera distance | 42 to 374 mm | 162 to 374 mm |
| Motion direction | Toward the seat | Exactly opposite, same axis; distances similar but not copied (D8 54 = 54, D7 68 = 68, R2 30 = 30, capacitor 29 = 29; but D6 45 vs 64, Nano 31 vs 44, stems 62.5 vs 44) |
| Multi-stage moves | D3 tilt-in (2 steps), D10 clip (2 stages) | Flattened to one straight pull each |

One useful continuity: the build already uses the take-apart idiom for its two removal actions — peel the
backing (build [001]-[003]) and unscrew the nut (build [034]-[036]) are both "arrow on `Step N` -> auto
Transition moving the part away -> part hidden at `Nc`". The deconstruction guide is that idiom applied to
every step.

### 6.4 Other guides

Not examined in depth. Structure-only check of the other two take-apart guides shows the same shape:
`19075-lac_deconstruction` has 47 steps with 33 Transitions and no cards; `19075-piano-memory-game-deconstruction`
has 23 steps with 14 Transitions and no cards. LSM Parts 1-4 were not opened for this report.
