# TechBox build-guide rulebook

How TechBox's published Cadasio guides are authored, written down as rules so that new guides
(construction and deconstruction) follow the same conventions without anyone having to re-derive them.

**Source.** All 20 guides published at instructions.online as of 2026-10-13: Laser STEM Matrix (LSM, 8 guides),
LCD Alarm Clock (LAC, 7) and Piano Memory Game (PMG, 5); 1,037 step views. Each guide was read from its published
data and its step pictures; every rule below was then re-checked against the data by a second, independent pass (189 rules: 103 held as stated, 86 were narrowed, none was thrown out).
The numbers, exceptions and verdict behind each rule are in [cadasio-patterns-evidence.md](cadasio-patterns-evidence.md);
the per-guide and per-topic working reports are in [research/](research/).

**How to read it.** "Always" means no counter-example was found in the 20 guides. "Usually" gives the count.
PMG is the newest kit and LSM the oldest; where they differ, the newer habit is the one to follow unless noted.
Section 13 lists the places where the published guides disagree with each other, which are decisions for TechBox.
Section 14 says what the in-house player does today against each rule.

---

## 1. The rules that matter most

1. **One kit item per numbered step.** One part, one wire, one fastener, or one hand action. Never two different parts in motion.
2. **Every numbered step is a pair.** `Step N` shows what is about to happen and waits. `Step Nc` shows it done and waits.
3. **One wire per step, never grouped.** A loose jumper is one step for both of its ends.
4. **A part hovers along the way it really goes in**, then travels home in one straight move. Not from "above" by default.
5. **Red lead lines join mating features**: tab tip to slot, pin to hole, screw to hole. 1, 2 or 4 per step.
6. **The camera never moves inside a pair.** It is set on `Step N` and held through `Step Nc`.
7. **Nothing is ever recoloured or highlighted** to draw attention. A part looks the same new, hovering and seated.
8. **Almost no text.** The only text on the canvas is a 2-3 character destination name (a hole, a pin). No sentences, no part names on mechanical steps.
9. **The eye icon means "this one"**: the thing to pick up, or the detail to check.
10. **Bench work is shown on its own.** Preparing a part or building a sub-assembly hides everything else.
11. **Anything with wires attached is never slid into place.** It is shown in one pose, then in the next.
12. **Taking apart is the build run backwards, but coarser**, with red arrows instead of lead lines.

---

## 2. The skeleton of a guide

- A guide is `Start`, then section cards / numbered pairs / Transitions, then `Completed View`. Nothing else. (Always.)
- **`Start`** is the title page: logo top-left, a title block bottom-left (kit name with its acronym in brackets, the guide variant such as "Part 2", the copyright line), and the finished model *of this guide* in the right half. (19 of 19.)
- **`Step N` / `Step Nc`.** Lower-case `c` for "completed". Both wait for the student. Numbers run 1..N with no gaps, restart at 1 in each Part guide, and run continuously through a Full Build.
- **Every hand action gets a number**, including ones that add no part: peel a backing, bend leads, split a ribbon, swing a panel shut, pick something up. About a quarter of all steps add no part.
- **Section cards** are un-numbered and named after a component ("Nano I/O Module", "Push Buttons"). They show the component alone, close up, usually with a framed photo of the real part with the relevant pins boxed in red. They come directly before the component's first use. Used for bought-in modules whose pins the student must identify; never for wood, the Nano or the breadboard.
- **`Transition`** steps advance on their own (no click), are hidden from the step list, and hide the navigation bar while they play. They are used for the middle of a motion that needs more than two keyframes (the first leg of a two-leg fit, a part sliding off before it fades). Occasionally one sits between two numbered steps for a big camera re-orientation the student should not have to click for.
- **`Completed View`** is one last waiting step that only moves the camera: a clean three-quarter view of the result, usually from the title page's side, with no annotations.
- **Every annotation lives for exactly one view.** On with a `Step N`, gone on the next. `Step Nc` is clean, except for an occasional single "check this" cue (5% of result views). (In-house exception, Lee, 2026-10-20: parts that can no longer be told apart once placed are named on `Step Nc`: section 13, the PMG.)
- **Timing is uniform.** Every change takes 800 ms: parts and annotations fade in and out, part moves and camera moves glide. Going backwards is animated too.
- **Parts and Full Builds.** A long build is cut into Parts of 5-26 numbered steps (median 13), each ending where a wiring run or a mechanical block is complete. A Full Build is the Parts run together: one `Start`, one `Completed View`, every section card kept, nothing inserted at the seams.
- **TechBox's Part guides (Lee, 16 Oct 2026).** A kit's Part guides (in the web addresses `<kit>-part-1`, `-part-2` ...) are cut
  from its Full Build: the core steps of a Part are the Full Build's steps, the same order, wording and cameras. What a Part has
  of its own is its title card / `Start` (the model as that Part shows it), its `Completed View` (the model as that Part leaves
  it) and its Parts List, which lists only the parts new in that Part, not those carried over from earlier Parts (Lee, 21 Oct
  2026: a part an earlier Part took off again and this Part puts back is listed again, as the MRA's servos, unplugged after the
  electronics test and fitted later; a sub-assembly an earlier Part only put together and set aside whole is not, as the Nano
  Board in the I/O module). A card only the Full Build has (the MRA's Testing Checklist) is in no Part. Step numbers
  restart at 1 in each Part. When a step in a Part is changed, ask whether the change also belongs in the Full Build (and so in
  every guide that shares the step) or in that Part only, and say which was done.
- **No instruction text outside the canvas.** Step descriptions and pop-ups are not used. Part names live in hover tooltips ("Housing Rear Side - Part D4").

## 3. What goes in one step, and in what order

- **One rigid part per placement step** (44 of 48 in the full builds; the rest are identical pairs). Two *different* parts in motion: never (0 of 48).
- **If the part in the student's hand needs a new part to go into, that receiver simply appears in place** in the same step; it does not get a step of its own. The base panel of every kit appears this way.
- **The hand-held piece is the one that moves**, even when the other piece is the new one.
- **Two identical parts** may share a step only on first placement, with the same motion, both clearly visible. Four identical posts were done 2 + 2 with a camera turn between.
- **A set of four or more identical drop-in parts** (64 LED stems, 4 piano keys, 4 button modules): show one in full, then one "do the rest" step where the others appear in place with a quantity cue ("64x"). A set of four can go either way (the four posts were 2 + 2); the divider is whether each part needs its own lead lines and viewpoint. Never used where each part needs its own destination label: identical modules are wired in full every time.
- **Every fastener gets its own step**, coming off and going on (15 of 15: knob, nut, washer). Refit order is the exact reverse of removal. *No published kit contains a screw*, so identical screws are a TechBox decision (section 13).
- **A fit that needs two motions is two stages**, never one long animation: either the second motion is its own numbered step, or it is chained by an auto-advancing Transition. (Hook in then swing shut; drop then slide to lock; leave proud then push home.) **In-house (Lee, 2026-10-19), the LSM's four D11 posts:** posts that pass through one panel into slots in another come down two by two only until their tabs reach the slots (each pair seen from the side its engraved codes face); then, the kit turned over and the lower panel (and the wall in front of it) see-through, all four are pushed home together as the panel turns solid again, and a close-up shows a tab through its slot.
- **Anything that arrives pre-assembled is one part**: a jumper with its two end housings, a switch with its leads, a module with its coin cell.
- **Preparation is its own numbered step, immediately before first use**, with the part alone on screen. A jumper ribbon is split into exactly the wires the next wiring run needs.
- **An already-wired sub-assembly usually takes two steps**: pick it up (eye icon), then attach it (lead lines).
- **Order.** Electronics on the open base first: carrier, controller, small plug-in parts, then all wiring. The USB cable is the last electrical step. Then the enclosure. Finish one module completely (mount, then every wire) before starting the next. Within a module, wire in the physical order of its pins, not "power first". Enclosure order follows dependency, not height: datum panel first, each support before what it carries, the panel that covers the interior last. Group work that needs the kit turned over into one block.

## 4. Motion

- **Two beats per rigid part.** It fades in standing still at its hover pose (`Step N`), then makes one straight move to its seat (`Step Nc`). It never moves while fading in, and never rotates during an ordinary insertion.
- **The hover pose lies back along the real insertion path**: straight up for anything that plugs into a breadboard or socket, along the tab axis for panels (often sideways), tilted for a panel that hooks in on one edge. Across 48 placements: down 50%, sideways 35%, oblique 10-13%, up 2%.
- **Hover distance depends on the kind of fit** (see section 12): about 35 mm for plug-in electronics, about 65 mm for a flat panel pushed face-on, about one part-length for a part that truly slides lengthwise (40-140 mm), about 80 mm for other wood, 60 mm for a nut or knob on its shaft, 80-100 mm for a panel-mount part with trailing leads. The distances were set by eye: identical parts differ by a few millimetres.
- **On screen the hovering part is always above or beside its seat, never below it.** When the real insertion is from underneath, the kit is shown turned over (section 7).
- **Hook-and-swing panels** arrive already tilted by their swing angle (8-26 degrees), slide in their own tilted plane until the tabs engage, then rotate flat about the engaged edge as a separate stage.
- **Wires are never animated into a connection.** `Step N` shows a loose, straight wire; `Step Nc` replaces it with a separately modelled, already-routed wire. (101 of 101.)
- **The loose wire is parked** flat and straight at one spot beside the assembly on the camera side, and that spot is reused for every wire of the run.
- **Wired things are moved by swapping poses**: complete copies (part + its routed wires) cross-fade. They are tweened only before any wire constrains them.
- **A change of shape** (bent leads, split ribbon) is a swap between two models of the part alone on screen.
- **Parts appear already seated when there is nothing to teach**: the rest of an identical set, free-standing modules introduced on a card, plugged cables.
- **A part carried in several moves is turned in the earlier move (Lee, 2026-10-19)**, so that the later one is just a lift and move (the LSM's LED matrix, turned on its way out over D4 in Step 26 rather than spun as it is lifted over the box in Step 30). A long carry plays a beat per stretch, its wires keeping pace (slower: the LSM's Step 31 in two beats).
- **A part that is set down before it goes in is set down in line with its way in (TechBox, Lee, 2026-10-16)**, so that the next step is one straight move with no sideways shift (the RCC's barrel plug, held in line with the power socket; the battery placed to allow it). A part carried over others to its seat clears what is already there (the RCC's right motor plug, carried high over the left one already on its header).
- **A removal inside a build** is hold, slide, fade: `Step N` shows it in place with an arrow, a Transition slides it off along its axis, `Step Nc` fades it out.
- **Threaded parts may spin** about half a turn while travelling, on a 1600 ms frame (LSM habit; not consistent). **In-house (Lee, 2026-10-19):** a nut coming off or going on turns as it travels, one or two whole turns over the move, unscrewing clockwise seen from the head: the idea of turning, not a true thread pitch (the LSM's push-button nut: two turns over two beats, a quarter turn a pose, so that a hexagon is never seen turning backwards).

## 5. Red lead lines and arrows

**Lead lines**
- Drawn on `Step N` whenever a rigid part is about to travel onto mating features. Removed as the part starts to move. Never on `Step Nc`.
- **Never drawn for wires**, ribbon splitting, lead bending, picking up a wired module, or "do the rest" steps.
- **1, 2 or 4 per step. Never 3 or 5; 4 is the maximum on all but two frames** (two older cuts of one LSM step show 6).
  - 1 for an axial part (nut, knob, button through its hole) or a single hook.
  - 2 for a two-lead component or a part with two tabs.
  - 4 for a flat body at its corners (breadboard onto base), a pin-header board at its four corner pins, or a panel closing onto two neighbours (2 lines per neighbour).
  - A panel with many tabs still gets at most 4: a representative few are drawn, not every tab, and which ones follows no fixed rule.
- **Each end is anchored to a part at a mating point**: one end at the tip of the male feature (tab tip, pin tip), the other inside the female feature (slot, hole). The ends follow their parts.
- **Straight, and parallel to the travel** (median 0.4 degrees off; 97% within 5).
- **Length is the gap between the features at the hover pose**, about 1.0 x the travel (78% within 15%). In a breadboard hole the line ends on the floor of the hole, about 7 mm down. In a plywood slot it ends in the slot; when it ends on the slot's far face it is shorter than the travel by the tab's protrusion (3.4 mm).
- A fit split over two numbered steps gets fresh lines on each (6 of 6). For two legs inside one step the guides vary: one bent line through the waypoints, or lines for the first leg only. Do not put new cues on an auto-advancing Transition (PMG does; they are on screen for 0.8 s).
- Lines are drawn straight through whatever lies between the features; nothing routes them around wiring.
- **Style:** pure red `#ff0000`, solid, thin, constant width on screen (5 px at the authoring size, about 0.2% of that view's width), no arrowhead, drawn in 3D so parts in front hide it.

**Arrows**
- A fat red 3D arrow is for a hand move with no mating features: peel, pull off, spread apart, carry over. And for every removal in a deconstruction guide.
- One arrow per part or per sub-assembly moved as one; two when two separate parts are handled; never more. Tail on the part, head in free space along the motion, about as long as the travel (median 51 mm).
- **Arrows and lead lines never share a step.** No curved or rotation arrows.
- Style: `#ff0000`, straight, flat; body : head width : head length = 5 : 20 : 17; sized in model space (body about 4 mm).

## 6. Labels, the eye icon, pictures and cards

**Text labels**
- **What they say:** only a destination, as printed on the hardware. A breadboard hole in lower case (`c15`, `i23`); a power rail as `(+) red` / `(-) blue`; a module or shield pin in capitals (`GND`, `VCC`, `SDA`, `V4`, `S4`, `G4`). 2-3 characters; rail labels are the long ones at 7-8. Never a sentence, a verb, a part name, a wire colour or a step number.
- **How many:** one per wire end being placed, two on screen at most. Only on `Step N`. (In-house exception, Lee, 2026-10-20: section 13, the PMG's push buttons named by colour on `Step Nc`.)
- **Never on mechanical steps.** 0 text labels across 173 wood and fastener steps. Wooden parts are identified by the code engraved on them.
- **Style:** bold black sans (Arial in LSM and LAC; PMG falls back to the viewer's default font), centred over a light-blue `#7fdbff` rule; one straight leader of the same blue and thickness from the end of the rule nearest the target; a dashed blue ring on the exact hole or pin. No box, no arrowhead.
- **Where:** in white space outside the model, normally above the target, never over the model and never in the bottom third of the view. With two labels the left label owns the left target and leaders never cross. A label follows its target from step to step rather than keeping a fixed spot.
- **Size:** text about 4% of the view height; rule about 8% of the view width; leader typically 19% of the view height at about 35 degrees.

**Eye icon**
- One black eye glyph, about 8% of the view's width, with the same blue leader and ring. One per step, two at most. **In-house
  (Lee, 2026-10-18):** it sits on a white box, as the labels do, so that it stands out over the model (on its own it had too
  little contrast where it fell over dark parts).
- The usual cue on `Step N` when the thing to act on is *not* shown by a hovering part with lead lines (79% of such views): the loose wire to pick up, a pre-wired module to pick up, a feature to notice on a card. And as the "check this" cue on a result view (wires through a notch, a tab locked in its slot).
- Every `Step N` carries at least one cue (423 of 425), and usually exactly one kind: lead lines, an eye, an arrow or an inset.
- Sits in the nearest white space, 15-35% of the view height from its target.

**Pictures**
- Any explanatory picture is a framed inset: white rounded rectangle, 5 px `#7fdbff` border, blue leader and ring to the feature, thin red rectangles inside marking the exact detail.
- A real product photo with the pin names boxed, on a module's section card. A close-up render in the guide's own style on a step (a hidden face, a latch to release, a result to check).
- **In-house (Lee, 2026-10-20):** a close-up sits on the side of the part its leader goes to, so that the leader does not cross the
  part (the LSM's capacitor picture, to the right of the capacitor).
- **In-house (Lee, 2026-10-20):** a part shown on its own beside a picture TechBox supplies is turned to match the picture (the LSM's
  capacitor, Step 6: its stripe on the left and the GND leg left, as Lee's picture), its labels placed as the picture's (under the
  legs), and the step that puts it in is seen the same way round (Step 7).
- **In-house (Lee, 2026-10-19, second round):** a close-up of something under a part draws that part faintly (about a 90% fade) rather than leaving it out, and is seen from where the detail reads (the LSM's Step 32: the matrix faint over the wires in D10's slot, seen along the slot). A picture supplied by TechBox can be the close-up (the LSM's Step 6, the Capacitor breakout picture). A close-up never covers the step's labels or eyes (Step 14), nor its arrows (in-house, 21 Oct 2026: the LSM deconstruction's four D11 posts, one arrow hidden behind the close-up of a tab).
- **In-house (Lee, 2026-10-19):** a part whose way round matters gets a step of its own first, alone in the hand, its legs labelled and a close-up of its mark with a red box (the LSM's capacitor: GND (-) and +, the grey stripe), in place of the published Capacitor card; a module's pins are shown on the module itself, turned to show them, labelled as printed, with a close-up (the LSM's LED matrix, its label V- IN V+), in place of a diagram card. The model carries the printing (a decal), so it matches the photographs.
- **In-house (Lee, 2026-10-21):** a wire's `Step Nc` may have a close-up from above of the pin it has just gone onto, the new cap (or wire end) boxed in red among those already in, where Lee asks for one or the pin cannot be made out from the step's view (the LAC's Step 39c, b9, seen from nowhere in front; the PMG's Steps 17 - 20, the 4-digit display's wires on the I/O module, asked for by Lee "similar to a breakout image you did in the LAC", and Steps 21 - 25, the dot matrix display's, "the breakout highlight of the pin location, like you did on 17-20"). Not a rule for every wire: the PMG's button wires onto the same header have none. The close-up sits on the pin's side of the model, its leader not across the module (Steps 19c - 20c); where that side holds the wire's other device, on the other side, its leader along the module's edge (Steps 21c - 25c: on the left it covered the dot matrix display, in a narrow window its header too).

**Never annotated:** the final view; wooden panels with text; wire colours; part names or values; the route of a wire; step numbers; warnings, ticks, tools or hands.

## 7. Camera

- One lens everywhere: perspective, 45 degree field of view, no roll, 800 ms glide between views.
- **Set only on entering `Start`, a card, a `Step N` or `Completed View`.** Never on `Step Nc` (0 of 424), never on a Transition inside a pair.
- **A three-quarter view from above**: elevation about 34 degrees (20-50 on 87% of steps), looking at a corner of the model (LSM and LAC; PMG is freer).
- **Look across the motion, never along it.** The travel axis is at least 40 degrees off the view axis (45 or more on 96%), so the hover gap and its lead lines are seen side-on.
- **Keep the whole action in frame**: the hovering or loose part and where it is going. Centre on the destination and let the hovering part ride above it. Idle parts may be cropped.
- **Do not zoom in on a small part in context.** Distance follows the whole assembly on screen (content fills about 60% of the view height), stepping back as the build grows. Close-ups happen only with everything else hidden: cards, preparation, sub-assembly work. (TechBox's exceptions, decided 2026-10-13: the first fastener of a set, and a wire going into a slot or onto a pin. See section 13.)
- **Hold one camera for a whole wiring run** (86% of consecutive wire steps). For rigid inserts expect a new camera about two times in three, chosen for that joint.
- **The one hard trigger for a new camera** is an action that would not fit in the current frame.
- **To work on the underside, the kit is shown turned over** (the scene's "up" is re-declared) and still viewed from above. The camera never goes below the horizon, the model is never rotated, and no "flip it" graphic is shown.
- `Completed View`: centred three-quarter view, elevation about 39 degrees, title-page distance or a little closer.

## 8. Look, and the colour library

- **White background. Flat two-tone shading. Thin black edges** (crease angle 40 degrees, the "40" on Cadasio's Toon setting, used for every part; PMG softens jumper wires to 69). No shadows, floor, textures, gloss or highlight colour. One light from above and to one side; faces turned towards it get the lit tone (about 1.2 x the base colour), the rest the shaded tone (about 0.95 x).
- **Printed and engraved markings are flat decals with their own colour**, never textures.
- **Transparency is used once in 20 guides** (two panels at 50% to see post tips through them).
- **Red `#ff0000` is reserved for motion** (lead lines, arrows, highlight boxes inside pictures). **Light blue `#7fdbff` is reserved for pointing** (label rules, leaders, rings, picture frames). Text and the eye are black.

| Part or feature | Colour |
|---|---|
| Laser-cut wood | `#deb887` |
| Engraved part code, black plastic, black boards | `#1e1616` |
| Cable jackets, black leads | `#2d2926` |
| Metal (pins, shells, hardware) | `#a6a9aa` (PMG pins `#e4e4e4`) |
| Arduino Nano board; Nano I/O module (shield) board (Lee, 2026-10-14: section 13); PMG button boards | `#000f41` |
| 4-digit display board (and, in the published models, the Nano I/O module's board) | `#224bbe` |
| I/O module header blocks (every row, whatever the CAD names it) / their pins / socket strips | `#ffff80` / `#e3e3e3` / `#181818` |
| RTC board, resistor bodies, breadboard (-) rail | `#0074d9` |
| LCD board / bezel / glass | `#1a7e26` / `#1e1616` / `#cccccc` |
| IC bodies | `#191919` |
| Breadboard body / legends / (+) rail | `#ffffff` / `#000000` / `#ff0e00` |
| Pre-wired leads | red `#ef3340`, tan `#b28362`, black `#2d2926` |
| Dupont housings / pins | `#1e1616` / `#a6a9aa` |
| Jumper wires | one saturated colour each, in ribbon order (identity only, not function) |
| Logo panel | `#00b0ef`; title text `#585858` |

## 9. Wiring

- **One wire per numbered step** (100 of 103). Loose jumper: both ends in one step, two labels. A lead already attached to a component: its free end, one label.
- **The cue set for a wire step is fixed**: one eye icon on the wire to pick up, plus one label per end being plugged in. Nothing else: no lead lines, no arrows.
- `Step N` shows the wire loose and straight; `Step Nc` shows it routed. Same camera. No annotation on `Step Nc`.
- **Wire colour identifies the wire, nothing more.** Colours come from the ribbon order. Never rely on colour to mean power or ground (the published guides contradict convention in places).
- **Each ribbon gets its own preparation step** before the run that uses it: the ribbon alone with an eye icon, then its wires separated.
- **Each module whose pins appear on labels gets a section card** with a photo of the real board and the header boxed in red.
- **One module at a time**, in the physical order of its pins.
- **Anything that plugs into the breadboard or a socket** (Nano, resistor, capacitor) is a rigid part: hover about 35 mm straight above, lead lines to the end holes, the two end holes labelled.
- **Connector gender is modelled correctly**: male pins into breadboard holes, female housings onto header pins. Every housing is black.
- **All wiring is done on the open base before any enclosure wall is fitted.** Modules that mount to the enclosure are wired loose and mounted later.
- **Hold one camera for the run**; do not zoom to the pin. (In-house, Lee 2026-10-13 and 2026-10-19: punch in where a wire has to be seen going into its hole, from a corner where nothing hides the hole.)
- **In-house (Lee, 2026-10-19): wires never pass through parts or through each other**, at rest or while they move: a lead that runs under a part in the real kit is drawn under it (the LSM's matrix wires under the engraved end of the D9 nearer D4, and in through the slot in D10). `tools/wirecheck.py` checks every view, `tools/motioncheck.py` every move (the LSM's Step 26, where the wires had passed through the matrix and D4 mid-move: Lee, second round).
- **In-house (Lee, 2026-10-20): wires seen together are clearly different colours.** Where the published colours are too alike, one
  is changed (the LSM's white jumper drawn yellow: beside the published light grey it was "very close"), in every step, its captions
  and its name on hover too.
- **In-house (Lee, 2026-10-20): a hole label's leader crosses a red lead line, never runs along it.** Where both end on one hole, the
  label keeps its ring on the hole and its leader comes in from the side, at an angle to the lead line (the LSM's c16, Step 3; a first
  try that stopped the leader beside the hole without its ring was not wanted).
- **In-house (Lee, 2026-10-19): wires from one ribbon stay a ribbon**, side by side and apart only at their ends, rather than spreading out on their own ways ("somewhat confusing to look at"); neither crosses over the other's hole, so that a pin pushed in after its neighbour never comes down through it (the LSM's white and grey wires, i2 and i3).
- **In-house (Lee, 2026-10-19): a wire that a part slides along lies dead straight there**, past where the part comes in (the LSM's matrix wires along under its edge, past where D10 comes up and slides along under them).
- **In-house (Lee, 2026-10-19): a wired socket going onto a module's pin is shown with the module held so that its pin and the wire's other end, in the breadboard, are seen together**: the pin's label, the hole's label, an eye on the socket (the LSM's LED matrix held upright over the breadboard, Steps 15 - 17).

## 10. Wood, fasteners and enclosures

- **The base panel is the datum**: it appears in place and never hovers. The first mover hovers against it.
- **Two ways a panel goes on.** *Edge-first*: the moving part carries the tabs and travels in its own plane (median 82 mm). *Face-on*: the moving panel carries the slots and is pushed along its normal onto tabs of two fixed neighbours (median 64 mm).
- **Lead lines tab tip to slot mouth**, 1 / 2 / 4 as in section 5.
- **Thirteen of the 34 wooden part kinds need two motions.** Those are two stages, each with its own lead lines.
- **A panel-mount component** (button, switch, potentiometer) is fitted on its loose panel in an isolated view: the panel appears in place, the component travels leads-first from 80-100 mm away with exactly one lead line down its axis.
- **Fastener on:** fades in on the axis 60 mm away, one thin lead line, no arrow. **Fastener off:** one fat arrow on `Step N`, a Transition slides it off, `Step Nc` hides it.
- **Sub-assemblies are built on the bench and joined later.** A bench sub-assembly is built in an isolated view at the spot where it will lie parked, so coming back to the full scene needs no motion and no step. Once its wires are plugged in at the far end it is tethered: pick up (eye), then attach (lead lines to the tabs), by swapping poses (7 of 11 seats take the two steps; the rest are done in one).
- **Wiring stays visible while the case goes on.** Parts are hidden only for bench work, or (PMG) while a bare frame is built before the electronics are involved.
- **Where a joint ends up hidden or small**, the result view gets an eye icon or a framed close-up with a red box on the detail.
- **A cable through a notch is shown by the result** (eye on the notch), not by animating the cable.
- No tool is ever drawn. No fastener size is ever printed.

## 11. Deconstruction guides

- **Same skeleton as a build** (`Start`, numbered pairs from 1, `Completed View`), with no section cards and no text labels. Starts on the finished model, ends showing only what is left assembled. (TechBox's own take-aparts, Lee, 2026-10-22: no
  `Completed View`; the last step leads straight to the Full Build's parts list pages, below.)
- **`Step N` changes nothing in the model**: the part is still seated and carries every cue. Pressing Next plays the removal to its end without a further click: the part travels out along the arrow and disappears. The pulled-out state is never a resting frame, and removed parts are not left on screen.
- **One red arrow per moving unit, never lead lines** (LSM 24, LAC 22, PMG 31 arrow showings; lead lines only where hardware is refitted for storage).
  **In-house (Lee, 2026-10-18):** smaller than the published ones (15 - 40 mm, sized to the part: a screw's is about 17 mm), where
  the camera can see it, never pointing at the camera (an eye on the part instead), and on the part that matters (the joystick,
  not the walls it carries). A plug moved on its lead gets an eye, not an arrow; several ends at once, an eye each. A part hidden
  from the step's camera gets a close-up from the other side, punched in, with its frame and lead line. Two steps on one
  sub-assembly in the hand keep one camera. **Lee's third round (2026-10-18):** a screw taken off with its part has an arrow as
  big as the part's; several screws, an arrow on each (the close-up has the hidden one's, not a red box); an arrow sits where
  it reads (the top of R7 and R8, clear of the lead through them; above wires; at the edge of B2's cut-out round the servo horn,
  to say where it comes away from); the A9s keep their arrows though they come towards the camera; small parts' arrows are
  scaled up where Lee asked (twice for the USB plug, the extension's join, the six base screws and the base motor; half again
  for the claw and its C8 screw, C6 screws, C4 and C5).
- **The part leaves along its build hover path, reversed**, to the pose it hovered at in the build.
- **A two-stage joint is undone inside one step**: small unhook or tilt first, then the long pull.
- **Wires are unplugged by swapping** the routed model for a loose one (eye icon on the plug to pull), never by animating the route.
- **Wired modules are lifted off the housing first, still wired**, and unplugged later. Sub-assemblies are taken apart in an isolated view.
- **A latch or tab that must be released gets a framed close-up** with a red box on the catch (LSM habit).
- **Order is near-reverse, not exact reverse** (reverse-order correlation -0.90 to -0.99). The housing comes apart in reverse; electronics are worked component by component; plug-in parts and the controller go last; the base carrier is never removed.
- **Coarser than the build**: 0.45-0.82 deconstruction steps per build step. Preparation, handling and check steps have no counterpart; steps on one part merge; "one, then the rest" merges into one group.
- **Cameras are reused** from the build step being undone where possible.

**Deriving a deconstruction from a build:** start on the build's title page with the subtitle swapped; walk the build's steps last to first; skip preparation and check steps; stop at the permanent first steps; merge steps on the same part into one step with stages. For a rigid part: the build step's camera, part seated, one red arrow along the hover direction with length equal to the hover distance, then slide and fade.

**TechBox's own conventions (Lee, 2026-10-17):** a deconstruction guide largely follows its construction guide in reverse; some
parts are removed in unison (several units in one step, each its own way: beyond the published guides' identical sets and
inseparable units, and so past their two arrows a frame, which the generator notes); every step has a description of its own
(not the build's captions reworded); and a part, once disconnected, disappears: it is removed, never reconnected (so nothing is
refitted for storage, as LAC does). Still open: whether "disconnected" means each plug (a lead unplugged at one end dangles from
its other end until that end's part goes, as the published guides do, and as the in-house generator does) or fully free.

**Lee, 2026-10-18 (the MRA's deconstruction):** its title page shows the finished model (the Full Build's), not an empty screen;
its Completed View shows only what is left (the I/O module: the Nano Board comes out last). As a first draft it is the build in
reverse, with two exceptions: wires that went on one at a time may come off together (the eight breadboard wires, off the
joysticks and the module at once; or in phases, the joysticks pulled off the wires, then the wires off the module), and a test
the build makes on the bench (the electronics test: motors plugged in, then out again) has no counterpart. The fade of a part
taken off: slower and smoother, as Cadasio's (below, section 13).

**Lee, 2026-10-19 (the curriculum director):** a servo is named "X Servo (Y Dot)" on its labels and on hover alike ("Elbow Servo
(Black Dot)"; the Base Servo has no dot), in the Full Build and the deconstruction; the parts list names it "X Servo" with the dot
as its tag. The deconstruction's unplugging of a servo from its row carries the Full Build's labels for that row ("Row 6" and the
servo), instead of an eye (an exception to "no text labels" above); and the deconstruction ends with the Full Build's parts list,
after its Completed View.

**Lee, 2026-10-18 (first round on the MRA's draft):** where a screw and the part it held come off in the same step (Lee named the
MRA's A12, A13, A11, A5 and the A1 - A3 lever), they go in sequence: the screw slides out and fades, then the part slides out and
fades (a stack of plates on one screw: the screw, then each plate in turn). Elsewhere a screw keeps its own step before its part, as
in the build (R6's screw before A10 and A11 are lifted, in Lee's own order); whether every such pair should be merged is open.
A screw that the model hides from the step's camera gets an eye. With the cover (B8) off, the electronics come out where they
are, before the housing around them: the breadboard wires off both ends, the I/O module out of its slots, the Nano Board out of
the module; then each joystick with its walls, the walls off it in the hand. So the guide ends on the base carrier, R1, as the
published take-aparts end on the base (above). A sub-assembly taken apart in the hand is seen the way the build showed it,
from above where the build did; Lee asked for the claw's C3 from above (the build had turned it over).

**Lee, 2026-10-18 (the RCC's deconstruction):** a sub-assembly that comes off is taken apart on its own, the rest hidden, close in,
then the guide returns to the main model: the controller (first: its USB cable, seen a little wider so that the cable shows, then
the joysticks, the radio module and the Nano Board), the 9V battery with its adapter (the adapter off the battery), the I/O module
(the radio module, the adapter board, the Nano Board), one camera for each such run. Leads are unplugged before the structure
around them comes out, as the build plugged them in last (the wheel motors before L6, L7 and the I/O module). A cable unplugged and removed has one arrow, on the plug that is pulled, clear of the
cable, and none on its far end. Wood that holds a part (the motors' L4 and L5) comes off that part in the hand, and the guide ends
on the base (L1). Its card is the Full Build's (as the MRA's).

**Lee, 2026-10-21 (the LSM's deconstruction):** on a first draft that walked the Full Build back: "you need to base the deconstruction
process off of this guide: https://instructions.online/?id=19075-laser_stem_matrix_lsm_-_deconstruction - so there are a lot of edits
needed." Where TechBox has published a take-apart of the kit, ours follows it: its order and groups, its camera for each step, its arrows
(size and tail), eyes and close-ups, drawn from our model; departures only where our model or Lee's own groups need them (the three
breadboard wires in one step), or where ours would hide or lose what the published picture shows, each named in the script. Its model
swaps (a module set down beside the box, a wire unplugged and left loose) are fades (`reappear=True`), as section 11 says wires are
unplugged; whether to keep them as fades is put to Lee. A two-stage joint the published guide flattens is still undone in two stages
inside the step (D10 slid off its hooks, then down: above; and see Lee's two notes of 22 Oct below). "Eyes instead of hole labels are okay for this kit" (the unplugged wires),
and a Pry Tool the kit has but the model does not show still gets its caution (the Nano Board).

**Lee, 2026-10-21 (the LSM):** "Let's use gray": TechBox writes American English (its MRA take-apart's "center"), so "gray", not
"grey", in every guide's student-facing words (captions, cautions, close-up captions, hover names); colour and part ids in the code may
keep their spelling.

**Lee, 2026-10-21 (the PMG's deconstruction, "same principles as you used for the MRA"):** "some things can be removed in groups
(like the breadboard wires, four buttons, four H9 parts, etc.)": parts the build put in one at a time come off together where they
are alike or go together, each with its own arrow. The PMG's draft follows TechBox's published PMG take-apart where it has one (the
wired modules lifted out of the case still wired; each device pulled off the ends of its wires, then the wires off the I/O module
together; the Nano Board last of the electronics), within the in-house principles above (the power cable first; the electronics
taken apart on their own, then back to the case; it ends on the base, H1, with the Full Build's parts list after it).

**Lee, 2026-10-21 (the PMG's take-apart, first round: "H12 and H11's removal have the arrow going upward, which is right, but there's
a motion toward H1 required first before the lift ... the arrow sizes and sequencing need refinement. Examine the Cadasio"):** a part
that comes off in stages shows an arrow for each, in turn, as the published take-apart's auto-advancing frames do: Step N the first
stage's (H11 and H12 toward H1); as the step plays, the next stage's arrow appears while the stage before it plays (then up), and goes
as its own plays. A still of the step (the step list, the 2D PDF) shows them all at once. The PMG's arrows take the published guide's
sizes, step by step (docs/research/pmg/deconstruction/published_arrows.txt: mostly 30 - 116 mm long, 4 - 12 mm thick), not the in-house
15 - 40 mm set for the MRA; groups have one arrow (the four keys, the four buttons off their wires), and the buttons out of their pockets
an eye, as published. The step order stays the in-house one (Lee, the same day: "Keep the current step order; the arrows were what
needed changing"): the power cable first, the electronics taken apart on their own before the case's last plates, ending on H1.

**Lee, 2026-10-21 (the PMG's take-apart, second round: "Step 10 - the second arrow appears too early and is partially occluded in H12
for part of the animation. Step 11 - Same as Step 10"; "Step 7 needs a wider arrow"):** a later stage's arrow appears only once the stage
before it has finished: the part rests for a beat, its next arrow fades in, then it moves on (for every part that comes off in stages,
not only H12 and H11). An arrow drawn on a plate that moves along itself is set in front of the plate, towards the camera, so the plate
never covers it. Step 7's arrow (the I/O module lifted off H4) is the published 6.5 mm thick.

**Lee, 2026-10-22 (the PMG's take-apart, once live: "remove the Completed View and progress directly from Step 26c to the Parts
List"):** as the LSM's, no Completed View: the last step leads straight to the Full Build's parts list pages.

**Lee, 2026-10-22 (the MRA's and the RCC's take-aparts, once live):** the same for both: the MRA's Step 73c leads straight to its
parts list pages, and the RCC's, which had none, gets the Full Build's parts list pages after Step 20c ("like the others"). So every
kit's take-apart now ends this way: its last step, then the Full Build's parts list, no Completed View; a new one does too unless Lee
says otherwise.

**Lee, 2026-10-22 (the LSM's take-apart, notes on the draft built on the published one):** a close-up stands beside the model on the
side of the spot it shows, its leader not across the model ("instead of having it cross the model": Steps 3, 5 and 6); its red boxes
cover the whole catch with room round it ("The squares in many of the breakouts are too small"). An arrow starts at the moving part's
outer surface or beyond, never inside it or another part (Steps 4, 5, 7 and 24): a published tail that lies inside is moved out to the
surface. Two catches of one part get an eye each, spaced as the catches are (D3's two tabs: "evenly spaced like the tabs of D3"). An
eye's leader never crosses an arrow (Step 19). Like parts taken out the same way have arrows of one size (the 12 kOhm resistor's as the
330 Ohm resistor's), whatever the published sizes. A nut comes off its thread in one smooth move, turning as it goes ("doesn't need a 3
step animation"). (Where our way out took a part into the wires, D10 was first dropped straight off as published; Lee's second note
of the day put the slide back: below.) Hardware that belongs to a part goes back on it once the part is out,
in a step of its own (the push button's nut, screwed back on once the button is out of D2: "we need a step that shows the nut being
replaced onto the push button"); this is the one exception to a part once off being gone for good. A take-apart may go straight from
its last step to the parts list, with no Completed View (`take_apart(completed_view=False)`).

**Lee, 2026-10-22, second notes (the LSM's take-apart):** a part that hooked on by sliding comes off by sliding ("Remember, D10 must slide
off of the LED Matrix"), and it comes off where the build hooked it on, so that the wires lie as they did then (the matrix held over the
box: the Full Build's Step 31 reversed; laid on the table the wires had other shapes, and D10 passed through them). Wires from a module
come off it in a group and stay in the breadboard ("left attached to the breadboard"), and come out of the breadboard after, once what
lies over them is off (the D9s). An eye points at the catch itself, not at the part above it ("at the bottom where the actual latch
element is": a D11 post's foot, where its tab goes into D1). A latch's red box takes in every tab of the latch ("both tabs of the
latch"). Hardware put back on a part starts just off where it goes on, in a close view of the two, not after a move through empty space
("start the nut just off the end of the push button's wires, then animate it back on").

**Lee, 2026-10-22 (the LAC's take-apart, notes on its first draft, remade from the published one):** one wire per step, for this kit only,
"given the excess number of wires" (the PMG's and LSM's groups stay theirs). The order follows the published where Lee named it: the
potentiometer's wires, then the potentiometer out of F1, before F9; F9 last of its sub-assembly, "after the Potentiometer / Buzzer and
LCD Display are all removed". The potentiometer's washer, nut and knob go back on it once it is out of F1, a step each (as the LSM's
nut on its button: the published LAC does the same). A latch that holds a part gets an eye "as well" as the part's arrows (F9's lower
rear latch); clips that must be squeezed get the instruction and a close-up with a red box on each (the rocker switch's, under F4). An
arrow along a panel's edge starts at that edge and lies parallel to it, as published (F1's lower edge), and starts outside the part's
surface, never in it (F2; the nut's arrow, not in the potentiometer's body); none reaches into the instruction boxes (F4: shorter than
the published). A part the kit uses but the model does not show still gets its caution (the Pry Tool for the Nano Board).

**Lee, 2026-10-22, second notes (the LAC's take-apart):** what comes off fades away even when it goes back on later ("You don't
need the removed components to be persistent. Keep them fading away": the knob, nut and washer off the potentiometer). A part put back
on appears where it is ready to go on, as its step opens, and goes on as the Full Build put it on ("similar to the Full Build's
version": a lead line from the part to its seat, no arrow), seen close (the Full Build's own camera of that part, not one framed round
everything waiting). A camera that lets a part hide what the step works on is changed (F9 in front of the potentiometer's leads in
the breadboard: Lee's view has F9 behind them). A lead carried with its connector passes into no part on the way (the LCD's SDA and SCL
into F9): the connector comes off its pin only as far as clears the pin.

## 12. Numeric defaults

| Setting | Default | Basis |
|---|---|---|
| Step animation | 800 ms; fade for show/hide, glide for moves and camera | 1,030 of 1,037 steps |
| Camera lens | perspective, 45 degrees | 20 of 20 guides |
| View elevation | 34 degrees (20-50) | 87% of steps |
| Travel axis vs view axis | at least 40 degrees, typically 60 | 96% at 45 or more |
| Content height in frame | about 60% | IQR 51-74% |
| Hover: plug-in part into breadboard or socket | 35 mm straight up | 29-44, median 34 |
| Hover: breadboard onto base | 47 mm | 39-49 |
| Hover: flat panel face-on | 65 mm | 22-69, median 64 |
| Hover: part truly sliding lengthwise | 1.0 x its length along the travel, 40-140 mm | ratio 0.83-1.05 |
| Hover: other wood, edge-first | about 80 mm; about 0.7 x the part's longest dimension | median 81, range 40-139 |
| Hover: nut, washer, knob | 60 mm along the shaft | 56-61 |
| Hover: panel-mount part with leads | 80 mm; 100 if body + leads exceeds 70 mm | 79-103 |
| Hover: anything else | 60 mm | overall median 61 |
| Tilt of a hook-in panel | its swing angle; 20 degrees if unknown | 8-26 |
| Lead lines per step | 1, 2 or 4 | 147 of 149 line-bearing steps |
| Lead line length | 1.0 x travel (accept 0.85-1.15) | 360 lines |
| Lead line colour / width | `#ff0000` / 5 px at authoring size | 363 of 363 |
| Arrow | `#ff0000`, 5 : 20 : 17, body about 4 mm, length about the travel | 106 arrows |
| Labels per step | 2 at most | all guides |
| Label text height / rule length | 4% of view height / 8% of view width | 212 labels |
| Callout colour | `#7fdbff`, rule and leader 5 px at authoring size | 212 of 212 |
| Eye icon width | 8% of view width | 224 uses |
| Inset width | about 16% of view width on steps; 31% on cards | 46 insets |
| Wires per step | 1 | 100 of 103 |
| Loose wire parking | 50-60 mm from its routed position on a compact board, 80-125 mm on a spread layout; same spot all run | 33 steps |
| Steps per Part | median 13 (5-26) | 11 guides |
| Deconstruction steps per build step | 0.45-0.82 | 3 kits |

## 13. Where the published guides disagree (decisions for TechBox)

| Question | What the guides do | Suggested default |
|---|---|---|
| Whole wire per step, or one wire end per step? | LAC and PMG: whole wire, eye + two labels (41 of 48). LSM: one end per step, no eye. | Whole wire (the newer form). |
| Identical screws | No published kit has a screw. Nearest evidence: every nut, washer and knob gets its own step; sets of four or more identical drop-in parts are "one in full, then the rest". | **Decided (Lee, 2026-10-13): one in full, then the rest**, per joint. The first screw is shown close up (the camera punches in on it) hovering over its hole, then going in. The next step pulls back; the others appear above their holes, each with its own lead line, and go in together. They never simply appear in place. |
| Printing a fastener size | Never done. The nearest device is a bare quantity ("64x"). | Leave it off the canvas; put it in the tooltip and the caption. |
| Quantity cue | Four forms: "2x" in blue, "64X", "64x", "3x" inside a picture. | "Nx" with the eye icon. |
| Deconstruction wire granularity | LAC: one wire per step. PMG: whole bundles. LSM: mixed. | Per module bundle (the newest guide). |
| Removal: three beats or two | Three (cue, slide, gone) in LSM and most of LAC; two in most of PMG. | Three. **Decided (Lee, 2026-10-17): with a fade.** The cue on Step N; Next plays the part out (800 ms a stage), fading out over the second half of the last stage (so it slides while it fades, Cadasio's two-beat form, with no resting pulled-out frame); its leads fade with it. Prev brings it back fading in. (Parts appearing in a build still do not fade in.) **Changed (Lee, 2026-10-18: "the fade on Cadasio seems smoother / less abrupt, and slower"):** the part slides out (800 ms a stage), then fades out over a beat of its own (800 ms, on a cosine curve, from 150 ms before the slide comes to rest), as the published take-aparts slide (Transition) and then fade (Step Nc); its leads fade with it. Prev fades it in where its way out ended, then slides it back. |
| Label size and font | 3em Arial (LAC, most guides) vs 2.5em (older LSM); PMG falls back to the viewer's default font. | 3em-equivalent, Arial bold. |
| Pin-name case | Capitals everywhere except eight PMG labels ("clk", "dio", "s8", "s9"). | Capitals for pins, lower case for breadboard holes. |
| Second stage: own step or Transition | Both occur; a new viewpoint goes with 5 of 7 own-step cases. | Transition if one view shows both stages; own step if the camera must move. |
| Section card for every module | Coverage is uneven and has grown with each kit. | Card for every module with pins to identify. |
| Engraved codes in build order | Only PMG (H1-H14 in order). | Worth doing on new kits. |
| USB cable: fade in, or hover and plug | LSM, LAC: fades in with an eye. PMG: hovers with one lead line. | Hover and plug (the newest guide). **Done for the MRA (2026-10-14):** the Mini-B end, from TechBox's own STEP file, hovers along the socket's axis with one lead line from its tip to the socket mouth and plugs in; the A end lies on the table; the cable between them is drawn. |
| Servos | No published kit has one. Nearest evidence: push button, switch, potentiometer, mounted on a loose panel in an isolated view, leads riding. "All wiring before any wall" would leave every servo bracket tethered through the mechanical build. | **Decided for the MRA (Lee, 2026-10-13):** a servo is shown with its lead from the moment it appears, the plug on the loose end. The lead stands clear (straight up, or straight out) while the parts round it go on, is moved into its slot in its own step once that slot exists, and is plugged in at the end of its section with the row number as the destination label. A servo that arrives with its horn fitted is shown that way, and motor and horn move as one. |
| A module that arrives already wired to another (the MRA's joysticks to the I/O module) | No published kit has one. | **Decided (Lee, 2026-10-13):** while the module is handled on its own (an isolated sub-assembly view) its wires are shown cut short. As soon as it is on the model the other module is shown too, lying beside the model, with the wires whole; the wires stretch and re-route as either end moves. **Changed (Lee, 2026-10-14):** the cut ends fade out over the last 30 mm or so instead of carrying a zigzag break mark, which read as conductors trimmed inside the insulation; the picture must say "the wire runs on" without text. |
| A motion that is not a straight push (the MRA's base horn through R1: angle in, level, quarter turn, set down) | The published guides only ever translate a part. | **Decided (Lee, 2026-10-13):** show the real motion, as a short sequence of tilts and turns inside the one `Step Nc`, one 800 ms beat per stage. |
| A part that goes on underneath (the MRA's B1 under B2; parts of the claw under C3) | Section 4: a hovering part is above or beside its seat, never below it; to work on the underside the kit is shown turned over. | **Decided (Lee, 2026-10-14), replacing the 2026-10-13 "seen from above":** work done with the kit upside down is shown with the model turned over, lit as usual (`flip=True`): B2 sliding in between the horn and R5 / R6 and B1 going on, seen from underneath; and the whole claw, which the video builds upside down, so that its parts go on from above. The model turns over (and back) as the step opens. |
| Punching in on one small part | Section 7: never done in context. | **Decided (Lee, 2026-10-13):** done for the first fastener of a set (see "Identical screws"), and where a wire has to be seen going into a slot or onto a pin. |
| Part names | The published guides name parts only in tooltips. | **Decided (Lee, 2026-10-13):** names follow the tooltips of TechBox's own Cadasio project for the kit (for the MRA: Base / Shoulder / Elbow / Claw Motor, Joystick, Nano I/O Module, 6mm / 10mm / 16mm Hex Screw, Servo Extension Wire, Breadboard Wire (F-F)); wood parts are named by their engraved code. |
| A cue for turning the kit over | None exists: the model simply appears the other way up, engraved codes upside down. | Consider one; young students may not notice. |
| Telling wires apart | By colour alone; loose and routed models differ in colour on 5 of 103 pairs. | Keep colours identical between the two models; consider a second cue. |
| Contrast and size of callouts | Light blue on white is 1.56 : 1; red on wood 2.15 : 1. Labels are sized in fixed pixels, pictures in percent of width, arrows in millimetres. | Size everything relative to the view; consider a darker blue. |
| A power-on or test step | None in any guide. | **Decided for the MRA (Lee, 2026-10-14):** an electronics test comes before the mechanical build, on the bench: the Nano onto the I/O module, each joystick wired to the module one wire at a time (both ends in one step, a label at each end: the pin as printed on the joystick, and the module pin, e.g. `GND` and `A2 G`), the four servos plugged into their rows, USB and power, a test card, then "disconnect all servos". The parts are then put away until the build needs them. |
| Part-name labels and a caption line on every step | Neither appears in the published guides (labels there are destination names on wiring steps only; there is no caption text). | **Decided (Lee, 2026-10-13): both on by default** in the in-house player; a guide or an embed turns them off with `?labels=0` / `?captions=0` when wanted. |
| Colour of the I/O module's header bases | Published models: yellow `#ffff80`. The MRA CAD names its rows by colour (black, red, yellow, white). | **Decided (Lee, 2026-10-13): all yellow**, whatever the CAD names them. |
| Seeing the engraved codes | Section 7 picks the view across the motion; nothing says which face of a panel to show. | **Decided (Lee, 2026-10-14):** a step that brings in a wood part is seen from the side its engraved code faces, so the student can read it (both codes when two parts meet, e.g. A6 and A7). The generator prefers such a view by itself. |
| Destination label on a servo row | Published destination labels are bare pin names. | **Decided (Lee, 2026-10-14):** `Row 5`, `Row 6`, `Row 9`, `Row 10` (not a bare number), its leader ending on the top of the pin with no dotted ring, plus a label on the plug naming its motor; the caption says "Row N" too (Lee, 2026-10-15: "Plug the base motor into Row 5 for the test", "Reconnect the base motor to Row 5"). A motor with a coloured dot is named with it wherever it is labelled (later the same day): `Elbow Motor (Black Dot)`, `Shoulder Motor (White Dot)`, `Claw Motor (Blue Dot)`. |
| Where lead lines and the camera are set by hand | Section 6 / 7. | Lee's Option-click points go straight into `lines_at=`; a step whose motion is hidden by a wall is seen through an opening in it rather than from the usual diagonal (the MRA's shoulder screw and lever, through R5). Lee asked for three lead lines on one step (the claw onto the arm), against the "1, 2 or 4" pattern. |
| Title page and finished model | The published guides open on the finished product. | **Decided (Lee, 2026-10-14):** seen from the front, above (for the MRA, from the claw's end), not from behind. The title page closer in, as in Lee's screenshot of that day (its camera is reproduced exactly). **Decided (Lee, 2026-10-17, RCC):** the title page much closer in, as in Lee's screenshot ("WAY too zoomed out"), and the Completed View "much more punched in" too, gliding from the last step. **Done so, and confirmed (Lee, 2026-10-17: "Everything looks correct as it is"):** the Completed View as close as the title page, centred, the USB cable's end cut off by the bottom edge as in Lee's picture (the website's card shows the whole model); in a window that cannot show those cameras (the title, a fixed size on the page, would cover the model, as in the LMS's frame; or the frame is too narrow), the closest of a few wider cameras that keeps the model in the frame and clear of the title, and in a frame taller than wide the whole model (`clear_title`, `otherwise=[...]`). **Decided (Lee, 2026-10-21, LSM):** the title page as Lee's screenshot: the finished model large (about 88% of the view's height) and to the right of the middle, from the same corner as the Completed View (the camera moved aside, not turned); solved from the picture as `start_view`, which the player keeps in every window (a frame taller than wide centres it). |
| Picking a part in the viewer | Cadasio's viewer tints a clicked part and names it. | **Decided (Lee, 2026-10-14):** the same in the player: a click tints the whole part (or wire) orange, as Cadasio does (blue was too faint), and keeps its name up, white on dark with an orange edge, until the next click or step. **Decided (Lee, 2026-10-17):** or until the view moves (section 14). |
| Lead lines on a panel that goes onto several tabs | Section 6: 1, 2 or 4 lines. | **Decided (Lee, 2026-10-14):** as many as the joint needs when Lee asks: one per tab (the B5 / B6 and B6 / B7 groups have 6 and 5), and for a plate going down onto tabs (B8) one line per slot, from the middle of the slot on the plate's underside straight down to the top of its tab, never through or above the plate. |
| Steps of one small build in the hand | Section 7: hold the camera where nothing calls for a move. | **Decided (Lee, 2026-10-14):** the T1 / T2 block keeps one camera for all three steps, from the side of the first T2's code. In the upside-down claw build the model stays put and the framing holds for as long as the corner does (Steps 78-90 had slid about); it changes only with the corner. **Decided (Lee, 2026-10-19):** the claw closer in, and as close when the corner changes as before it (C5's step as close as C4's): one zoom through a sub-assembly, each framing the closest that keeps what the step shows clear of the caption. A step whose parts come in from far off the others' (C8, slid in from the side), or that would sit off-centre in its corner's framing (C5, in the framing made for C6, C7 and C9 above it), is framed on its own (`own_frame`). |
| What students check after the electronics test | Not in any guide. | **Decided (Lee, 2026-10-14):** TechBox's Testing Checklist, word for word, on a note card (a card's text can be a list); the kit is powered by USB alone. **Changed later that day:** no separate card to unplug the USB cable (the checklist's last line says it); the cable is simply gone after the checklist, and the four servos are unplugged in one 3D step (their plugs lift off their rows) with a caution to set the servos and the I/O module aside. One step for four plugs, against "one wire per step": Lee asked for one step. Its cue is an eye on the plugs. |
| Warnings | Never annotated (section 6). | **Decided (Lee, 2026-10-14):** a **Caution** box under the caption where a student could go wrong: brown to G on the first servo plugged in for the build, a servo horn that may need turning to fit its slot (B1, C7), the joysticks' wires that stay on the I/O module (naming its pins), the wire colours matching across a join, setting parts aside. Orange edge and a warning sign, on both views of the step, read aloud with the caption. Not the yellow Review notes, which are questions for TechBox. |
| Review notes once a guide is past review | Not in the published guides. | **Decided (Lee, 2026-10-14):** `Guide(review_notes=False)` hides the notes and their switch (the MRA from now on); the feature stays for new builds, and `?review=1` shows them. |
| The title page's small print | The published guides show the copyright. | **Decided (Lee, 2026-10-14):** "© TechBox. A division of TARIS Industries, LLC. All Rights Reserved." |
| Parts list | The published guides open with "Parts List" pages: one band per kind of part (quantity, a size tag over the name, the picture at the end of the band with a halo), bands coloured by kind, an icon per kind (images Lee sent on 2026-10-14). | **Decided (Lee, 2026-10-14):** the same pages after the title page (`Guide(parts_list=)`), grouped as electronics, motors, screws and wood by code family; the tag is the screw size or the motor's dot. Only the parts the guide shows are listed, so a guide for one part of the build lists that part's parts. A click (or Enter) on a band shows its picture large (500 x 500 px). A part whose first CAD piece alone is not the whole part is pictured whole (`g.part_picture`: the servo extension wire with both ends and the wire between, and the breadboard wire; `g.list_part`: lists the breadboard wires). **Decided (Lee, 2026-10-15):** the breadboard wire is pictured straight with its two caps in line, not kinked as the CAD routes it (`g.list_part` lists it, `g.part_picture` lays it out); T2 turned so its code reads the right way up (`part_views` roll). (The USB cable is still pictured by its Mini-B end.) **Decided (Lee, 2026-10-16):** the wood groups' bands are blue-grey (`#dbe4ef`, halo `#8ea6c4`), not orange: the wood pictures stood out too little from orange; the other groups keep their colours. **On trial (Lee, 2026-10-16):** in the step list a Parts List page is pictured as the page itself, small, instead of its name (may be reverted). |
| Text over the model | Labels sit in white space, with no box (section 6). | **Decided (Lee, 2026-10-14)** for the final wiring, where a close-up leaves no white space: a white box behind the label. Drawn behind every label: it cannot be seen in white space, so it shows only where a label has to lie over the model. Labels also keep clear of the instructions box. |
| The camera after the viewer has turned the view | One camera per view. | **Decided (Lee, 2026-10-14):** every step opens on its own camera, whatever the viewer turned or zoomed to before (the camera swings back to it, or is simply there after a jump). The cameras themselves did not change. |
| Checking that parts move freely | Check steps are skipped in deconstruction; builds use a card or nothing. | **Decided (Lee, 2026-10-14):** the arm check is a 3D step of one view only (`single=True`: one advance, no Step Nc) with the previous step's view and an eye on A12; A13 and A12, whose far ends are still free, jiggle a little about their screws whenever the step opens (`wiggle=True`). A11 stays put (corrected the same day). The claw's "jaws open and close" card was dropped. |
| A detail hidden by the part on top of it (C7 and C8's gears under C9) | Section 6: a framed inset with a leader. | **Done (Lee, 2026-10-14):** on Step Nc, a framed close-up drawn with C9 left out, a blue leader and ring to where the teeth meet, a thin red box round it and "Seen without C9" under it. |
| A plate slid along a slot (B2 along the horn's slot) | Lead lines along the slot's edges. | **Decided (Lee, 2026-10-14):** a fat red arrow along the slot instead, from its round end out of its mouth, the way the plate moves (section 5's arrow). |
| Lead lengths (RCC) | The published guides' wires are separate models per pose. | **Decided (Lee, 2026-10-16):** a lead's length is representative and may be whatever presents best. **Decided (Lee, 2026-10-17):** the RCC's motor leads are 115 mm straight in the hand and back over L1, where they run on past its rear edge into space, clear of it ("they don't have to lay on L1"), not shortened to fit on it; on the bench they start straight to the rear of the motor; each may be as long as a smooth path needs ("I am not worried about the wires exact length ... lengthen them as needed to create a smooth path"). **Done so, and confirmed (Lee, 2026-10-17: "Everything looks correct as it is"):** plugged in, 118 and 132 mm; on the bench the straight lead is 55 mm and held out level (its plug starts in Steps 8 and 9's close frames; it does not lie on the table as a laid-aside lead would); from one shape to the next such a lead stretches evenly (`stretch` routes, section 14, Wiring). |
| The controller on the title page and the Completed View (RCC) | One model state for both. | **Decided (Lee, 2026-10-16):** turned round (180 degrees about the vertical), so that it faces the other way beside the car. **Decided (Lee, 2026-10-17):** turned already in Step 29, where its USB cable goes in, and the build leaves it so; Step 29c glides into the Completed View. Steps 1 - 4 and the test (Step 12) show it as built. |
| Destination labels on a board's sockets (RCC) | Published destination labels are bare pin names. | **Decided for the RCC (Lee, 2026-10-16):** none for the sockets a part plugs into when the caption names them (H1 / H2, NRF24L01, L-JS / R-JS, U3, LWh / RWh): "they don't add much and get in the way". The part's own name label stays, on its first step. (The MRA's `Row N` labels stand.) |
| Parts that come fitted to another (RCC) | Section 3: anything that arrives pre-assembled is one part. | **Decided for the RCC (Lee, 2026-10-16):** the controller's guards come fitted to the controller board, and each wheel to its wheel motor: no step to fit them, one part in the parts list ("Controller Board", "Wheel Motor"), and on hover the fitted piece is named as its part. The parts list may split one kind of part between bands by where each goes (the controller's band holds one of the two Nano Boards and one of the two radio modules). |
| The I/O module's board colour | Published models: house blue `#224bbe`. | **Decided (Lee, 2026-10-14):** the Nano's navy `#000f41`, as TechBox's own Cadasio project has it: the lighter blue looked off beside the Nano. |
| Printing on a board (the I/O module's silkscreen) | Published models show boards plain. | **Decided (Lee, 2026-10-14):** the module carries its silkscreen (pin names, G V S, POWER, RESET, the capacitor's and regulator's print), from photos of the real board, placed from the CAD's pin positions (`decals.json`, written by `silkscreen.py`, carried in `model.glb` as data by `build_model.py`, drawn by the player). |
| Section cards, pin labels and wiring cameras for printed boards (PMG) | Section 6 / 9: a section card with a photo, the header boxed in red; bare pin names. | **Decided (Lee, 2026-10-19, the PMG):** every bought-in board carries its printing (the push buttons, the 4-digit display front and back, the dot matrix's back: `silkscreen.py`), and its section card is a one-view step showing the board alone, close up, with a framed close-up of its header and the printed pin names boxed in red (the PMG's Step 3, in place of the published photo). A pin's label ends on the top of that pin, on the module and on the board (as the MRA's `Row N`). A board whose pin names are printed on its back is wired from a camera that shows its back and the module's pins (the PMG's dot matrix). A part carried past another board's wires passes under them, so that its own wires never cross theirs (the PMG's 4-digit display, under the dot matrix's wires); a plate hooked in and swung (H5 - H7) goes a beat at a time, seen from the side the hinge is seen from. **Decided (Lee, 2026-10-20, the PMG):** parts that can no longer be told apart once placed (the push buttons upside down in the case, only their backs showing) are named by colour on `Step Nc` (Lee asked for colour callouts, or a close-up per button; done as one label per part, all on one side, in the caption's order: `labels_done=`, the PMG's Step 33c): an exception to section 6 (labels only on `Step N`, two at most, never a part name or a colour) and to "`Step Nc` is clean" (section 2). |
| A part a new kit shares with an earlier one (the Nano Board, the USB cable's ends, the Dupont caps) | Each published project models it on its own. | **Decided (Lee, 2026-10-19, the LAC):** use the version made for the MRA or RCC, where the kit has the same part: its model (the MRA's export of the Nano model, cut to the new kit's place by `tools/cut_part.py`; the MRA's USB A end) and its colours (the MRA's atlas entry). A part that differs (the LAC's right-angle Mini-B plug) stays the kit's own. |
| 2D instructions (PDF) | Cadasio exports a guide's 2D instructions as a PDF. | **Decided (Lee, 2026-10-21):** landscape, a page per view: the title page, the Parts List pages, each `Step N` and `Step Nc` on pages of their own, one after the other (not side by side), the note cards and the `Completed View`; every page with the step's instruction and caution, TechBox's logo and the guide's name at the top, the copyright and "Page n of N" at the foot (`tools/make_pdf.py`). The Full Build and the deconstruction first; the Part guides' once Lee had checked them (done the same day). |

## 14. The in-house player against these rules

Status on 2026-10-14 (third round of that day), for the MRA full build (electronics test, base, controller, arm, claw, T1 / T2 block).

| Rule | Status |
|---|---|
| Skeleton: Start, Step N / Step Nc pairs, Completed View | Done. |
| One part per step; receiver appears in place; hand-held piece moves | Done. Sub-assemblies (each joystick between its walls; the upper arm, the lever and the claw) are shown on their own, then seated. |
| Hover along the real insertion axis, distance by kind of fit | Done, computed from the CAD by collision test; defaults from section 12. Set by hand only where the CAD cannot say (screws thread into the wood; a part that has to be tilted or turned on its way in). |
| A motion that is not a straight push | Done: a hand-set path of poses, each a shift or a turn about an axis, played one 800 ms beat per stage (the base motor's horn through R1). Checked against the CAD for collisions when it is written. |
| Lead lines tab-to-slot, 1 / 2 / 4, parallel to travel, 3D and hidden behind parts | Done, computed from the CAD: joints are found where the moving part and its neighbours grip each other. Where the automatic lines are not the wanted ones, `lines_to=` limits which parts they may attach to and `lines_at=` sets the points by hand (Option-click a spot in the player to copy its coordinates). |
| Camera fixed inside a pair; three-quarter view; across the motion; whole action in frame | Done, chosen automatically from the four diagonal views, preferring one from which the engraved codes of the parts coming in can be read. `focus=` punches in on named parts (section 13: the first fastener of a set, a wire going onto a pin); `view_dir=` sets an exact direction (through an opening). |
| Look: white, two-tone, black edges; colour library | Done. Edges use the 40 degree crease angle on every part. Rounded corners that no single edge marks (the rim of a screw head) get a line too, and round parts with no creases on their sides (wires, screws) a silhouette line of the same weight. Colours come solid by solid from TechBox's own Cadasio project for the kit, with TechBox's decisions over the top (`materials.json`). |
| Engraved codes as dark decals; print on parts | Done (the wood codes; the lettering on the servo labels; the I/O module's silkscreen, drawn by the player from the `decals.json` data the model carries). |
| 800 ms everywhere; backward animated | Done. One 800 ms beat per stage of a move with several stages. Going back from a step whose wire passes through routes in between (a lead laid into a slot; the servo extension onto row 10) plays that step backwards, stage by stage, since straight back the wire would cut through what it was laid round. |
| Picture of every step in the step list; Transitions hidden from it | Done (pictures). No Transition steps are authored yet. |
| Tooltip with the part's name | Done. Names follow the tooltips of TechBox's Cadasio project; wood parts answer with their engraved code. A click tints the part and keeps its name up (section 13). **Decided (Lee, 2026-10-17):** as soon as the view moves (a drag that turns, slides or pinches it, the wheel, the view reset) the part is let go and a name shown on hover goes too, since the name stays where it was put and would no longer point at the part. |
| "One in full, then the rest" | Done as decided in section 13: the first fastener close up, then the rest hover over their holes and go in together. (The older form, eye + "Nx" with the rest simply appearing, is still available as `g.rest()`.) |
| Labels fixed on screen, leader follows the part | Done. A label can also sit on an exact spot (a pin row), as the published destination labels do. |
| **Differs on purpose:** part-name labels on mechanical steps | The published guides show none. The player labels each new part. Decided 2026-10-13: on by default; `?labels=0` turns them off. |
| **Differs on purpose:** a caption line per step | The published guides have no text. Captions carry the build notes' wording. Decided 2026-10-13: on by default; `?captions=0` turns them off. |
| Wiring | **Exception (Lee, 2026-10-21), the PMG's Step 42 only:** the I/O module lifted onto H4 with every wire on it fades out where it lies and fades in where it is held, with its A end (`reappear`), as the published guides move wired things (section 4); its way could not be shown without the wires passing through one another. Elsewhere: done differently from the published guides, as decided in section 13. A wire is not a CAD part: it is a centre line that the player draws as a tube, tied to the part at each end. It follows those parts when they move, and from one step to the next it bends to a new route, keeping its length-wise place so that what both routes share stays still and extra length grows out of its tip. A lead's plug rides on its loose end until a step plugs it in. **Decided (Lee, 2026-10-15), for a lead laid aside between steps:** it keeps the length it had when it was last handled (the extension wire from Step 97 to Step 100: it had shrunk to half), and lies on a surface with its plug flat, not standing as if plugged into the wood. (A lead fed into a slot or a hole, or plugged in, still changes length as above.) A wire that runs on beyond the picture fades out (section 13). **Decided (Lee, 2026-10-17):** leads are drawn as smooth curves, never straight runs joined by tight bends ("very angular instead of smooth"); **(Lee, 2026-10-16):** a plug's move to its header is not rushed ("a little rapid / doesn't look smooth"). **Done so (RCC), and confirmed (Lee, 2026-10-17: "Everything looks correct as it is"):** a plug goes in four beats, its tip turning no more than a quarter turn in each (lying back along its lead; picked up, tip up; carried over, tip forward; held over its header, tip down; pushed in), each stop with a smooth shape of its own, all lying flat the same way (the player blends shapes bit by bit along their length, and very unlike shapes, or shapes twisted the opposite way, fold or cross their wires); such a representative lead may change length between shapes, stretching evenly, and is carried by its ends' moves only while it changes shape (`stretch`). Still as published: one wire action per step, a destination label on the pin. Not done: the loose straight wire token swapped for the routed one (the wire itself moves instead). |
| Section cards with a product photo | Not yet as photos. Text-only note cards exist for steps the model cannot show; a board's card is a one-view step with a framed close-up of its printed pin names (section 13, the PMG's Step 3). |
| Arrows | Done: flat red 3D arrows (body : head width : head length 5 : 20 : 17), shown on Step N in place of lead lines (`arrows=` on a step). One so far (B2). |
| Removal inside a build; deconstruction guides | **Deconstruction guides: done (2026-10-17)**, as a guide of its own (stepgen `take_apart()`, then `remove()`, `unplug()`, `lift()`): Step N shows the parts where they are with one red arrow per unit (an eye on a plug), Next plays them out the way the Full Build put them in, reversed, by that step's camera, fading as they go; Prev brings them back the same way. Hardware put back on its part for storage (the LAC's washer, nut and knob, Lee 2026-10-22) comes back ready to go on and goes on with a lead line, as in a build (`bring_back()`, `lift(lines=)`). The guide's card on the website is its title page (Lee, 2026-10-17). A lead goes with its parts when both its ends go; an unplugged plug dangles from its lead until its part goes. Removal inside a build: not yet (the bench test's unplugging is a plain Step / Step c pair, plugs lifting off). |
| Fade for parts appearing | Not yet: parts appear at once, and new parts glide in from a little further out. |
| Framed insets and "check this" cues on result views | Done: the eye icon, and a framed close-up on Step Nc (`inset=`: drawn once as the view opens, with chosen parts left out, a blue leader and ring, a red box round the detail; on a one-view step, on that view; several red boxes with `marks`: the LSM's four slots in D1, 2026-10-19). |
| See-through parts (the LSM's published Step 34) | Done (2026-10-19): `ghost={id: alpha}` on a step draws those parts see-through on Step N; on Step Nc they turn solid again over the motion. |
| Parts list | Done (section 13): pages after the title page, from the guide's own parts. Pictures load only when a page is shown (or the step list, which pictures each page small, is opened). |
| **Differs on purpose:** a view reset | A button at the top right, beside full screen, swings the camera back to the step's own view (Lee, 2026-10-16); hidden on note cards and the parts list. Pointing at or clicking a part names it as its labels do where the parts list groups it (Left / Right Joystick). |
| **Differs on purpose:** cautions; reading aloud; keyboard and screen reader | Cautions as decided in section 13. A speaker button beside the caption reads the step (caption and caution) with the browser's own voice: nothing is downloaded. Every control is a button, list or tick box (Tab, then Enter or Space); Left / Right arrow, Home and End step through. A screen reader is told each step as it opens (name, caption, caution, labels); the 3D view, the parts list and the close-ups have text for it. |
| Turning the kit over (re-declared "up") | Done (`flip=True`): the model is shown turned over and turns over as the step opens; the light and the controls stay upright. No cue for "turn it over" yet beyond the motion itself. |
| Moving joints | Not modelled: the arm is shown in the one pose the CAD has it in. |

---

## Appendix A. How the published guides were studied

All 20 guides are published at `https://instructions.online/?id=<guide id>`. The viewer loads each project from a public endpoint, so a guide can be read as data rather than by clicking through it:

    https://api.cadasio.com/api/getProjectViewer?id=<guide id>&withSteps=true&hostname=instructions.online

What comes back (3 to 10 MB of JSON per guide):

| Field | What it holds |
|---|---|
| `orderedSteps`, `steps` | Every authored step: `name`, `behaviour` (`pause` waits for the student, `play` auto-advances, `hidden` is never shown), `animationDuration`, `image` (a rendered picture of the step), and `properties`. |
| `steps[*].properties` | Changes made by that step, keyed by object id: a part (`visible`, `position`, `rotation`, `colour_main`, `style`), an annotation, `default_camera`, or the scene. |
| `assemblyStructure` | The CAD tree as exported by Cadasio's SolidWorks add-in: every component and solid, with its name, bounding box and base colour. `scaleFactor` converts units: millimetres = scene units / `scaleFactor`. |
| `toolboxComponentsProperties` | Every annotation object: lead lines and arrows (3D, with the two parts each end is anchored to), labels and image callouts (2D, positioned in percent of the viewport, with the part feature their leader is anchored to). |
| `scenes`, `cameraProperties` | Background, render style, edge settings, lights, field of view. |

Things that are easy to get wrong when reading it:

- Step `properties` are **changes on top of the previous step** in `orderedSteps`, hidden steps included. To know what a step shows, replay every step before it.
- Visibility is **per solid**. Each solid starts hidden if it or any ancestor carries the CAD "hidden" flag, and is then switched by its own entries; a parent being flagged hidden does not hide solids that were switched on individually.
- (Two rules for visibility were tried against the saved pictures; the per-solid rule above is the one that reproduces them.)
- A part's `position` replaces the translation of its CAD transform. For solids whose own transform is the identity (nearly all of them) that makes it an offset from the assembled pose: `(0, 0, 0)` means seated.
- A part's displayed colour is the last `colour_main` set on it, which a late hidden step may reset. Take the colour it has most often while visible, not the final one.
- Wires are not moved. A loose wire and the same wire routed in place are two separate models that are cross-faded.
- The step picture is saved when the author last touched the step, so a few are stale. The data is the truth for what is visible; the pictures are the truth for how it looks.
- Annotation positions are stored in percent of a roughly 2:1 authoring window.

`tools/cadasio/` holds the scripts used: `digest.py` (one guide's payload to a per-step summary), `thumbs.py` (step pictures and contact sheets) and `atlas.py` (per-solid colours of a named assembly, used to colour our own model of the same part).

## Appendix B. Slips in the published guides

Found along the way; none is a convention. Worth fixing at source.

- Step names: "Transititon" (LAC Deconstruction), "Ttansition" (LAC Full Build, LAC Part 2), "Transiton" (LSM Deconstruction), "Copmleted View" (LSM Part 3 + 4), "Step 20C" (LSM Part 1 + 2), "Step 14C" (LAC Part 1), "Completed Build" instead of "Completed View" (LSM Part 2, Part 1 + 2).
- Numbering: LSM Part 4 has "Step 8" closed by "Step 9c"; LAC Deconstruction uses "Step 41" and "Step 45c" twice; PMG Part 1 and PMG Deconstruction close their last step with "Completed View".
- Labels: PMG Step 10 says "S5" where S6 is meant; PMG has "clk", "dio", "s8", "s9" in lower case; LSM has "Pin d12" (the only label with a word); LSM Full Build Step 19 has the j5 / j16 labels swapped.
- Titles: "Laser Stem Matrix (LSM) - Part 3." has a trailing full stop; "Stem" is not capitalised as "STEM"; PMG Deconstruction's title text runs under the model.
- Tooltips: "Laster Stem Matrix (LSM) - Part 1" on 58-80 solids; "Housing Base - Part A1".
- Colours differ between guides of the same kit for the same part (Nano header strips, Nano USB shell, capacitor can, Dupont pins); PMG's dark wires (`#000000`, `#411900`, `#662639`, `#343232`) are hard to tell apart.
- A few solids keep the CAD default colour `#cad1ee` (two on the LSM push button, one on a USB plug).
- LAC Electronics (the parts overview) is titled "Electronics" but its second view is the wood.
