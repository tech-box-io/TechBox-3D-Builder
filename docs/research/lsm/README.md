# `lsm/`: the Laser Stem Matrix (19 Oct 2026)

What the LSM guide's first draft is built on.

- `cad_study.md`: Lee's four STEP files, what is missing or broken in them, how `assemble.py` puts the model back together from them
  and the published Cadasio assembly, and every correction made to Cadasio's placements (all under 1.4 mm).
- `cadasio/`: TechBox's published LSM Full Build (instructions.online, `19075-laser_stem_matrix_lsm_-_full_build`): the raw payload
  (`raw/`), its per-step digest (`tools/cadasio/digest.py`: `19075-...md` / `.json`), the published pictures and contact sheets
  (`thumbs/`, `tools/cadasio/thumbs.py`), `cadasio_world_boxes.json` (every top-level component's placement matrix and box in assembly
  mm, with its tooltip) and `replay.json` (for each shown step: which components are visible, how far each is moved from its CAD
  place, and the camera).
- The step-by-step report on the published guide, its conventions and slips, is `../guide_19075-laser_stem_matrix_lsm_-_full_build.md`
  (written 13 Oct 2026 with the other 19 published guides); the Part guides' reports sit beside it.
