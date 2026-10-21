"""Paste each design's code into a copy of the CURRENT guide.py (text only, as Lee's session would), then run the patched buzzer
section with guide.py's own setup lines (AST-selected; no Guide, no model) and compare Step 43's path and routes, the lying routes
(Steps 33c - 42c) and the seated routes (Step 43c on) with the designer's checked steps copy.

    python paste_check.py low|high
"""
import ast, json, re, sys
from pathlib import Path
import numpy as np

ROOT = Path('/Users/lee-johnson/Desktop/Claude_Cadasio')
KIT = ROOT / 'LAC Build Instructions'
R2 = ROOT / 'docs/research/lac/scripts/round2'
SCR = Path(__file__).resolve().parent
SP = SCR.parent
sys.path.insert(0, str(ROOT / 'tools'))

which = sys.argv[1]
src = (KIT / 'guide.py').read_text()
lines = src.split('\n')


def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    raise SystemExit(f'not found: {prefix!r}')


if which == 'low':
    md = (ROOT / 'docs/research/lac/round2/step43_low.md').read_text()
    sec3 = md[md.index('## 3. Paste-ready code'):md.index('## 4. Checks')]
    blocks = re.findall(r'```python\n(.*?)```', sec3, re.S)
    a, b, c, d = blocks
    # (a) BUZZER_LIFT line replaced, BUZZER_LIFT_WAY deleted
    i = find('BUZZER_LIFT = tidy(compose(')
    lines[i:i + 1] = a.rstrip('\n').split('\n')
    i = find('BUZZER_LIFT_WAY = {')
    assert lines[i + 1].startswith('                   \'black\'')
    del lines[i:i + 2]
    # (b) BUZZER_SEAT_WAY['red'] replaced (black unchanged)
    new_red = re.search(r"BUZZER_SEAT_WAY = \{'red': (\[\[.*?\]\]),", b).group(1)
    i = find('BUZZER_SEAT_WAY = {')
    old = re.search(r"BUZZER_SEAT_WAY = \{'red': (\[\[.*?\]\]),", lines[i]).group(1)
    lines[i] = lines[i].replace(old, new_red)
    # (c) added after buzzer_clamped
    i = find('def buzzer_clamped(')
    j = i + 1
    while not lines[j].startswith('    return W.route('):
        j += 1
    lines[j + 1:j + 1] = ['', ''] + c.rstrip('\n').split('\n')
    # (d) the Step 43 call (and its comment line) replaced
    i = find("g.place('Lower the buzzer in between")
    assert lines[i - 1].startswith('# (lifted, carried over and lowered')
    j = i
    while 'CASE_CAMERA)' not in lines[j]:
        j += 1
    lines[i - 1:j + 1] = d.rstrip('\n').split('\n')
else:
    patch = (R2 / 'step43_high/guide_patch.txt').read_text().rstrip('\n').split('\n')
    p43 = (R2 / 'step43_high/guide_patch_step43.txt').read_text().rstrip('\n').split('\n')
    i = find("# Each lead's way to its hole, the buzzer lying (Steps 33 - 42) and lifted 60 mm")
    j = find('def buzzer_clamped(')
    while not lines[j].startswith('    return W.route('):
        j += 1
    lines[i:j + 1] = patch
    i = find("g.place('Lower the buzzer in between")
    assert lines[i - 1].startswith('# (lifted, carried over and lowered')
    j = i
    while 'CASE_CAMERA)' not in lines[j]:
        j += 1
    lines[i - 1:j + 1] = p43

patched = '\n'.join(lines)
(SCR / f'guide_{which}.py').write_text(patched)
tree = ast.parse(patched)            # (the whole patched guide.py must still parse)

b0 = find('# ================================================================ THE BUZZER (begin)')
b1 = find('# ================================================================ THE BUZZER (end)')
SETUP_NAMES = {'paths', 'HOLES', 'CAPS', 'LINES', 'LCD_RAIL_SHIFT', 'ZERO', 'LEAD_COLOURS', 'WIRE_R', 'HOVER_MM', 'UP', 'POSES', 'BUZZER_LEADS'}
SETUP_FUNCS = {'unit', 'tidy', 'wire_at', 'cap_mid', 'into_hole', 'posed_line'}
body = []
for node in tree.body:
    names = set()
    if isinstance(node, ast.Assign):
        for t in node.targets:
            names |= {n.id for n in ast.walk(t) if isinstance(n, ast.Name)}
    if isinstance(node, ast.FunctionDef) and node.name in SETUP_FUNCS:
        body.append(node)
    elif isinstance(node, ast.Assign) and (names & SETUP_NAMES or 'BUZZER' in names):
        body.append(node)
    elif isinstance(node, ast.For) and getattr(node.target, 'id', '') == '_cap':
        body.append(node)
    elif b0 < node.lineno - 1 < b1 and isinstance(node, (ast.Assign, ast.FunctionDef)):
        body.append(node)
ns = {}
exec("import numpy as np\nimport wires as W\nfrom stepgen import Guide, apply_pose, compose, relative_pose, turned, unapply_pose, via\n"
     f"HERE = __import__('pathlib').Path({str(KIT)!r})\n", ns)
exec(compile(ast.Module(body=body, type_ignores=[]), 'guide_patched', 'exec'), ns)
call = next(n.value for n in tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
            and getattr(n.value.func, 'attr', '') == 'place' and isinstance(n.value.args[0], ast.Constant)
            and str(n.value.args[0].value).startswith('Lower the buzzer'))
kw = {k.arg: k.value for k in call.keywords}
ev = lambda e: eval(compile(ast.Expression(e), 'kw', 'eval'), ns)
path, wd = ev(kw['path']), ev(kw['wires_done'])
from stepgen import pose_out

copy_file = {'low': SP / 's43_low/steps_low.json', 'high': SP / 's43_high/steps-final.json'}[which]
S = json.load(open(copy_file))
NOW = json.load(open(KIT / 'steps.json'))
V = {v['name']: v for v in S['views']}
v43 = V['Step 43c']


def cmp(a, b):
    pa, pb = np.asarray(a['pts']), np.asarray(b['pts'])
    d = float(np.abs(pa - pb).max()) if pa.shape == pb.shape else f'shape {pa.shape} vs {pb.shape}'
    ka = {k: v for k, v in a.items() if k != 'pts'}
    kb = {k: v for k, v in b.items() if k != 'pts'}
    return d, ka == kb, ka, kb


print(which, 'patched guide.py parses; selected', len(body), 'statements')
print('path pasted == path in steps copy:', [pose_out(p) for p in path] == v43['path'], ' stops in copy:', v43.get('stops'))
print('beats:', len(path) - 1, ' routes per wire:', {w: len(r) for w, r in wd.items()})
for w, rs in wd.items():
    nos = v43.get('wire_via', {}).get(w, []) + [v43['wires'][w]]
    for k, (r, no) in enumerate(zip(rs, nos)):
        d, same_keys, ka, kb = cmp(r, S['routes'][no])
        print(f'  {w} shape {k + 1}: max point diff {d}, keys same {same_keys}', '' if same_keys else f'{ka} vs {kb}')
# lying routes (Steps 33c - 42c) as pasted vs the CURRENT steps.json
VN = {v['name']: v for v in NOW['views']}
for c, cap, _, e, _, _ in ns['BUZZER_LEADS']:
    ly = ns['buzzer_plugged'](c, cap, e, ns['BUZZER_LYING'], ns['BUZZER_WAY'][c])
    d, sk, ka, kb = cmp(ly, NOW['routes'][VN['Step 42c']['wires'][f'buzzer {c}']])
    print(f'  lying {c} vs current steps.json Step 42c: max diff {d}, keys same {sk}')
# seated route in every view from Step 43c on, in the steps copy
names = [v['name'] for v in S['views']]
i43 = names.index('Step 43c')
for w in wd:
    fin = v43['wires'][w]
    bad = [v['name'] for v in S['views'][i43:] if w in (v.get('wires') or {}) and v['wires'][w] != fin]
    print(f'  {w}: views after 43c not on the final route: {bad[:6]}{"..." if len(bad) > 6 else ""}')
# what differs between the copy and the current steps.json (views)
diff = []
for va, vb in zip(NOW['views'], S['views']):
    for k in set(va) | set(vb):
        if k in ('wires', 'wire_via'):
            ra = {w: NOW['routes'][n] if isinstance(n, int) else [NOW['routes'][x] for x in n] for w, n in (va.get(k) or {}).items()}
            rb = {w: S['routes'][n] if isinstance(n, int) else [S['routes'][x] for x in n] for w, n in (vb.get(k) or {}).items()}
            ch = [w for w in set(ra) | set(rb) if ra.get(w) != rb.get(w)]
            if ch:
                diff.append((va['name'], k, sorted(ch)))
        elif va.get(k) != vb.get(k):
            diff.append((va['name'], k, None))
print('views/keys that differ from the current steps.json:')
from collections import defaultdict
agg = defaultdict(list)
for n, k, ch in diff:
    agg[(k, tuple(ch) if ch else None)].append(n)
for (k, ch), ns_ in agg.items():
    print(f'  {k} {list(ch) if ch else ""}: {ns_[0]} .. {ns_[-1]} ({len(ns_)} views)')
