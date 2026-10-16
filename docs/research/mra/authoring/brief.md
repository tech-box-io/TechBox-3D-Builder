# Brief for writing guide steps (MRA full build)

You are extending TechBox's 3D build guide for the Mini Robot Arm. The base and controller are written and checked. You add one
more section in the SAME STYLE, test it, and report. Read this whole brief first.

## Where you work

- Sandbox kit folder: `/private/tmp/claude-501/-Users-lee-johnson-Desktop-Claude-Cadasio/06aa2268-0605-4ce1-8b0c-854218069941/scratchpad/kit_full/`
  (called SANDBOX below). It holds `guide.py` (a copy of the real guide; edit THIS file only) and links to the kit's CAD, materials,
  player and wire paths. Generated files (`steps.json`, `parts.json`, `model.glb`) land in the sandbox.
- Project: `/Users/lee-johnson/Desktop/Claude_Cadasio` (PROJECT). Do NOT edit anything under PROJECT: not `tools/`, not the kit folder,
  not `docs/`. If the generator or player cannot do something you need, do the nearest thing it can do and say exactly what was
  missing in your report. (One exception: you may add stills or notes under `PROJECT/docs/research/mra/authoring/`.)
- Generate with: `PROJECT/.venv.nosync/bin/python SANDBOX/guide.py` (about 20 s; run ONE at a time: this Mac has 16 GB and crashed
  earlier today when memory ran out). It prints one line per step: `auto` = direction found from the CAD, `hand` = set by hand;
  `lines=N` = red lead lines; `WARNING` lines need fixing.
- See the result at `http://localhost:8793/player.html` (already being served) with the built-in browser pane (tools named
  `mcp__Claude_Browser__*`; load them with ToolSearch; use the tab that is already open, do not open others). In the page run once
  `(0, eval)(await fetch('js/runthrough.js', {cache: 'no-store'}).then(r => r.text())); _dev.freeze();` and then
  `_dev.show('Step 31')` (the hover view), `_dev.show('Step 31c')` (seated), `_dev.show('Step 31c', 0.5)` (half-way through the
  animation), `_dev.look('NAUO58', [1, 0.6, 0.4], 2)` (camera on one part), and `_runthrough()` (checks every view; must report
  0 problems when you finish). Reload the page after every regeneration (add `?v=<number>` to the address). A screenshot can lag one
  frame: take a throwaway one at scale 0.1 first. Keep screenshots small (scale 0.5) and few (about 30 in all): look at the hover and
  seated view of every step that has a hand-set path, a sub-assembly, a wire or a close-up, and spot-check the rest.

## What to read (in this order)

1. `PROJECT/CLAUDE.md` is already in your context. `PROJECT/docs/cadasio-patterns.md` sections 1 to 7, 9, 10 and 13: the house rules.
2. `SANDBOX/guide.py`, all of it: the worked example. Then the top of `PROJECT/tools/stepgen.py` (module docstring; `turned`, `via`,
   `compose`; the `Guide` methods `carry`, `rest_at`, `wire`, `note`, `place`, `seat` and their docstrings) and `PROJECT/tools/wires.py`
   (`route`, `rounded`, `along`, `join`, `straight`, `ribbon`, `plug`, `loose_lead`, `plugged_lead`, `cut_mark`).
3. The research for this kit in `PROJECT/docs/research/mra/`: the video report(s) for your section (the merged `video_<name>.md`,
   and the `_seg` files where the merge is thin), `cad_arm_claw.md` (+ `.json`: screws, servos, horns, contact graph, a tested
   geometric order, what a builder must get right), `cad_codes_base.md` (the table of ENGRAVED codes: the CAD names are wrong for most
   arm and claw parts), `cad_wire_paths.md` and `cad_pins.md` (leads, slots they pass through, shield rows), and section 3 of
   `cadasio_mra_project.md` (names). `SANDBOX/wire-paths.json` holds every wire centre line, the chains and the plugs as data.

## How steps are written

- One part or one action per step. `g.place(caption, move=[ids])` adds a part: the generator finds a free straight direction by
  collision test, the hover distance, tab-to-slot lead lines, a label and the camera. Give `direction=`, `hover=`, `path=`,
  `against=`, `lines_to=`, `lines_at=` only where the automatic result is wrong (the log and the picture tell you).
- A sub-assembly built in the hand: `g.place(..., show=[first part], move=[second], staged=True)`, more `staged=True` steps, then
  `g.seat(caption, [all its ids])` brings it to the model (it takes `direction=`, `hover=`, `path=`, `lines_at=`, `lines=False` like place()).
  Only one sub-assembly can be in hand at a time: seat it before starting the next. A sub-assembly is shown in its CAD orientation.
- A motion that is not a straight push: `path=[pose, ..., [0, 0, 0]]` with `turned(axis, degrees, at, t)` poses, `via(pose)` for
  pass-through points. Poses are relative to the seated (CAD) position. Check a hand-set path for collisions yourself (transform
  the trimesh of the moving parts with `stepgen.apply_pose` or `_matrix`, and test against the neighbours as the horn search did:
  see how `Model`, `blocked` and `apply_pose` are used in `tools/stepgen.py`).
- Screws thread into the wood, so the CAD cannot give their direction: `direction=[...]` pointing from the hole towards where the
  screw hovers (back along its axis, towards its head), `hover=g.cfg['hover_fastener']`, `axial=True` (or `axial='each'` for several).
- Lee's rule for a set of three or more identical fasteners into one joint: the FIRST is shown close up
  (`focus=[screw], focus_pad=2.0`), then ONE step where the rest appear hovering and go in together (`axial='each'`). One or two
  screws: each its own ordinary step (a close-up is fine when the screw would otherwise be too small to see).
- A screw that is a pivot (an axle the parts turn on; `cad_arm_claw.md` section 3 lists which) is put in like any other; say in the
  caption if the video shows it left a little loose. Do not invent tightening advice the sources do not give.
- Wires: a motor's lead is three wires (`lead_wires(name)`), drawn along routes, with its plug riding on the loose end
  (`g.carry([plug], by=motor, pose=...)`) until a step plugs it in (`move=[plug]`, `wires_done=...`, a destination label such as
  `labels=[dict(text='6', anchor=<pin row>, id=MODULE)]`). Follow the base motor's lead in `guide.py` exactly: loose first
  (`W.loose_lead`), moved into its slot in a wire-only step (`wires_done=`, `ride=`, an `eye=` on the slot), plugged in last
  (`W.plugged_lead` along the chain's `middle`). Brown is G, red is V, orange is S; `W.plug(info, g_towards=...)` needs the direction
  from the G contact to the S contact. A loose lead should be short (50 to 80 mm) and must not pass through wood or other parts.
- Names: wood parts by ENGRAVED code; motors "Shoulder Motor" (NAUO66), "Elbow Motor" (NAUO58), "Claw Motor" (NAUO72); screws
  "6mm Hex Screw", "10mm Hex Screw", "16mm Hex Screw"; "Servo Extension Wire". A horn that arrives on its motor goes in `PART_OF`;
  plugs and other hover-only names go in `NAMES` and `UNLISTED`. Add new ids, names and helpers near the top of `guide.py`, next to the
  existing ones, and your steps between the markers for your section. Do not change the existing base and controller steps.
- Captions: short imperatives in TechBox's wording, as in the existing steps ("Add R3.", "Insert B3 into B2.", "Then place B5 and B6
  onto B3."). Use the engraved codes. A step whose motion or order you could not confirm from the video or the CAD gets
  `review='...'` saying what to check (it shows as a yellow note for the reviewer).
- Things the model cannot show (centring a servo, testing motion, tidying wires) are `g.note(caption)` cards, only where the video
  or the build notes call for them.

## What good looks like

- The order follows the build video wherever it is clear; where the video and the CAD's tested order disagree, follow the video if
  the CAD allows it (no part passing through another), and say so in your report.
- Every step's hover view shows the new part clear of the model with lead lines to where it goes; the seated view matches the CAD.
- No `WARNING` in the log; every `hand` step is one you meant; `_runthrough()` reports 0 problems.
- Your report lists: the steps you added (caption, ids, auto or hand), every place you departed from the video or guessed, anything
  the generator or player could not do, and questions for Lee.
