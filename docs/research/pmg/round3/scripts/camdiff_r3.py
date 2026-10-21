import json, sys
old = json.load(open(sys.argv[1]))['views']
new = json.load(open('/Users/lee-johnson/Desktop/Claude_Cadasio/PMG Build Instructions/steps.json'))['views']
N = {v['name']: v for v in new}
cam = lambda v: (tuple(round(x, 4) for x in v['camera']['dir']), tuple(round(x, 2) for x in v['camera']['target']), round(v['camera']['radius'], 2), v['camera'].get('flip'))
changed = [v['name'] for v in old if v['name'] in N and cam(v) != cam(N[v['name']])]
print(len(old), len(new), 'views; cameras changed:', changed, '; names differ:', sorted({v['name'] for v in old} ^ set(N)))
