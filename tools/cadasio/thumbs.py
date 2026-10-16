"""Fetch the published picture of every step of a guide and build labelled contact sheets.

    python tools/cadasio/thumbs.py <digest folder> <raw picture folder> <picture folder> <contact sheet folder>

Reads the <guide id>.json files written by digest.py. Needs Pillow.
"""
import json, sys, os, subprocess, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
dig, raw_dir, out_dir, sheet_dir = sys.argv[1:5]
def fetch(job):
    url, dst = job
    if os.path.exists(dst) and os.path.getsize(dst) > 500: return True
    r = subprocess.run(['curl', '-sS', '-m', '60', '--retry', '2', '-o', dst, url], capture_output=True)
    return r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 500
font = ImageFont.load_default(size=30)
for f in sorted(os.listdir(dig)):
    if not f.endswith('.json'): continue
    gid = f[:-5]; d = json.load(open(os.path.join(dig, f)))
    rd = os.path.join(raw_dir, gid); od = os.path.join(out_dir, gid); sd = os.path.join(sheet_dir, gid)
    for p in (rd, od, sd): os.makedirs(p, exist_ok=True)
    jobs = [(s['image'], os.path.join(rd, '%03d.webp' % i)) for i, s in enumerate(d['steps']) if s.get('image')]
    with cf.ThreadPoolExecutor(8) as ex: ok = list(ex.map(fetch, jobs))
    cells = []
    for i, s in enumerate(d['steps']):
        src = os.path.join(rd, '%03d.webp' % i)
        try:
            im = Image.open(src).convert('RGB')
        except Exception as e:
            im = Image.new('RGB', (1280, 460), (240, 240, 240)); ImageDraw.Draw(im).text((40, 200), 'no image', fill=(150, 0, 0), font=font)
        im.thumbnail((1400, 1400)); im.save(os.path.join(od, '%03d.jpg' % i), quality=82)
        cells.append((i, s['name'], s['behaviour'], im))
    # contact sheets: 2 columns x 4 rows
    CW, CH, PAD, CAP = 1000, 380, 10, 40
    for a in range(0, len(cells), 8):
        chunk = cells[a:a + 8]; rows = (len(chunk) + 1) // 2
        sheet = Image.new('RGB', (2 * CW + 3 * PAD, rows * (CH + CAP + PAD) + PAD), (120, 120, 120))
        dr = ImageDraw.Draw(sheet)
        for n, (i, name, beh, im) in enumerate(chunk):
            x = PAD + (n % 2) * (CW + PAD); y = PAD + (n // 2) * (CH + CAP + PAD)
            dr.rectangle([x, y, x + CW, y + CAP + CH], fill=(255, 255, 255))
            dr.rectangle([x, y, x + CW, y + CAP], fill=(20, 40, 70))
            dr.text((x + 10, y + 3), '[%03d] %s%s' % (i, name, '  (auto-advance)' if beh == 'play' else ''), fill=(255, 255, 255), font=font)
            c = im.copy(); c.thumbnail((CW, CH)); sheet.paste(c, (x + (CW - c.width) // 2, y + CAP + (CH - c.height) // 2))
        sheet.save(os.path.join(sd, 'sheet_%03d-%03d.jpg' % (chunk[0][0], chunk[-1][0])), quality=80)
    print(gid, 'steps', len(cells), 'fetched ok', sum(ok), '/', len(jobs), 'sizes', sorted({c[3].size for c in cells})[:4])
