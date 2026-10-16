# Review v10: Lee's second note of 15 Oct 2026

Three independent reviewers (the code of guide.py against the copy from before the round, rebuilding the new routes; coverage of
Lee's requests and the docs; the result in the browser, against a replay of the guide from before the round), then an
adversarial verifier for each medium or high finding. Workflow run `wf_c0ef4b3c-e3e`.

The reviewers confirmed: only the asked captions and the motions of Steps 98 and 99 changed (their end states, every camera and
every other view as before); the new routes in steps.json match a rebuild of guide.py's helpers to 0.00 mm, each drawn for the
plug pose it is used with, three beats with two in-between routes each so the wires keep pace; Step 98's elbow lead, 0.93 - 0.98 mm
into the base motor's lead before, now stays clear of it (0.02 mm at the closest, where the two lie side by side as in the CAD);
`_runthrough()` 211 views, 0 problems.

| Finding | Severity | Outcome |
|---|---|---|
| Step 99: the shoulder plug still turned 140 degrees in its second beat (the off-the-hook stage could not be turned half-way with the lead heading as the CAD has it there), and its lead's three wires pinched together mid-move (to 0.39 mm centre to centre, about 280 ms) | medium, verified | Fixed: off the hook the lead dips towards the row, so the plug is half-way round there; 85 and 83 degrees in the two beats. The pinch is down to 0.71 mm (a slight narrowing for about a quarter of a second; 1.0 mm is normal). |
| Step 99: the two places the plug passes through over the joysticks' wires carried no turn, so it stood up, tilted 23 degrees over the row and straightened again (288 degrees of turning for a net 175) | low, verified with the above | Fixed: they carry the tilt it has over the row; it straightens once, going down onto the row. |
| Step 98: the off-the-hook route had an unrounded 46-degree bend where it leaves the CAD's line | low | Fixed: that point is rounded like the other corners (both leads); Step 98 rechecked clear of the base motor's lead. |
| "15 mm and more below the base motor's lead" measured 12 - 14.5 mm | low | Fixed in the note and the guide.py comment. |
| review_v10.md and the round's checkpoint missing | low | Written; checkpoint `share/MRA Full Build 2026-10-15b/`. |
| The scanner's "76 degrees per frame" at the beat boundaries | not a defect | Confirmed a sampling artefact: the drawn wire changes by at most 0.14 mm across the boundary. |
| Step 100's Z-bend in the extension wire mid-move | low | Kept: unchanged from before, and Lee approved Step 100. |
