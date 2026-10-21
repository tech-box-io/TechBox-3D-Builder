import sys, json
sys.argv = sys.argv[:1]
sys.path.insert(0, '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad/s43_judge')
import mc_bends as M
SP = '/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/46c40992-e0fc-4f94-b08e-62c20da998a4/scratchpad'
files = {'now': 'steps.json', 'low': SP + '/s43_low/steps_low.json', 'high': SP + '/s43_high/steps-final.json'}
import contextlib, io
for key, f in files.items():
    M.BENDS.clear()
    with contextlib.redirect_stdout(io.StringIO()):
        M.main(['/Users/lee-johnson/Desktop/Claude_Cadasio/LAC Build Instructions', '--steps', f, '--moments', '199', 'Step 43c'])
    print(key)
    for w in ('buzzer red', 'buzzer black'):
        rows = [r for r in M.BENDS if r[1] == w]
        rows.sort(key=lambda r: -r[2])
        top = rows[0]
        over = sorted({r[0] for r in rows if r[2] > 30})
        span = (over[0], over[-1], len(over)) if over else None
        print(f'  {w}: sharpest {top[2]} deg/mm at t {top[0]}, {top[3]} mm from the hole, near {top[4]} (lead {top[5]} mm); moments over 30 deg/mm: {span}')
        # the worst few distinct moments
        seen = []
        for r in rows:
            if all(abs(r[0] - s) > 0.03 for s in seen):
                seen.append(r[0]); print(f'      t {r[0]}: {r[2]} deg/mm at {r[3]} mm, near {r[4]}')
            if len(seen) >= 4: break
