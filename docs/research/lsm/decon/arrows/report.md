# The published LSM take-apart's arrows, measured (21 Oct 2026)

For the LSM deconstruction's arrow sizes, as the PMG's were set after Lee's note on its take-apart ("the arrow sizes and sequencing
need refinement. Examine the Cadasio"). Made by an agent of the LSM session; files in this folder:

- `measure_arrows.py`: `python -I measure_arrows.py <payload.json> <out.txt> [title] [--json out.json]`
- `published_arrows.txt` (and `.json`, with each arrow's tail and tip in mm, direction, scale and raw numbers): every arrow of TechBox's
  published LSM take-apart, frame by frame, in the PMG file's format. The payload:
  `docs/research/lsm/cadasio/raw/19075-laser_stem_matrix_lsm_-_deconstruction.json` (getProjectViewer, as tools/cadasio/digest.py).
- `pmg_reproduced.txt`: the script's output on the PMG's raw, for the calibration.

## How Cadasio stores an arrow

An entry in `toolboxComponentsProperties` with type `arrow`, sub_type `straight`: `points` (two, in scene units: the tail, then the tip
of the head), `body_width`, `head_width`, `head_length` (usually 5 : 20 : 17 or 5 : 20 : 15), `scale` (one factor, applied to the widths
only), `arrow_quaternion` (the roll of its flat face about its own axis), `object_ids[0]` (only the solid under the cursor when it was
placed) and `visible` (false by default). A step's `properties[arrowId]` changes `visible` (and sometimes `points`) on top of the step
before; hidden steps count, so the whole sequence is replayed. With SF = `assemblyStructure.scaleFactor` (PMG 0.04236, LSM 0.47846):

    L = |points[-1] - points[0]| / SF        (tail to tip, the head included)
    w = body_width * scale / SF              head = head_width * scale / SF  by  head_length * scale / SF

The published LSM's coordinates are in our assembly frame (the tails of R330, the capacitor, R12K and the Nano are within 3 mm of
ours). Our player draws the head 4w wide and min(0.6 L, 3.4 w) long, so `dims=(L, w)` gives the usual 5 : 20 : 17 arrow.

## Calibration against the PMG

30 of the 31 showings in docs/research/pmg/deconstruction/published_arrows.txt are reproduced to the last digit. The other, [040] Step 14,
H5: the length matches (34.8), but the PMG file's w 3.76 / head 15.1 x 12.8 are those of "Arrow 3D_straight_1" (scale 0.0319), which no
frame shows; the arrow Step 14 shows is "Arrow 3D_straight_18" (scale 0.0524): w 6.19, head 24.7 x 21.0. Told to the PMG session.

## The published LSM arrows (L / w, mm)

| Published step | Part | Direction | L / w |
|---|---|---|---|
| 1 | stems | up | 69.4 / 4.57 |
| 2 | D8 | up | 65.6 / 3.21 |
| 3 | D7 | up | 59.3 / 4.20 |
| 4 | D5 | +X | 62.8 / 7.14 |
| 5 | D4 | -X | 80.1 / 6.24 |
| 6 | D11 at x 599, z 1166 / x 599, z 1242 | up | 45.6 / 3.43, 47.0 / 3.95 |
| 7 | D11 at x 677, z 1242 / x 677, z 1166 | up | 45.0 / 3.88, 41.7 / 3.62 |
| 8 | D6 | up | 70.6 / 3.83 |
| 9 | matrix with D10 (Step 8's arrow again) | up | 70.6 / 3.83 |
| 10 | D9 at x 657 / x 619 | up | 69.2 / 3.45, 61.2 / 3.45 |
| 14 | D10 | down | 50.8 / 4.43 |
| 15 | the three-wire cable | +Z | 31.6 / 3.45 |
| 16 | D3 | -Z | 50.7 / 3.53 |
| 17 | D2 | +Z | 86.5 / 3.89 |
| 18 | nut | -Z | 56.3 / 5.00 |
| 19 | button | +Z | 38.4 / 3.66 |
| 20 | USB | +Z | 63.3 / 5.02 |
| 21 | 330 ohm resistor | up | 32.0 / 2.30 |
| 22 | capacitor | up | 21.2 / 2.09 |
| 23 | 12 kOhm resistor | up | 31.5 / 1.28 |
| 24 | Nano Board | up | 40.5 / 2.85 |

Published Steps 11 - 13 (the three wires at the breadboard) have an eye and no arrow. Arrow length over travel: median 1.06, 0.40 - 1.57.

## As used in our deconstruction (LSM Build Instructions/deconstruction.py, `PUBLISHED`)

Each of our arrows takes the size of the published arrow on the same part going the same way. Where our draft has a stage the published
guide has no arrow for, it takes the same part's size (by analogy): D10's slide (D10's), the matrix's two stages over D4 (the matrix's),
D3's slide (D3's), D4's lift (D4's), the matrix's lift off the connectors (the cable's, the pull off the same joint). D10's drop is
shorter, 30 mm (ours drops 22 mm; the published one 48). The four D11 posts take their own corner's published arrow. The matrix carried
back beside the D5 end (our Step 12, a hand-placed arrow) takes the matrix's size. The button's wires and the three breadboard wires have
eyes, no arrows, as published.
