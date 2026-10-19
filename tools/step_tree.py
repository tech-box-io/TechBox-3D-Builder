"""Read a STEP file's assembly tree as text (no geometry): products, instances, placements, solids per product.

    python3 tools/step_tree.py <in.STEP> <out.json>

Streams the file so memory stays small (about 15 MB for a 58 MB STEP): a first look at a new kit's STEP before converting it,
to see whether it holds an assembly (instances placed) or loose parts, and which sub-assemblies point at files that are missing
(roots other than the assembly). "from" is each instance's placement in its parent (origin, z axis, x axis), as SolidWorks writes it.
"""
import sys, re, json, collections, math

src, out = sys.argv[1], sys.argv[2]
WANT = ('PRODUCT', 'PRODUCT_DEFINITION_FORMATION', 'PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE', 'PRODUCT_DEFINITION',
        'PRODUCT_DEFINITION_SHAPE', 'SHAPE_DEFINITION_REPRESENTATION', 'NEXT_ASSEMBLY_USAGE_OCCURRENCE',
        'CONTEXT_DEPENDENT_SHAPE_REPRESENTATION', 'ITEM_DEFINED_TRANSFORMATION', 'SHAPE_REPRESENTATION',
        'ADVANCED_BREP_SHAPE_REPRESENTATION', 'MANIFOLD_SURFACE_SHAPE_REPRESENTATION', 'SHAPE_REPRESENTATION_RELATIONSHIP',
        'MANIFOLD_SOLID_BREP', 'BREP_WITH_VOIDS', 'SHELL_BASED_SURFACE_MODEL', 'GEOMETRIC_CURVE_SET',
        'FACETED_BREP_SHAPE_REPRESENTATION', 'FACETED_BREP', 'MAPPED_ITEM', 'REPRESENTATION_MAP')


def records(path):
    buf = []
    with open(path, 'r', errors='replace') as f:
        for line in f:
            buf.append(line)
            if line.rstrip().endswith(';'):
                yield ''.join(buf); buf = []


ent = {}
need_ax = set()
rx = re.compile(r'^\s*#(\d+)\s*=\s*(.*);\s*$', re.S)
for rec in records(src):
    m = rx.match(rec)
    if not m: continue
    body = m.group(2).strip()
    if body.startswith('('):   # complex entity
        if 'REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION' in body:
            ent[int(m.group(1))] = ('RRWT', body)
        continue
    t = body.split('(', 1)[0].strip()
    if t in WANT:
        ent[int(m.group(1))] = (t, body)
refs = lambda s: [int(x) for x in re.findall(r'#(\d+)', s)]
for k, (t, b) in ent.items():
    if t == 'ITEM_DEFINED_TRANSFORMATION':
        need_ax.update(refs(b))
ax = {}
need_pt = set()
for rec in records(src):
    m = rx.match(rec)
    if not m: continue
    i = int(m.group(1))
    if i in need_ax:
        ax[i] = refs(m.group(2)); need_pt.update(ax[i])
pts = {}
for rec in records(src):
    m = rx.match(rec)
    if not m: continue
    i = int(m.group(1))
    if i in need_pt:
        nums = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', m.group(2).split('(', 2)[-1])]
        pts[i] = nums[-3:]


def strings(b):
    return re.findall(r"'((?:[^']|'')*)'", b)


prod = {k: strings(b)[1] if len(strings(b)) > 1 else strings(b)[0] for k, (t, b) in ent.items() if t == 'PRODUCT'}
pdf = {k: refs(b)[0] for k, (t, b) in ent.items() if t.startswith('PRODUCT_DEFINITION_FORMATION')}
pd = {k: refs(b)[0] for k, (t, b) in ent.items() if t == 'PRODUCT_DEFINITION'}
pd_name = {k: prod.get(pdf.get(v)) for k, v in pd.items()}
pds = {k: refs(b)[0] for k, (t, b) in ent.items() if t == 'PRODUCT_DEFINITION_SHAPE'}
sdr = {}
for k, (t, b) in ent.items():
    if t == 'SHAPE_DEFINITION_REPRESENTATION':
        a, r = refs(b)[:2]; sdr[pds.get(a)] = r   # product_definition -> shape rep
reps = {k: (t, refs(b)) for k, (t, b) in ent.items() if t.endswith('SHAPE_REPRESENTATION')}
srr = collections.defaultdict(list)
for k, (t, b) in ent.items():
    if t == 'SHAPE_REPRESENTATION_RELATIONSHIP':
        a, c = refs(b)[:2]; srr[a].append(c); srr[c].append(a)
solidtypes = {k: t for k, (t, b) in ent.items() if t in ('MANIFOLD_SOLID_BREP', 'BREP_WITH_VOIDS', 'SHELL_BASED_SURFACE_MODEL', 'FACETED_BREP', 'GEOMETRIC_CURVE_SET', 'MAPPED_ITEM')}
solidname = {k: (strings(b) or [''])[0] for k, (t, b) in ent.items() if k in solidtypes}


def bodies(pdk):
    r = sdr.get(pdk)
    seen, todo, out = set(), [r], []
    while todo:
        x = todo.pop()
        if x in seen or x is None: continue
        seen.add(x)
        if x in reps:
            for y in reps[x][1]:
                if y in solidtypes: out.append((solidtypes[y], solidname[y]))
            todo.extend(srr.get(x, []))
    return out


def frame(axk):
    p, z, xd = (ax[axk] + [None, None, None])[:3]
    o = pts.get(p, [0, 0, 0]); zz = pts.get(z, [0, 0, 1]) if z else [0, 0, 1]; xx = pts.get(xd, [1, 0, 0]) if xd else [1, 0, 0]
    return o, zz, xx


# NAUO -> transform via CDSR(RRWT, PDS(nauo))
pds_of = {v: k for k, v in pds.items()}
nauo = {}
for k, (t, b) in ent.items():
    if t == 'NEXT_ASSEMBLY_USAGE_OCCURRENCE':
        s = strings(b); r = refs(b)
        nauo[k] = dict(id=s[0], name=s[1], parent=pd_name.get(r[0]), parent_pd=r[0], child=pd_name.get(r[1]), child_pd=r[1])
for k, (t, b) in ent.items():
    if t == 'CONTEXT_DEPENDENT_SHAPE_REPRESENTATION':
        rr, p = refs(b)[:2]
        n = pds.get(p)
        if n in nauo and rr in ent:
            idt = [x for x in refs(ent[rr][1]) if x in ent and ent[x][0] == 'ITEM_DEFINED_TRANSFORMATION']
            if idt:
                a1, a2 = refs(ent[idt[0]][1])[:2]
                nauo[n]['from'] = frame(a1); nauo[n]['to'] = frame(a2)
roots = set(pd) - {v['child_pd'] for v in nauo.values()}
res = dict(file=src, products=len(prod), roots=[pd_name[r] for r in roots],
           instances=[dict(v, parent_pd=None, child_pd=None, bodies=len(bodies(v['child_pd']))) for v in nauo.values()],
           part_bodies={pd_name[k]: bodies(k) for k in pd})
json.dump(res, open(out, 'w'), indent=1)
print(src, 'products', len(prod), 'instances', len(nauo), 'roots', res['roots'])
