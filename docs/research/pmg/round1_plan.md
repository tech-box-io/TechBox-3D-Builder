# PMG, Lee's first round (19 Oct 2026): what was asked and how it is being done

Kept in the project so that a crash cannot lose it (the Mac went down once during this round). Step numbers are the first draft's
(47 steps, commit f5d9422); this round adds one step (the push button card before the first wire), so from the old Step 3 on, the
new number is one higher.

## Lee's requests

| # | Where (old step) | Request | Plan |
|---|---|---|---|
| 1 | model | Dot matrix's dots round, in 8 x 8 grids | Done by the silkscreen work (decals; `silkscreen.md`) |
| 2 | parts list | I/O module and Nano Board shown turned round (their backs) | `part_picture(... poses=)` turning each to show its face |
| 3 | parts list | Push button picture: the yellow one (the black blends in) | `part_picture('Push Button', piece=yellow)` as the main picture |
| 4 | parts list | H5, H6, H7, H9, H10 upside down | turned the right way up for their pictures |
| 5 | parts list | H13 badly angled, H14 hard to see | better picture poses |
| 6 | 3 | A breakout card of the push button (as Cadasio's), highlighting its printed pin names | a single-view step before the first wire, with a close-up (red box on VCC / OUT / GND) |
| 7 | 3 | Silkscreen on the push buttons | Done (decals) |
| 8 | 3 - 14 | The I/O module pin's label (V4 ...) should point at the top of the pin | label anchor at the pin's measured tip (`make_source.py` measures every pin tip) |
| 9 | 15 | Higher camera, to show the wires separated | camera from higher up |
| 10 | 16 - 19 | The 4-digit display's wires conflict with the push buttons' | new bench routes behind the buttons' wires |
| 11 | 20 - 24 | Wire the dot matrix with a camera that shows its back (pin labels) and the I/O module's pins; silkscreen its rear | camera from behind; rear decal (done) |
| 12 | 16 - 24 | Pin lead lines/labels of the display and matrix slightly off their pins | anchors at the measured pin tips |
| 13 | model | Silkscreen of the display (front, back) and matrix | Done (decals) |
| 14 | 29, 30, 33 | Slower; camera from the corner to the left, or from the front near H1, to see H5 (H6, H7) slot into H2 then H3 | more stops in the hinge path; new camera |
| 15 | 31, 32 | Wires clip H5's back edge; the black button's black wire runs into H4 | wires settled clear of every part |
| 16 | 36, 37 | Step 35's camera, no spin | same camera as Step 35 |
| 17 | 38 | Punch in; the upper corner closest to H1's etching | camera |
| 18 | 39 | The other front (H1) corner for H12 | camera |
| 19 | 40 | Zoom in some | camera |
| 20 | 42, 42c | The display's wires (and some white and black buttons' wires) conflicted | wires routed in layers (below) and settled |
| 21 | 43 | The display passes under the MAX7219's (matrix's) wires up to its place, no wire conflicts | a path with stops, and a route per stop |
| 22 | 44 | The display's wires cross at an X | ribbon routing (no crossing within a bundle) |
| 23 | 45 | The dot matrix into place without clipping through the build | a path over the top, with a route per stop |
| 24 | 47 | Slower, and highlight H14's tabs going down onto the dot matrix | more stops; lead lines / close-up on the tabs |

## How the wires are laid out (module on the back of H4: pins point +x at x 606.5, header at the module's -z end, z 1270 - 1276)

- Rows 4 - 7 (y 924 - 932), the push buttons: from the case (out through H4's slot under H5's tongue, y ~897), up behind H4 at
  x ~610 - 616, along z under the Nano Board (its bottom y 917; it stands out to x 618 at z 1281 - 1299), then into the pins.
- Rows 8 - 9 (y 936.5 - 939), the 4-digit display: out +x to x ~621, +z beside the Nano and UNDER the matrix's wires, up behind
  H4 beyond the module's +z edge (z ~1312 - 1322), over H4's top at z ~1328 (outside H11 and H13's ear), to the display's pins.
- Rows 11 - 13 (y 944 - 952), the dot matrix: out +x to x ~628, then +z out to the bench matrix (while it lies there) or -z round
  H3 to the seated matrix. The display's wires are always inside (nearer H4) and below the matrix's.
- The USB cable comes down behind the module's -z end (x 612 - 631, z ~1250) to its A end on the table.

Every set of wires shown together is built as ribbons (each device's wires side by side, turned so that none crosses another of
its bundle) and then settled: wires pushed apart where they come within 0.4 mm of each other, and out of every part on screen,
the pushes smoothed along each wire (`PMG Build Instructions/routing.py`). Checked by `docs/research/pmg/scripts/check_wires.py`
(wire in a part) and `check_overlaps.py` (wire through wire).
