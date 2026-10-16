# Review of the 14 Oct 2026 evening changes and the first shareable checkpoint, and what was done

Two reviewers (the checkpoint opened as a recipient would; this round's code and data) with an adversarial verifier per
finding: 11 agents.

| Finding | Fix |
|---|---|
| Step 17's review note still asked which way round the dot colours go, after Lee had answered; it shipped in the checkpoint. | Removed. No view has a review note now. |
| Each dot went to the first spot with the most clear face, so on a face with room to spare it sat toward one end. | It goes to the spot nearest the middle of what shows that leaves a little room round it. The Claw dots are now central; on the Elbow / Shoulder label faces the screw heads of R7 / R8 still push it to one end. |
| The checkpoint's read-me named the CSV columns wrongly and left out parts.json. | Corrected. |
| The kit README gave the old dot colours. | Corrected. |
| player.html preloaded js/core.js without the query the player now imports it with. | Preload removed. |

Not changed, as Lee asked for no other changes without permission: the Elbow Motor's black dot on its unlabelled top face
is black on black (the CAD has its label on the underside only; video_arm.md item 24 says both side servos show a pink
label face up on the real kit). Asked in the report.

Refuted: the pick tool being on in the shared file (an authoring aid, harmless); the orange tint on pink and blue parts
(as asked); Steps 39 and 40 holding Step 38's camera as numbers (correct today).

Checked and found right: the zip unpacks to the folder exactly (no __MACOSX); the HTML opens from disk in headless Chrome
and starts; it is byte-identical to a fresh bundle.py run; its model, logo and steps equal the kit's; it requests nothing
outside itself; `_runthrough()` 209 views, 0 problems; only Steps 39, 40, 41, 96 and 100-102 changed camera and only
Steps 17, 28 and 92 lost their review notes against the morning's steps.json.
