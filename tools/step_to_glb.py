"""Convert a STEP file to GLB, the form the model tools read (one node and one mesh, in metres, as the main CAD export).

    python tools/step_to_glb.py <in.STEP> <out.glb>

For a purchased part that arrives as its own STEP file (the MRA's USB cable ends): the GLB goes in the kit folder and
materials.json "extra_parts" places it in the assembly. Uses cascadio (OpenCASCADE), 0.01 mm chord tolerance.
"""
import sys
from pathlib import Path

import cascadio


def convert(step, glb, tol_linear=0.01, tol_angular=0.3):
    step, glb = Path(step), Path(glb)
    if cascadio.step_to_glb(str(step), str(glb), tol_linear, tol_angular, False, True, False, False, set(), False) != 0:
        raise SystemExit(f'{step.name}: cascadio could not convert it')
    return glb


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    out = convert(sys.argv[1], sys.argv[2])
    print(f'{sys.argv[1]} -> {out} ({out.stat().st_size / 1e3:.0f} kB)')
