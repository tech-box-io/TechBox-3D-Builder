# Cross-guide patterns — Step granularity and build ordering

Scope: what counts as ONE numbered step in TechBox's 20 published Cadasio guides, how many student-level parts a step handles, when parts are grouped, and in what order a build is laid out. Everything below was recomputed from the raw payloads and digests; the per-guide reader reports were used as leads only.

## 0. Data, method and definitions

**Guides.** 20 guides, three kits: LSM (Laser STEM Matrix, authored Jul-Aug 2025), LAC (LCD Alarm Clock, Oct-Dec 2025), PMG (Piano Memory Game, May-Aug 2026). 19 have numbered steps; `19075-lac_electronics` is a two-view parts overview with no steps. Dates are the raw `createdDate` fields (LSM 1+2 2025-07-17, LSM Full 2025-08-28, LAC Full 2025-10-06, PMG Full 2026-05-20), so LSM is the oldest convention and PMG the newest.

**Unit of analysis = one numbered step.** A numbered step is the run `Step N` (annotated "what to do" frame, waits) + zero or more auto-advancing `Transition` frames + `Step Nc` (result frame, waits). I grouped viewer frames into such units by order, not by the printed number, so the naming slips do not break the count (LSM Part 4 `Step 8`/`Step 9c`; LAC Deconstruction `Step 41` twice and `Step 45c` twice; PMG Part 1 and PMG Deconstruction whose last step is closed by `Completed View`).

| | guides | numbered steps |
|---|---|---|
| Full builds (LSM 38, LAC 57, PMG 51) | 3 | 146 |
| Part / combined build guides | 14 | 185 |
| All build guides | 17 | **331** |
| Deconstruction guides (LSM 24, LAC 47, PMG 23) | 3 | **94** |
| Parts overview (LAC Electronics) | 1 | 0 |
| Total | 20 | 425 |

**Slices are copies.** Every part/combined guide is a slice of its kit's full build. I mapped each part step to its full-build step and compared an event signature (CAD components appearing/disappearing on the completed frame, kinds that move, annotation counts, number of Transitions): LAC 57/57 identical, PMG 51/51 identical, LSM 47/77 identical; the 30 LSM differences are data-level only (which connector housings are separate CAD nodes, one added Transition in Step 1, 2 extra labels on the Nano step, 6 vs 4 lead lines on D5) and none changes what the step does. So there are **240 independently authored steps** (146 build + 94 take-apart). I report "master" (the 3 full builds, n=146) and "all 17 build guides" (n=331) side by side; the second mostly repeats the first.

**State tracking.** The digest's APPEAR/MOVE lines use ancestor visibility and miss parts whose parent node is flagged hidden (all LAC/LSM wall panels, pose copies). I therefore wrote a leaf-level tracker (`reports/_work_dim_granularity/track.py`): a solid is visible when its own last `visible` says so (initial value = not hidden on itself or any ancestor), node-level flags are ignored; world displacement = sum over the chain of R(ancestors) x (position - own translation). It reproduces the thumbnails where the digest fails (e.g. LAC Electronics [001]: 9 wood parts, digest says 5; LSM Full Step 22 [048]: D4 hovering 69 mm, digest shows nothing).

**Student-level part.** One kit item as the student holds it, not one CAD node. A loose jumper = wire body + 2 black housings (3 CAD components); a captive lead = wire + 1 housing; the rocker switch or potentiometer with its three leads = 7 CAD components; push button with leads = 5; buzzer with leads = 5; RTC with coin cell = 3; USB cable = 3.

**Step types** (hand-labelled for the 240 master steps from the tracker's event table, then propagated through the slice mapping; the event table and labels are in the appendix):

| code | meaning |
|---|---|
| PLACE | a rigid part hovers on its insertion axis and tweens to its seat |
| STAGE2 | second motion of a part that is already on (swing shut, lock, push home) |
| WIRE | a wire connection (straight model swapped for a routed model) |
| CABLE | USB cable plugged in |
| PREP | prepare a part before use (bend leads, split a ribbon) |
| REMOVE_PREP | take something off as preparation (peel backing, strip knob/nut/washer) |
| ADJUST / FLEX | turn a knob / spread or close two posts |
| PICKUP | identify and reposition an already-wired sub-assembly (pose swap, not seated) |
| SEATW | seat an already-wired sub-assembly (pose swap) |
| BATCH | "do the rest": remaining identical parts appear seated |
| RM / RMW / RMCABLE / RMMOD / DISMOUNT / REFIT | take-apart equivalents (remove rigid part / unplug wire(s) / unplug cable / take a freed module away / lift a wired module off the housing / refit hardware) |

## 1. What one step contains — the numbers

### 1.1 Step-type inventory

| type | LSM | LAC | PMG | master (146) | all 17 build guides (331) |
|---|---|---|---|---|---|
| PLACE | 18 | 16 | 14 | 48 (33%) | 114 |
| WIRE | 7 | 20 | 21 | 48 (33%) | 103 |
| SEATW | 2 | 4 | 4 | 10 | 23 |
| PICKUP | 2 | 4 | 3 | 9 | 20 |
| PREP | 3 | 4 | 2 | 9 | 21 |
| STAGE2 | 2 | 1 | 4 | 7 | 16 |
| REMOVE_PREP | 2 | 4 | 0 | 6 | 14 |
| BATCH | 1 | 0 | 2 | 3 | 7 |
| CABLE | 1 | 1 | 1 | 3 | 7 |
| FLEX | 0 | 2 | 0 | 2 | 4 |
| ADJUST | 0 | 1 | 0 | 1 | 2 |
| total | 38 | 57 | 51 | 146 | 331 |

Take-apart (94): RM 45, RMW 26, DISMOUNT 11, RMMOD 5, RMCABLE 3, REFIT 3, FLEX 1.

Steps that add **no** new part to the assembly (PREP, REMOVE_PREP, STAGE2, ADJUST, FLEX, PICKUP): 34/146 master (23%; LSM 9, LAC 16, PMG 9), 77/331 over all build guides.

### 1.2 Student-level parts handled per numbered step, by part kind (master builds, n=146)

| part kind | step type | steps | parts per step |
|---|---|---|---|
| loose jumper wire, both ends (LAC 12, PMG 21) | WIRE | 33 | 1 x33 |
| jumper wire, one end (LSM) | WIRE | 6 | 1 x6 |
| captive lead end (LAC switch/pot/buzzer 8, LSM button) | WIRE | 9 | 1 x8, **2 x1** (LSM Step 19) |
| wood panel | PLACE | 29 | 1 x25, **2 x4** |
| wood panel | STAGE2 | 7 | 1 x6, 4 x1 |
| wood panel | BATCH | 1 | 3 x1 (piano keys) |
| wood panel | FLEX | 2 | 2 x2 (the F7 pair) |
| board / plug-in component (breadboard, Nano, RTC, resistor, capacitor) | PLACE | 11 | 1 x11 |
| pre-wired panel component (switch, pot, push button) | PLACE | 3 | 1 x3 |
| fastener / hardware (nut, washer, knob) | PLACE | 4 | 1 x4 |
| fastener / hardware | REMOVE_PREP | 4 | 1 x4 |
| fastener / hardware | ADJUST | 1 | 1 x1 |
| adhesive backing | REMOVE_PREP | 2 | 1 x2 |
| USB cable | CABLE | 3 | 1 x3 |
| wired module / sub-assembly (LED matrix, LCD, display, shield, buzzer, button module, panel+component) | PICKUP | 9 | 1 x9 |
| wired module / sub-assembly | SEATW | 10 | 1 x10 |
| wired module / sub-assembly | BATCH | 1 | 3 x1 (button modules) |
| LED stem | PLACE | 1 | 1 x1 |
| LED stem | BATCH | 1 | 63 x1 |
| resistor leads | PREP | 3 | 1 x2, 2 x1 ("2x") |
| jumper ribbon | PREP | 6 | 2, 3, 4, 6, 9, 12 wires |

Exactly one student-level item per step: **128/146 (88%)** master, 288/331 (87%) all build guides, 82/94 (87%) take-apart. The 18 master exceptions are all of four kinds: ribbon/lead preparation (7), identical pairs (4 PLACE + 2 FLEX + 1 STAGE2 of four), "do the rest" batches (3), and one two-lead wiring step (LSM Step 19).

There are **no screws** in any of the three kits (0 screw components in any inventory). The only fasteners are one hex nut (LSM push button) and the potentiometer's knob / nut / washer (LAC).

### 1.3 Frames per numbered step

| | 2 frames (N, Nc) | 3 (one Transition) | 4 | 5 |
|---|---|---|---|---|
| master builds (146) | 131 (90%) | 13 | 2 | 0 |
| all build guides (331) | 300 (91%) | 27 | 4 | 0 |
| take-apart (94) | 37 (39%) | 50 | 5 | 2 |

In builds a Transition inside a step occurs only for REMOVE_PREP (6/6 master), two-leg PLACE (6/48) and wired seats (3/10). Viewer frames per numbered step, whole guide: 2.29-2.32 for the three full builds, 2.65-2.88 for the three take-aparts.

How the completed frame is produced (master builds): PLACE = tween 47/48 (the 48th, LSM nut-on, tweens a sub-solid); WIRE = model swap 48/48; PICKUP and SEATW = pose swap 19/19; BATCH = fade-in or swap 3/3; CABLE = fade-in 2, tween 1.

## 2. Granularity rules

### GRAN-1 — One student action per numbered step; every hand action gets a number, including those that add no part
A numbered step is always a `Step N` / `Step Nc` pair (331/331 build steps have both halves; the only missing halves are naming slips). 88% of steps act on exactly one kit item. Manipulations that add nothing still get their own number: 34/146 master steps (peel backing, bend leads, split ribbon, strip hardware, swing a panel shut, push posts home, spread posts, turn a knob, pick up a wired module).
Exceptions: grouping rules GRAN-3, GRAN-4, GRAN-7 below; LSM Step 19 [041] connects two leads.

### GRAN-2 — One rigid part per placement step; never two different parts in motion
PLACE: 44/48 master steps seat exactly one part (103/114 over all build guides); the other 4 (11) seat two *identical* parts (GRAN-3). 0/48 steps move two different kit items. Every step that carries destination labels (hole or pin names) handles exactly one part: 54/55 master steps with labels (exception LSM Step 19).
Systematic nuance: in 6/48 PLACE steps a second, different part *appears* but does not move — the stationary receiving panel fades in already seated and the hand-held part is the one that hovers and travels: LSM Step 2 [004] (base D1 under the breadboard), LSM Step 17 [037] (panel D2 for the push button), LAC Step 2 [004] (F3), LAC Step 15 [032] (F4 for the switch), LAC Step 25 [055] (F1 for the pot), PMG Step 26 [059] (H1 datum, H2 hovers).

### GRAN-3 — Two identical parts may share one placement step only when they share one motion and one view
4 master steps: LSM Step 27 [060] 2x D9 (64.6 mm each, 4 lead lines), LSM Step 32 [071] and Step 33 [073] 2x D11 each (81.6/81.6 and 83.1/77.4 mm, 2 lead lines = one per post), LAC Step 41 [090] 2x F7 (80.3 mm each, 2 lead lines). All are wood, all have 0 labels, all move by the same vector. Four identical D11 posts are split 2+2 with an 82 degree camera turn between, because only two are clearly visible from one side. Never more than 2 parts are animated together in a build.
Not grouped although identical: the two LAC resistors (Steps 5 and 6: each needs its own hole labels); the four PMG button modules while being wired; every jumper wire.

### GRAN-4 — Three or more identical drop-in parts: show one in full, then one "do the rest" step
3/3 cases: LED stems 1 + 63 (LSM Step 37 [083] with one lead line, Step 38 [085] eye icon then 63 fade in seated at [086], preceded by the `LED Stems` card with "64x" [082]); piano keys 1 + 3 (PMG Step 38 [083], Step 39 [085] with an inset "H9 3x", [086] three keys appear); button modules into their slots 1 + 3 (PMG Step 33 [073] two eye icons, Step 34 [075] one eye on the next button, [076] the other three swap to installed). The batch step has no per-part motion and no lead lines.
Inconsistency (anomaly, not convention): the quantity cue differs each time — a card with "64x" plus an eye, an inset with "3x", or just an eye.

### GRAN-5 — One wire per step, never grouped; a loose jumper is one step for both ends
47/48 master WIRE steps connect one wire (100/103 over all guides). The exception is LSM Step 19 (both leads of the push-button pigtail, two labels) in its 3 copies.
Ends per step differ by kit and this is a convention that changed over time:
- LSM (2025, oldest): one wire END per step. The 3-wire male-female ribbon takes 6 steps: male ends into i2, i3, b19 (Steps 10-12), then female ends onto V+, In, V- (Steps 13-15), one label per step.
- LAC and PMG (later): one whole loose jumper per step, both ends, exactly 2 labels + 1 eye icon: 33/33 master (LAC 12, PMG 21), 66/66 over all guides.
- Captive leads (wire soldered to a component): one free end per step with 1 label + 1 eye: 8/8 LAC (switch 3, pot 3, buzzer 2).
No wire step has a lead line (0/48), none has a Transition (0/48), none is shown in isolation (0/48), and none moves a part.

### GRAN-6 — A kit item that arrives pre-assembled is one part and moves as one unit
Jumper = wire + its housings, always together: loose jumper completed frame adds 1 wire + 2 housings in 66/66 LAC+PMG steps; captive lead 1 wire + 1 housing in 16/16. No step anywhere adds housings on their own. Pre-wired components travel rigidly with their leads: rocker switch 7 CAD components moving 81.2 mm together (LAC Step 15), potentiometer 7 components 79.1 mm (LAC Step 25), push button 5 components 102.5 mm (LSM Step 17), RTC + coin cell 3 components 33.6 mm (LAC Step 7), USB plug 3 components 22.9 mm (PMG Step 25). The LAC Electronics overview confirms the unit: 31 CAD components are shown as 9 kit items (switch group 7, buzzer group 5, pot + knob + nut + washer 4, USB 3 share one displacement each).

### GRAN-7 — Preparation is its own numbered step, shown in isolation, immediately before first use
15/146 master steps are preparation (9 PREP + 6 REMOVE_PREP): peel backing (LSM 1, LAC 1), bend resistor leads (LSM 4 and 7, LAC 4), split a ribbon (LSM 9; LAC 8, 19, 35; PMG 2, 15), strip hardware (LSM 16; LAC 22-24). All 15 are shown with the rest of the build hidden (13 hide an existing assembly; the 2 peel steps are Step 1, where only breadboard + backing exist). All 6 removals in the full builds use Step N (red arrow) -> auto Transition (part slides off) -> Step Nc (part gone).
Ribbon splitting is the one place where many wires are handled at once, and it is sized to the wiring block that follows: 6/6 (LSM 3 wires -> Steps 10-15; LAC 6 -> 9-14, 2 -> 20-21, 4 -> 36-39; PMG 12 -> 3-14, 9 -> 16-24).
Exceptions: LAC bends both resistors in one prep step with a "2x" label (Step 4) while LSM gives each resistor its own bend step (Steps 4, 7). The LSM capacitor has no prep step, only a card. In LSM Part 1 and Part 1+2 the peel step has no Transition (2 of 14 removal steps over all guides).

### GRAN-8 — Every fastener gets its own step, coming off and going on
8/8 master hardware operations are single-part steps: LAC knob, nut, washer off (Steps 22, 23, 24) and washer, nut, knob on (26, 27, 28); LSM nut off (16) and on (18). Take-apart: 7/7 (LAC knob/nut/washer off 12-14, refit 16-18; LSM nut 18). Never grouped (0/15), although three of them sit on one shaft. Off order is outside-in and on order is the exact reverse.
No screws exist in these kits, so there is no evidence for or against batching identical screws; the nearest evidence (identical drop-in parts) is GRAN-3 / GRAN-4.

### GRAN-9 — A second motion of the same part is either its own numbered step or an auto Transition, never one long animation
Own numbered step (STAGE2), 7 master: PMG H5 (29/30), H6 (31/32), H7 (35/36), H10 (40/41); LSM D3 (24/25) and D11 push-home (34); LAC F9 (45/46). Auto Transition inside one step, 9 master: LSM D10 (29); LAC F9 slide (45, two Transitions), F2 (56), LCD seat (52, two); PMG H11 (42), H12 (43), H14 (51), display (48), matrix (50).
What decides: in PMG the camera turns 62-85 degrees between the two numbered halves in 4/4 cases and never moves inside a Transition (0/9), so "needs a new viewpoint -> new numbered step" holds 5/7 overall. Exceptions: LSM Step 25 and LAC Step 46 are separate numbered steps with the camera unchanged.

### GRAN-10 — An already-wired sub-assembly takes two numbered steps: pick up, then attach
7/10 master SEATW steps are immediately preceded by a PICKUP step for the same item: LAC F4 (48 -> 49), LCD (51 -> 52), F1 (53 -> 54); PMG I/O module (45 -> 46), display (47 -> 48), LED matrix (49 -> 50); LSM LED matrix (28, then D10 clipped on in 29, seated in 30). PICKUP has an eye icon and no lead line (9/9); the attach step has lead lines or an arrow.
Single-step seats (3): LAC buzzer (43), PMG first button module (33) — small modules with no tabs, cued by two eye icons (part + destination) — and LSM panel D2 (21, arrow only).
Two further PICKUP steps only move a wired item out of the way (LSM Step 23 matrix through the wall notch; LAC Step 47 front panel aside).

### GRAN-11 — Things the student does not attach get no step
The base/datum panel never has its own step (GRAN-2). Loose modules are introduced by a named section card and are simply present when the build returns: PMG shield, display, dot matrix; LAC buzzer, LCD; the LSM LED matrix just appears hovering at Step 13 [028]. In PMG the 2nd-4th button modules fade in during auto Transitions between steps ([013], [020], [027]). Section cards precede the first step that uses the component in 14/14 cases across the three full builds and consume no step number (once, PMG `4-Digit Display`, a ribbon-split step sits between the card and the first wire).

### GRAN-12 — A Part is a self-contained block of 5-26 numbered steps and restarts at Step 1
Single-part guides: 5, 8, 8, 11, 12, 13, 14, 14, 17, 18, 26 numbered steps (median 13, mean 13.3). Combined guides 18 and 21; full builds 38, 57, 51. Part boundaries always fall after a wiring run or mechanical block is complete (LSM after Steps 8, 21, 26; LAC after 14, 32, 40; PMG after 14, 25) and never between a prep step and its use or between the two stages of one joint. The enclosure is always its own final Part(s). Numbering restarts at 1 in every Part (11/11) and is continuous in full builds.

## 3. Ordering rules

### ORD-1 — Electronics on the open base first, enclosure afterwards; the USB cable is the last electronics step
Sequence strings for the three full builds (P place, w wire, r prep, x remove-prep, C cable, S seat wired, u pick up, 2 second stage, B batch, f flex, a adjust):

```
LSM  xPPrPPrPrwwwwwwxPPwCSPuP2PPuPSPPP2PPPB
LAC  xPPrPPPrwwwwwwPwwwrwwxxxPPPPawwwwwrwwwwCPfSfP2uuSPuSuSPPP
PMG  PrwwwwwwwwwwwwrwwwwwwwwwCPPPP2P2SBP2PPBP2PPPuSuSuSP
```

All wiring is finished before the first enclosure panel in 3/3 full builds (last wire step 19 / 39 / 24; first enclosure step 21 / 41 / 26). The USB cable is the step directly after the last wire and directly before the enclosure in 3/3 (Step 20 / 40 / 25), i.e. at 53% / 70% / 49% of the numbered steps. The first component placed is always the controller on its carrier: breadboard then Nano (LSM, LAC Steps 2-3 after peeling the backing), Nano onto shield (PMG Step 1). Small plug-in parts follow (LSM resistor, capacitor, resistor; LAC two resistors, RTC), then wiring.
Exception: LSM Part 2 and Part 1+2 put the button panel (their Step 12 / 20) before the USB cable (13 / 21); the Full Build reverses the two.

### ORD-2 — Finish one component completely before starting the next: prepare -> mount -> wire all its pins
LAC: RTC placed (7), ribbon split (8), its 4 wires (9-12); switch mounted (15), 3 leads (16-18), 2 bridging jumpers (19-21); pot stripped, mounted, refitted, set (22-29), 3 leads (30-32); buzzer card, 2 leads (33-34); LCD card, 4 wires (36-39). PMG: each of 4 buttons, the display and the matrix gets its wires in one unbroken run before the next module appears. 11/11 component blocks in LAC + PMG are contiguous. Wiring runs (consecutive WIRE steps): LSM 6, 1; LAC 6, 3, 2, 5, 4; PMG 12, 9 — each run starts right after a PLACE of that component or a ribbon-split PREP.
Exception: LSM connects all three near ends (10-12) before the module is even shown, then all three far ends (13-15).

### ORD-3 — Within a module, wire in the physical order of its pins or leads, not by electrical function
- PMG: 6/6 modules follow header order (button VCC, OUT, GND x4; display CLK, DIO, VCC, GND; matrix VCC, GND, DIN, CS, CLK) and the shield pin number never decreases across all 21 wires (4,4,4,5,5,5,6,6,6,7,7,7,8,9,9,9,11,11,11,12,13: 20/20 adjacent pairs).
- LAC: LCD header GND, VCC, SDA, SCL (4/4). Captive leads always red, tan, black (switch 16-18, pot 30-32) and red, black (buzzer 33-34): 3/3 components.
- LSM: far ends follow pad order V+, In, V-.
Power-pair-first holds in only 4 of 13 module blocks (LSM near ends, LAC RTC, LAC LCD, PMG matrix), so it is not a rule. Wire colour is not electrical either: wires are taken in ribbon order in LSM (3/3) and PMG (21/21); red is GND on the PMG display (Step 19), black goes to (+) in LAC (Step 9).
Exceptions: LAC RTC goes i23 (VCC), i24 (GND), i22, i21 — one swap against pin order; LAC's 6-wire ribbon is not used in ribbon order (ribbon green, blue, purple, grey, dark red, black [018]; used black, green, purple, blue, grey, dark red); the Nano's own two rail jumpers come after the RTC's (Steps 13-14).

### ORD-4 — Panel-mounted components are sub-assembled on their loose panel, in isolation, long before that panel joins the box
3/3: LSM push button into D2 (Steps 16-18, only button + nut + panel on screen), leads wired (19), panel onto base (21). LAC switch into F4 (15), wired (16-18), panel attached at Step 49; pot into F1 (22-29), wired (30-32), panel attached at Step 54. All 7 mount/hardware steps are shown with the rest of the build hidden; the build fades back for the first lead.

### ORD-5 — Enclosure: datum first, carriers before what they carry, wired modules just in time, the covering panel last
Common to 3/3 kits: (a) the base panel is the datum and is on screen from the first mechanical step; (b) a bracket or support is placed before the thing it holds (LSM D9 before the matrix, D11 posts before D7/D8; LAC F7 posts before the buzzer, F9 before the LCD; PMG H11/H12/H13 before display and matrix); (c) each wired module is seated at the last moment access allows, immediately after its mount exists; (d) the panel that hides the interior goes last (LSM top plate D8 then stems; LAC end F6; PMG face plate H14); (e) high-count small parts go at the very end (64 stems).
Not common: the direction of growth. LSM builds walls first (D2, D4, D3, D5), then the interior, then stacks upward; LAC builds the interior first (F7, buzzer, F9), then top, front, ends, back; PMG builds frame, underside deck, then upper parts. "Bottom-up" is therefore not a universal rule. First-leg insertion direction of the 48 measurable PLACE/CABLE moves, relative to the displayed up-axis (the scene up-axis is re-declared for some steps): straight down 25 (LSM 14, LAC 7, PMG 4), sideways 17 (2, 8, 7), oblique 5 (0, 1, 4), up 1. All 11 breadboard/shield plug-ins drop straight down.

### ORD-6 — Group work that needs the same orientation so the model is turned over once
PMG does all underside work in one block of 8 consecutive steps (29-36) with the scene up-axis flipped once and flipped back once. LSM has 5 non-upright steps in 3 separate episodes (23; 24-26; 34) and LAC 10 in 3 (22-29 as an isolated sub-assembly; 35; 56). Only the newest kit follows this cleanly, so treat it as the target rather than a proven habit.

### ORD-7 — Engraved part numbers equal the build order only in the newest kit
PMG: H1...H14 are installed in exactly numeric order (14/14). LSM: D1, D2, D4, D3, D5, D9, D10, D6, D11, D7, D8 (7/10 adjacent pairs ascending). LAC: F3, F4, F1, F7, F9, F8, F5, F2, F6 by first appearance (4/8 ascending). This is a PMG convention, not a kit-wide one.

## 4. Take-apart guides

### DEC-1 — One removable unit per step; identical multiples go together; wired modules come off as a unit and are dismantled later
RM: 39/45 steps remove one part; the 6 others remove identical sets (64 stems in one step, 4 piano keys, 2x D11 twice, 2x D9, 2x F7). Wired modules are first lifted off the housing still wired (DISMOUNT 11 steps, pose swap), set aside, and unplugged later; 4 button modules leave the housing in one step and their wires in another.

### DEC-2 — Wire granularity in take-apart is inconsistent between kits
LAC (2025-11): one wire per step, 20 wires in 20 steps (12 whole jumpers with a Transition, 8 lead ends without). LSM: three male ends one per step (11-13), then the 3-way connector in one step (15). PMG (2026-08, newest): bundles — 5 matrix wires in one step (18), 16 wires in one step with two arrows (22).

### DEC-3 — Take-apart is close to, but not exactly, the reverse of the build, and has fewer steps
Steps: LSM 24 vs 38 (0.63), LAC 47 vs 57 (0.82), PMG 23 vs 51 (0.45). Matching each removed CAD component to the build step where it first appears gives Spearman rank correlation between take-apart order and build order of -0.93 (LSM), -0.91 (LAC), -0.99 (PMG). PMG housing steps 1-16 undo build 51 down to 26 in strict order. Build pairs are merged (slide + lock, one + the rest, pick up + seat) and preparation steps have no counterpart. The base carrier is never removed (breadboard on D1 / F3; bare shield).

## 5. Numeric defaults

| quantity | value | basis |
|---|---|---|
| frames per numbered step | 2 (Step N, Step Nc); +1 auto Transition in 9%, +2 in 1% | 146 master build steps |
| frames per numbered step, take-apart | 3 typical (53%); 2 in 39% | 94 steps |
| viewer frames per numbered step, whole guide | 2.3 build, 2.7-2.9 take-apart | 6 master guides |
| student-level parts per step | 1 (88%) | 128/146 |
| max parts animated together | 2, identical only | 4 master steps |
| batch after exemplar | 3 or more identical parts; seen 3, 3, 63 | 3/3 cases |
| wires per wiring step | 1 | 47/48 |
| wire ends per step | 2 for a loose jumper (LAC, PMG); 1 for a captive lead; 1 in LSM | 33/33; 8/8; 6/6 |
| labels per wiring step | 2 loose jumper, 1 captive lead | 33/33; 8/8 |
| fasteners per step | 1 | 15/15 |
| ribbon split | one prep step for exactly the next run: 2-12 wires | 6/6 |
| share of steps that add no part | 23% | 34/146 |
| share of wiring steps | 33% (LSM 18%, LAC 35%, PMG 41%) | 48/146 |
| numbered steps per Part | median 13, range 5-26 | 11 single-part guides |
| numbered steps per full build | 38, 57, 51 | 3 |
| end of electronics phase | USB cable at 49-70% of the steps | 3 full builds |
| CAD components per kit item | jumper 3, captive lead 2, switch/pot with leads 7, push button 5, buzzer 5, RTC 3, USB 3 | tracker |
| take-apart / build step ratio | 0.45-0.82 | 3 kits |
| take-apart vs build order | Spearman -0.91 to -0.99 | 3 kits |
| second stage as own step | when the view must turn; observed turns 62-117 degrees | 5/7 |
| flipped-orientation block | one block (8 steps) per build | PMG only |

## 6. Anomalies and inconsistencies (not conventions)

- Wire-end granularity changed between kits: LSM one end per step, LAC/PMG one wire per step; LSM Step 19 does two leads at once.
- LAC bends both resistors in one "2x" prep step; LSM bends each in its own step.
- Quantity cue for "do the rest" differs in all three cases (card "64x" + eye; inset "H9 3x"; eye only). The label is "64x" in LSM Full and "64X" in Part 4 / Part 3+4.
- LSM Part 2 / Part 1+2 order panel-then-USB; LSM Full orders USB-then-panel.
- LSM Part 3+4 Step 1 repeats the panel step that Part 2 already contains (a student doing 1+2 then 3+4 does it twice).
- LAC RTC wires swap VCC/GND against pin order; LAC's 6-wire ribbon is not used in ribbon order.
- PMG Step 10 [023] labels the shield pin "S5" where S6 is meant; PMG Step 15 [035] (ribbon split) has no annotation while the equivalent Step 2 has an eye icon.
- Numbering slips: LSM Part 4 `Step 8` is completed by `Step 9c` (numbers 1-13 for 12 steps); LAC Deconstruction has `Step 41` twice and `Step 45c` twice; PMG Part 1 and PMG Deconstruction have no final `c` step (Completed View stands in).
- LSM Deconstruction Step 4 hides D5 together with all four D11 posts for one frame (the posts return and are really removed in Steps 6-7); Step 17 combines unplugging two leads with removing panel D2.
- PMG Deconstruction never removes H2 and H3 in a step; they vanish when the scene switches.
- Take-apart wire granularity differs per kit (DEC-2).
- The LED matrix in LSM is never "placed": it appears hovering at Step 13 and lies beside the base from Step 19 with no step for the change.
- Second-stage steps without a camera change (LSM 25, LAC 46) contradict the PMG pattern.

## 7. Open questions

See the structured result; they concern the one-end vs whole-wire choice, screws, the threshold for batching, and whether part numbers should follow build order.

## Appendix A — files

- `reports/_work_dim_granularity/track.py` — leaf-level state tracker (all 20 guides) -> `state/<guide>.json`
- `unitsmod.py`, `feat.py` — grouping into numbered steps and per-step events -> `units.json`
- `labels.py` — hand labels for the 240 master steps and the slice mapping; `check_map.py` verifies the mapping
- `stats1.py` ... `stats10.py`, `decon_map.py`, `elec.py` — the tables above

## Appendix B — per-step tables for the six master guides

Columns: `auto frames` = Transitions inside the step. Annotations on Step N: L lead lines, T text labels, A arrows, E eye icons, I inset pictures, D pin-disc images. The last column lists CAD components by kind (not student-level parts): new on the hover frame / new on the completed frame / removed on the completed frame / moved between hover and completed. `cap` = connector housing, `ribbon` = ribbon or one of its strands. `(context restored)` = more than 8 components appear at once on the hover frame (the build fading back after an isolated view, or a whole ribbon). A `-` in all four positions means the change is on sub-solids of one component (bent leads, nut on the push button).

#### LSM Full Build (38 numbered steps)

| # | viewer idx | step name | type | part kind | parts | wire ends | what the student does | auto frames | Step N annotations | CAD comps: hover + / done + / done - / moved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [001]-[003] | Step 1 | REMOVE_PREP | backing | 1 |  | peel adhesive backing off breadboard | 1 | A1 I1 | - / - / paper1 / paper1 |
| 2 | [004]-[005] | Step 2 | PLACE | breadboard | 1 |  | breadboard onto base D1 (D1 fades in seated) | 0 | L4 | wood1 / - / - / breadboard1 |
| 3 | [006]-[007] | Step 3 | PLACE | nano | 1 |  | Nano into breadboard | 0 | L4 | nano1 / - / - / nano1 |
| 4 | [008]-[009] | Step 4 | PREP | resistor | 1 |  | bend resistor 1 leads | 0 | E1 | resistor1 / - / - / - |
| 5 | [010]-[011] | Step 5 | PLACE | resistor | 1 |  | resistor 1 | 0 | L2 T2 | breadboard1,nano1,wood1 / - / - / resistor1 |
| 6 | [013]-[014] | Step 6 | PLACE | capacitor | 1 |  | capacitor | 0 | L2 T2 E1 | breadboard1,nano1,resistor1,wood1 / - / - / capacitor1 |
| 7 | [015]-[016] | Step 7 | PREP | resistor | 1 |  | bend resistor 2 leads | 0 | E1 | resistor1 / - / - / - |
| 8 | [017]-[018] | Step 8 | PLACE | resistor | 1 |  | resistor 2 | 0 | L2 T2 | breadboard1,capacitor1,nano1,resistor1,wood1 / - / - / resistor1 |
| 9 | [019]-[020] | Step 9 | PREP | ribbon | 3 |  | split 3-wire ribbon | 0 | E1 | (context restored) / ribbon1 / cap6,wire3 / - |
| 10 | [021]-[022] | Step 10 | WIRE | jumper-end | 1 | 1 | white male end -> i2 | 0 | T1 | (context restored) / cap2,wire1 / cap2 / - |
| 11 | [023]-[024] | Step 11 | WIRE | jumper-end | 1 | 1 | grey male end -> i3 | 0 | T1 | - / cap1,wire1 / cap1 / - |
| 12 | [025]-[026] | Step 12 | WIRE | jumper-end | 1 | 1 | purple male end -> b19 | 0 | T1 | - / cap2,wire1 / cap2,ribbon1 / - |
| 13 | [028]-[029] | Step 13 | WIRE | jumper-end | 1 | 1 | white female end -> V+ | 0 | T1 D2 | (context restored) / cap1,wire1 / cap1,wire1 / - |
| 14 | [030]-[031] | Step 14 | WIRE | jumper-end | 1 | 1 | purple female end -> In | 0 | T1 D2 | - / cap1,wire1 / cap1,wire1 / - |
| 15 | [032]-[033] | Step 15 | WIRE | jumper-end | 1 | 1 | grey female end -> V- | 0 | T1 D2 | - / cap1,wire1 / cap1,wire1 / - |
| 16 | [034]-[036] | Step 16 | REMOVE_PREP | nut | 1 |  | take nut off push button | 1 | A1 | cap2,pushbutton1,wire2 / - / - / - |
| 17 | [037]-[038] | Step 17 | PLACE | pushbutton | 1 |  | pre-wired push button into panel D2 (D2 fades in) | 0 | L1 | wood1 / - / - / cap2,pushbutton1,wire2 |
| 18 | [039]-[040] | Step 18 | PLACE | nut | 1 |  | nut back on | 0 | L1 | - / - / - / - |
| 19 | [041]-[042] | Step 19 | WIRE | lead | 2 | 2 | both button leads -> j5, j16 | 0 | T2 | (context restored) / cap2,wire2 / cap2,wire2 / - |
| 20 | [044]-[045] | Step 20 | CABLE | usb | 1 |  | USB cable into Nano (fade in) | 0 | E1 | (context restored) / usb2,wire1 / - / - |
| 21 | [046]-[047] | Step 21 | SEATW | panel+button | 1 |  | D2 panel sub-assembly onto base (pose swap, arrow) | 0 | A1 | - / pushbutton1,wire2,wood1 / pushbutton1,wire2,wood1 / - |
| 22 | [048]-[049] | Step 22 | PLACE | wood | 1 |  | D4 | 0 | L4 | wood1 / - / - / wood1 |
| 23 | [050]-[051] | Step 23 | PICKUP | matrix | 1 |  | carry LED matrix outside, wires through notch (pose swap) | 0 | A1 E1 | - / cap3,matrix1,wire3 / cap3,matrix1,wire3 / - |
| 24 | [053]-[054] | Step 24 | PLACE | wood | 1 |  | D3 hook in tilted | 0 | L2 | wood1 / - / - / wood1 |
| 25 | [055]-[056] | Step 25 | STAGE2 | wood | 1 |  | D3 swing shut | 0 | L2 | - / - / - / wood1 |
| 26 | [057]-[058] | Step 26 | PLACE | wood | 1 |  | D5 | 0 | L4 | wood1 / - / - / wood1 |
| 27 | [060]-[061] | Step 27 | PLACE | wood | 2 |  | 2x D9 supports | 0 | L4 | wood2 / - / - / wood2 |
| 28 | [062]-[063] | Step 28 | PICKUP | matrix | 1 |  | lift LED matrix (pose swap) | 0 | E1 | - / cap3,matrix1,paper1,wire3 / cap3,matrix1,wire3 / - |
| 29 | [064]-[066] | Step 29 | PLACE | wood | 1 |  | D10 clip onto matrix (2 legs via Transition) | 1 | L2 | wood1 / - / - / wood1 |
| 30 | [067]-[068] | Step 30 | SEATW | matrix | 1 |  | lower matrix + D10 into box (pose swap) | 0 | L2 | - / cap3,matrix1,wire3,wood1 / cap3,matrix1,wire3,wood1 / - |
| 31 | [069]-[070] | Step 31 | PLACE | wood | 1 |  | D6 | 0 | L4 I1 | wood1 / - / - / wood1 |
| 32 | [071]-[072] | Step 32 | PLACE | wood | 2 |  | 2x D11 posts | 0 | L2 | wood2 / - / - / wood2 |
| 33 | [073]-[074] | Step 33 | PLACE | wood | 2 |  | 2x D11 posts | 0 | L2 | wood2 / - / - / wood2 |
| 34 | [075]-[076] | Step 34 | STAGE2 | wood | 4 |  | push 4 posts home from underneath | 0 | L4 E1 | - / - / - / wood4 |
| 35 | [078]-[079] | Step 35 | PLACE | wood | 1 |  | D7 | 0 | L4 | wood1 / - / - / wood1 |
| 36 | [080]-[081] | Step 36 | PLACE | wood | 1 |  | D8 | 0 | L4 | wood1 / - / - / wood1 |
| 37 | [083]-[084] | Step 37 | PLACE | stem | 1 |  | one LED stem (exemplar) | 0 | L1 | (context restored) / - / - / stem1 |
| 38 | [085]-[086] | Step 38 | BATCH | stem | 63 |  | remaining 63 stems fade in | 0 | E1 | - / stem63 / - / usb1 |

#### LAC Full Build (57 numbered steps)

| # | viewer idx | step name | type | part kind | parts | wire ends | what the student does | auto frames | Step N annotations | CAD comps: hover + / done + / done - / moved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [001]-[003] | Step 1 | REMOVE_PREP | backing | 1 |  | peel adhesive backing | 1 | A1 I1 | paper1 / - / paper1 / paper1 |
| 2 | [004]-[005] | Step 2 | PLACE | breadboard | 1 |  | breadboard onto F3 (F3 fades in seated) | 0 | L4 E1 | wood1 / - / - / breadboard1 |
| 3 | [006]-[007] | Step 3 | PLACE | nano | 1 |  | Nano | 0 | L2 T2 | nano1 / - / - / nano1 |
| 4 | [008]-[009] | Step 4 | PREP | resistor | 2 |  | bend resistor leads (one shown, "2x") | 0 | T1 E1 | resistor1 / - / - / - |
| 5 | [010]-[011] | Step 5 | PLACE | resistor | 1 |  | resistor 1 | 0 | L2 T2 | breadboard1,nano1,wood1 / - / - / resistor1 |
| 6 | [012]-[013] | Step 6 | PLACE | resistor | 1 |  | resistor 2 | 0 | L2 T2 | resistor1 / - / - / resistor1 |
| 7 | [015]-[016] | Step 7 | PLACE | rtc | 1 |  | RTC module with coin cell | 0 | L2 T2 | breadboard1,nano1,resistor2,wood1 / - / - / coincell2,rtc1 |
| 8 | [017]-[018] | Step 8 | PREP | ribbon | 6 |  | split 6-wire ribbon | 0 | E1 | ribbon1 / - / - / - |
| 9 | [019]-[020] | Step 9 | WIRE | jumper | 1 | 2 | i23 -> (+) rail | 0 | T2 E1 | (context restored) / cap2,wire1 / ribbon1 / - |
| 10 | [021]-[022] | Step 10 | WIRE | jumper | 1 | 2 | i24 -> (-) rail | 0 | T2 E1 | ribbon1 / cap2,wire1 / ribbon1 / - |
| 11 | [023]-[024] | Step 11 | WIRE | jumper | 1 | 2 | i22 -> a8 | 0 | T2 E1 | ribbon1 / cap2,wire1 / ribbon1 / - |
| 12 | [025]-[026] | Step 12 | WIRE | jumper | 1 | 2 | i21 -> a9 | 0 | T2 E1 | ribbon1 / cap2,wire1 / ribbon1 / - |
| 13 | [027]-[028] | Step 13 | WIRE | jumper | 1 | 2 | a14 -> (-) rail | 0 | T2 E1 | ribbon1 / cap2,wire1 / ribbon1 / - |
| 14 | [029]-[030] | Step 14 | WIRE | jumper | 1 | 2 | a12 -> (+) rail | 0 | T2 E1 | ribbon1 / cap2,wire1 / ribbon1 / - |
| 15 | [032]-[033] | Step 15 | PLACE | switch | 1 |  | pre-wired rocker switch into F4 (F4 fades in) | 0 | L1 | wood1 / - / - / cap3,switch1,wire3 |
| 16 | [034]-[035] | Step 16 | WIRE | lead | 1 | 1 | switch red -> j27 | 0 | T1 E1 | (context restored) / cap1,wire1 / cap1,wire1 / - |
| 17 | [036]-[037] | Step 17 | WIRE | lead | 1 | 1 | switch tan -> (+) | 0 | T1 E1 | - / cap1,wire1 / cap1,wire1 / - |
| 18 | [038]-[039] | Step 18 | WIRE | lead | 1 | 1 | switch black -> j29 | 0 | T1 E1 | - / cap1,wire1 / cap1,wire1 / - |
| 19 | [040]-[041] | Step 19 | PREP | ribbon | 2 |  | split jumper pair | 0 | E1 | cap4,wire2 / - / - / cap4,wire2 |
| 20 | [042]-[043] | Step 20 | WIRE | jumper | 1 | 2 | j1 -> i27 | 0 | T2 E1 | (context restored) / cap2,wire1 / cap2,wire1 / - |
| 21 | [044]-[045] | Step 21 | WIRE | jumper | 1 | 2 | j3 -> i29 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 22 | [046]-[048] | Step 22 | REMOVE_PREP | knob | 1 |  | pull knob off pot | 1 | A1 | (context restored) / - / knob1 / knob1 |
| 23 | [049]-[051] | Step 23 | REMOVE_PREP | nut | 1 |  | nut off | 1 | A1 | - / - / nut1 / nut1 |
| 24 | [052]-[054] | Step 24 | REMOVE_PREP | washer | 1 |  | washer off | 1 | A1 | - / - / washer1 / washer1 |
| 25 | [055]-[056] | Step 25 | PLACE | pot | 1 |  | pre-wired pot through F1 (F1 fades in) | 0 | L1 | wood1 / - / - / cap3,pot1,wire3 |
| 26 | [057]-[058] | Step 26 | PLACE | washer | 1 |  | washer on | 0 | L1 | washer1 / - / - / washer1 |
| 27 | [059]-[060] | Step 27 | PLACE | nut | 1 |  | nut on | 0 | L1 | nut1 / - / - / nut1 |
| 28 | [061]-[062] | Step 28 | PLACE | knob | 1 |  | knob on | 0 | L1 | knob1 / - / - / knob1 |
| 29 | [063]-[064] | Step 29 | ADJUST | knob | 1 |  | turn knob to stop | 0 | E1 | - / - / - / knob1 |
| 30 | [065]-[066] | Step 30 | WIRE | lead | 1 | 1 | pot red -> (+) | 0 | T1 E1 | (context restored) / cap1,wire1 / cap1,wire1 / - |
| 31 | [067]-[068] | Step 31 | WIRE | lead | 1 | 1 | pot tan -> a5 | 0 | T1 E1 | - / cap1,wire1 / cap1,wire1 / - |
| 32 | [069]-[070] | Step 32 | WIRE | lead | 1 | 1 | pot black -> (-) | 0 | T1 E1 | - / cap1,wire1 / cap1,wire1 / - |
| 33 | [072]-[073] | Step 33 | WIRE | lead | 1 | 1 | buzzer red -> j4 | 0 | T1 E1 | (context restored) / cap1,wire1 / cap1,wire1 / - |
| 34 | [074]-[075] | Step 34 | WIRE | lead | 1 | 1 | buzzer black -> (-) | 0 | T1 E1 | - / cap1,wire1 / cap1,wire1 / - |
| 35 | [076]-[077] | Step 35 | PREP | ribbon | 4 |  | split 4-wire ribbon | 0 | E1 | (context restored) / - / - / cap6,wire3 |
| 36 | [079]-[080] | Step 36 | WIRE | jumper | 1 | 2 | LCD GND | 0 | T2 E1 | (context restored) / cap2,wire1 / cap2,wire1 / - |
| 37 | [081]-[082] | Step 37 | WIRE | jumper | 1 | 2 | LCD VCC | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 38 | [083]-[084] | Step 38 | WIRE | jumper | 1 | 2 | LCD SDA | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 39 | [085]-[086] | Step 39 | WIRE | jumper | 1 | 2 | LCD SCL | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 40 | [088]-[089] | Step 40 | CABLE | usb | 1 |  | USB cable (fade in) | 0 | E1 | (context restored) / usb2,wire1 / - / - |
| 41 | [090]-[091] | Step 41 | PLACE | wood | 2 |  | 2x F7 posts | 0 | L2 | wood2 / - / - / wood2 |
| 42 | [092]-[093] | Step 42 | FLEX | wood | 2 |  | spread F7 posts | 0 | A2 | - / - / - / wood2 |
| 43 | [094]-[095] | Step 43 | SEATW | buzzer | 1 |  | buzzer between posts (pose swap) | 0 | E2 | - / buzzer1,wire2 / buzzer1,wire2 / - |
| 44 | [096]-[097] | Step 44 | FLEX | wood | 2 |  | close F7 posts | 0 | E2 | - / - / - / wood2 |
| 45 | [098]-[101] | Step 45 | PLACE | wood | 1 |  | F9 hook in (2 Transitions) | 2 | L2 | wood1 / - / - / wood1 |
| 46 | [102]-[103] | Step 46 | STAGE2 | wood | 1 |  | F9 upright | 0 | L1 E1 | - / - / - / wood1 |
| 47 | [104]-[105] | Step 47 | PICKUP | panel+pot | 1 |  | move F1 panel aside (pose swap, arrow) | 0 | A1 E1 | - / knob1,pot1,wire3,wood1 / knob1,nut1,pot1,wire3,wood1 / - |
| 48 | [106]-[107] | Step 48 | PICKUP | panel+switch | 1 |  | pick up F4 (pose swap) | 0 | E1 | - / switch1,wire3,wood1 / switch1,wire3,wood1 / - |
| 49 | [109]-[110] | Step 49 | SEATW | panel+switch | 1 |  | attach F4 | 0 | L4 | - / switch1,wire3,wood1 / switch1,wire3,wood1 / - |
| 50 | [111]-[112] | Step 50 | PLACE | wood | 1 |  | F8 | 0 | L2 | wood1 / - / - / wood1 |
| 51 | [113]-[114] | Step 51 | PICKUP | lcd | 1 |  | pick up LCD | 0 | E1 | - / cap4,lcd1,wire4 / cap4,lcd1,wire4 / - |
| 52 | [115]-[118] | Step 52 | SEATW | lcd | 1 |  | hang LCD on F9 hooks | 2 | L2 I1 | - / cap4,lcd1,wire4 / cap4,lcd1,wire4 / - |
| 53 | [119]-[120] | Step 53 | PICKUP | panel+pot | 1 |  | pick up F1 | 0 | E1 | - / knob1,pot1,wire3,wood1 / knob1,pot1,wire3,wood1 / - |
| 54 | [121]-[122] | Step 54 | SEATW | panel+pot | 1 |  | attach F1 | 0 | L4 | - / knob1,nut1,pot1,wire3,wood1 / knob1,pot1,wire3,wood1 / - |
| 55 | [123]-[124] | Step 55 | PLACE | wood | 1 |  | F5 | 0 | L4 | wood1 / - / - / wood1 |
| 56 | [125]-[127] | Step 56 | PLACE | wood | 1 |  | F2 slide then hinge (Transition) | 1 | L2 | wood1 / - / - / wood1 |
| 57 | [128]-[129] | Step 57 | PLACE | wood | 1 |  | F6 | 0 | L4 | wood1 / - / - / wood1 |

#### PMG Full Build (51 numbered steps)

| # | viewer idx | step name | type | part kind | parts | wire ends | what the student does | auto frames | Step N annotations | CAD comps: hover + / done + / done - / moved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [002]-[003] | Step 1 | PLACE | nano | 1 |  | Nano into I/O shield | 0 | L4 | nano1 / - / - / nano1 |
| 2 | [004]-[005] | Step 2 | PREP | ribbon | 12 |  | split 12-wire ribbon | 0 | E1 | (context restored) / - / - / cap24,wire12 |
| 3 | [007]-[008] | Step 3 | WIRE | jumper | 1 | 2 | button VCC -> V4 | 0 | T2 E1 | cap2,nano1,shield1,wire1 / cap2,wire1 / cap2,wire1 / - |
| 4 | [009]-[010] | Step 4 | WIRE | jumper | 1 | 2 | button OUT -> S4 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 5 | [011]-[012] | Step 5 | WIRE | jumper | 1 | 2 | button GND -> G4 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 6 | [014]-[015] | Step 6 | WIRE | jumper | 1 | 2 | button VCC -> V5 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 7 | [016]-[017] | Step 7 | WIRE | jumper | 1 | 2 | button OUT -> S5 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 8 | [018]-[019] | Step 8 | WIRE | jumper | 1 | 2 | button GND -> G5 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 9 | [021]-[022] | Step 9 | WIRE | jumper | 1 | 2 | button VCC -> V6 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 10 | [023]-[024] | Step 10 | WIRE | jumper | 1 | 2 | button OUT -> S6 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 11 | [025]-[026] | Step 11 | WIRE | jumper | 1 | 2 | button GND -> G6 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 12 | [028]-[029] | Step 12 | WIRE | jumper | 1 | 2 | button VCC -> V7 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 13 | [030]-[031] | Step 13 | WIRE | jumper | 1 | 2 | button OUT -> S7 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 14 | [032]-[033] | Step 14 | WIRE | jumper | 1 | 2 | button GND -> G7 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 15 | [035]-[036] | Step 15 | PREP | ribbon | 9 |  | split 9-wire ribbon | 0 | - | (context restored) / - / - / cap18,wire9 |
| 16 | [037]-[038] | Step 16 | WIRE | jumper | 1 | 2 | CLK -> S8 | 0 | T2 E1 | (context restored) / cap2,wire1 / cap2,wire1 / - |
| 17 | [039]-[040] | Step 17 | WIRE | jumper | 1 | 2 | DIO -> S9 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 18 | [041]-[042] | Step 18 | WIRE | jumper | 1 | 2 | VCC -> V9 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 19 | [043]-[044] | Step 19 | WIRE | jumper | 1 | 2 | GND -> G9 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 20 | [046]-[047] | Step 20 | WIRE | jumper | 1 | 2 | VCC -> V11 | 0 | T2 E1 | (context restored) / cap2,wire1 / cap2,wire1 / - |
| 21 | [048]-[049] | Step 21 | WIRE | jumper | 1 | 2 | GND -> G11 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 22 | [050]-[051] | Step 22 | WIRE | jumper | 1 | 2 | DIN -> S11 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 23 | [052]-[053] | Step 23 | WIRE | jumper | 1 | 2 | CS -> S12 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 24 | [054]-[055] | Step 24 | WIRE | jumper | 1 | 2 | CLK -> S13 | 0 | T2 E1 | cap2,wire1 / cap2,wire1 / cap2,wire1 / - |
| 25 | [057]-[058] | Step 25 | CABLE | usb | 1 |  | USB plug into Nano (tween 23 mm) | 0 | L1 | (context restored) / - / - / usb2,wire1 |
| 26 | [059]-[060] | Step 26 | PLACE | wood | 1 |  | H2 into H1 (H1 datum fades in seated) | 0 | L1 | wood2 / - / - / wood1 |
| 27 | [061]-[062] | Step 27 | PLACE | wood | 1 |  | H3 | 0 | L1 | wood1 / - / - / wood1 |
| 28 | [063]-[064] | Step 28 | PLACE | wood | 1 |  | H4 | 0 | L4 | wood1 / - / - / wood1 |
| 29 | [065]-[066] | Step 29 | PLACE | wood | 1 |  | H5 slide in | 0 | L2 | wood1 / - / - / wood1 |
| 30 | [067]-[068] | Step 30 | STAGE2 | wood | 1 |  | H5 swing down | 0 | L2 | - / - / - / wood1 |
| 31 | [069]-[070] | Step 31 | PLACE | wood | 1 |  | H6 slide in | 0 | L2 | wood1 / - / - / wood1 |
| 32 | [071]-[072] | Step 32 | STAGE2 | wood | 1 |  | H6 swing down | 0 | L2 | - / - / - / wood1 |
| 33 | [073]-[074] | Step 33 | SEATW | buttonmod | 1 |  | first button module into slot (pose swap) | 0 | E2 | (context restored) / buttonmod1,cap3,wire3 / buttonmod1,cap3,wire3 / - |
| 34 | [075]-[076] | Step 34 | BATCH | buttonmod | 3 |  | other 3 button modules (pose swap) | 0 | E1 | - / buttonmod3,cap9,wire9 / buttonmod3,cap9,wire9 / - |
| 35 | [077]-[078] | Step 35 | PLACE | wood | 1 |  | H7 slide in | 0 | L2 | wood1 / - / - / wood1 |
| 36 | [079]-[080] | Step 36 | STAGE2 | wood | 1 |  | H7 swing down | 0 | L2 | - / - / - / wood1 |
| 37 | [081]-[082] | Step 37 | PLACE | wood | 1 |  | H8 | 0 | L2 | wood1 / - / - / wood1 |
| 38 | [083]-[084] | Step 38 | PLACE | wood | 1 |  | one piano key H9 | 0 | L1 | wood1 / - / - / wood1 |
| 39 | [085]-[086] | Step 39 | BATCH | wood | 3 |  | other 3 piano keys | 0 | I1 | - / wood3 / - / - |
| 40 | [087]-[088] | Step 40 | PLACE | wood | 1 |  | H10 slide in | 0 | L2 | wood1 / - / - / wood1 |
| 41 | [089]-[090] | Step 41 | STAGE2 | wood | 1 |  | H10 swing down | 0 | L2 | - / - / - / wood1 |
| 42 | [091]-[093] | Step 42 | PLACE | wood | 1 |  | H11 drop + lock (Transition) | 1 | L1 | wood1 / - / - / wood1 |
| 43 | [094]-[096] | Step 43 | PLACE | wood | 1 |  | H12 drop + lock (Transition) | 1 | L1 | wood1 / - / - / wood1 |
| 44 | [097]-[098] | Step 44 | PLACE | wood | 1 |  | H13 | 0 | L4 | wood1 / - / - / wood1 |
| 45 | [099]-[100] | Step 45 | PICKUP | shield | 1 |  | pick up Nano I/O module cluster | 0 | E1 | - / cap21,shield1,usb2,wire22 / cap21,nano1,shield1,usb2,wire22 / - |
| 46 | [101]-[102] | Step 46 | SEATW | shield | 1 |  | seat I/O module (arrow) | 0 | A1 | - / cap21,nano1,shield1,usb2,wire22 / cap21,shield1,usb2,wire22 / - |
| 47 | [103]-[104] | Step 47 | PICKUP | display | 1 |  | pick up display | 0 | E1 | - / cap4,display1,wire4 / cap4,display1,wire4 / - |
| 48 | [105]-[107] | Step 48 | SEATW | display | 1 |  | seat display (Transition) | 1 | L2 | - / cap4,display1,wire4 / cap4,display1,wire4 / - |
| 49 | [108]-[109] | Step 49 | PICKUP | matrix | 1 |  | pick up LED matrix | 0 | E1 | - / cap5,matrix1,wire1 / cap5,matrix1,wire5 / - |
| 50 | [110]-[112] | Step 50 | SEATW | matrix | 1 |  | seat LED matrix (Transition) | 1 | L2 | - / cap5,matrix1,wire5 / cap5,matrix1,wire1 / - |
| 51 | [113]-[115] | Step 51 | PLACE | wood | 1 |  | H14 face plate (Transition) | 1 | L2 E1 | wood1 / - / - / wood1 |

#### LSM Deconstruction (24 numbered steps)

| # | viewer idx | step name | type | part kind | parts | wire ends | what the student does | auto frames | Step N annotations | CAD comps: hover + / done + / done - / moved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [001]-[003] | Step 1 | RM | stem | 64 |  | all 64 stems | 1 | A1 E1 | - / wood3 / stem64 / stem64 |
| 2 | [004]-[006] | Step 2 | RM | wood | 1 |  | D8 | 1 | A1 E1 D1 | - / - / wood1 / wood1 |
| 3 | [007]-[009] | Step 3 | RM | wood | 1 |  | D7 | 1 | A1 E1 I1 | - / - / wood1 / wood1 |
| 4 | [010]-[012] | Step 4 | RM | wood | 1 |  | D5 | 1 | A1 E1 I1 | - / - / wood5 / - |
| 5 | [013]-[015] | Step 5 | RM | wood | 1 |  | D4 | 1 | A1 E1 I1 | wood4 / - / wood1 / wood1 |
| 6 | [016]-[018] | Step 6 | RM | wood | 2 |  | 2x D11 | 1 | A2 E1 I1 | - / - / wood2 / wood2 |
| 7 | [019]-[021] | Step 7 | RM | wood | 2 |  | 2x D11 | 1 | A2 E1 I1 | - / - / wood2 / wood2 |
| 8 | [022]-[024] | Step 8 | RM | wood | 1 |  | D6 | 1 | A1 | - / - / wood1 / nano1,wood1 |
| 9 | [025]-[027] | Step 9 | DISMOUNT | matrix | 1 |  | lift matrix out, still wired (pose swap) | 1 | A1 | - / cap3,matrix1,wire3,wood1 / cap3,wire3,wood1 / - |
| 10 | [028]-[030] | Step 10 | RM | wood | 2 |  | 2x D9 | 1 | A2 | wood1 / - / wood2 / wood2 |
| 11 | [031]-[032] | Step 11 | RMW | jumper-end | 1 | 1 | unplug male end | 0 | E1 | - / cap2,wire1 / cap1,wire1 / - |
| 12 | [033]-[034] | Step 12 | RMW | jumper-end | 1 | 1 | unplug male end | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 13 | [035]-[036] | Step 13 | RMW | jumper-end | 1 | 1 | unplug male end | 0 | E1 | - / cap1,wire1 / cap2,wire1 / - |
| 14 | [037]-[039] | Step 14 | RM | wood | 1 |  | D10 off matrix | 1 | A1 E1 | cap2,matrix1 / - / wood1 / wood1 |
| 15 | [040]-[042] | Step 15 | RMW | jumper-bundle | 3 | 3 | 3-way connector off matrix | 1 | A1 E1 | - / - / cap6,wire3 / cap6,wire3 |
| 16 | [043]-[045] | Step 16 | RM | wood | 1 |  | D3 | 1 | A1 I1 | (context restored) / - / wood1 / wood1 |
| 17 | [046]-[047] | Step 17 | DISMOUNT | panel+button | 1 |  | unplug 2 button leads and take D2 panel off (combined) | 0 | A1 E2 I1 | - / cap2,pushbutton1,wire2,wood1 / cap2,pushbutton1,wire2,wood1 / - |
| 18 | [048]-[050] | Step 18 | RM | nut | 1 |  | nut off | 1 | A1 E1 | - / - / - / - |
| 19 | [051]-[053] | Step 19 | RM | pushbutton | 1 |  | button out of panel | 1 | A1 E1 | - / - / cap2,pushbutton1,wire2 / cap2,pushbutton1,wire2 |
| 20 | [054]-[055] | Step 20 | RMCABLE | usb | 1 |  | USB cable | 0 | A1 E1 | (context restored) / - / usb2,wire1 / - |
| 21 | [056]-[058] | Step 21 | RM | resistor | 1 |  | R2 | 1 | A1 | - / - / resistor1 / resistor1 |
| 22 | [059]-[061] | Step 22 | RM | capacitor | 1 |  | capacitor | 1 | A1 | - / - / capacitor1 / capacitor1 |
| 23 | [062]-[064] | Step 23 | RM | resistor | 1 |  | R1 | 1 | A1 | - / - / resistor1 / resistor1 |
| 24 | [065]-[067] | Step 24 | RM | nano | 1 |  | Nano | 1 | A1 | - / - / nano1 / nano1 |

#### LAC Deconstruction (47 numbered steps)

| # | viewer idx | step name | type | part kind | parts | wire ends | what the student does | auto frames | Step N annotations | CAD comps: hover + / done + / done - / moved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [001]-[003] | Step 1 | RM | wood | 1 |  | F6 | 1 | A1 | wire5,wood1 / - / wood1 / wood1 |
| 2 | [004]-[007] | Step 2 | RM | wood | 1 |  | F2 | 2 | A1 E1 | - / - / wood1 / wood1 |
| 3 | [008]-[010] | Step 3 | RM | wood | 1 |  | F5 | 1 | A1 | - / - / wood1 / wood1 |
| 4 | [011]-[012] | Step 4 | DISMOUNT | panel+pot | 1 |  | F1 off (pose swap) | 0 | A1 | - / knob1,pot1,wire3,wood1 / knob1,nut1,pot1,wire3,wood1 / - |
| 5 | [013]-[014] | Step 5 | DISMOUNT | panel+pot | 1 |  | F1 set aside | 0 | E1 | - / knob1,pot1,wire3,wood1 / knob1,pot1,wire3,wood1 / - |
| 6 | [015]-[018] | Step 6 | DISMOUNT | lcd | 1 |  | LCD off hooks | 2 | E1 I1 | - / cap4,lcd1,wire4 / cap4,lcd1,wire4 / - |
| 7 | [019]-[021] | Step 7 | RM | wood | 1 |  | F8 | 1 | A1 | - / - / wood1 / wood1 |
| 8 | [022]-[024] | Step 8 | DISMOUNT | panel+switch | 1 |  | F4 off | 1 | A1 | - / switch1,wire3,wood1 / switch1,wire3,wood1 / - |
| 9 | [025]-[026] | Step 9 | RMW | lead | 1 | 1 | pot lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 10 | [027]-[028] | Step 10 | RMW | lead | 1 | 1 | pot lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 11 | [029]-[030] | Step 11 | RMW | lead | 1 | 1 | pot lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 12 | [031]-[034] | Step 12 | RM | knob | 1 |  | knob | 2 | A1 | nut1,washer1 / - / knob1 / knob1 |
| 13 | [035]-[037] | Step 13 | RM | nut | 1 |  | nut | 1 | A1 | - / - / nut1 / nut1 |
| 14 | [038]-[040] | Step 14 | RM | washer | 1 |  | washer | 1 | A1 | - / - / washer1 / washer1 |
| 15 | [041]-[042] | Step 15 | RM | pot | 1 |  | pot out of F1 | 0 | A1 | - / - / - / cap3,pot1,wire3 |
| 16 | [043]-[044] | Step 16 | REFIT | washer | 1 |  | washer back on loose pot | 0 | L1 | washer1 / - / - / washer1 |
| 17 | [045]-[046] | Step 17 | REFIT | nut | 1 |  | nut back on | 0 | L1 | nut1 / - / - / nut1 |
| 18 | [047]-[048] | Step 18 | REFIT | knob | 1 |  | knob back on | 0 | L1 | knob1 / - / - / knob1 |
| 19 | [049]-[051] | Step 19 | RMW | jumper | 1 | 2 | LCD GND | 1 | T1 E1 | (context restored) / - / cap2,wire1 / - |
| 20 | [052]-[054] | Step 20 | RMW | jumper | 1 | 2 | LCD VCC | 1 | T1 E1 | - / - / cap2,wire1 / - |
| 21 | [055]-[057] | Step 21 | RMW | jumper | 1 | 2 | LCD SDA | 1 | T1 E1 | - / - / cap2,wire1 / - |
| 22 | [058]-[060] | Step 22 | RMW | jumper | 1 | 2 | LCD SCL | 1 | T1 E1 | - / - / cap2,wire1 / - |
| 23 | [061]-[062] | Step 23 | RMMOD | lcd | 1 |  | LCD away | 0 | E1 | - / - / lcd1 / - |
| 24 | [063]-[066] | Step 24 | RM | wood | 1 |  | F9 | 2 | A1 I1 | - / - / wood1 / wood1 |
| 25 | [067]-[069] | Step 25 | RMCABLE | usb | 1 |  | USB cable | 1 | A1 E1 | - / - / usb2,wire1 / usb2,wire1 |
| 26 | [070]-[071] | Step 26 | FLEX | wood | 2 |  | spread F7 | 0 | A2 | - / - / - / wood2 |
| 27 | [072]-[073] | Step 27 | DISMOUNT | buzzer | 1 |  | buzzer out of posts | 0 | A1 E1 | - / buzzer1,wire2 / buzzer1,wire2 / - |
| 28 | [074]-[077] | Step 28 | RM | wood | 2 |  | 2x F7 | 2 | A2 | - / - / wood2 / wood2 |
| 29 | [078]-[079] | Step 29 | RMW | lead | 1 | 1 | buzzer lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 30 | [080]-[081] | Step 30 | RMW | lead | 1 | 1 | buzzer lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 31 | [082]-[083] | Step 31 | RMMOD | buzzer | 1 |  | buzzer away | 0 | E1 | - / - / buzzer1,cap2,wire2 / - |
| 32 | [084]-[085] | Step 32 | RMW | lead | 1 | 1 | switch lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 33 | [086]-[087] | Step 33 | RMW | lead | 1 | 1 | switch lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 34 | [088]-[089] | Step 34 | RMW | lead | 1 | 1 | switch lead | 0 | E1 | - / cap1,wire1 / cap1,wire1 / - |
| 35 | [090]-[091] | Step 35 | RM | switch | 1 |  | switch out of F4 | 0 | A1 | - / - / - / cap3,switch1,wire3 |
| 36 | [092]-[094] | Step 36 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | (context restored) / - / cap2,wire1 / - |
| 37 | [095]-[097] | Step 37 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | - / - / cap2,wire1 / - |
| 38 | [098]-[100] | Step 38 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | - / - / cap2,wire1 / - |
| 39 | [101]-[103] | Step 39 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | - / - / cap2,wire1 / - |
| 40 | [104]-[107] | Step 41 / Step 40c | RMW | jumper | 1 | 2 | loose jumper | 1 | - | - / - / cap2,wire1 / - |
| 41 | [108]-[110] | Step 41 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | - / - / cap2,wire1 / - |
| 42 | [111]-[113] | Step 42 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | - / - / cap2,wire1 / - |
| 43 | [114]-[116] | Step 43 | RMW | jumper | 1 | 2 | loose jumper | 1 | E1 | - / - / cap2,wire1 / - |
| 44 | [117]-[119] | Step 44 | RM | rtc | 1 |  | RTC + coin cell | 1 | A1 | - / - / coincell2,rtc1 / coincell2,rtc1 |
| 45 | [120]-[122] | Step 45c (misnamed hover) / Step 45c | RM | resistor | 1 |  | resistor | 1 | A1 | - / - / resistor1 / resistor1 |
| 46 | [123]-[125] | Step 46 | RM | resistor | 1 |  | resistor | 1 | A1 | - / - / resistor1 / resistor1 |
| 47 | [126]-[128] | Step 47 | RM | nano | 1 |  | Nano | 1 | A1 | - / - / nano1 / nano1 |

#### PMG Deconstruction (23 numbered steps)

| # | viewer idx | step name | type | part kind | parts | wire ends | what the student does | auto frames | Step N annotations | CAD comps: hover + / done + / done - / moved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [001]-[003] | Step 1 | RM | wood | 1 |  | H14 | 1 | A2 | - / - / wood1 / wood1 |
| 2 | [004]-[008] | Step 2 | DISMOUNT | matrix | 1 |  | matrix off housing | 3 | E1 | - / cap5,matrix1,wire5 / cap5,matrix1,wire5 / - |
| 3 | [009]-[013] | Step 3 | DISMOUNT | display | 1 |  | display off housing | 3 | E1 | - / cap4,display1,wire4 / cap4,display1,wire4 / - |
| 4 | [014]-[016] | Step 4 | DISMOUNT | shield | 1 |  | I/O module off housing | 1 | A1 | - / cap21,nano1,shield1,usb2,wire22 / cap21,nano1,shield1,usb2,wire22 / - |
| 5 | [017]-[018] | Step 5 | RM | wood | 1 |  | H13 | 0 | A1 | - / - / wood1 / - |
| 6 | [019]-[021] | Step 6 | RM | wood | 1 |  | H12 | 1 | A1 | - / - / wood1 / wood1 |
| 7 | [022]-[024] | Step 7 | RM | wood | 1 |  | H11 | 1 | A1 | - / - / wood1 / wood1 |
| 8 | [025]-[027] | Step 8 | RM | wood | 1 |  | H10 | 1 | A1 | - / - / - / wood1 |
| 9 | [028]-[029] | Step 9 | RM | wood | 4 |  | 4 piano keys | 0 | A1 E1 | - / - / wood4 / - |
| 10 | [030]-[031] | Step 10 | RM | wood | 1 |  | H8 | 0 | A1 | - / - / wood1 / - |
| 11 | [032]-[034] | Step 11 | RM | wood | 1 |  | H7 | 1 | A1 | - / - / wood1 / wood1 |
| 12 | [035]-[036] | Step 12 | DISMOUNT | buttonmod | 4 |  | 4 button modules out of housing | 0 | E1 | - / buttonmod4,cap12,wire12 / buttonmod4,cap12,wire12 / - |
| 13 | [037]-[039] | Step 13 | RM | wood | 1 |  | H6 | 1 | A1 | - / - / wood1 / wood1 |
| 14 | [040]-[042] | Step 14 | RM | wood | 1 |  | H5 | 1 | A1 | - / - / wood1 / wood1 |
| 15 | [043]-[044] | Step 15 | RM | wood | 1 |  | H4 | 0 | A1 | - / - / wood1 / - |
| 16 | [045]-[046] | Step 16 | RM | wood | 1 |  | H1 (H2, H3 vanish) | 0 | A1 | - / - / wood1 / - |
| 17 | [047]-[048] | Step 17 | RMMOD | matrix | 1 |  | matrix off its wires | 0 | A1 | (context restored) / - / matrix1 / - |
| 18 | [049]-[050] | Step 18 | RMW | jumper-bundle | 5 | 10 | 5 matrix wires | 0 | A1 | - / - / cap10,wire5 / - |
| 19 | [051]-[052] | Step 19 | RMCABLE | usb | 1 |  | USB cable | 0 | A1 | - / - / usb2,wire1 / - |
| 20 | [053]-[054] | Step 20 | RMMOD | buttonmod | 4 |  | 4 button modules off wires | 0 | A1 | - / - / buttonmod4 / - |
| 21 | [055]-[056] | Step 21 | RMMOD | display | 1 |  | display | 0 | A1 | - / - / display1 / - |
| 22 | [057]-[058] | Step 22 | RMW | jumper-bundle | 16 | 32 | 16 wires | 0 | A2 | - / - / cap32,wire16 / - |
| 23 | [059]-[060] | Step 23 / Completed View (acts as c) | RM | nano | 1 |  | Nano | 0 | A1 | - / - / nano1 / - |
