# Code review of the 14 Oct 2026 changes (independent agent), and what was done

Scope: the turned-over views (`world` group in `js/core.js`, the turn in `js/player.js`), faded wire ends, click
highlight, labels without a ring, per-part paths, `put_away`, code-aware cameras (`tools/stepgen.py`), `own_parts`,
pose adjusts and stickers (`tools/build_model.py`), `wires.smoothed` / `route(fade=)`.

| Finding | Status |
|---|---|
| A clicked part showed tinted in the step pictures drawn while it was picked. | Fixed: `renderThumb` drops the highlight for the picture and puts it back (`stage.highlighted()`). |
| Per-part `paths` were not played: every moving part took the first part's path (harmless for the two-pose jumper paths). | Fixed in `go()` / `stepAnimation`. Lead lines are still worked out from `path` for every part; documented in `place()` (wire steps have none). |
| Stepping again while the model was half turned over snapped it to the end of the previous turn. | Fixed: the turn starts from the orientation on screen (`worldLive`). |
| A picked faded wire lost its tint when it was redrawn. | Fixed: `setWires` swaps a fading wire's material only when its fade starts or stops, and keeps a tint. |
| Latent: a part put away and shown again in the very next view would glide, and its wires bend, from the bench. | Documented in `put_away()`: put a card between (the electronics test does). |
| Latent: `Guide.put_away` kept the riding of parts carried by a put-away part. | Fixed: they are released with it, as `build()` already did. |

Checked and found correct: flipped views with labels, lead lines, picking, step pictures and depth range (shown,
entered, left, jumped to); the sticker node matrix (it undoes the motor mesh's de-quantization); `promote`; the
rotate-in-place adjust in both tools; codes moved by the adjust; `smoothed` and `fade`.

After the fixes: `_runthrough()` 207 views, 0 problems; the turn stays at 90 degrees when Next is pressed half way and
ends at 180; a picked part is plain in a step picture and tinted again after it; a picked faded wire stays tinted.
