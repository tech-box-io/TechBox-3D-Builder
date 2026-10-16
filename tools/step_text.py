"""The wording of a guide's steps, out to a spreadsheet for editing and back again.

    python3 tools/step_text.py export "MRA Build Instructions Prototype" "share/<folder>/MRA step text.csv"
    python3 tools/step_text.py import "MRA Build Instructions Prototype" "edited.csv"

export writes one row per step (as the player's step list names it) and per note card, from the kit's steps.json: the
instruction, the caution, a column for comments, and the step's key, a short code (text_key in steps.json, from the guide's
own wording of the step) that import matches on, so that edits still find their step when steps have been added or moved
since, and a word replaced all through the sheet cannot break the match. Open it in Excel, Numbers or Google Sheets, change
the text in the Instruction and Caution columns (an empty Caution removes it; an empty Instruction keeps the current one; a
line break in a cell is a new line of a checklist) and save it as CSV (UTF-8 if asked; Excel's plain CSV is read too).

import compares each row with the guide as it is now and writes what changed (only the fields that changed) into the kit's
step-text.json, which the generator applies when guide.py is next run (it lists any edited step it can no longer find). It
prints what changed, the comments, and any row it could not use (with its text, so nothing written there is lost). Run
guide.py afterwards, then check the guide as usual.
"""
import csv
import io
import json
import re
import sys
from pathlib import Path

COLUMNS = ['Step', 'Type', 'Instruction', 'Caution', 'Comments for TechBox', 'Key (do not edit)']
NEEDED = {'instruction': 'Instruction', 'caution': 'Caution', 'key': 'Key (do not edit)'}


def steps_of(kit):
    """[(name, type, instruction, caution, key)] for each step and note card, in order."""
    views = json.loads((Path(kit) / 'steps.json').read_text(encoding='utf-8'))['views']
    seen, out = set(), []
    for v in views:
        if v['kind'] not in ('hover', 'done', 'card') or v.get('parts') or not v.get('caption'):
            continue
        if 'text_key' not in v:
            raise SystemExit('steps.json has no text keys: run guide.py first (with tools/stepgen.py of 16 Oct 2026 or later)')
        if v['text_key'] in seen:              # (a step's two views, Step N and Step Nc, share its key)
            continue
        seen.add(v['text_key'])
        name = v['name'][:-1] if v['kind'] == 'done' and v['name'].endswith('c') else v['name']
        kind = 'Note card' + (' (checklist: one item per line)' if '\n' in v['caption'] else '') if v['kind'] == 'card' else '3D step'
        out.append((name, kind, v['caption'], v.get('caution') or '', v['text_key']))
    return out


def export(kit, csv_path):
    rows = steps_of(kit)
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:   # (the byte-order mark makes Excel read it as UTF-8)
        w = csv.writer(f)
        w.writerow(COLUMNS)
        for name, kind, caption, caution, key in rows:
            w.writerow([name, kind, caption, caution, '', key])
    print(f'{len(rows)} steps written to {path}')


clean = lambda t: (t or '').replace('\r\n', '\n').replace('\r', '\n').strip()
norm = lambda h: re.sub(r'[^a-z]+', ' ', (h or '').lower()).strip()


def parse(text):
    """Rows of a CSV as {column: value}, with the columns import needs found by name (loosely: case, spaces and the like)."""
    first = text.split('\n', 1)[0].split('\r', 1)[0]
    delimiter = csv.Sniffer().sniff(first, delimiters=',;\t').delimiter if first else ','   # (some Excel settings save with ;)
    rows = list(csv.reader(io.StringIO(text, newline=''), delimiter=delimiter))
    if not rows:
        raise SystemExit('The file is empty.')
    header = [norm(h) for h in rows[0]]
    where = {}
    for want, label in NEEDED.items():
        hits = [i for i, h in enumerate(header) if h == norm(label) or h == want or (want == 'key' and h.startswith('key'))]
        if not hits:
            raise SystemExit(f'The file has no "{label}" column (its columns: {", ".join(rows[0])}). Nothing was imported: '
                             f'keep the column names as exported.')
        where[want] = hits[0]
    for want, label in (('step', 'Step'), ('comments', 'Comments for TechBox')):
        hits = [i for i, h in enumerate(header) if h == norm(label) or h.startswith(want[:-1])]
        where[want] = hits[0] if hits else None
    get = lambda r, k: r[where[k]] if where[k] is not None and where[k] < len(r) else ''
    return [{k: get(r, k) for k in ('step', 'instruction', 'caution', 'comments', 'key')} for r in rows[1:] if any(c.strip() for c in r)]


def read_rows(path, current):
    """The rows of an edited CSV, in whichever text encoding reads it best: UTF-8 if it is UTF-8 (what "CSV UTF-8" saves);
    otherwise Windows or Mac Excel's plain CSV, told apart by which leaves more rows reading as the guide does now."""
    raw = Path(path).read_bytes()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        raise SystemExit('This file is saved as UTF-16 ("Unicode Text"). Save it as "CSV UTF-8" (or plain CSV) and import that.')
    try:
        return parse(raw.decode('utf-8-sig')), 'utf-8'
    except UnicodeDecodeError:
        pass
    best = None
    for enc in ('cp1252', 'mac_roman'):
        try:
            rows = parse(raw.decode(enc))
        except UnicodeDecodeError:
            continue
        same = sum(1 for r in rows if r['key'].strip() in current and clean(r['instruction']) == current[r['key'].strip()][1])
        if best is None or same > best[2]:
            best = (rows, enc, same)
    if best is None:
        raise SystemExit('The file could not be read as text. Save it as "CSV UTF-8" and import that.')
    return best[0], best[1]


def import_(kit, csv_path):
    order = steps_of(kit)
    current = {key: (name, caption, caution) for name, _, caption, caution, key in order}
    out_path = Path(kit) / 'step-text.json'
    kept = {e['key']: e for e in (json.loads(out_path.read_text(encoding='utf-8')).get('steps', []) if out_path.exists() else [])}
    rows, encoding = read_rows(csv_path, current)
    changed, notes, comments, done = [], [], [], {}
    for r in rows:
        key, step = r['key'].strip(), r['step'].strip() or '(no step)'
        text, caution_text, comment = clean(r['instruction']), clean(r['caution']), clean(r['comments'])
        if key not in current:
            what = 'a row with no key (a new row?)' if not key else f'{step}: its key {key} is not a step of the guide as it is now'
            notes.append(f'left out, {what}' + (f'\n    instruction: {text}' if text else '') + (f'\n    caution: {caution_text}' if caution_text else '')
                         + (f'\n    comment: {comment}' if comment else ''))
            continue
        name, caption, caution = current[key]
        if comment:
            comments.append((name, comment))
        if key in done:
            if (text, caution_text) != done[key]:
                notes.append(f'{name} appears twice with different wording; the first is used')
            continue
        done[key] = (text, caution_text)
        entry = dict(kept.get(key, {}), key=key, step=name)
        edited = False
        if not text:
            notes.append(f'{name}: the instruction was left empty; the current one is kept')
        elif text != caption:
            entry['caption'] = text
            edited = True
        if caution_text != caution:
            entry.setdefault('was_caution', caution if 'caution' not in kept.get(key, {}) else kept[key].get('was_caution', ''))
            entry['caution'] = caution_text
            edited = True
        if edited:
            kept[key] = entry
            changed.append(name)
    rank = {key: k for k, (_, _, _, _, key) in enumerate(order)}
    entries = sorted(kept.values(), key=lambda e: rank.get(e['key'], len(rank)))
    out_path.write_text(json.dumps(dict(note='Edited wording of the steps (tools/step_text.py), only what was edited; applied when '
                                         'guide.py is run. key: the step\'s text_key in steps.json.', steps=entries),
                                    indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'read {len(rows)} rows ({encoding})')
    print(f'{len(changed)} step(s) changed: {", ".join(changed) or "none"}')
    for n in notes:
        print(n)
    for name, text in comments:
        print(f'comment on {name}: {text}')
    print(f'wrote {out_path} ({len(entries)} edited step(s) in all); now run guide.py and check the guide')


if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[1] not in ('export', 'import'):
        raise SystemExit(__doc__)
    (export if sys.argv[1] == 'export' else import_)(sys.argv[2], sys.argv[3])
