"""The wording of a guide's steps, out to a spreadsheet for editing and back again.

    python3 tools/step_text.py export "MRA Build Instructions Prototype" "share/<folder>/MRA step text.csv"
    python3 tools/step_text.py import "MRA Build Instructions Prototype" "edited.csv"
    python3 tools/step_text.py export "RCC Build Instructions" "<csv>" steps-deconstruction.json   # a guide of its own in the kit
    python3 tools/step_text.py export "RCC Build Instructions" "<csv>" steps-part-2.json           # a Part guide's wording
    python3 tools/step_text.py import "RCC Build Instructions" "<csv>" steps-part-2.json --only-this-part   # (or --everywhere)

A Part guide is cut from the Full Build (stepgen chapter()), so its wording is the Full Build's unless the Part has its own
(in_part() in guide.py, or edits imported --only-this-part, kept in step-text-<part>.json). Importing a Part's sheet asks which
is meant: --only-this-part (the Full Build and the other guides keep their wording) or --everywhere (the Full Build's wording
changes, and with it every guide that has the step; a step that has wording of its own in the Part keeps that, and is listed).
A guide of its own (a deconstruction guide) has its own wording file, step-text-<name>.json.

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


def text_file(steps_file):
    """Where a guide's edited wording is kept: step-text.json for the Full Build (its Parts share its steps and so its wording),
    step-text-<name>.json for a guide of its own (steps-<name>.json, a deconstruction guide). (As stepgen.step_text_file.)"""
    return 'step-text.json' if steps_file == 'steps.json' else 'step-text-' + steps_file[len('steps-'):-len('.json')] + '.json'


def steps_of(kit, steps_file='steps.json'):
    """[(name, type, instruction, caution, key)] for each step and note card, in order."""
    views = json.loads((Path(kit) / steps_file).read_text(encoding='utf-8'))['views']
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


def export(kit, csv_path, steps_file='steps.json'):
    rows = steps_of(kit, steps_file)
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


def part_files(kit):
    """The steps files of the kit's Part guides (chapters.json)."""
    path = Path(kit) / 'chapters.json'
    return [c['file'] for c in json.loads(path.read_text(encoding='utf-8')).get('chapters', [])] if path.exists() else []


def import_(kit, csv_path, steps_file='steps.json', scope=None):
    order = steps_of(kit, steps_file)
    current = {key: (name, caption, caution) for name, _, caption, caution, key in order}   # (as the sheet's guide shows them)
    shared = None                                # (a Part's sheet imported --everywhere: the Full Build's wording is what changes)
    if steps_file in part_files(kit):
        if scope not in ('--only-this-part', '--everywhere'):
            raise SystemExit(f'{steps_file} is a Part guide: say whether the edits are for this Part only (--only-this-part) or for '
                             f'the Full Build and every guide that has those steps (--everywhere). Nothing was imported.')
        if scope == '--everywhere':
            shared = {key: (name, caption, caution) for name, _, caption, caution, key in steps_of(kit, 'steps.json')}
            steps_file_out = 'steps.json'
        else:
            steps_file_out = steps_file
    elif scope:
        raise SystemExit(f'{scope}: only for a Part guide\'s sheet ({", ".join(part_files(kit)) or "this kit has no Parts"}). Nothing was imported.')
    else:
        steps_file_out = steps_file
    out_path = Path(kit) / text_file(steps_file_out)
    kept = {e['key']: e for e in (json.loads(out_path.read_text(encoding='utf-8')).get('steps', []) if out_path.exists() else [])}
    rows, encoding = read_rows(csv_path, current)
    if steps_file == 'steps.json' and part_files(kit):   # (a Part's sheet given as the Full Build's: its step names give it away)
        pairs = {(r['key'].strip(), r['step'].strip()) for r in rows if r['key'].strip()}
        if pairs and any(current.get(k, (None,))[0] != n for k, n in pairs):
            for f in part_files(kit):
                names = {key: name for name, _, _, _, key in steps_of(kit, f)}
                if all(names.get(k) == n for k, n in pairs):
                    raise SystemExit(f'This is the sheet of {f} (its step names are that Part\'s): import it with {f} and --only-this-part '
                                     f'or --everywhere. Nothing was imported.')
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
        base = shared.get(key, current[key]) if shared is not None else current[key]   # (the wording the edit replaces)
        if shared is not None and ((text and text != caption and base[1] != caption) or (caution_text != caution and base[2] != caution)):
            notes.append(f'{name}: has wording of its own in this Part; the Full Build\'s wording was changed, and this Part keeps its own '
                         f'(import it --only-this-part as well to change it here too)')
        if not text:
            notes.append(f'{name}: the instruction was left empty; the current one is kept')
        elif text != caption:
            entry['caption'] = text
            edited = True
        if caution_text != caution:
            prior = kept.get(key, {})                # (an earlier edit that is in use keeps the caution it was made against)
            entry['was_caution'] = prior.get('was_caution', '') if 'caution' in prior and (prior['caution'] or '') == base[2] else base[2]
            entry['caution'] = caution_text
            edited = True
        if edited:
            kept[key] = entry
            changed.append(name)
    if shared is not None:                       # (named as the Full Build's step list names them)
        for e in kept.values():
            if e['key'] in shared:
                e['step'] = shared[e['key']][0]
    rank = {key: k for k, (_, _, _, _, key) in enumerate(order)}
    entries = sorted(kept.values(), key=lambda e: rank.get(e['key'], len(rank)))
    out_path.write_text(json.dumps(dict(note='Edited wording of the steps (tools/step_text.py), only what was edited; applied when '
                                         'guide.py is run. key: the step\'s text_key in steps.json.'
                                         + (' This Part\'s own wording, over the Full Build\'s.' if steps_file_out in part_files(kit) else ''), steps=entries),
                                    indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'read {len(rows)} rows ({encoding})')
    print(f'{len(changed)} step(s) changed: {", ".join(changed) or "none"}')
    for n in notes:
        print(n)
    for name, text in comments:
        print(f'comment on {name}: {text}')
    print(f'wrote {out_path} ({len(entries)} edited step(s) in all); now run guide.py and check the guide')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    if len(args) not in (3, 4) or args[0] not in ('export', 'import') or len(flags) > 1 or (flags and args[0] != 'import'):
        raise SystemExit(__doc__)
    if args[0] == 'export':
        export(*args[1:])                        # (a 4th argument: a Part's or a guide of its own's steps file, steps-<name>.json)
    else:
        import_(args[1], args[2], args[3] if len(args) > 3 else 'steps.json', flags[0] if flags else None)
