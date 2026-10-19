import re, sys, collections
path = sys.argv[1]
ents = {}
pat = re.compile(r"^#(\d+)\s*=\s*(PRODUCT_DEFINITION_FORMATION(?:_WITH_SPECIFIED_SOURCE)?|PRODUCT_DEFINITION|PRODUCT|NEXT_ASSEMBLY_USAGE_OCCURRENCE)\s*\((.*)\)\s*;\s*$")
buf = ''
with open(path, encoding='latin-1') as f:
    for line in f:
        if line.startswith('#'):
            buf = line.strip()
        else:
            buf += line.strip()
        if buf.endswith(';'):
            m = pat.match(buf)
            if m:
                ents[int(m.group(1))] = (m.group(2), m.group(3))
            buf = ''
prod = {}; pdf = {}; pd = {}
for k, (t, a) in ents.items():
    if t == 'PRODUCT':
        prod[k] = re.findall(r"'([^']*)'", a)[0]
    elif t.startswith('PRODUCT_DEFINITION_FORMATION'):
        ref = int(re.findall(r'#(\d+)', a)[0]); pdf[k] = ref
    elif t == 'PRODUCT_DEFINITION':
        ref = int(re.findall(r'#(\d+)', a)[0]); pd[k] = ref
name_of_pd = {k: prod[pdf[v]] for k, v in pd.items()}
children = collections.defaultdict(list); parents = set(); kids = set()
for k, (t, a) in ents.items():
    if t == 'NEXT_ASSEMBLY_USAGE_OCCURRENCE':
        s = re.findall(r"'([^']*)'", a); refs = [int(x) for x in re.findall(r'#(\d+)', a)]
        children[refs[0]].append((s[0], refs[1]))
        parents.add(refs[0]); kids.add(refs[1])
roots = [p for p in parents if p not in kids]
def walk(p, d):
    for nid, c in sorted(children[p], key=lambda x: int(re.sub(r'\D', '', x[0]) or 0)):
        n = len(children[c])
        print('  ' * d + f'{nid}: {name_of_pd[c]}' + (f'  [{n} children]' if n else ''))
        if d < int(sys.argv[2]):
            walk(c, d + 1)
for r in roots:
    print('ROOT', name_of_pd[r]); walk(r, 1)
