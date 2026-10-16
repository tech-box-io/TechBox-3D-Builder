"""Contact sheets from a folder of frames named tMMmSSs.jpg (as written by the frames tool).
    python sheets.py <frames dir> <out dir> [cols=4] [rows=2] [cell_width=400]
Each cell is labelled with its timestamp. Sheets are named sheet_<first timestamp>.jpg."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
rows = int(sys.argv[4]) if len(sys.argv) > 4 else 2
cw = int(sys.argv[5]) if len(sys.argv) > 5 else 400
os.makedirs(out, exist_ok=True)
files = sorted(f for f in os.listdir(src) if f.endswith('.jpg'))
try:
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
except Exception:
    font = ImageFont.load_default()
per = cols * rows
for i in range(0, len(files), per):
    chunk = files[i:i + per]
    ims = [Image.open(os.path.join(src, f)) for f in chunk]
    ch = max(int(im.height * cw / im.width) for im in ims)
    sheet = Image.new('RGB', (cols * cw, rows * ch), 'white')
    d = ImageDraw.Draw(sheet)
    for k, (f, im) in enumerate(zip(chunk, ims)):
        x, y = (k % cols) * cw, (k // cols) * ch
        sheet.paste(im.resize((cw, int(im.height * cw / im.width))), (x, y))
        d.rectangle([x, y, x + 96, y + 28], fill='black')
        d.text((x + 4, y + 2), f[1:-4], fill='yellow', font=font)
    sheet.save(os.path.join(out, 'sheet_' + chunk[0][:-4] + '.jpg'), quality=80)
print(len(files), 'frames ->', (len(files) + per - 1) // per, 'sheets in', out)
