"""Write colour-atlas-lsm.json: the colour of every solid of the LSM's purchased parts, as TechBox's published Cadasio guide shows them.

    .venv.nosync/bin/python "LSM Build Instructions/make_atlas.py"

Read with tools/cadasio/atlas.py from the published LSM Full Build (docs/research/lsm/cadasio/raw/...), then regrouped by the mesh
names of lsm.glb (assemble.py): a Cadasio component that is several meshes here (a resistor: its body, its legs drawn as wires) gives
each mesh only its own solids. The boxes are Cadasio's, in the part's own frame, which is the frame of our mesh (assemble.py checked
each to 0.01 mm). Cadasio's coloured face copies ("Surface-Offset": the breadboard's printing, the resistors' bands, the capacitor's
stripe) are marked skin, so the face underneath takes their colour. The Nano is the MRA's model and keeps the MRA's colours.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parent
ROOT = KIT.parent
PAYLOAD = ROOT / 'docs/research/lsm/cadasio/raw/19075-laser_stem_matrix_lsm_-_full_build.json'

# our mesh name: (Cadasio component, which of its solids (name prefix), or None for all)
MESHES = {
    'Breadboard': ('Breadboard-1', None),
    '8x8 LED': ('8x8 LED-4', None),
    'Resistor body 12k': ('Resistor 1-1', 'Resistor body'),
    'Resistor body 330': ('Resistor 2-1', 'Resistor body'),
    'Capacitor body': ('Capacitor V3-1', 'Capacitor body'),
    'Push button': ('Push button-1', lambda s: not s['name'].startswith('Push button-Boss-Extrude6')),   # (less its nut)
    'USB Right Angle': ('USB Right Angle-1', None),
    'Wire Cap V2': ('Wire Cap V2-1', None),
}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / 'atlas.json'
        subprocess.run([sys.executable, str(ROOT / 'tools/cadasio/atlas.py'), str(PAYLOAD), str(raw)] + sorted({c for c, _ in MESHES.values()}),
                       check=True, capture_output=True)
        comps = json.load(open(raw))
    out = dict(_about=__doc__.split('\n\n')[0] + ' Written by make_atlas.py.',
               _source=dict(payload=str(PAYLOAD.relative_to(ROOT)), tool='tools/cadasio/atlas.py', mra='MRA Build Instructions Prototype/colour-atlas-mra.json'))
    for mesh, (comp, which) in MESHES.items():
        solids = comps[comp]['solids']
        if isinstance(which, str):
            solids = [s for s in solids if s['name'].startswith(which)]
        elif callable(which):
            solids = [s for s in solids if which(s)]
        solids = [dict(s, **({'skin': True} if 'Surface-Offset' in s['name'] else {})) for s in solids]
        lo = [min(s['min'][a] for s in solids) for a in range(3)]
        hi = [max(s['max'][a] for s in solids) for a in range(3)]
        out[mesh] = dict(cadasio_part=comp, bbox_min=lo, bbox_max=hi, solids=solids)
    mra = json.load(open(ROOT / 'MRA Build Instructions Prototype/colour-atlas-mra.json'))
    out['nano_Varsayılan'] = dict(mra['nano_Varsayılan'], source='mra_atlas')
    json.dump(out, open(KIT / 'colour-atlas-lsm.json', 'w'), indent=1, ensure_ascii=False)
    print('colour-atlas-lsm.json:', ', '.join(f"{m} ({len(out[m]['solids'])})" for m in out if not m.startswith('_')))


if __name__ == '__main__':
    main()
