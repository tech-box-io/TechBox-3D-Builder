# Lee's third note of 15 Oct 2026, and what was done

"After testing the build, I found that the Elbow Motor's Wire should really be above the Base Motors Wire. So currently, the
build has the Elbow Motor wire pass under the Base Motor Wire. I think we should instead pass the Elbow Motor's wire above the Base
Motor's wire and into its Row slot." (It impacts Step 98.)

| What | Done |
|---|---|
| The elbow motor's lead over the base motor's lead | The CAD routes the elbow motor's lead under the arch that the base motor's lead makes over to row 5. Now it is as the CAD has it as far as just past the hook-shaped slot in R5, then rises in wide bends over that arch (about 8 mm above it at its top, middle wire to middle wire) and comes straight down into row 6 beside the base motor's lead, as before. 262 mm (243 under the arch). From Step 98c to the Completed View, and on the title page: no closer than 1.6 mm to the base motor's lead (where the two come down side by side), clear of every part and other wire. |
| Step 98 | Three beats as before. The plug is drawn off the hook and up to the top of the arch, then over it and upright over row 6, then down; it passes along the way its own lead will lie, the plug leading (each stage is the plugged lead cut short, so the lead only lengthens along its own way and its wires keep their order). Checked at 241 frames forwards and 121 back: its wires stay 1.0 mm or more from the base motor's lead (surface to surface) and pass through no part or wire; the plug's surface stays 0.5 mm or more from every wire; it turns at most 4.6 degrees in a hundredth of a second (as the shoulder plug in Step 99); for about a fifth of a second as it goes over the arch the lead is a little narrower as it turns (its wires 0.69 mm apart, centre to centre, against about 1.0 mm). |
| Nothing else | Loose and hooked, the elbow motor's lead is exactly as before (Steps 53 - 97c unchanged); no camera changed. Only the title page, Step 98 and the plugged elbow motor's lead in Steps 98c - 101 and the Completed View differ from before. |

After the change: `_runthrough()` 211 views, 0 problems. Review: review_v11.md. Checkpoint: `share/MRA Full Build 2026-10-15c/` and its zip.
