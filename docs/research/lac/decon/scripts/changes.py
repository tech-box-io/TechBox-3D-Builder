"""Per view of a steps.json: what changed from the view before (visible in/out, offsets, carry, wire routes). Read-only."""
import json, sys
s = json.load(open(sys.argv[1]))
names = s['names']
V = s['views']
def short(x, n=140):
    t = json.dumps(x)
    return t if len(t) <= n else t[:n] + '...'
prev = None
for i, v in enumerate(V):
    if v.get('kind') == 'card':
        print(f"[{i}] {v['name']} (card)"); continue
    out = []
    if prev is not None:
        a, b = set(prev.get('visible', [])), set(v.get('visible', []))
        if b - a: out.append(f"  +visible {sorted(b - a)}")
        if a - b: out.append(f"  -visible {sorted(a - b)}")
        po, no = prev.get('offsets', {}), v.get('offsets', {})
        for k in sorted(set(po) | set(no)):
            if po.get(k) != no.get(k):
                out.append(f"  offset {k} ({names.get(k, k)}): {short(po.get(k))} -> {short(no.get(k))}")
        pc, nc = prev.get('carry', {}), v.get('carry', {})
        for k in sorted(set(pc) | set(nc)):
            if pc.get(k) != nc.get(k):
                out.append(f"  carry {k} ({names.get(k, k)}): {short(pc.get(k), 100)} -> {short(nc.get(k), 100)}")
        pw, nw = prev.get('wires', {}), v.get('wires', {})
        for k in sorted(set(pw) | set(nw)):
            if pw.get(k) != nw.get(k):
                out.append(f"  wire '{k}': {pw.get(k)} -> {nw.get(k)}")
    print(f"[{i}] {v['name']} moving={v.get('moving')}")
    print('\n'.join(out))
    prev = v
