import sys, re, collections
def counts(f):
    c = collections.Counter()
    for line in open(f):
        m = re.match(r'(Step \d+c?)\s', line)
        if m and ('mm' in line):
            kind = 'cap' if ' cap ' in line else ('pair' if ' and ' in line else 'part')
            c[(m.group(1), kind)] += 1
    return c
a, b = counts(sys.argv[1]), counts(sys.argv[2])
steps = sorted({k[0] for k in a} | {k[0] for k in b}, key=lambda s: (int(re.findall(r'\d+', s)[0]), s))
for s in steps:
    ra = {k: a[(s, k)] for k in ('part', 'pair', 'cap')}; rb = {k: b[(s, k)] for k in ('part', 'pair', 'cap')}
    if ra != rb:
        print(f'{s:9s} before {ra}  now {rb}')
print('totals', sum(a.values()), '->', sum(b.values()))
