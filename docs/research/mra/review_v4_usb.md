# Review of the USB cable and the title-page camera (14 Oct 2026), and what was done

A workflow of three reviewers (code, geometry, what a student sees) with an adversarial verifier per finding: 14 agents.

Confirmed, and fixed:

| Finding | Fix |
|---|---|
| The title-page camera taken from Lee's screenshot fits only wide frames: at 4:3, on a tablet or a phone the robot runs under the title or off the right edge. | `start_view` has `min_aspect=1.7`; below it the player uses the finished model's camera with the usual title-page shift (`poseFor`, `camera.otherwise`). Checked at 2000 x 1104 (Lee's framing) and 1024 x 768 (fallback, clear of the title). |
| In the hover views the cable, bent from its seated route, folded back on itself. | The hover views have a route of their own, drawn with the plug 30 mm out (`usb_cable(plug=30)` as `wires=`, the seated route as `wires_done=`). |
| A lone USB-A plug showed behind R3 on the title page (the cable hidden by the base). | `start_view` `hide=['USB_B', 'USB_A']`: the cable is left off the title page only. |
| The cable was drawn in black plastic #1e1616, not the house cable-jacket colour. | `cable_black` #2d2926 in the palette. |
| build_model placed extra parts in the assembly node's frame, stepgen in the world frame (identical for the MRA, whose assembly node is the identity). | `add_extra_parts` cancels the assembly node's matrix. |
| With several scene roots build_model skipped extra parts silently, and the model would rebuild on every run. | It now stops with a message. |

Refuted (no change): the Completed View's framing (as before this round), the USB label's position (the player's general label rule), the lead line ending at the socket mouth (no rule broken), the missing part picture (rendered after the run).

Checked and found right: the GLB merge (offsets, alignment, byteLength, indices); the same pose in both tools (difference 0.0); the Mini-B wide side up as the socket's, on its axis, tip 0.24 mm short of the cavity floor, overlap at most 0.15 mm (the tongue inside the hollow plug); the overmould clear of the board edge and the module; the A end on the table and on the bench; no cable route within its radius of any part, hover or seated; `_runthrough()` 209 views, 0 problems.
