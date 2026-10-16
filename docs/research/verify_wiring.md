# Verification notes: Electronics and wiring conventions (skeptic pass on dim_wiring.md)

Guide short names as in dim_wiring.md (LSM1, LSM2, LSM12, LSM3, LSM4, LSM34, LSMF, LSMD; LAC1-4, LACF, LACD, LACE; PMG1-3, PMGF, PMGD). Step indices in square brackets are digest viewer indices.

## Method (independent of the analyst's walker)

- Step tables for all 20 guides rebuilt from `digest/*.json` (`_work_verify_wiring/overview.py`, `pairs.py`, `wiremoves.py`).
- My own leaf-level walker over `cadasio_raw/*.json` (`_work_verify_wiring/vwalk.py`): world bounding boxes in mm, effective colours, full raw annotation properties, camera. Step `position` replaces the node's local translation (checked on Paper-1: transform 449.83/537.41/743.22, step position 449.8/565.7/743.0 scene units).
- Visibility: the digest rule (all ancestors visible) misses parts whose top-level reference is flagged hidden while the leaves are switched on (the LSMF LED matrix copies `8x8 LED-1..7`). I re-ran everything with leaf-explicit visibility; the render LSMF [028] confirms the matrix is on screen. The 103-pair statistics are identical under both rules.
- Wire-connection pair = `Step N` carrying at least one pin/hole label whose next viewer step is its `Nc`, where `Nc` swaps wire parts with no leaf moving more than 0.3 mm. Lines and arrows were not part of the definition.
- Renders opened: LSMF [021] [027] [028] [030] [041]; LSM2 [003] [010]; LACF [019] [034] [065] [078]; PMGF [001] [006] [007] [037] [043]; contact sheet PMGF [032]-[039].

## Headline result

13 of 19 patterns confirmed, 6 qualified, 0 refuted. The analyst's counts reproduce almost everywhere (103 pairs; 48 in the full builds; 0 lines, 0 arrows, 0 annotations on Nc, camera held, 800 ms pause on both halves). The qualifications are:

1. WIRE-6 / label style default: the font is not Arial in PMG. PMG wire labels carry no `font-family` at all (0 of 42 in PMGF, 0 of 84 over PMG1/PMG2/PMGF) and render in the project default `PublicSansMedium`; Arial is explicit only in LAC (32 of 32) and LSM (8 of 8). Visible in PMGF [007] against LACF [019].
2. WIRE-1: "Step N shows the wire straight and unconnected, Nc seated at both ends" is the LAC/PMG form only. In LSM the swap is per END: 3 of 7 pairs per LSM guide end with a half-seated wire and 3 of 7 start from an already bent, half-seated wire (LSM2 [010], LSMF [028] [030] [032]). Colour is identical between loose and routed model on 98 of 103 pairs (45 of 48), not all. Wire tweens in the full builds are 12 step pairs, not 9.
3. WIRE-9: physical pin order is 10 of 11 (the RTC belongs in the denominator); module order by ascending controller pin is evidenced only in PMG.
4. WIRE-19: "eye, cross-fade" describes LACD and most of LSMD; LSMD Step 15 tweens three wires 30.5 mm along an arrow; PMGD uses arrows and a plain fade-out.

## Per-pattern verdicts

| ID | Verdict | What I recomputed | Counter-examples / corrections |
|---|---|---|---|
| WIRE-1 | qualified | 103 of 103 pairs are appear + disappear, 0 wire leaves move more than 0.3 mm between N and Nc, Nc is always the next viewer step, both `pause`, 800 ms | LSM per-end form (9 of 103 pairs start bent and half-seated; 9 end half-seated). Colour drift: LAC1 [021] [027] and LACF [021] [027] (green #2ecc40 to #10cc62, grey #aaaaaa to #cccccc), LSMF [023] (#a6a9aa to #b1b3b3). Tween step pairs = 12: LSMF 17; LACF 8, 9, 15, 19, 20, 25, 35; PMGF 2, 15, 16, 25. The analyst missed LACF [019] (177 mm), LACF [042] (150 mm), PMGF [037] (12 mm) |
| WIRE-2 | confirmed | 0 line and 0 arrow objects on all 103 N and Nc steps; every labelled step with lead lines is a rigid plug-in | none for jumpers and leads |
| WIRE-3 | confirmed | 0 annotations visible on 103 of 103 Nc; camera position/target/rotation identical N to Nc on 103 of 103 | naming only: LAC1 [030] "Step 14C", PMG1 [033] "Completed View" |
| WIRE-4 | confirmed | LAC 12 + PMG 21 jumpers and 8 LAC leads each have one pair; 82 of 82 over all LAC/PMG guides | LSM: 3 jumpers x 2 steps, 2 button leads in 1 step (as stated) |
| WIRE-5 | confirmed | 41 of 41 LAC/PMG full-build steps have exactly 1 eye (same PNG) and 2 or 1 labels; 82 of 82 with part guides; eye on wire body 32 of 33, on pin housing 8 of 8 | eye sits at the wire mid-point (0.44-0.54 of body length) on only 27 of 33: LACF [085] at the very end, PMGF [039] [041] [043] at 0.13-0.26, LACF [083] on the housing |
| WIRE-6 | qualified | 26 of 26 hole labels lower case; 5 + 5 rail labels; module pins capital 23 of 25; shield pins capital 19 of 21; 3em 74 of 74, 2.5em 7 of 8; underline 5 px #7fdbff 172 of 172; ring 1.2 on 80 of 82; box 175 x 90 on 64 of 82 | Font: Arial only in LAC and LSM, PMG inherits PublicSansMedium. Box: 175 x 90 on 63 of 64 short 3em labels (LACF [025] is 175 x 91); the 10 LAC rail labels auto-widen to 200-258 x 90; LSM 2.5em labels are 175 x 75 (6 of 7), LSMF [032] is 152 x 76 |
| WIRE-7 | confirmed | 33 of 33 free jumpers along world Z = board long axis; centre 66-119 mm from board centre, 36-89 mm clear; height 2.7-10.0 mm (PMG), 42-68 mm (LAC); camera side on 33 of 33; spread 4.7 / 2.2 / 4.1 mm (LAC), 19.2 / 3.5 / 7.0 mm (PMG); leader tip y 53.6-81.7 %, left of centre 30 of 33 | PMGF [037] 40 mm off (it sits at the dot-matrix run's Z); the PMG I/O module is nearly square (53.3 x 59.0 mm), so "long axis" is weak there; LAC bridges are 56 mm bodies, 70.5-71.2 mm overall |
| WIRE-8 | confirmed | no eye on 21 of 21 LSM pairs (7 per guide); badge pair on 3 of 3 pad steps per guide, widths 5.82-7.81 %; ribbon 26.8 mm and matrix 40.5 mm above breadboard top; plug 24.0-24.8 mm above and 8.9-39.1 mm beside its seat; camera changes on entering 5 of 7 wire steps (LSMF [021] [025] [030] [032] [041]), 125.3 and 108.5 degrees between pad steps | none |
| WIRE-9 | qualified | LSM pads x = 669.5, 667.6, 665.7; button tips 44.9/45.7/46.4 etc.; display y 36.2/37.7/38.9/39.8; matrix y 31.3-36.5; LCD, switch, pot monotonic; supply-first 4 of 13 | RTC is 23, 24, 22, 21 so pin order is 10 of 11. LAC module order (RTC, rail feeds, switch, pot, buzzer, LCD = columns 8/9, 12/14, 1/3, 5, 4, 8/9) is not ascending; only PMG is |
| WIRE-10 | confirmed | 12 supply (3 red/dark red), 12 ground (3 black/charcoal); jumpers 2 of 10 and 1 of 10; 21 distinct PMG colours; LAC re-uses #611b6c, #0074d9, #eac80d; ribbon order used in PMG 12 of 12 and 9 of 9, LAC LCD 4 of 4 | loose-versus-routed colour identical on 45 of 48 only; housings #000000 / #1e1616 everywhere except two pale (#cad1ee) button-lead housings on LSMF [000] and [087] |
| WIRE-11 | confirmed | 6 prep pairs, 6 of 6 isolated (0 non-wire parts), eye on 5 of 6; camera 103, 110, 119, 128, 175, 175 mm; counts 3, 6, 2, 4, 12, 9; joined pitch 1.7/1.8 mm | over all 10 wiring guides: 13 prep pairs, eye on 11 (PMG2 [002] and PMGF [035] lack it). Per-gap pitch after separation is 4.5-5.4 mm (12 wires) and 4.1-4.6 mm (9 wires); 4.85 and 4.39 are the means. LACF [076] is viewed from below (elevation -47) |
| WIRE-12 | confirmed | 13 cards, each shows only the module (1-7 components counting its own leads); framed photos 17.15, 29.02, 33.56, 36.72 %; rectangle frame #7fdbff 5 px; red box seen on LSM diagram, LCD, button, 4-digit display | the Nano I/O card is a label object with an embedded image (798 x 799 px box), not an image callout; photo silkscreen reads CLK / DIO while the wire labels say clk / dio |
| WIRE-13 | confirmed | wiring ends before the first wall in 3 of 3; 4 of 4 mounted first; 9 of 9 wired loose with no placement step (PMGF [013] [020] [027] are the auto Transitions) | LSM matrix: copy LED-2 at Steps 13-15, LED-1 from Step 19, no step in between |
| WIRE-14 | confirmed | 9 constant-camera runs over 41 steps (LACF 6, 3, 2, 3, 2, 4; PMGF 12, 4, 5); every Nc and every auto Transition inside a run holds the camera; 173/173/202 mm and 277-439 mm; elevation 21-57 | a run is a ribbon or lead set, not a module: PMG buttons = 4 modules under one view, LAC run 1 = RTC + rail feeds |
| WIRE-15 | confirmed | USB card + one pair in 7 of 7 guides that contain it; last connection in 3 of 3 full builds; PMG plug moves 22.9 mm with one 28.5 mm line | as stated |
| WIRE-16 | confirmed | drops 29.1, 29.8, 30.3, 32.4, 33.6, 37.1, 39.8, 40.0, 44.1 mm, all pure vertical; 2 lines on 7, 4 on 2; two labels on 7 of 9 | LSM1 capacitor also shifts 3.4 mm sideways (part guide only) |
| WIRE-17 | confirmed | routed models: LSM 5 + LAC 28 male breadboard ends; 3 + 4 female header ends; PMG 42 of 42 female | the 12 loose PMG button jumpers use the male housing component with its pin leaf hidden on one end |
| WIRE-18 | confirmed | 20 re-pose pairs (LSMF 21, 23, 28, 30; LACF 43, 47-49, 51-54; PMGF 33, 34, 45-50); no wire leaf moves in any step after wiring ends; copies shown: LED matrix 5, LCD 4, pot 4, switch 3, display 4, dot matrix 4, shield 3, buttons 2 | LACF 52 and PMGF 48, 50 pass through an extra pose on an auto Transition |
| WIRE-19 | qualified | LACD 20 wires in 20 steps, eye 20 of 20, 4 pin labels, loose model reappears at the build's parking spot; 0 hole labels in LACD, LSMD, PMGD | LSMD Steps 15 and 17 add an arrow; LSMD [041] tweens 3 wires + 3 housings 30.5 mm before they fade; PMGD wires fade out with no loose model; LACD USB removal is arrow + eye + 43 mm tween; LSMD [037] moves the three loose wires 2.7 m with a rotation across a camera cut |

## Numeric defaults

| Default | Result |
|---|---|
| Wire step timing 800 ms, pause, no Transition | confirmed, 103 of 103 |
| Lead lines / arrows 0 / 0 | confirmed, 103 of 103 |
| Annotations on Nc = 0 | confirmed, 103 of 103 |
| Labels per step 2 / 1 | confirmed, 33 of 33 and 8 of 8 |
| Eye icons per step 1; anchor | 1 on 41 of 41; on wire body 32 of 33, but at the mid-point only 27 of 33; pin housing 8 of 8 |
| Eye width 7.81 % (LSM, LAC), 8.2 % (PMG) | confirmed; all guides: 7.81 x143, 8.2 x62 (every PMG eye), 7.92 x10, others x8 |
| Label text style | bold black 3em (LAC, PMG 74 of 74), 2.5em (LSM 7 of 8). Font: Arial explicit in LAC and LSM only; PMG = project default PublicSansMedium |
| Underline / leader / ring | underline 5 px #7fdbff 82 of 82; ring 30 px x 1.2 on 80 of 82; leader #7fdbff 5 px explicit on 74 of 82, inherited on 8 |
| Label box 175 x 90 | 64 of 82; rail labels 200-258 px wide; LSM 175 x 75 |
| LSM badge pair | confirmed, 5.82-7.81 % |
| Loose jumper model | 58.2 mm body, 1.2 mm; F housing 8.0, M housing with pin 12.0; M-M 74.2, M-F 69.4, F-F 65.4-65.5 overall. Exceptions: LAC bridges 56.0 / 55.5 mm body, 70.5 / 71.2 overall; PMG display ribbon 58.8 mm body |
| Captive lead length | confirmed: 30.1-30.3, 38.9-39.0, 49.8-50.1, 49.6 mm |
| Ribbon pitch | 1.75 mm joined; after separation gaps 4.1-4.6 (9 wires), 4.5-5.4 (12 wires), 6.1-9.0 (LAC 6 wires), 7.7 / 10.2 / 13.1 (4 wires), 21.7 (pair) |
| Parking spot | 66-119 mm from board centre, 36-89 mm clear, camera side 33 of 33; spread 2-7 mm in 5 of 6 runs |
| Parked wire on screen | y 53.6-81.7 % for the 33 free jumpers (83 % is a buzzer lead); left of centre 30 of 33 |
| Parked wire height | confirmed: 2.7-2.9 and 9.8-10.0 mm (PMG); 42, 58.5, 68 mm (LAC) |
| LSM hover heights | confirmed: 26.8, 40.5, 24.0-24.8 mm |
| Plug-in hover | confirmed: 29.1-44.1 mm, median 33.6; 2 lines on 7, 4 on 2 |
| USB plug hover (PMG) | confirmed: 22.9 mm, 28.5 mm line |
| Wiring camera | confirmed: 173, 173, 202 mm; 277 x4, 323, 439 mm; elevation 21-57; 0 moves in 9 runs |
| Ribbon-prep camera | confirmed: 103-175 mm, 6 of 6 isolated |
| Pinout photo | confirmed: 17.15-36.72 %, #7fdbff rectangle frame 5 px |
| Annotation count on N | confirmed: 3 or 2 on 41 of 41 |

## Patterns the analyst missed

1. Wire steps carry no text. `description` is empty and there is no popup on N and Nc for 89 of 103 pairs: every LAC and PMG guide (82 of 82) and LSMF (7 of 7). Only LSM2 and LSM12 have descriptions, and those are stale.
2. The first wire of a ribbon glides to the parking spot. When a wire step follows ribbon preparation directly, the first wire stays on screen and tweens from its separated-ribbon position while the camera pulls back: LACF [019] 177 mm, LACF [042] 150 mm, PMGF [037] 12 mm (which is why that wire ends up 40 mm from the others). When a module card sits in between (PMGF [006], LACF [078]) the wire fades in at the spot.
3. Wire length is not conserved between the two models. The loose model is a fixed token (58 mm body; leads 30 / 39 / 50 mm); the routed model is as long as the route needs: jumpers 23-113 mm span, switch leads 94-136 mm, pot leads 229-240 mm.
4. Re-pose steps keep the normal mounting callouts but complete by cross-fade. Of the 20 re-pose pairs, 10 carry red lead lines or an arrow on Step N (LACF 47, 49, 52, 54; PMGF 46, 48, 50; LSMF 21, 23, 30) and 10 carry only an eye. A player must allow a lead-line step whose completed view is a swap.
5. Wire steps show the whole assembly so far; isolation is reserved for cards and ribbon preparation. The first wire step of each run re-shows everything hidden by the card (LACF [034] +27 parts, [065] +40, [079] +58; PMGF [046] +57).

## Anomalies seen in passing (not conventions)

- PMGF [037]: the eye icon overlaps the I/O module.
- LSMF [000] and [087]: two push-button lead housings render pale (#cad1ee / #cad1ed) instead of black.
- LSMD [037]: three loose wires jump 2.7 m with a rotation between two steps.
- LACD: "Step 41" [104] precedes "Step 40" [105]; "Step 45c" is used for both [120] and [122].

## Working files

`reports/_work_verify_wiring/`: `vcommon.py`, `overview.py` and `ov_<guide>.txt`, `pairs.py`, `wiremoves.py`, `vwalk.py` (walker, cached as `vstate2_<guide>.pkl`), `wtab.py`, `swap.py`, `anns.py` and `annrows.json`, `park.py`, `swap_leafvis.txt`.
