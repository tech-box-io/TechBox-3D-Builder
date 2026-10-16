# Lee's feedback of 14 Oct 2026 (third round), and what was done

Step numbers are those of the second round (lee_notes_2026-10-14b.md). Step 76c is gone (the arm check is one view), so views
after it are one fewer; step numbers do not change.

| Request | Done |
|---|---|
| The servo extension wire's parts-list picture showed one end only | Pictured whole, as it lies loose in Step 96: the coupler, the three wires and the row 10 plug (`g.part_picture`). |
| Clicking a part in the parts list should show its picture bigger | Each band is a button: a click, or Tab and Enter, shows the 500 x 500 px picture large with its name; Escape, the cross or a click outside closes it and the keyboard goes back to the band. Nothing loads until the page is opened (in the single-file checkpoint the pictures are inside it). |
| The I/O module's board the same blue as the Nano's | Navy `#000f41` (palette `pcb_navy`), as TechBox's own Cadasio project has it; the house blue is gone from the module. The white silkscreen reads well on it. |
| The Elbow Motor's dot just off black (#181818 or #141414) | `#181818` (palette `sticker_off_black`). It still has the dot's black outline ring. |
| The jiggle on A13 and A12, not A11; one advance | Step 76 is a single view (no Step 76c): A13 and A12, whose far ends are still free, rock about 6 degrees about their own screws as the step opens (stepping, going back or jumping to it); A11 stays put. |
| Step 100: the extension wire clipped through the right joystick's wires | Measured: the extension lay against the right joystick's GND wire where it comes down to A0 (0.2 mm), and went straight through the jumper wires while it was lifted to row 10. Now its plug hangs just in front of R4 beside the module from Step 97 on (clear of the jumper wires and of the elbow and shoulder plugs' paths), and Step 100 takes it in three beats: straight up clear of B6's tower, then up under the shoulder motor's wire beside the module (no jumper wires there), across with its underside 7 mm above the jumper wires beside the shoulder motor's wire, and down onto row 10. The wire changes route stage by stage, in step with the plug, passing 4 mm beside the shoulder motor's wire and over the plug's top in a wide turn. Step 97's plug goes over higher too (it had grazed the jumper wires), and Step 97's wire now goes down the stem of R4's L-shaped slot turned on edge (the flat lead is wider than the 2.1 mm stem) and across into the pocket, where before it passed through R4's wood. Checked at 41 - 121 frames of every step from 96c to 101, forwards and backwards: the plug touches no wire, the extension passes through no part (its surface stays inside R4's slot) and through no other wire (1.0 mm centre to centre at the closest, two 1 mm wires touching). Going back from Step 97c or 100c plays the step backwards. |
| Title page: "(C) TechBox. A division of TARIS Industries, LLC. All Rights Reserved." | "© TechBox. A division of TARIS Industries, LLC. All Rights Reserved." |
| Hide the Review Notes for this model | `Guide(review_notes=False)`: no notes and no switch in the MRA guide; the feature stays for new builds (`?review=1` shows any notes left). |
| A new shareable checkpoint | `share/MRA Full Build 2026-10-14c/` and its zip. |

No camera changed (compared view by view with steps.json from before the round). After the independent review (review_v8.md):
`_runthrough()` 211 views, 0 problems.
