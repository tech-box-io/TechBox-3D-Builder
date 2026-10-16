# Review v11: the elbow motor's lead over the base motor's lead (Lee, 15 Oct 2026, third note)

Two independent reviewers (the code and docs, against guide.py and steps.json from before the change; the result in the browser,
against the version from before side by side), then an adversarial verifier for any medium or high finding (there were none).
Workflow run `wf_eef3e717-d72`.

The reviewers confirmed: the plugged lead goes over the base motor's lead's arch, not under it, and comes down beside it into row
6; the elbow motor's loose and hooked states, every earlier view and every camera are unchanged; Step 98 keeps three beats with
two in-between routes each drawn for the plug pose it is used with; `_runthrough()` 211 views, 0 problems.

| Finding | Severity | Outcome |
|---|---|---|
| A brief zig-zag in the lead in the middle of Step 98 (about 0.1 s), where the first stop had cut it | low | Fixed: the first stop is at the top of the arch (the plug passes the old one on its way), so the middle move is shorter and turns less. Rechecked: no zig-zag; the lead stays 1.0 mm or more from the base motor's lead (it was 0.45) and comes no closer to itself than 7.6 mm. |
| The plug turned up to 5.7 degrees per 10 ms over the arch | low | Fixed with the above: 4.6, as the shoulder plug in Step 99. |
| The new stretch over the arch looked drawn with a ruler from the front (6 mm bends) | low | Fixed: 12 mm bends; 1.6 mm from the base motor's lead at the closest, as before. |
| The note overstated the plug's clearance (0.43 mm measured, not 0.5) and the height over the arch ("6 mm and more") | low | Remeasured after the fixes and corrected (0.53 mm; about 8 mm, middle wire to middle wire). |
| The README put the crossing of the arch in the first beat; a comment still said "the CAD's lead" | low | Fixed. |
| The lead is a little narrower for about a fifth of a second as it turns over the arch (wires 0.69 mm apart, centre to centre) | low | Kept, as in Step 99 (0.71 mm); reported. |
| review_v11.md and the checkpoint named before they existed | low | Written; checkpoint `share/MRA Full Build 2026-10-15c/`. |
