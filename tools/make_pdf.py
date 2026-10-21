"""A guide's 2D instructions as a PDF (Lee, 21 Oct 2026): landscape US Letter, one page per view in the guide's order, as
Cadasio exports its 2D instructions, with page numbers and TechBox's logo.

    .venv.nosync/bin/python tools/make_pdf.py "MRA Build Instructions Prototype" "share/<folder>/MRA Full Build.pdf"
    .venv.nosync/bin/python tools/make_pdf.py "MRA Build Instructions Prototype" "share/<folder>/MRA Deconstruction.pdf" steps-deconstruction.json

The pictures of the model come from the player, drawn by player/js/pages.js into the kit's pages/<steps file>/ folder (run it
first, for the same steps file, in the player served by tools/serve.py): the title page, every Step N (the part on its way, with
its lead lines or arrows, labels and eyes) and every Step Nc (the step done) on pages of their own, one after the other, and the
Completed View. A step's two pictures are cut to the same box (what either shows, with a margin), so the two pages line up.
The Parts List pages and the note cards are laid out here from the steps file and the kit's part pictures (parts/*.png).
Every page has the step's instruction and caution, as the player shows them, the logo and the guide's name at the top, and the
copyright and the page number at the foot; the PDF has a bookmark for every step.

The PDF is written by this file alone (no PDF library): pictures as JPEG, text in the PDF's own Helvetica (laid out with Arial's
widths, which are Helvetica's), so the text stays text: sharp at any size, and searchable.
"""
import json
import re
import sys
import zlib
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PAGE_W, PAGE_H = 792.0, 612.0                     # US Letter, landscape (points)
MARGIN = 34.0
BLUE = (0x00, 0xB0, 0xEF)                          # TechBox's blue (the logo's)
INK, GREY = (0x11, 0x11, 0x11), (0x6B, 0x72, 0x80)
CAUTION_LINE, CAUTION_FILL, CAUTION_INK = (0xC2, 0x41, 0x0C), (0xFF, 0xF4, 0xE6), (0x9A, 0x34, 0x12)   # the player's caution box
FONT_FILES = {'F1': '/System/Library/Fonts/Supplemental/Arial.ttf', 'F2': '/System/Library/Fonts/Supplemental/Arial Bold.ttf'}
PICTURE_QUALITY = 86                               # JPEG quality of the model's pictures
PICTURE_MAX_PX = 2600                              # (wider than this is more than print needs)

_fonts = {}


def width(text, size, font='F1'):
    """The width of `text` in points, in Helvetica (or Helvetica-Bold, F2) at `size`: measured with Arial, which has its widths."""
    if font not in _fonts:
        _fonts[font] = ImageFont.truetype(FONT_FILES[font], 1000)
    return _fonts[font].getlength(text) / 1000.0 * size


def wrap(text, size, max_w, font='F1'):
    """Lines of `text` no wider than max_w (a line break in the text starts a new line, as in a checklist card)."""
    lines = []
    for para in text.split('\n'):
        words, line = para.split(' '), ''
        for w in words:
            trial = (line + ' ' + w) if line else w
            if line and width(trial, size, font) > max_w:
                lines.append(line)
                line = w
            else:
                line = trial
        lines.append(line)
    return lines


def pdf_text(s):
    """A string as a PDF literal in WinAnsi (Windows-1252), the encoding of the PDF's own fonts."""
    s = s.replace('→', '->').replace(' ', ' ').replace(' ', ' ')
    b = s.encode('cp1252', errors='replace')
    return b'(' + b.replace(b'\\', b'\\\\').replace(b'(', b'\\(').replace(b')', b'\\)') + b')'


def rgb(c):
    return ' '.join(f'{v / 255:.3f}' for v in c)


class Pdf:
    """Just enough PDF: pages of text, filled shapes and pictures, two standard fonts, bookmarks."""

    def __init__(self, title, author='TechBox'):
        self.objs, self.pages, self.outline = [], [], []
        self.catalog, self.pages_id = self.reserve(), self.reserve()
        self.fonts = {'F1': self.add(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>'),
                      'F2': self.add(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>')}
        self.info = self.add(b'<< /Title ' + pdf_text(title) + b' /Author ' + pdf_text(author) + b' /Creator (TechBox make_pdf.py) >>')

    def reserve(self):
        self.objs.append(None)
        return len(self.objs)

    def add(self, data, oid=None):
        if oid is None:
            self.objs.append(data)
            return len(self.objs)
        self.objs[oid - 1] = data
        return oid

    def stream(self, data, extra=b'', compress=True):
        if compress:
            data, extra = zlib.compress(data, 9), extra + b' /Filter /FlateDecode'
        return self.add(b'<< /Length ' + str(len(data)).encode() + extra + b' >>\nstream\n' + data + b'\nendstream')

    def jpeg(self, image, quality=PICTURE_QUALITY):
        """A picture (PIL, any mode: transparency onto white) as a JPEG image object: (id, width px, height px)."""
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGBA')
            flat = Image.new('RGB', image.size, (255, 255, 255))
            flat.paste(image, mask=image.split()[-1])
            image = flat
        image = image.convert('RGB')
        buf = BytesIO()
        image.save(buf, 'JPEG', quality=quality, optimize=True, subsampling=0 if quality >= 90 else 2)
        data = buf.getvalue()
        head = (f' /Type /XObject /Subtype /Image /Width {image.width} /Height {image.height} /ColorSpace /DeviceRGB'
                f' /BitsPerComponent 8 /Filter /DCTDecode').encode()
        oid = self.add(b'<< /Length ' + str(len(data)).encode() + head + b' >>\nstream\n' + data + b'\nendstream')
        return oid, image.width, image.height

    def page(self, content, images, bookmark=None):
        res = b'<< /Font << /F1 %d 0 R /F2 %d 0 R >>' % (self.fonts['F1'], self.fonts['F2'])
        if images:
            res += b' /XObject << ' + b' '.join(b'/%s %d 0 R' % (n.encode(), i) for n, i in images.items()) + b' >>'
        res += b' >>'
        contents = self.stream(content.encode('latin-1') if isinstance(content, str) else content)
        pid = self.add(b'<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %g %g] /Resources %s /Contents %d 0 R >>'
                       % (self.pages_id, PAGE_W, PAGE_H, res, contents))
        self.pages.append(pid)
        if bookmark:
            self.outline.append((bookmark, pid))
        return pid

    def save(self, path):
        self.add(b'<< /Type /Pages /Kids [' + b' '.join(b'%d 0 R' % p for p in self.pages) + b'] /Count %d >>' % len(self.pages), self.pages_id)
        cat = b'<< /Type /Catalog /Pages %d 0 R' % self.pages_id
        if self.outline:
            root = self.reserve()
            ids = [self.reserve() for _ in self.outline]
            for k, ((title, pid), oid) in enumerate(zip(self.outline, ids)):
                links = b''.join([b' /Prev %d 0 R' % ids[k - 1] if k else b'', b' /Next %d 0 R' % ids[k + 1] if k + 1 < len(ids) else b''])
                self.add(b'<< /Title ' + pdf_text(title) + b' /Parent %d 0 R' % root + links + b' /Dest [%d 0 R /Fit] >>' % pid, oid)
            self.add(b'<< /Type /Outlines /First %d 0 R /Last %d 0 R /Count %d >>' % (ids[0], ids[-1], len(ids)), root)
            cat += b' /Outlines %d 0 R /PageMode /UseOutlines' % root
        self.add(cat + b' >>', self.catalog)
        out, offsets = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'), []
        for k, obj in enumerate(self.objs, 1):
            offsets.append(len(out))
            out += b'%d 0 obj\n' % k + obj + b'\nendobj\n'
        xref = len(out)
        out += b'xref\n0 %d\n0000000000 65535 f \n' % (len(self.objs) + 1)
        out += b''.join(b'%010d 00000 n \n' % o for o in offsets)
        out += b'trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(self.objs) + 1, self.catalog, self.info, xref)
        Path(path).write_bytes(bytes(out))
        return len(out)


class Canvas:
    """One page's drawing commands (PDF coordinates: points, from the bottom left)."""

    def __init__(self):
        self.ops, self.images = [], {}

    def text(self, x, y, s, size, font='F1', colour=INK):
        self.ops.append(f'BT /{font} {size:g} Tf {rgb(colour)} rg {x:.2f} {y:.2f} Td ' + pdf_text(s).decode('latin-1') + ' Tj ET')

    def rect(self, x, y, w, h, fill=None, stroke=None, line=1.0, radius=0.0):
        path = rounded(x, y, w, h, radius) if radius else f'{x:.2f} {y:.2f} {w:.2f} {h:.2f} re'
        ops = [f'{line:g} w'] + ([f'{rgb(fill)} rg'] if fill else []) + ([f'{rgb(stroke)} RG'] if stroke else [])
        self.ops.append(' '.join(ops) + f' {path} ' + ('B' if fill and stroke else 'f' if fill else 'S'))

    def line(self, x1, y1, x2, y2, colour, w=1.0):
        self.ops.append(f'{w:g} w {rgb(colour)} RG {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S')

    def image(self, name, oid, x, y, w, h):
        self.images[name] = oid
        self.ops.append(f'q {w:.2f} 0 0 {h:.2f} {x:.2f} {y:.2f} cm /{name} Do Q')

    def content(self):
        return '\n'.join(self.ops)


def rounded(x, y, w, h, r):
    k = 0.5523 * r
    return (f'{x + r:.2f} {y:.2f} m {x + w - r:.2f} {y:.2f} l {x + w - r + k:.2f} {y:.2f} {x + w:.2f} {y + r - k:.2f} {x + w:.2f} {y + r:.2f} c '
            f'{x + w:.2f} {y + h - r:.2f} l {x + w:.2f} {y + h - r + k:.2f} {x + w - r + k:.2f} {y + h:.2f} {x + w - r:.2f} {y + h:.2f} c '
            f'{x + r:.2f} {y + h:.2f} l {x + r - k:.2f} {y + h:.2f} {x:.2f} {y + h - r + k:.2f} {x:.2f} {y + h - r:.2f} c '
            f'{x:.2f} {y + r:.2f} l {x:.2f} {y + r - k:.2f} {x + r - k:.2f} {y:.2f} {x + r:.2f} {y:.2f} c h')


def content_box(image, threshold=246):
    """The box round everything drawn on a white picture: (left, top, right, bottom) in pixels, or None."""
    grey = image.convert('L').point(lambda v: 255 if v < threshold else 0)
    return grey.getbbox()


def union(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def padded(box, size, frac=0.04, aspect_min=0.9):
    """A box grown by a margin (a share of its larger side), kept inside the picture, and no narrower than aspect_min x its
    height (a tall thin part is not drawn as a sliver down the page)."""
    l, t, r, b = box
    m = frac * max(r - l, b - t)
    l, t, r, b = l - m, t - m, r + m, b + m
    if (r - l) < aspect_min * (b - t):
        grow = (aspect_min * (b - t) - (r - l)) / 2
        l, r = l - grow, r + grow
    W, H = size
    return (int(max(0, l)), int(max(0, t)), int(min(W, r)), int(min(H, b)))


class Guide:
    def __init__(self, kit, steps_file):
        self.kit = Path(kit)
        self.steps_file = steps_file
        self.data = json.load(open(self.kit / steps_file))
        self.meta = self.data['meta']
        self.views = self.data['views']
        folder = self.kit / 'pages' / steps_file.replace('.json', '')
        made = json.load(open(folder / 'pages.json')) if (folder / 'pages.json').exists() else None
        if made is None:
            raise SystemExit(f'no pictures in {folder}: run player/js/pages.js for {steps_file} first (see its first lines)')
        if made.get('model') != self.data.get('model') or made.get('views') != len(self.views) or made.get('run') != self.meta.get('run'):
            raise SystemExit(f'the pictures in {folder} were drawn from another version of {steps_file}: run player/js/pages.js again')
        self.pictures = {p['index']: folder / p['file'] for p in made['pictures']}
        missing = [v['name'] for i, v in enumerate(self.views) if v['kind'] in ('start', 'hover', 'done', 'end') and i not in self.pictures]
        if missing:
            raise SystemExit(f'pages.js drew no picture for {", ".join(missing[:5])}: run it again')
        self.title = self.meta.get('title', '')
        self.part = self.meta.get('part', '')
        self.logo = None
        for name in ('logo.png', 'logo.webp'):
            if (self.kit / name).exists():
                self.logo = Image.open(self.kit / name)
                break


def build(kit, out, steps_file='steps.json'):
    g = Guide(kit, steps_file)
    pdf = Pdf(f'{g.title} - {g.part}')
    logo = None
    if g.logo is not None:
        lw = 720
        small = g.logo.resize((lw, round(g.logo.height * lw / g.logo.width)), Image.LANCZOS)
        logo = pdf.jpeg(small, quality=92)
    pages = [v for v in g.views if v['kind'] in ('start', 'hover', 'done', 'end', 'card')]
    total = len(pages)
    # a step's two pictures (Step N, Step Nc) share one box, so the two pages line up
    boxes, pair = {}, {}
    for i, v in enumerate(g.views):
        if i in g.pictures:
            im = Image.open(g.pictures[i])
            boxes[i] = (content_box(im), im.size)
        m = re.fullmatch(r'Step (\d+)c?', v['name'])
        if m and v['kind'] in ('hover', 'done'):
            pair.setdefault(m.group(1), []).append(i)
    shared = {}
    for idx in pair.values():
        box = None
        for i in idx:
            box = union(box, boxes[i][0])
        for i in idx:
            shared[i] = box

    def chrome(c, number, heading=None):
        """The logo, the guide's name and a rule at the top; the copyright and the page number at the foot."""
        top = PAGE_H - MARGIN
        if logo:
            lh = 20.0
            c.image('Logo', logo[0], MARGIN, top - lh, lh * logo[1] / logo[2], lh)
        name = f'{g.title}  |  {g.part}'
        c.text(PAGE_W - MARGIN - width(name, 10, 'F2'), top - 14, name, 10, 'F2', GREY)
        c.line(MARGIN, top - 28, PAGE_W - MARGIN, top - 28, BLUE, 1.5)
        foot = MARGIN - 14
        if g.meta.get('copyright'):
            c.text(MARGIN, foot, g.meta['copyright'], 7.5, 'F1', GREY)
        label = f'Page {number} of {total}'
        c.text(PAGE_W - MARGIN - width(label, 9, 'F2'), foot, label, 9, 'F2', GREY)
        return top - 28 - 16                     # (where the page's own content starts)

    def instruction(c, y, badge, caption, caution):
        """The step's name in a blue badge, its instruction beside it, and its caution under them (as the player's boxes)."""
        size, bsize = 15.0, 14.0
        bw, bh = width(badge, bsize, 'F2') + 22, 26.0
        c.rect(MARGIN, y - bh, bw, bh, fill=BLUE, radius=8)
        c.text(MARGIN + 11, y - bh + 8.5, badge, bsize, 'F2', (255, 255, 255))
        x0 = MARGIN + bw + 14
        lines = wrap(caption or '', size, PAGE_W - MARGIN - x0) if caption else []
        ty = y - 18
        for ln in lines:
            c.text(x0, ty, ln, size, 'F1', INK)
            ty -= size * 1.3
        y = min(y - bh, ty + size * 1.3 - 6) - 10
        if caution:
            csize, label = 12.5, 'Caution: '
            inner = PAGE_W - 2 * MARGIN - 28
            first = wrap(label + caution, csize, inner)
            ch = len(first) * csize * 1.3 + 14
            c.rect(MARGIN, y - ch, PAGE_W - 2 * MARGIN, ch, fill=CAUTION_FILL, stroke=CAUTION_LINE, line=1.6, radius=8)
            cy = y - 7 - csize
            for k, ln in enumerate(first):
                if k == 0 and ln.startswith(label):
                    c.text(MARGIN + 14, cy, label.strip(), csize, 'F2', CAUTION_INK)
                    c.text(MARGIN + 14 + width(label, csize, 'F2'), cy, ln[len(label):], csize, 'F1', INK)
                else:
                    c.text(MARGIN + 14, cy, ln, csize, 'F1', INK)
                cy -= csize * 1.3
            y -= ch + 10
        return y

    def picture(c, i, y_top, y_bottom, name='Pic', box=None):
        im = Image.open(g.pictures[i]).convert('RGB')
        b = box if box is not None else boxes[i][0]
        if b is not None:
            im = im.crop(padded(b, im.size))
        if im.width > PICTURE_MAX_PX:
            im = im.resize((PICTURE_MAX_PX, round(im.height * PICTURE_MAX_PX / im.width)), Image.LANCZOS)
        oid, pw, ph = pdf.jpeg(im)
        avail_w, avail_h = PAGE_W - 2 * MARGIN, y_top - y_bottom
        s = min(avail_w / pw, avail_h / ph)
        w, h = pw * s, ph * s
        c.image(name, oid, (PAGE_W - w) / 2, y_bottom + (avail_h - h) / 2, w, h)

    def parts_page(c, y, v):
        """A Parts List page: its groups, each under a coloured band, its parts in a grid with their pictures and counts."""
        groups = v.get('parts') or []
        items = sum(len(gr['items']) for gr in groups)
        avail_w, avail_h = PAGE_W - 2 * MARGIN, y - (MARGIN + 4)
        band = 20.0
        # the fewest columns whose grid fits the page (cells a little flatter if need be), and never fewer than 6, so that a page
        # of a few parts (a Part guide's) draws them no larger than a full page does (the Full Build's pages have 6 - 8)
        for cols in range(6, 14):
            cell_w = avail_w / cols
            rows = sum(-(-len(gr['items']) // cols) for gr in groups)
            room = (avail_h - len(groups) * (band + 10)) / max(rows, 1)
            cell_h = min(cell_w * 0.9 + 26, room)
            if cell_h >= cell_w * 0.62 + 26:
                break
        for gr in groups:
            colour = tuple(int(gr.get('colour', '#dddddd')[k:k + 2], 16) for k in (1, 3, 5))
            halo = tuple(int(gr.get('halo', '#bbbbbb')[k:k + 2], 16) for k in (1, 3, 5))
            c.rect(MARGIN, y - band, avail_w, band, fill=colour, stroke=halo, line=1, radius=6)
            c.text(MARGIN + 10, y - band + 6, gr.get('title', ''), 11.5, 'F2', INK)
            y -= band + 6
            for k, it in enumerate(gr['items']):
                col, row = k % cols, k // cols
                x0, y0 = MARGIN + col * cell_w, y - (row + 1) * cell_h
                pic = it.get('picture')
                if pic and (g.kit / pic).exists():
                    im = Image.open(g.kit / pic)
                    side = 360
                    im.thumbnail((side, side), Image.LANCZOS)
                    oid, pw, ph = pdf.jpeg(im, quality=90)
                    box_w, box_h = cell_w - 12, cell_h - 36
                    s = min(box_w / pw, box_h / ph)
                    c.image(f'P{len(c.images)}', oid, x0 + (cell_w - pw * s) / 2, y0 + 26 + (box_h - ph * s) / 2, pw * s, ph * s)
                label = it['name'] + (f" ({it['tag']})" if it.get('tag') else '')
                lsize, q = 9.0, (f"  x{it['qty']}" if it.get('qty', 1) > 1 else '')
                lines = wrap(label + q, lsize, cell_w - 8, 'F2')[:2]
                ly = y0 + 14 + (len(lines) - 1) * 10
                for k2, ln in enumerate(lines):             # (the count, in blue, after the name)
                    x = x0 + (cell_w - width(ln, lsize, 'F2')) / 2
                    if q and k2 == len(lines) - 1 and ln.endswith(q.strip()):
                        name_part = ln[:len(ln) - len(q.strip())].rstrip()
                        c.text(x, ly, name_part, lsize, 'F2', INK)
                        c.text(x + width(name_part + '  ', lsize, 'F2'), ly, q.strip(), lsize, 'F2', BLUE)
                    else:
                        c.text(x, ly, ln, lsize, 'F2', INK)
                    ly -= 10
            y -= -(-len(gr['items']) // cols) * cell_h + 4

    number = 0
    for i, v in enumerate(g.views):
        if v['kind'] not in ('start', 'hover', 'done', 'end', 'card'):
            continue
        number += 1
        c = Canvas()
        if v['kind'] == 'start':                     # the title page: the logo large, the guide's name, the finished model
            top = PAGE_H - MARGIN
            if logo:
                lh = 44.0
                c.image('Logo', logo[0], MARGIN, top - lh, lh * logo[1] / logo[2], lh)
            c.text(MARGIN, MARGIN + 56, g.title, 30, 'F2', INK)
            c.text(MARGIN, MARGIN + 30, g.part, 19, 'F2', BLUE)
            c.text(MARGIN, MARGIN + 12, 'Step-by-step instructions', 11, 'F1', GREY)
            if g.meta.get('copyright'):
                c.text(MARGIN, MARGIN - 14, g.meta['copyright'], 7.5, 'F1', GREY)
            label = f'Page {number} of {total}'
            c.text(PAGE_W - MARGIN - width(label, 9, 'F2'), MARGIN - 14, label, 9, 'F2', GREY)
            picture(c, i, top - 56, MARGIN + 90)
            pdf.page(c.content(), c.images, bookmark='Title page')
            continue
        y = chrome(c, number)
        if v['kind'] == 'card' and v.get('parts'):
            c.text(MARGIN, y - 18, v['name'], 18, 'F2', INK)
            parts_page(c, y - 34, v)
            pdf.page(c.content(), c.images, bookmark=v['name'])
            continue
        if v['kind'] == 'card':                      # a note card: its first line as a heading, the rest as its list
            lines = (v.get('caption') or '').split('\n')
            y = instruction(c, y, v['name'], lines[0], v.get('caution'))
            ty = y - 20
            for para in lines[1:]:
                for ln in wrap(para, 14, PAGE_W - 2 * MARGIN - 40):
                    c.text(MARGIN + 20, ty, ln, 14, 'F1', INK)
                    ty -= 19
                ty -= 4
            pdf.page(c.content(), c.images, bookmark=v['name'])
            continue
        if v['kind'] == 'end':
            y = instruction(c, y, 'Completed View', None, None)
            picture(c, i, y, MARGIN + 4)
            pdf.page(c.content(), c.images, bookmark='Completed View')
            continue
        y = instruction(c, y, v['name'], v.get('caption'), v.get('caution'))
        picture(c, i, y, MARGIN + 4, box=shared.get(i))
        pdf.page(c.content(), c.images, bookmark=v['name'] if v['kind'] == 'hover' else None)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    size = pdf.save(out)
    print(f'{out}: {len(pdf.pages)} pages, {size / 1e6:.1f} MB')


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    kit = Path(sys.argv[1])
    kit = kit if kit.is_absolute() else ROOT / kit
    out = Path(sys.argv[2])
    out = out if out.is_absolute() else ROOT / out
    build(kit, out, sys.argv[3] if len(sys.argv) == 4 else 'steps.json')
