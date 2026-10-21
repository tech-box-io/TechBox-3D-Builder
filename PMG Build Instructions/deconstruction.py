"""Piano Memory Game (PMG), deconstruction: the finished game taken apart, down to H1. A guide of its own
(steps-deconstruction.json), made from the Full Build as guide.py last wrote it (run that first, and this again after any change to
it). It opens on the Full Build's title page, ends on what is left, H1, followed by the Full Build's parts list (as the MRA's), and
its card on the website is the Full Build's.

First draft (Lee, 21 Oct 2026: "take this PMG Full Build guide and create a Deconstruction Guide based on it. Same principles as you
used for the MRA. Remembering some things can be removed in groups (like the breadboard wires, four buttons, four H9 parts, etc.)"):
the Full Build in reverse (rulebook section 11), in the order of TechBox's own published PMG take-apart where it has one
(docs/research/guide_19075-piano-memory-game-deconstruction.md; this draft's reasons: docs/research/pmg/deconstruction/):
  1. the USB cable first (power off before anything is handled, as the MRA's and the RCC's);
  2. H14; then the dot matrix display, the 4-digit display and the I/O module lifted out of the case to the table, still wired, each
     the way the Full Build brought it in, reversed, its wires through the Full Build's own shapes: each display in two steps, as
     the Full Build had them (lifted off its hooks or out of its notches, then carried back over the case), each by the camera of
     the Full Build's step it undoes; the I/O module in one, by a fade, as the Full Build's Step 42 (Lee: "Let's keep the fade on
     42");
  3. the case in reverse: H13, H12, H11, H10, the four keys at once, H8; turned over: H7, then the four push buttons out of their
     pockets at once, to the table, still wired;
  4. the electronics, taken apart on their own (as the RCC's controller and I/O module): each device pulled off the ends of its wires
     (the dot matrix display, the 4-digit display, the four push buttons at once), then all 21 breadboard wires off the I/O module at
     once, then the Nano Board out of it (as TechBox's published take-apart, which unplugs the module end last);
  5. back to the case, still upside down: H6, H5; the right way up: H4, H3, H2. H1 is left.
No counterpart for the Full Build's preparation (peeling the wires off the ribbon) or its cards."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
from stepgen import Guide, _shifted, _unit, apply_pose, compose, via  # noqa: E402

# ---------------------------------------------------------------- parts (as guide.py names them; the CAD's instance ids)
H1, H2, H3, H4, H5, H6, H7, H8 = 'NAUO63', 'NAUO65', 'NAUO66', 'NAUO73', 'NAUO67', 'NAUO60', 'NAUO68', 'NAUO61'
KEYS = ['NAUO72', 'NAUO71', 'NAUO70', 'NAUO69']                     # the four H9 piano keys
H10, H11, H12, H13, H14 = 'NAUO64', 'NAUO62', 'NAUO77', 'NAUO75', 'NAUO74'
MODULE, NANO = 'NAUO78', 'NANO'
BUTTONS = ['NAUO76', 'NAUO83', 'NAUO84', 'NAUO85']                 # push buttons: black, yellow, white, blue
COLOURS = ['black', 'yellow', 'white', 'blue']
DISPLAY, MATRIX = 'NAUO79', 'NAUO81'
USB_B, USB_A = 'NAUO282', 'NAUO283'
HOVER_NAMES = {b: f'{c.title()} Push Button' for b, c in zip(BUTTONS, COLOURS)}

# ---------------------------------------------------------------- the Full Build, as guide.py last wrote it
FULL = json.loads((HERE / 'steps.json').read_text(encoding='utf-8'))
VIEW = {v['name']: v for v in FULL['views']}
ROUTES = FULL['routes']
END = VIEW['Completed View']
ENDS = {w: ROUTES[n] for w, n in END['wires'].items()}                # each lead: a = the cap on the device's pin, b = the module's
JUMPERS = [w for w in ENDS if w != 'usb cable']                        # the 21 breadboard wires
leads_of = lambda part: [w for w in JUMPERS if END['carry'].get(ENDS[w]['a'], {}).get('by') == part]   # (the leads whose device end is on it)
caps_on = lambda part: [ENDS[w]['a'] for w in leads_of(part)]
MODULE_CAPS = [ENDS[w]['b'] for w in JUMPERS]
DEVICE_CAPS = [ENDS[w]['a'] for w in JUMPERS]


def camera_of(step):
    """The camera of a Full Build step, for a step of ours that undoes it by hand (the generator reuses it by itself otherwise)."""
    c = VIEW[step]['camera']
    return dict(view_dir=c['dir'], frame=(c['target'], c['radius']))


def lifted_back(lowered, part):
    """The Full Build's step that lowered a device into its seat (from where it held it), walked back: wire_via and wires for
    lift(), the way itself being the generator's (the Full Build's way, reversed). Its leads pass back through the Full Build's own
    shapes, a stage with each beat."""
    down, down_c = VIEW[lowered], VIEW[lowered + 'c']
    stages = {w: [ROUTES[n] for n in down_c['wire_via'][w][::-1]] for w in leads_of(part)}
    assert all(len(r) + 1 == len(down['path']) - 1 for r in stages.values()), (lowered, {w: len(r) for w, r in stages.items()})   # (a stage a beat)
    return stages, {w: ROUTES[down['wires'][w]] for w in leads_of(part)}


def carried_back(carried, part):
    """The Full Build's step that carried a device to where it held it (riding on H1, a beat a stretch), walked back: (path,
    wire_via, wires) for lift(). H1 is in its seat, so the poses of the ride are where the device is."""
    ride, ride_c = VIEW[carried], VIEW[carried + 'c']
    c = ride_c['carry'][part]
    assert c['by'] == H1, carried
    stops = [*c.get('via', [])[::-1], ride['carry'][part]['pose']]
    stages = {w: [ROUTES[n] for n in ride_c['wire_via'][w][::-1]] for w in leads_of(part)}
    assert all(len(r) + 1 == len(stops) for r in stages.values()), (carried, len(stops), {w: len(r) for w, r in stages.items()})
    return stops, stages, {w: ROUTES[ride['wires'][w]] for w in leads_of(part)}


g = Guide(HERE, title='Piano Memory Game (PMG)', part='Deconstruction', names=dict(FULL['names']), steps_file='steps-deconstruction.json',
          source='pmg-guide.glb', hover_names=HOVER_NAMES, hero_azimuth=315,
          copyright_line='© TechBox. A division of TARIS Industries, LLC. All Rights Reserved.')
g.take_apart(parts_list_at_end=True)                                # (the Full Build's parts list, after the Completed View, as the MRA's)


def where(i):
    """Where a part is now (on what it rides, if it rides)."""
    if i in g.riding:
        by, rel = g.riding[i]
        return compose(where(by), rel, g._pivot(i))
    return g.resting.get(i)


def centre(i, pose):
    return apply_pose(pose, g._pivot(i))


def off_the_pins(caps):
    """The way caps come off their pins, in assembly space: from each cap pushed on to where the Full Build held it off its pin just
    before (the last stop of its way in, Steps 4 - 25: the caps rode on the module, lying on the bench where it lies again now)."""
    out = []
    for cap in caps:
        done = next(v for v in FULL['views'] if v['kind'] == 'done' and ((v.get('carry') or {}).get(cap) or {}).get('via'))
        c, bench = done['carry'][cap], done['offsets'][MODULE]
        out.append(centre(cap, compose(bench, c['via'][-1], g._pivot(cap))) - centre(cap, compose(bench, c['pose'], g._pivot(cap))))
    return _unit(np.mean([_unit(v) for v in out], axis=0))


# ---------------------------------------------------------------- the arrows, as TechBox's published PMG take-apart has them
# (Lee, 21 Oct 2026: "the arrow sizes and sequencing need refinement. Examine the Cadasio"): (length, shaft width) in mm, measured from
# its data (docs/research/pmg/deconstruction/published_arrows.txt); a part that comes off in stages shows an arrow for each, in turn
# (arrow_style then=), as its auto-advancing frames do: H14, H12 and H11 (toward H1, then up: Lee), H10, H7, H6, H5.
PUBLISHED = dict(usb=(42.2, 8.2), h14=(29.0, 5.2), matrix=(62.2, 8.5), display=(29.1, 5.5), module=(83.6, 2.1),
                 h13=(74.4, 6.1), h12=(37.6, 4.5), h12_up=(43.1, 5.3), h11=(46.1, 6.2), h11_up=(57.2, 6.1), h10=(52.4, 6.7),
                 h10_out=(116.1, 6.9), keys=(109.5, 11.8), h8=(71.7, 6.9), h7=(45.2, 8.0), h6=(34.5, 4.8), h5=(34.8, 3.8),
                 buttons=(44.7, 9.7), matrix_off=(45.1, 6.7), display_off=(30.6, 6.1), matrix_wires=(65.9, 7.3),
                 button_wires=(50.9, 7.0), display_wires=(43.3, 7.0), nano=(28.5, 3.0), h4=(105.0, 7.6), h1=(84.0, 7.8))
size = lambda key, **more: dict(dims=PUBLISHED[key], **more)


# ================================================================ POWER (Lee's principle, as the MRA's and RCC's: the cable first)
PLUG_OUT = compose(where(MODULE), VIEW['Step 26']['carry'][USB_B]['pose'], g._pivot(USB_B))   # (the way the Full Build pushed it in, reversed)
g.remove('Unplug the USB cable from the Nano Board at the top of the I/O module, and lift its other end off the table.', [USB_B, USB_A],
         units=[[USB_B]], arrow_style={USB_B: size('usb')},        # (one arrow, on the plug that is pulled: the RCC's and MRA's)
         paths={USB_B: [PLUG_OUT], USB_A: [[0.0, 30.0, 0.0]]},
         view_dir=VIEW['Step 42']['camera']['dir'], frame=([630.0, 945.0, 1280.0], 82.0))   # (Step 42's, from behind, closer: the cable shows whole)

# ================================================================ H14, THEN THE DISPLAYS AND THE I/O MODULE OUT OF THE CASE, STILL WIRED
g.remove('Swing the top of H14 out from over H11 and H12, then lift its two bottom tabs off the top edge of the dot matrix display.', [H14],
         arrow_style={H14: size('h14', stage=0, then=[size('h14', stage=1)])},   # (its top swung out, then its tabs lifted off the dot matrix
         eye=[dict(id=H14, anchor=[575.0, 1002.0, 1290.5])])          # display's edge. The swing comes towards this camera: an eye on its wood
         #                                                 instead, as before. Ours leaves forward, the Full Build's way reversed;
         #                                                 the published H14 leaves backward, over the stand. The lift arrow as
         #                                                 big as the published first ones: its 64 mm one left this close view)
# (each in two steps, as the Full Build brought it in: lowered from where it was held (Steps 47, 45), by that step's camera, then
# carried back to the table (46, 44), by that one's, which sees the way behind the case; one camera could not show both)
stages, last = lifted_back('Step 47', MATRIX)
g.lift('Tilt the top of the dot matrix display forward, then lift it up off the hooks of H11 and H12 and hold it in front of them. '
       'Leave its wires connected.',
       [MATRIX], wire_via=stages, wires=last,                     # (the Full Build's way, reversed, by its camera)
       arrow_style={MATRIX: size('matrix', at=[533.0, 974.0, 1338.0])})   # (from its far end: from its middle it rose across the 4-digit display)
path, stages, last = carried_back('Step 46', MATRIX)
g.lift('Lift the dot matrix display back over the case and set it on the table behind it.', [MATRIX], path=path, wire_via=stages,
       wires=last, arrow_style={MATRIX: size('matrix', stage=0)}, **camera_of('Step 46'))   # (the arrow up and over, the first stage)
stages, last = lifted_back('Step 45', DISPLAY)
g.lift('Tilt the 4-digit display forward off H13, then lift it out of the notches in H11 and H12 and hold it over the gap between '
       'them. Leave its wires connected.', [DISPLAY],
       wire_via=stages, wires=last, arrow_style={DISPLAY: size('display')})
path, stages, last = carried_back('Step 44', DISPLAY)
g.lift("Carry the 4-digit display back over the top of the case and down behind it, out under the dot matrix display's wires, to "
       'the table.', [DISPLAY], path=path, wire_via=stages, wires=last, arrow_style={DISPLAY: size('display', stage=0)}, **camera_of('Step 44'))
MODULE_BENCH = VIEW['Step 42']['carry'][MODULE]['pose']             # (on the table behind the case: on H1, which is in its seat)
g.lift('Lift the I/O module straight up off the back of H4, its edges out of the notches in the tabs of H10, and hold it over H4.',
       [MODULE], wires={w: ROUTES[VIEW['Step 43']['wires'][w]] for w in JUMPERS},   # (the Full Build's Step 43 reversed, by its camera)
       arrow_style={MODULE: size('module')})
g.lift('Set the I/O module down on the table behind the case, with everything still plugged into it.', [MODULE],
       path=[MODULE_BENCH], reappear=True,                          # (a fade, as the Full Build's Step 42 brought it: Lee kept that fade)
       wires={w: ROUTES[VIEW['Step 41c']['wires'][w]] for w in JUMPERS},   # (as the wires lay before Step 42)
       arrows=[], eye=[MODULE], **camera_of('Step 42'))             # (an eye on it, by the Full Build's Step 42's camera, as there)

# ================================================================ THE CASE, TOP DOWN
g.remove('Slide H13 up from between H11 and H12, bringing its hooks out of H4.', [H13], arrow_style={H13: size('h13')})
# (H12 and H11: toward H1 out of H4, then up out of H10, an arrow for each in turn: Lee, 21 Oct 2026, as published)
g.remove('Slide H12 forward until it comes out of H4, then lift it out of the slot in H10.', [H12],
         arrow_style={H12: size('h12', stage=0, at=[526.0, 960.0, 1268.5], then=[size('h12_up', stage=1, at=[537.4, 965.0, 1268.5])])})   # (up from its face, slid toward
         #                                                 H1: from its top, it seemed to lift the parts lying behind, as published)
g.remove('Slide H11 forward until it comes out of H4, then lift it out of the slot in H10.', [H11],
         arrow_style={H11: size('h11', stage=0, at=[526.0, 960.0, 1312.5], then=[size('h11_up', stage=1, at=[538.3, 965.0, 1312.5])])})
# (each from the plate's front edge, as published: from its middle they lay over H10 and the keys)
g.remove('Lift the front of H10 off H2 and H3, then unhook its rear tabs from the slots in H4.', [H10],
         arrow_style={H10: size('h10', stage=0, at=[519.0, 936.0, 1290.5], then=[size('h10_out', stage=1)])})   # (its front up, at its front
         #                                                 edge, as published, then out over the keys)
g.remove('Slide all four piano keys (H9) out of the slots in H4 and back through H8 to the front.', KEYS,
         units=[KEYS], arrow_style={KEYS[0]: size('keys')})        # (in one step: Lee; one arrow for the four, as published)
g.remove('Pull H8 up out of the slots in H5.', [H8], arrow_style={H8: size('h8')})
g.remove('Turn the case over. Swing H7 up out of the notches in H3, then unhook its tabs from the windows in H2.', [H7],
         arrow_style={H7: size('h7', stage=0, then=[size('h7', stage=1)])})   # (swung up, then out of the windows: the second as long as the
         # first, not the published 116 mm, since ours comes 5 mm out of H2's windows where the published plate slides 140 mm along itself)
g.lift('Press the four push buttons out of their pockets in H6 and set them on the table beside the I/O module. Leave their wires '
       'connected.', BUTTONS, arrows=[], eye=[BUTTONS[1]],         # (in one step: Lee; each the way the Full Build pressed it in, reversed; an
       #                                                              eye, as published: an arrow hid a button)
       ride_on=MODULE,                                              # (lying beside it from then on, each its own: pulled off its wires on its own way)
       wires={w: ROUTES[VIEW['Step 32']['wires'][w]] for b in BUTTONS for w in leads_of(b)})   # (as they lay on the bench)

# ================================================================ THE ELECTRONICS, ON THEIR OWN (the case hidden)
HARNESS = [MODULE, NANO, *BUTTONS, DISPLAY, MATRIX]
BENCH = [0.8, 0.55, 0.24]                                           # (from beyond the I/O module: the dot matrix display left, the 4-digit display right)
BENCH_VIEW = dict(view_dir=BENCH, frame=([667.0, 918.0, 1350.0], 130.0))   # (the whole layout, for the two displays)
CLOSER = dict(view_dir=BENCH, frame=([665.0, 925.0, 1290.0], 96.0))  # (the rest, once the dot matrix display is off: one camera for them,
#                                                                       room above for the buttons' arrow)
for device, caption in ((MATRIX, 'Pull the dot matrix display off the ends of its five wires.'),
                        (DISPLAY, 'Pull the 4-digit display off the ends of its four wires.')):
    shown = [i for i in HARNESS + DEVICE_CAPS + MODULE_CAPS if i in g.placed]   # (with the ends of the wires pulled off before: they
    away = -off_the_pins(caps_on(device))                                      #  ride on nothing once let go)
    ends = np.mean([centre(c, where(c)) for c in caps_on(device)], axis=0)   # (the ends of its wires, on its pins)
    g.remove(caption, [device], let_go=caps_on(device), alone=shown, path=[_shifted(where(device), away * 30.0)],
             arrow_style={device: size('matrix_off', at=(ends + away * 10.0 + [0.0, 18.0, 0.0]).round(2).tolist())} if device == MATRIX
             else {device: size('display_off')},                    # (the dot matrix display's from its pins, above the board: at its far
             #                                                        end, its arrow left the view in a narrow window)
             **(BENCH_VIEW if device == MATRIX else CLOSER))
g.remove('Pull the four push buttons off the ends of their wires.', BUTTONS, let_go=[c for b in BUTTONS for c in caps_on(b)],
         alone=[i for i in HARNESS + DEVICE_CAPS + MODULE_CAPS if i in g.placed], units=[BUTTONS], keep_camera=True,
         arrow_style={BUTTONS[0]: size('buttons')},                 # (one arrow for the four, as published)
         paths={b: [_shifted(where(b), -off_the_pins(caps_on(b)) * 30.0)] for b in BUTTONS})
UP = off_the_pins(MODULE_CAPS)                                      # (the wires come off the module's pins together, as one)
BUNDLES = [('matrix_wires', leads_of(MATRIX)), ('button_wires', [w for b in BUTTONS for w in leads_of(b)]), ('display_wires', leads_of(DISPLAY))]
caps_of = lambda leads: [c for w in leads for c in (ENDS[w]['b'], ENDS[w]['a'])]   # (each lead's caps, the module's first)
over = lambda leads: (np.mean([centre(ENDS[w]['a'], where(ENDS[w]['a'])) for w in leads], axis=0) + UP * 6.0).round(2).tolist()   # (over its
#                                                                       free ends, as published: over the module's pins the three bunched up)
g.remove('Unplug all 21 breadboard wires from the I/O module.', MODULE_CAPS + DEVICE_CAPS, alone=[MODULE, NANO] + MODULE_CAPS + DEVICE_CAPS,
         paths={c: [_shifted(where(c), UP * 25.0)] for c in MODULE_CAPS + DEVICE_CAPS}, keep_camera=True,
         units=[caps_of(leads) for _, leads in BUNDLES],           # (an arrow on each bundle, as published)
         arrow_style={caps_of(leads)[0]: size(key, at=over(leads)) for key, leads in BUNDLES})
NANO_OUT = compose(where(MODULE), VIEW['Step 1']['carry'][NANO]['pose'], g._pivot(NANO))   # (where the Full Build held it over the module)
g.remove('Lift the Nano Board out of the I/O module.', [NANO], alone=[MODULE, NANO], path=[NANO_OUT], arrow_style={NANO: size('nano')},
         **camera_of('Step 1'))
g.put_away([MODULE])                                                # (what is left of the electronics)

# ================================================================ THE REST OF THE CASE (H1 is left)
g.remove('With the case still upside down, swing H6 up out of the notches in H3, then unhook its tabs from the windows in H2.', [H6],
         arrow_style={H6: size('h6', stage=0, then=[size('h6', stage=1)])})
g.remove('Swing H5 up out of the notches in H3, then unhook its tabs from the windows in H2.', [H5],
         arrow_style={H5: size('h5', stage=0, then=[size('h5', stage=1)])})
g.remove('Turn the case the right way up. Pull H4 off the back tabs of H2 and H3.', [H4], arrow_style={H4: size('h4')})
g.remove('Pull H3 off the end of H1.', [H3], arrow_style={H3: size('h1')})   # (as big as the published H1's: the case's last plates)
g.remove('Pull the front tabs of H2 out of the slots at the other end of H1.', [H2], arrow_style={H2: size('h1')})

g.build()
