"""Turn the read code renders into world directions: letters-up and reading direction for each code (read by eye from
codes_sheet.png: 'up' = upright in the render, 'ccw' = reads bottom-to-top, 'cw' = reads top-to-bottom)."""
import sys, json, numpy as np
SP = sys.argv[1]
R = json.load(open(SP + '/codes_raw.json'))
READ = {'NAUO63': ('H1', 'ccw'), 'NAUO65': ('H2', 'up'), 'NAUO66': ('H3', 'cw'), 'NAUO73': ('H4', 'up'), 'NAUO67': ('H5', 'cw'),
        'NAUO60': ('H6', 'cw'), 'NAUO68': ('H7', 'cw'), 'NAUO61': ('H8', 'ccw'), 'NAUO69': ('H9', 'ccw'), 'NAUO70': ('H9', 'ccw'),
        'NAUO71': ('H9', 'ccw'), 'NAUO72': ('H9', 'ccw'), 'NAUO64': ('H10', 'up'), 'NAUO62': ('H11', 'up'), 'NAUO77': ('H12', 'up'),
        'NAUO75': ('H13', 'ccw'), 'NAUO74': ('H14', 'ccw')}
def word(v):
    v = np.asarray(v); k = np.argmax(np.abs(v))
    s = ('+' if v[k] > 0 else '-') + 'XYZ'[k]
    return s if abs(v[k]) > 0.99 else s + f'~({v.round(3).tolist()})'
out = {}
for i, (code, rot) in READ.items():
    r = R[i]; up = np.array(r['image_up']); right = np.array(r['image_right'])
    if rot == 'up':
        reading, lup = right, up
    elif rot == 'ccw':
        reading, lup = up, -right
    else:
        reading, lup = -up, right
    out[i] = dict(cad_name=r['name'], engraved=code, face_normal=r['engraved_face_normal'], centre=r['code_centre_on_face'],
                  letters_up=lup.round(4).tolist(), reading_dir=reading.round(4).tolist(), letter_height_mm=round(min(r['code_size_in_image']), 2),
                  code_length_mm=round(max(r['code_size_in_image']), 2))
    print(i, r['name'], '->', code, 'face', word(r['engraved_face_normal']), 'centre', r['code_centre_on_face'], 'letters up', word(lup), 'reads toward', word(reading))
json.dump(out, open(SP + '/codes.json', 'w'), indent=1)
