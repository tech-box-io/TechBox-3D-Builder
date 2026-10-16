# Review of the changes for Lee's notes of 14 Oct 2026 (afternoon), and what was done

A workflow of two reviewers (the code; every note checked in the browser) with an adversarial verifier per finding: 16 agents.

| Finding | Fix |
|---|---|
| Steps 78-90: the model no longer jumped, but each step seen from the same corner still had its own framing, so the claw slid across the screen and settled. | A stretch of upside-down views from one corner keeps one framing (the smallest sphere round all of theirs): 78-79, 80, 81-82 and 83-90. |
| The Completed View was off centre and cut the claw off on frames narrower than about 1.6. | Lee's camera kept where it stands and turned to face the model, so it sits in the middle: fits down to 1.25 (the model reaches 0.87 of the half-width); min_aspect 1.2, the front view below that. |
| The Completed View showed the Mini-B plug with no cable (hidden from Lee's camera, visible when turned). | The USB cable is left off it, as on the title page. |
| Step 98's longer loose extension ran out of the bottom of the picture. | Frame widened. |
| Step 105's only lead line was 0.1 mm long. | Hover set to 65 mm. |
| The Testing Checklist card was taller than a phone's screen and could not scroll. | The card fits its space and scrolls; smaller list text on phones. |
| A flipped view looking straight up would have written NaN into steps.json. | Guarded. |
| README: click colour, an old step number, the removed power card. | Corrected. |

Refuted: the orange highlight on the orange servo leads and on engraved codes (what Lee asked for); a claim that the shared turn changed nothing (it compared with the wrong earlier player).

Checked and found right: R8's moved code (on the outer face, 0.05 mm proud, the right size, upright, over solid wood above the notch; the old pocket filled flush with no stray edges); the turned model with a pivot that is not the target (labels, lead lines, picking, step pictures, depth range; jumping in, out and within a run; going back); Steps 15-20, 26, 35, 38, 39, 55, 91, 98, 103-106 as Lee asked; the Start view at 2000, 1600, 1280 and 1024 px; `_runthrough()` 209 views, 0 problems.
