# Review v8: Lee's third round of 14 Oct 2026

Independent reviewers (the player; the generator and guide; coverage of Lee's nine requests and the docs), then an adversarial
verifier for each medium or high finding. Workflow run `wf_d67de5e2-31a`. What was found and what was done:

| Finding | Severity | Outcome |
|---|---|---|
| Going back from Step 100c to 100 (and 97c to 97) moved the plug and its wire straight back, through the jumper wires the step had just been routed round | medium, verified | Fixed in the player: going back from a step whose wire passes through routes in between plays that step backwards (the part's way and its stops reversed, the wire back through the same routes, a riding plug back the way it came). Only steps of that kind (Steps 25, 78, 94, 95, 97 and 100) are affected; every other step goes back as before. Checked frame by frame both ways: the same clearances backwards as forwards. |
| Step 97c: the extension sank through R4's solid wood on its way from over the top edge to the pocket | medium, verified | Fixed: a stage in between. As the join goes down behind R4 the extension goes down the stem of R4's L-shaped slot to its foot, then across into the pocket. The stem is 2.1 mm wide and the flat lead about 3 mm, so through R4 the lead is turned on edge (brown on top, away from the base motor's lead in the same slot), flat again either side. Checked against R4's mesh at 121 frames each way: the wire's surface stays inside the slot; it touches the base motor's lead (1.01 mm centre to centre) and passes through no part. |
| Step 100c: the plug cut the corner of B6's tower beside it as it set off | low | Fixed: it goes straight up 26 mm first (a pass-through pose, so still three beats). |
| Step 100c: the extension lay 0.47 mm into the shoulder motor's orange wire in the last beat | low | Fixed by the reroute: 1.5 mm centre to centre at the closest. |
| Step 100's first stage: the lead's turn over the plug's top passed through itself | low | Fixed: up beside the plug 4 mm to the side of the shoulder motor's wire and over the plug's top in a 7 mm wide turn. While the lead changes shape on the way there, its last centimetre kinks for two or three frames (about 80 ms). Kept: it reads as the lead bending into the plug. |
| Step 97: the lead left the coupler backwards | low | Fixed: it leaves the coupler straight out of its mouth. |
| The large part picture: on a change of view it gave the keyboard back to a band about to be removed; the step list could be opened over it | low | Fixed: it closes without moving the keyboard on a change of view (the keyboard goes to Next as for any hidden button), and opening the step list closes it; closing the list goes back to the part's band. Checked. |
| Wires in part pictures shared ids across parts (a reused wire keeps the colour it was made with) | low (latent) | Fixed: an id per part. The pictures re-render identically. |
| The extension's length differs from stage to stage (51 - 146 mm) | low | Kept: the player grows or shortens a wire from its free end as it changes route; the run from the coupler to the slot, which the eye follows, stays the same. |
| A 'no straight-line path' Review note is hidden with the notes switched off | low | Fixed: the generator's log prints a WARNING line as well. |
| Docs: README (wires "not pictured"; the board "house blue"), CLAUDE.md (the bundle carries the pictures; Review-note wording), rulebook (colour library, section 14's date line), materials.json notes ("second round") | low | Fixed. |

After the fixes: `_runthrough()` 211 views, 0 problems; every camera diffed against steps.json from before the round
(none changed; Step 76c is gone, as asked); steps 96c to 101 checked forwards and backwards for parts and wires.
