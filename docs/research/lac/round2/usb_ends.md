# LAC Step 40: the USB cable off-centre at both plugs (Lee's second round, lee_5 and lee_6)

Read-only study, 21 Oct 2026. Nothing in the kit was changed, regenerated or committed. All numbers are assembly mm, seated, Y up.

## Cause

`usb_cable()` takes both ends of the cable from the CAD cable's centre line in `wire-paths.json` (`lines.NAUO123`, guide.py:912-913
and 926). That line's first and last points are wrong. The extraction put them on the rim of each end face, not in its middle:

| | where the guide's cable starts or ends now | the plug's real middle (axis) | off by |
|---|---|---|---|
| Mini-B end (NAUO122) | `_usb[0]` = [658.34, 903.33, 1352.65], leaving along `unit(_usb[3]-_usb[0])` = [-0.903, 0.034, 0.428] | [658.34, 903.33, 1354.39], axis [-1, 0, 0] | 1.74 mm in z, and 25 degrees off the axis |
| A end (USB_A), as the CAD has it | `_usb[-1]` = [602.32, 876.64, 1389.92] | [599.97, 876.35, 1389.92], axis [0, 0, -1] (the cable side) | 2.37 mm (2.35 in x, 0.29 in y) |
| A end on the table (`A_ON_TABLE`) | the route ends at `A_TARGET` = [575.0, 888.91, 1327.34] | [575.00, 888.62, 1324.99], axis [+1, 0, 0] | 2.37 mm (2.35 in z, 0.29 in y) |

The A end is laid on the table by `A_ON_TABLE`, which turns it about `A_CABLE_END` and moves that point to `A_TARGET`. Because
`A_CABLE_END` is the off-centre point, the plug's real middle ends up 2.35 mm off the cable's straight run (lee_6). The same 0.29 mm
error in y also leaves the A end's underside at y 884.35, which is 0.26 mm into the table (TABLE_Y, F3's underside, = 884.608).

Two independent measurements give the same middles:

- **Mini-B (NAUO122, `lac-guide.glb` node 19):** the plug has a short cable stub, a cylinder of radius 2.25 that runs along -x from
  x 666.34 to its flat end face at x 658.34. All 48 end-face vertices lie 2.246 - 2.254 mm from (y 903.33, z 1354.39). The cross-sections
  at x 658.34 and 667.84 share that centre, so the axis is exactly -x. The boot (r 3.1) runs from x 666.34 to 670.34, then the
  right-angle housing.
- **A end (`usb-a-end.glb`, byte for byte the MRA's file):** in its own frame the strain relief's end face is at x 184, 8 x 8 mm, centred on
  (y 0, z 4.125), and the axis is local +x. With `materials.json` `extra_parts.USB_A.pose` that gives [599.967, 876.354, 1389.919],
  facing [0, 0, -1].
- **The CAD's own cable body (NAUO123 in `lac.glb`, read with glbio, 104 MB peak):** its end faces are centred at
  [658.34, 903.33, 1354.39] and [599.97, 876.35, 1389.92]. These are exactly the two plug middles above. Its cross-section 5 mm along,
  at x 653.0, is still centred on (903.33, 1354.40), so the CAD cable runs straight out along the stub's axis. Only the centre line's
  end points are wrong. (The CAD cable is 5.25 mm across. The stub is 4.5 mm and the guide's tube is 3.5 mm, r 1.75, the MRA's.)

## How the MRA does it

The MRA does not take its cable's ends from a CAD line. It writes them by hand, "where the cable leaves each end, as materials.json
places them" (MRA guide.py:564): `USB_B_EXIT = [69.46, 120.94, 223.6]`, `USB_A_EXIT = [69.46, 91.81, 280.0]`, and `W.curve` leaves each
end along the plug's axis ([0, 0, 1]). I checked both against the plug meshes:

- `USB_A_EXIT` is the middle of the A end's strain relief, [69.46, 91.805, 280.0], facing [0, 0, -1]. This is the same file and the
  same local point (184, 0, 4.125) as above.
- `USB_B_EXIT` is the middle of the end of the MRA Mini-B's cable stub (local x -47, 3.5 mm across, centred on the axis), under
  the pose t [69.46, 120.94, 176.6], r [0, 1, 0, 90].
- The MRA's A end on the table, `A_ON_THE_TABLE = turned([0, 1, 0], 90, USB_A_EXIT, ...)`, turns the plug about its middle. That is
  what the fix below does for the LAC.

## The fix (guide.py; nothing in materials.json)

1. **guide.py:912-913.** Replace the two lines `_usb = cad_line('NAUO123')` and `USB_EXIT, USB_EXIT_DIR = _usb[0], unit(_usb[3] - _usb[0])`
   with:

```python
# Where the cable leaves each plug, measured from the plugs' meshes (docs/research/lac/round2/usb_ends.md; Lee, 21 Oct 2026, Step 40:
# the cable met both plugs off-centre): the middle of the end of the Mini-B plug's cable stub (4.5 mm across, along -x from x 666.34),
# and of the A end's strain relief (8 mm across, facing -z as the CAD has the A end). The CAD's own cable body (NAUO123) ends on both;
# the centre line wire-paths.json has for it starts 1.74 mm and ends 2.37 mm off them, and leaves the Mini-B end 25 degrees off its axis.
USB_EXIT, USB_EXIT_DIR = np.array([658.34, 903.33, 1354.39]), np.array([-1.0, 0.0, 0.0])
USB_TUCK = 1.0                                                      # (the tube runs on 1 mm into each plug, so its flat end does not show)
```

2. **guide.py:926.** Replace the `A_CABLE_END = _usb[-1]` line with:

```python
A_CABLE_END = np.array([599.97, 876.35, 1389.92])                   # the middle of the A end's strain relief, as the CAD has it (its plug towards +z)
```

   Lines 927-929 (`A_TARGET`, `A_ON_TABLE`, `rest_at`) stay as they are. `A_ON_TABLE` now turns the plug about its middle and puts that
   middle on `A_TARGET`, so the plug is centred on the cable's straight run, which is in line with F2's slit as intended.

3. **guide.py:945.** Replace the `line = W.resample(...)` line in `usb_cable()` with:

```python
    line = W.resample(W.join(W.straight(start - USB_EXIT_DIR * USB_TUCK, USB_EXIT_DIR, USB_TUCK), inside, outside,
                             W.straight(outside[-1], [-1, 0, 0], 12.0 + USB_TUCK)), 1.0)   # (down to the table, and straight into the A end's middle)
```

   Nothing else in `usb_cable()` changes. `start`, the `W.smooth` calls (whose `start_dir=USB_EXIT_DIR` is now the stub's axis) and the
   `to_slit` / `tail_from` lines are as they are. `_usb` is used nowhere else (grep: guide.py:912, 913, 926 only), so it can go.

Why tuck the ends in by 1 mm: the player gives every wire flat end caps and an outline hull (player/js/core.js:333-334, 391-395). If the tube
ended exactly on a plug's end face, its cap would be coplanar with that face and its outline would draw a ring on it. One mm in, the
tube's end is hidden: the stub (r 2.25) and the strain relief (r 4.0) are both wider than the tube (r 1.75).

## What the fix does (checked by reproducing `usb_cable()` outside the guide)

**Reproduction.** I rebuilt `usb_cable()` in a scratch script with the same constants and the same `tools/wires.py` and
`stepgen.turned` / `apply_pose` calls, without running guide.py. With the current constants it reproduces `steps.json` routes 65, 66,
104 and 105 to within 0.01 mm, with the same `tail_from` and `b_ref`. With the fix:

**The A end's resting pose (`offsets.USB_A` in every view from Start on).** It changes from
`{t: [-27.32, 12.27, -62.58], r: [0, 1, 0, -90], at: [602.32, 876.64, 1389.92]}`
to `{t: [-24.97, 12.56, -62.58], r: [0, 1, 0, -90], at: [599.97, 876.35, 1389.92]}`.
The plug moves +0.29 mm in y and +2.35 mm in z. Its middle is then [575.00, 888.91, 1327.34] = `A_TARGET`. Its underside is at
y 884.64, 0.03 mm above the table (it was 0.26 mm into it). Its x range is unchanged (525.3 - 575.0).

**The routes:**

| route | used in | points | length mm | tail_from | first point | last point |
|---|---|---|---|---|---|---|
| hover (now 65) | Step 40 | 118 -> 121 | 116.7 -> 119.6 | 60.8 -> 62.8 | [659.34, 903.33, 1372.39] | [574.0, 888.91, 1327.34] |
| seated (now 66) | Steps 40c - 55 | 101 -> 104 | 99.4 -> 102.4 | 43.7 -> 45.7 | [659.34, 903.33, 1354.39] | same |
| swung (now 104) | Step 55c, via | 99 -> 102 | 97.4 -> 100.4 | 32.8 -> 34.8 | same | same |
| shut (now 105) | Step 55c on, Start, Completed View | 97 -> 100 | 95.1 -> 98.2 | 23.7 -> 25.8 | same | same |

**How well each end now sits on its plug's axis.**
- Mini-B: the first two points are on the stub's axis (0.00 mm off; the old route was 1.74 mm off). The third point, 1 mm out of the
  stub, is 0.08 - 0.11 mm off.
- A end: the last 13 mm are on the strain relief's axis to 0.005 mm (old: 2.37 mm off).

**What else moves.** Apart from the two ends, each new route stays within 0.17 mm of the old one: within 0.6 mm 5 - 10 mm from the
Mini-B end, and within 0.17 mm from 20 mm on. The slit, F2 and the run on the table are unchanged.

**Bends.** The new start has no hook: the old route left the plug heading towards +z and turned back. The tightest bend over each
whole route is gentler:

| route | tightest bend radius now | after the fix |
|---|---|---|
| hover | 2.48 mm | 4.13 mm |
| seated | 2.29 mm | 3.80 mm |
| swung | 1.97 mm | 3.24 mm |
| shut | 2.21 mm | 2.86 mm |

**Clearances.** The first 25 mm against the parts near the Mini-B end (triangles from `lac-guide.glb` and the extra parts,
`trimesh.proximity.closest_point`, tube surface to part):

| shape | breadboard | F2 | j1 cap |
|---|---|---|---|
| seated | 0.96 (was 0.85) | | 6.65 |
| swung | 1.18 (was 1.12) | | |
| shut | 0.65 (was 0.65) | 0.74 (was 0.72) | |

The tube's ends against every other wire drawn in the same view (`steps.json` routes, both radii taken off):
- hover: buzzer red 1.11 (was 1.34), jumper orange 11.96.
- seated: buzzer red 2.47 (was 2.47), jumper orange 7.11.
- shut: jumper orange 7.10.

Nothing new is touched. (In the hover shape the cable passes through where F5 will be, as it does now, but F5 is not on screen until
Step 54.)

**The A end against F2.** I checked the moved A end against F2 at 43 samples of F2's way in at Step 55 (off, hooked, swung, shut).
The nearest vertex-to-vertex distance is 10.8 mm (it was 9.7 mm).

**Cameras.** No camera should change:
- Every view that shows the A end after Step 40 has its camera set in guide.py: Step 40 and the steps from Step 41 on, which use
  CASE_CAMERA, `frame_on` of other parts, END_CAMERA or an explicit `view_dir` / `frame`.
- The title page and the Completed View are framed by `_fit(self.model, used, [{}])` (stepgen.py:1951), which uses every part at its
  seat, not its resting pose.

Still, diff every view's camera against a copy of steps.json saved before the edit, as usual. The card picture (`cards/steps.json.webp`)
shows the A end and should be taken again before the guide is next published.

## Not changed, for Lee if wanted

- The tube stays 3.5 mm across (r 1.75, as the MRA's). Centred, it leaves a 0.5 mm lip of the Mini-B's 4.5 mm stub showing all round,
  which reads as the plug's strain relief.
- r 2.25 would make that join flush. It would also leave only 0.25 mm each side in F2's 5 mm slit, and the clearance to the breadboard in
  the shut shape would fall to 0.15 mm.
- The CAD's own cable is 5.25 mm across and would not fit the slit.

## Checking after the edit

1. Run guide.py.
2. Check that steps.json has the routes and the `USB_A` offset in the tables above.
3. In the player, look at Steps 40, 40c, 55 and 55c and the Completed View close up at both plugs (`_dev.look('NAUO122', [-1, 0.3, 0])`
   and `_dev.look('USB_A', [1, 0.4, 0.3])`).
4. Run `.venv.nosync/bin/python tools/motioncheck.py "LAC Build Instructions" "Step 40c" "Step 55c"` for the plug going in and F2 sliding
   along the cable. (It loads the model, so run it alone.)
5. Run the camera diff, then `_runthrough()`.
