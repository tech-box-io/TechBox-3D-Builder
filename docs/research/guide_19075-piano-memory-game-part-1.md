# Guide report: Piano Memory Game (PMG) - Part 1

- guide id: `19075-piano-memory-game-part-1` (kit PMG, role: part). Viewer title: "Piano Memory Game(PMG) Part 1".
- sources read: `digest/19075-piano-memory-game-part-1.md` + `.json` (all 34 viewer steps), all 5 contact sheets, 22 individual thumbs, 8 full-resolution crops from `thumbs_raw` ([002] [004] [005] [006] [007] [009] [023] [032]), targeted queries on `cadasio_raw/19075-piano-memory-game-part-1.json`, and the digests of the four sibling PMG guides for comparison.
- crops and query scripts are in `reports/_work_pmg_p1/` (`q1.py` ... `q8.py`, `crop.py`, `bbox.py`, `c0NN.jpg`).

## 1. Summary

Part 1 is a pure electronics/wiring guide with 34 viewer steps (31 `pause`, 3 auto-advancing `play`; every step 800 ms; 6 further hidden authoring steps). The student (a) plugs an Arduino Nano into the blue "Nano I/O Module" expansion shield, (b) takes a 12-way female-female jumper ribbon and separates it into 12 single wires, then (c) wires four push-button modules (black, yellow, white, blue caps) to the shield's D4-D7 header columns, three wires per button (VCC->V, OUT->S, GND->G), one wire per numbered step. There is no wood, no screw and no enclosure in this part; the button modules float in space at the positions the enclosure will give them in Part 3. The guide has 14 numbered steps, two unnumbered section cards with real-photo insets ("Nano I/O Module", "Push Buttons"), three "Transition" steps and a "Completed View". No step has a text description or popup: everything is said with the 3D scene, two short pin labels per wire, an eye icon, and (once) four red lead lines. The camera moves on only 6 of 34 steps and then stays completely fixed for the whole 27-step wiring run. Part 1 is, step for step, the first 34 viewer steps of the PMG full build.

## 2. Step table (every viewer step)

Camera notation: d = distance mm, e = elevation deg (90 = straight down), az = azimuth deg; "same" = camera unchanged. Label/eye positions are the stored `screen (x, y)%` (see caveat D3 in section 5). "Parts" = top-level components visible after the step.

| idx | name | kind | what is added / done | annotations | camera |
|---|---|---|---|---|---|
| [000] | Start | title page (pause) | Finished Part-1 assembly (42 parts: shield, Nano, 4 button modules, 12 routed wires, 24 black wire housings) shown right of centre. Nothing to do. | 2 unanchored 2D images: TechBox logo SVG top-left (w 39.5, at 2,8%); title PNG lower-left (w 46.5, at 2,65%) reading "Piano Memory Game (PMG)" / "Part 1" / "(c) 2026 TechBox. A division of TARIS Industries, LLC. All Rights Reserved." | MOVES (from file default) to d148 e22 az-60 |
| [001] | Nano I/O Module | section card (pause) | Everything hidden except the shield (1 part), seen in plan. Nothing to do: learn the silk-screen (rows G/V/S, columns by pin number). | 1 framed real photo of the shield with small grey caption "NANO I/O MODULE LABELS" (a text label holding an image, 899x864 px, light-blue rounded rectangle, drop shadow; stored at 50,13%), to the right of the 3D shield; light-blue leader + dashed ring on the PCB's right edge. 3D shield is oriented exactly like the photo (DC jack lower-left). | MOVES: rot 68 deg to d133 e90 (top-down) az90 |
| [002] | Step 1 | hover | Arduino Nano fades in 29.8 mm straight above its seat on the shield's two 15-way socket strips; USB end on the DC-jack side. 2 parts. | 4 red lead lines, vertical, 25.7 / 26.6 / 26.5 / 28.7 mm, from the 4 corner pin tips of the Nano's two header rows to the 4 end holes of the two black socket strips. No label, no eye. | MOVES: rot 56 deg to d142 e34 az-70 |
| [003] | Step 1c | completed | Nano tweens 29.8 mm straight down -> seated. | none | same |
| [004] | Step 2 | part ID / prep, before | Shield + Nano hidden. The 12-way jumper ribbon alone (12 wires + 24 housings = 36 components), flat. | 1 black eye icon (w 8.2, at 58,26%) to the right of the ribbon; light-blue leader from the eye's left tip to a ring mid-length on the ribbon (yellow wire). | MOVES: rot 28 deg to d128 e49 az-37 |
| [005] | Step 2c | prep, after | The 12 wires fan apart sideways (per-wire X moves from -17.3 to +16.9 mm, about +3.1 mm extra gap per wire, bundle about 34 mm wider) = "separate the ribbon into 12 single wires". | none | same |
| [006] | Push Buttons | section card (pause) | Wires hidden. One push-button module (black cap) fades in alone, already at its final pose. Nothing to do: learn its 3 pins. | 1 framed real photo of a button module (image w 17.15, at 59,19%; light-blue rounded frame) with a red box around the silk-screen "VCC OUT GND"; leader + ring (orange #ff5F0B, the only non-blue ring) on the 3D module's middle pin. | MOVES: rot 50 deg, zoom x2.96 to d43 e17 az-85 |
| [007] | Step 3 | wire, before | Shield + Nano fade back in (button 1 stays). Loose straight red wire parked lower-left of the model. 6 parts. | labels "VCC" (51,28%; ring on button 1 left pin) and "V4" (57,43%; ring on shield header pin); eye (28,45%) with leader + ring on the wire's mid-point. | MOVES: rot 22 deg, zoom x0.25 to d173 e21 az-62 |
| [008] | Step 3c | wire, after | Loose red wire fades out; routed red wire + 2 black housings fade in seated (button 1 VCC <-> V4). | none | same |
| [009] | Step 4 | wire, before | Loose white wire parked at the same spot. 9 parts. | "OUT" (52,25%; middle pin), "S4" (58,44%), eye (28,48%). | same |
| [010] | Step 4c | wire, after | Swap to routed white wire (OUT <-> S4). | none | same |
| [011] | Step 5 | wire, before | Loose dark-grey wire. 12 parts. | "GND" (53,26%; right pin), "G4" (56,43%), eye (26,46%). | same |
| [012] | Step 5c | wire, after | Swap to routed dark-grey wire (GND <-> G4). Button 1 fully wired. | none | same |
| [013] | Transition | auto-advance (play, 800 ms) | Button 2 (yellow cap) fades in at its final pose, bare pins. 13 parts. | none | same |
| [014] | Step 6 | wire, before | Loose bright-green wire. 16 parts. | "VCC" (56,29%), "V5" (59,43%), eye (27,45%). | same |
| [015] | Step 6c | wire, after | Routed green wire (button 2 VCC <-> V5). | none | same |
| [016] | Step 7 | wire, before | Loose brown wire. 19 parts. | "OUT" (56,26%), "S5" (60,46%), eye (26,46%). | same |
| [017] | Step 7c | wire, after | Routed brown wire (OUT <-> S5). | none | same |
| [018] | Step 8 | wire, before | Loose yellow wire. 22 parts. | "GND" (57,27%), "G5" (57,44%), eye (27,43%). | same |
| [019] | Step 8c | wire, after | Routed yellow wire (GND <-> G5). Button 2 fully wired. | none | same |
| [020] | Transition | auto-advance (play) | Button 3 (white cap) fades in, bare pins. 23 parts. | none | same |
| [021] | Step 9 | wire, before | Loose maroon wire. 26 parts. | "VCC" (61,34%), "V6" (59,47%), eye (26,46%). | same |
| [022] | Step 9c | wire, after | Routed maroon wire (button 3 VCC <-> V6). | none | same |
| [023] | Step 10 | wire, before | Loose grey wire. 29 parts. | "OUT" (62,28%), **"S5"** (65,52%) - typo, the wire goes to S6 - eye (30,50%). | same |
| [024] | Step 10c | wire, after | Routed grey wire (OUT <-> S6). | none | same |
| [025] | Step 11 | wire, before | Loose blue wire. 32 parts. | "GND" (62,30%), "G6" (62,46%), eye (27,47%). | same |
| [026] | Step 11c | wire, after | Routed blue wire (GND <-> G6). Button 3 fully wired. | none | same |
| [027] | Transition | auto-advance (play) | Button 4 (blue cap) fades in, bare pins. 33 parts. | none | same |
| [028] | Step 12 | wire, before | Loose pink-purple wire. 36 parts. | "VCC" (67,32%), "V7" (60,47%), eye (30,46%). | same |
| [029] | Step 12c | wire, after | Routed pink-purple wire (button 4 VCC <-> V7). | none | same |
| [030] | Step 13 | wire, before | Loose red-orange wire. 39 parts. | "OUT" (62,30%), "S7" (59,45%), eye (30,46%). | same |
| [031] | Step 13c | wire, after | Routed red-orange wire (OUT <-> S7). | none | same |
| [032] | Step 14 | wire, before | Loose teal-green wire. 42 parts. | "GND" (65,31%), "G7" (64,48%), eye (24,43%). | same |
| [033] | Completed View | final view, doubles as "Step 14c" | Swap to routed teal-green wire (GND <-> G7). Nothing else changes. 42 parts. | none | same (no camera move) |

Totals: 1 title + 2 section cards + 14 `Step N` + 13 `Step Nc` + 3 `Transition` + 1 `Completed View` = 34. Camera moves on 6 of 34 steps ([000] [001] [002] [004] [006] [007]). Annotations actually shown: 4 lead lines, 24 pin labels, 13 eye icons, 2 framed photo insets, 2 title images, 0 arrows.

Wiring map as built (button order is left to right as seen in the wiring view):

| button (cap) | VCC wire -> pin | OUT wire -> pin | GND wire -> pin |
|---|---|---|---|
| 1 black | red -> V4 [007] | white -> S4 [009] | dark grey -> G4 [011] |
| 2 yellow | bright green -> V5 [014] | brown -> S5 [016] | yellow -> G5 [018] |
| 3 white | maroon -> V6 [021] | grey -> S6 (labelled "S5") [023] | blue -> G6 [025] |
| 4 blue | pink-purple -> V7 [028] | red-orange -> S7 [030] | teal green -> G7 [032] |

## 3. Conventions found

### Structure
- **S1. Fixed skeleton** (always): `Start` -> [section card] -> numbered pairs -> `Completed View`.
- **S2. Numbered steps come as pairs** `Step N` / `Step Nc`: `Step N` is the annotated "before" (part hovering, or loose part presented), `Step Nc` is the same scene after the action. 13 of 14 steps have a literal `Nc`. Exception: Step 14 [032] has no "Step 14c"; `Completed View` [033] performs the Step-14 wire swap (see anomaly A2).
- **S3. `c` steps are always clean**: 0 annotations in all 13 `Nc` steps, the 3 Transitions and the Completed View (17/17). Every annotation introduced in `Step N` is removed on the very next step (14/14). Nothing persists across a pair boundary.
- **S4. Section cards** ([001] "Nano I/O Module", [006] "Push Buttons"; 2/2): named after a component (not "Step"), unnumbered, `pause`, placed immediately before the first step that uses that component's pins, show the component alone (1 part on screen), and carry one framed real photo that shows the printed pin names. They ask for no action.
- **S5. Numbering is continuous (1-14)** and is not consumed by cards, Transitions or the final view. A preparation action does consume a number (Step 2 = separate the ribbon).
- **S6. No text**: 0 of 34 steps have a description; 0 popups. Step names are the only prose ("Step 3", "Step 3c", "Transition", "Completed View").
- **S7. Hidden authoring steps exist and are invisible to the student**: 6 of 40 authored steps (`Step 143`, `Step 144`, a hidden `Start`, `Step 148`, a hidden `Step 1`, and a trailing `Step 21c` after the Completed View).

### Granularity
- **G1. One wire per numbered step, always** (12/12: Steps 3-14). A "wire" is 3 components: wire body + 2 black Dupont housings; they always appear together. Wires are never grouped, even though three consecutive wires go to the same button and the same header column.
- **G2. One rigid part per step** for the plug-in board (Step 1: Nano only).
- **G3. The only multi-part step is a kit item that physically arrives as one piece**: the 12-wire ribbon in Step 2 (36 components shown as one object), and its `c` step separates it.
- **G4. Parts that the student does not attach get no step number**: the 4 push-button modules are never "added" by a numbered step. Button 1 arrives on the "Push Buttons" card [006]; buttons 2-4 fade in during the auto-advancing Transitions [013] [020] [027] (3/3). The shield, as the base part, is simply present from [001].

### Ordering
- **O1. Base electronics first**: Nano onto shield (Step 1), then wire prep (Step 2), then all wiring.
- **O2. Peripherals in spatial order**: buttons left to right (black, yellow, white, blue), which is also ascending pin number D4, D5, D6, D7 (4/4).
- **O3. Within a peripheral, wires follow the module's physical pin order left to right**: VCC, OUT, GND (4/4 buttons, 12/12 wires). It is therefore power, signal, ground - not "all power first" and not "ground first".
- **O4. One peripheral is completed before the next appears** (3 wires, then Transition; 3/3).
- **O5. Wire colours are consumed in ribbon order**: the k-th wire of the Step-2 ribbon (red, white, dark grey, bright green, brown, yellow, maroon, grey, blue, pink-purple, red-orange, teal) is the wire used in Step k+2 (12/12). Colour has no electrical meaning (VCC is red, green, maroon, pink-purple on the four buttons).

### Motion
- **M1. Rigid plug-in part: hover then drop** (1/1): the Nano first appears 29.8 mm straight above its seat (+Y only, no sideways offset, no tilt) in Step 1 and tweens straight down in Step 1c. The hover gap is about two thirds of the Nano's 45 mm length; pin tips clear the socket tops by about 26-29 mm.
- **M2. Wires never travel** (12/12): in `Step N` the loose, straight wire is shown parked at a fixed staging spot (camera-left/front of the shield, lying flat and parallel to the shield's header edge; stored offset from its CAD pose [-75.6, +27.8, -25.6] mm, drifting about 1.75 mm per step because each wire sits in its own ribbon slot). In `Step Nc` the straight model fades out and a separate pre-routed (curved) model fades in already seated: APPEAR + DISAPPEAR, 0 MOVE.
- **M3. Context parts fade in seated**: all 4 button modules appear "already in seated pose" ([006] [013] [020] [027]).
- **M4. Preparation is shown as a before/after pair of the part on its own**: ribbon whole [004] -> wires fanned apart [005] (the only step where many parts move at once: 36 components, pure sideways translations).
- **M5. Uniform timing and easing** (34/34): 800 ms; show/hide = fade; move = tween; camera = tween, no orbit animation. No rotation is animated in any viewer step.

### Lead lines and arrows
- **L1. Red lead lines are used only for the rigid insertion** (Step 1 [002]): exactly 4, colour #ff0000, solid, thin, perfectly vertical, one at each corner pin of the Nano (pin 1 and pin 15 of both rows; 15.3 mm x 35.6 mm rectangle), each starting at the pin tip and ending on the top of the matching end hole of the black socket strip (2 lines per strip). Lengths 25.7-28.7 mm = 86-96% of the 29.8 mm hover offset (the line stops at the socket's top face; the pin continues into it). They vanish in Step 1c.
- **L2. Wires get no lead lines** (0/12) and nothing draws the wire's path; the two end labels replace them.
- **L3. No arrows** are shown anywhere (0/34).

### Labels and callouts
- **C1. Every wire step has exactly two text labels, one per wire end** (12/12 steps, 24 labels): the peripheral-end label is the pin's printed name on the module ("VCC", "OUT", "GND"), the shield-end label is row letter + pin number ("V4", "S4", "G4", ...). Text is 2-3 characters, upper case, no sentences.
- **C2. Label style is constant** (24/24 visually): bold black text (3em on a 20 px base, cap height about 5% of viewport height) sitting on a light-blue #7fdbff underline (5 px), 175x90 px box (6.8% of the width of the 2560 px saved render), white fill; a 5 px light-blue leader leaves the left end of the underline and ends in a 30 px dashed "life-saver" ring on the target.
- **C3. Ring targets are the exact pins**: the module's own pin for the peripheral end (left pin = VCC, middle = OUT, right = GND) and the specific header pin on the shield (row R/B/N header block for V/S/G). At this camera distance the ring spans about two pin pitches, so V4/S4/G4 rings look almost identical; the text carries the information.
- **C4. Label placement**: both labels sit to the right of the model, stacked: peripheral-end label above (stored x 51-67%, y 25-34%), shield-end label below (x 56-65%, y 43-52%). The upper label drifts right as buttons are added further right. Leaders run down-left to the pins and do not cross each other.
- **C5. Eye icon = "pick up / look at this loose part"** (13/13: the ribbon in Step 2 and each of the 12 wires): a black eye PNG, width 8.2% of the viewport, light-blue leader from the eye's nearest tip to a ring on the part's mid-point. For wires it sits above-left of the parked wire, on the side away from the model (stored x 24-30%, y 43-50%); for the ribbon it sits to the right. It is not used for the Nano (which has lead lines instead) and never appears on a `c` step.
- **C6. Photo insets on section cards** (2/2): real product photo in a light-blue rounded-rectangle frame (5 px border, white fill) placed to the right of the 3D part, with a leader + ring back to the 3D part; the 3D part is posed to match the photo. The button photo additionally has a red rectangle drawn around the pin silk-screen.
- **C7. Title page layout**: logo top-left, title/part/copyright block lower-left, finished model for this part on the right; both images are unanchored 2D overlays.

### Camera
- **K1. The camera moves only when the subject changes**: 6 of 34 steps ([000] title, [001] card, [002] Step 1, [004] Step 2, [006] card, [007] Step 3). It never moves on a `c` step (0/13), on a Transition (0/3) or on the Completed View.
- **K2. One fixed view for an entire wiring run**: from [007] to [033] (27 consecutive steps) the camera is d173 e21 az-62. It is framed from the first wire for the final 4-button assembly (the model fills about 52% of viewport height and sits just right of centre), leaving room on its left for the eye + parked wire and on its right for the two labels. There is no per-wire zoom to the pin.
- **K3. Close-ups are reserved for cards and single-part steps**: plan view (e90) for the shield card so it matches the photo; near face-on close-up (d43, x2.96 zoom) for the button card; three-quarter views for Step 1 (e34) and Step 2 (e49). The subject fills more of the frame than in the wiring view: 68% of viewport height on the shield card, 71% in Step 1, 73% on the button card, 46-62% for the ribbon.
- **K4. Isolation**: on cards and on the ribbon step everything else is hidden ([001] 1 part, [004]-[005] wires only, [006] 1 part); the full context fades back in on the next assembly step ([007]).
- **K5. Transition steps here are not camera moves**: all 3 are `play`, 800 ms, camera unchanged, no annotations; each only fades in the next button module so that the following step can introduce its first wire. Because they are `play` steps, one press of Next on `Step 5c` runs two 800 ms beats (button appears, then wire + labels appear) and stops on `Step 6`.
- **K6. Perspective camera, FOV 45**, view cube enabled, navigation bar at the bottom, auto-start on.

### Look
- **V1.** Pure white background, no ground plane, no shadows; every solid is toon-shaded with thin black edge lines (5367 solids with style `toon`, edges `normal`).
- **V2. Annotation colour code**: red = lead lines only; light blue #7fdbff = every callout (underline, leader, ring, photo frame); black = label text and the eye icon.

## 4. Part looks

| part | look in the renders |
|---|---|
| Nano I/O shield PCB | flat royal blue (#224bbe), white mounting holes, row of tiny holes along the edges, black outline |
| Shield 15-way female socket strips (x2) | black (#181818) blocks with square holes |
| Shield 3-row pin header blocks | pale yellow/cream plastic bases (#ffff80, a few #fffc9f) with light-grey/silver pins (#e3e3e3) |
| Shield DC barrel jack, capacitor, regulator, small SMD parts | jack black with silver (#c0c0c0) contacts; capacitor can black (#191919); small parts light grey/white (#e5eaed, #d8d8d8, #d1d1d1) |
| Arduino Nano | navy PCB (#000f41), black header strips and ICs (#191919), silver/white pins and pads (#e4e4e4), white/silver mini-USB shell (#e4e4e4, #d3d6d3), tan capacitors (#a5936d), 2x3 pin header at the end opposite the USB |
| Push-button module | navy PCB (#000f41), black tactile-switch body (#1e1e1e), large round cap in the button's colour - black #000000, yellow #ffdc00, white #ffffff, blue #0074d9 - black pin-header base (#1a1a1a) with 3 right-angle silver/off-white pins (#c6c1bc) pointing down |
| Jumper wires | single-colour round tube with black outline; 12 colours: red #b70101, white #e4e4e4, dark grey #343232, bright green #21f17a, brown #7c5a30, yellow #ffdc00, maroon #85144b, grey #737980, blue #3876ac, pink-purple #a75294, red-orange #ff4136, teal green #3d9970. Loose = straight; installed = smooth hand-routed curve |
| Wire end housings (Dupont) | flat black (#000000) rectangular blocks, one per wire end, with a tiny window showing the wire colour (loose wire) or a light notch (installed) |
| 12-way ribbon (Step 2) | the 12 straight wires side by side; the 12 housings at each end read as one black bar with 12 coloured dots |
| Lead lines | thin solid red #ff0000 |
| Labels | bold black text on a light-blue #7fdbff underline, light-blue leader and dashed ring |
| Eye icon | solid black eye glyph with white iris ring, no frame |
| Photo insets | colour photograph in a light-blue rounded frame on white |
| Title page | cyan TechBox logo block (white wordmark), dark grey condensed title text, small serif copyright line |

## 5. Anomalies

- **A1. Wrong label text in Step 10 [023]**: the shield-end label reads "S5" but the wire (button 3 OUT) goes to S6. "S5" is therefore shown twice ([016] and [023]) and "S6" never. The same error is in the full build.
- **A2. No "Step 14c"**: the last pair is `Step 14` [032] -> `Completed View` [033]. The Completed View is the full build's "Step 14c" renamed: same camera as the previous 26 steps, it still performs the last wire swap, and there is no separate beauty-shot camera move (Part 2, Part 3 and the full build all have a real final `Nc` followed by a Completed View that moves the camera).
- **A3. Orange anchor ring on the "Push Buttons" photo inset [006]** (#ff5F0B) while every other ring in the guide is light blue #7fdbff.
- **A4. Two implementations of the same card inset**: [001] is a text label containing an embedded image plus caption (rectangle container, drop shadow on); [006] is an image annotation with a rectangle container (no shadow, no caption).
- **A5. Inconsistent anchoring object**: the "V4" label [007] is linked to the socket-strip part (`Samtec-SSW-115-01-F-S-4`) whereas V5/V6/V7 are linked to the R-row header block (`Samtec-TLW-104-01-F-S_R-3`). On screen the ring still lands on the header pin.
- **A6. Leftovers from the full-build file**: 88 of the 133 annotation objects in the project are never shown in this guide (44 lead lines, 22 images, 20 labels incl. "CLK", "DIN", "dio", "s9", and both arrows); hidden steps named `Step 143`, `Step 144`, `Step 148`, `Step 21c`; project step counter at 150. Part tooltips are enabled but every tooltip is the placeholder "Description" / "none".
- **A7. Button modules float unsupported**: with no enclosure in Part 1 the four modules hang in mid-air, pins down, at their full-build positions; one routed wire (Step 13, red-orange) makes a visible hook over the Nano.
- **A8. White wire on white background** ([009] [010]): only its black outline is visible.
- **A9. Mixed thumbnail aspect ratios**: saved renders for [000] [001] [033] are about 2:1 (3840 px wide), all others 2.79:1 (2560x919). [033] therefore looks more zoomed-in than [032] although the camera is identical.

Data-reading caveats (not authoring errors):
- **D1.** "parts still displaced: Ensamblaje_Shield_NANO" appears on every step. This is a permanent internal correction of the shield model (PCB, sockets and a few SMD parts repositioned relative to the header blocks in the hidden setup steps), not a hover.
- **D2.** The digest counts only 32 of 185 shield solids as visible, because the header-block sub-assemblies have `visible:false` on their parent node while their solids are `true`; the renders show the header blocks from [001] on.
- **D3.** Stored `screen (x, y)%` values were authored for a roughly 2:1 viewport. In the 2.79:1 saved renders the same items sit at about x = 50 + 0.71 * (x - 50); y is unchanged. Label positions are the top-left of the 175x90 px box.
- **D4.** Two labels ("V5" [014], "G7" [032]) and the eye of [032] have a partial leader record (digest prints "leader None"); they render with the normal light-blue leader.
- **D5.** The digest truncates the Step 2c move list to 10 groups; all 12 wires move.

## 6. Relation to the other PMG guides

- **Full build** (`19075-piano_memory_game_pmg-full_build`, 117 viewer steps): Part 1 is its viewer steps [001]-[033]. Steps [002]-[032] are identical in name, behaviour, camera, parts and annotations (31/31 no differences); [001] differs only in the stored position of the photo label (50,13% vs 54,17%); [033] differs only in name ("Completed View" vs "Step 14c"). The title page differs (Part-1 sub-assembly at d148 vs whole kit at d320). The "S5" typo is in both.
- **Part 2** (27 steps) = full-build steps 15-25 renumbered 1-11; **Part 3** (59 steps) = full-build steps 26-51 renumbered 1-26. Numbering restarts at 1 in every part.
- Part 2 continues the same wiring grammar on the same shield (2 labels + eye per wire, clean `c` step, one fixed view per wiring run - d173 for the 4-digit display, d202 for the dot matrix - and a section card with a photo before each new module). It confirms rule O3: wires follow each module's physical pin order (4-digit display: clk, dio, VCC, GND - signals first; dot matrix: VCC, GND, DIN, CS, CLK - power first). Part 2 uses lower-case text on four labels ("clk", "s8", "dio", "s9") where Part 1 is upper case throughout.
- Transitions: in Part 1 all 3 fade in a part. In Part 3 / the full build the later ones carry either a part move (3) or a batch of parts appearing (2). None of the 8 Transitions in the PMG build guides moves the camera; in the deconstruction guide 2 of 14 do.
- Part 1 has no wood, screws or mechanical lead-line work; those conventions have to come from Part 3.
