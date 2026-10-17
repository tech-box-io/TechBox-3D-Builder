# TechBox build instructions

An in-house replacement for Cadasio: step-by-step 3D build guides for TechBox kits, generated from the
CAD and a short guide script, played in the browser. The guides are maintained by asking Claude for
changes in chat; there is no visual editor.

## House rules come first

Before authoring or changing any guide, read `docs/cadasio-patterns.md`. It is the rulebook extracted
from TechBox's 20 published Cadasio guides (one part per step, one wire per step, `Step N` / `Step Nc`
pairs, lead lines tab-to-slot, camera fixed inside a pair, and so on) and it applies to construction and
deconstruction guides alike. If a kit needs to break a rule, say which one and why. When Lee states a new
convention, add it to the rulebook. The evidence behind each rule is in
`docs/cadasio-patterns-evidence.md`; the working reports are in `docs/research/`.

## How a guide is made

    CAD export (GLB from STEP)  +  guide.py (+ wire-paths.json)  +  materials.json (+ colour atlas)
              |                       |                                  |
              |        tools/stepgen.py, tools/wires.py          tools/build_model.py
              |                       |                                  |
              +---------------> steps.json                          model.glb  ---> played by player/ (one player, every kit)
                                parts.json  --------------------------------------> player/parts.html -> parts/*.png

    tools/publish.py:  kit content + player/  ->  releases/<guide>/r<N>/ (frozen, this computer only)  ->  site/<guide>/ (the website)

- `guide.py` (one per kit folder) lists the build in order: which part goes on next, the caption, and any
  motion that has to be set by hand. Everything else is worked out from the CAD by `tools/stepgen.py`:
  insertion direction (collision test), hover distance, lead-line anchors (where the parts grip each
  other), label anchors, and the camera for each step.
- `materials.json` gives colours and how much detail to keep. `tools/build_model.py` turns the raw CAD
  export into the small, coloured `model.glb`, keeping only the parts the guide shows. A mesh whose rule
  names no colour takes its colours, solid by solid, from the kit's colour atlas (for the MRA:
  `colour-atlas-mra.json`, read from TechBox's own Cadasio project for the kit); a rule that names a colour
  is a TechBox decision that overrides it.
- The player is `player/` (`player.html`, `parts.html`, `js/`, `vendor/`): the only copy, shared by every kit. A kit folder holds
  only its content. `tools/serve.py` serves a kit with the player as if it were in the kit folder, so a kit's addresses are as
  before (`http://localhost:8791/player.html`). `player.html` plays `steps.json`; `parts.html` renders one picture per part for
  the parts list. Never copy the player into a kit: a player change is a change for every kit, so after one, run the check
  below on every kit. A published guide keeps the player it was published with until it is published again.

What a guide can do beyond "part hovers, part goes in" (described at the top of `tools/stepgen.py` and in the
docstrings of `Guide.place` and `Guide.seat`):

- **Poses.** A part's position in a view is a pose relative to where it sits when built: `[x, y, z]`, or
  `turned(axis, degrees, at, t)` for a part that is tilted or spun on its way in. A hand-set `path=[...]` may
  have several poses; `via(pose)` marks one the part passes through without pausing.
- **Wires.** Flexible leads are not CAD parts. Each is a centre line (a "route", see `tools/wires.py`) that the
  player draws as a tube, tied to the part at each end so it follows them, and it can change route from one
  step to the next (`wires=`, `wires_done=`); going back from such a step plays it backwards. The CAD's own cable bodies are left out of the model
  (`"omit": true` in `materials.json`); their centre lines are in the kit's `wire-paths.json`.
- **Riding parts.** A plug on a loose lead, or the cap of a jumper wire, rides with another part
  (`g.carry(...)`) until a step moves it to its seat. `g.rest_at(...)` parks a part beside the model.
  `paths={id: path}` gives each moving part its own way in (the two ends of a jumper wire).
- **Cameras.** Chosen from the four diagonal views; the generator prefers one from which the engraved code
  of each wood part coming in can be read (`engraved-codes.json`). `look_from=` picks the diagonal nearest a
  direction, `view_dir=` gives an exact direction, `focus=` / `frame=` punch in. `flip=True` shows the step with
  the model turned over (work done with the kit upside down): the player turns the model, not the camera, so
  the light and the controls stay upright; a run of such steps shares one turn, so the model stays put between them.
  `Guide(start_view=, end_view=)` give the title page and the Completed View their own camera (one taken from a
  screenshot, with the narrowest window it suits, `min_aspect`), can leave parts off them (`hide=`) and can show parts
  turned or moved there (`poses={id: pose}`: the RCC's controller turned round beside the car; the Completed View then cuts in
  rather than gliding from the last step).
- **Note cards** take line breaks: a caption with `\n` in it is shown as a list, ranged left (a checklist).
- **A bench set-up before the build.** `g.put_away(ids)` takes parts off the screen; a later step brings them
  back as new parts (the MRA's electronics test, before the base). Declare their riding and resting for the
  build after it. The view after a put-away starts afresh: nothing glides over from the view before it.
- **On a step, too:** `caution=` (an orange Caution box under the caption, read aloud with it; not a Review note),
  `arrows=` (fat red arrows instead of lead lines, for a slide with nothing to line up), `inset=` (a framed close-up on
  Step Nc with some parts left out, e.g. gears under a cover, with a leader to the spot), `wiggle=True` (a jiggle on the
  spot, played as the step opens and as it completes: a check that parts move freely), `single=True` (one view, no Step Nc).
  Per-part `paths=` may use `via()`. A wire that changes route through as many routes as the moving part has stops keeps
  pace with it stop by stop (the MRA's extension wire onto row 10).
  For a plug carried to its row in stages, draw each stage as the plugged lead cut short with the plug on its end (the MRA's
  `cut_lead`), its turn split about evenly between stages: two routes twisted differently at the same length pinch the lead
  as it blends between them (Steps 98 and 99).
- **Parts list.** `Guide(parts_list=fn)` puts Parts List pages after the title page, built from the parts the guide
  shows (so a guide for one part of the build lists that part's parts); `fn` groups them (the MRA's is in its guide.py).
  `g.part_picture(name, add=, poses=, wires=)` pictures a part whole (both ends of an extension wire and the wire between);
  `g.part_picture(name, piece=, file=)` gives one piece of a kind its own second picture, for pieces that look different (the
  RCC's car Nano Board, blue dot against the controller's white): parts.html saves it under `file` made into a file name as
  part names are (`parts/Nano-Board-car.png`), the parts.json entry lists it under `also`, and the guide's `parts_list` shows it
  where that piece is listed (rows stay one per kind; the main picture is always of a piece without its own);
  `g.list_part()` lists a kit part whose CAD pieces are hover-only (the breadboard wires). `Guide(review_notes=False)` hides
  the Review notes and their switch once a guide is past review. `Guide(hover_names={id: name})` names a part more exactly
  on hover and click than the parts list does (the MRA's Left / Right Joystick, "Joystick x2" in the list). In the step list
  a Parts List page is pictured as the page itself, small (its part pictures load once the list is opened).
- **Step text, edited outside.** `tools/step_text.py export` writes every step's instruction and caution to a CSV for an
  editor, keyed by each step's `text_key` (a short code from the guide's own wording and which step with that wording it
  is, so edits find their step after renumbering and a Replace All cannot break them); `import` checks the columns, reads
  UTF-8 or Excel's plain CSV, and writes only what changed into the kit's `step-text.json`, which the generator applies on
  the next run. The wording in guide.py stays as written: rewording a step there gives it a new key (the generator warns of
  edits it no longer finds), and a caution changed in guide.py after it was edited outside is kept, with a warning.
- **Printing on a part.** `materials.json` `"decals"` names a JSON file of flat pictures to lay on parts (the I/O module's
  silkscreen, written by the kit's `silkscreen.py`); `build_model.py` puts them in the model and the player draws them.

## Commands

Run from this folder. The Python environment is `.venv.nosync` (the Desktop is iCloud-synced; the
`.nosync` suffix keeps it out of the sync). Create it with
`python3 -m venv .venv.nosync && .venv.nosync/bin/pip install -r tools/requirements.txt`.

    .venv.nosync/bin/python "MRA Build Instructions Prototype/guide.py"            # after editing guide.py
    .venv.nosync/bin/python tools/build_model.py "MRA Build Instructions Prototype" # after editing materials.json or replacing the CAD
    .venv.nosync/bin/python "MRA Build Instructions Prototype/silkscreen.py"       # after editing the module's printing (then build_model)
    /usr/bin/python3 tools/serve.py "MRA Build Instructions Prototype" 8791         # local server; then open http://localhost:8791/player.html

`guide.py` rebuilds the model by itself when the set of parts shown changes. Opening
`http://localhost:8791/parts.html` re-renders the part pictures and saves them into `parts/`.

    python3 tools/step_text.py export "MRA Build Instructions Prototype" "share/<folder>/MRA step text.csv"   # step text for editing
    python3 tools/step_text.py import "MRA Build Instructions Prototype" "<edited>.csv"                       # then run guide.py

To send a guide to someone, pack it into one HTML file that opens by double-click with no server and no internet
(player, model, steps, logo and the part pictures for the parts list's large view all inside), and put the part pictures
beside it as well, for the LMS:

    .venv.nosync/bin/python tools/bundle.py "MRA Build Instructions Prototype" "share/<name>/MRA Full Build.html"

`share/` holds the checkpoints made this way (a folder and its zip, with a read-me and a parts-list page). A checkpoint
is a snapshot: make a new one after changing the guide. (`bundle.py` takes a steps file as a third argument, for a guide other
than the kit's `steps.json`.) Checkpoints are for review; learners get the website (below).

## Publishing: the website

Learners open the guides on TechBox's website, `https://models.tech-box.io` (a Render static site; TechBox's own LMS,
`https://edu.tech-box.io`, embeds a guide by iframe). One fixed address per guide: `https://models.tech-box.io/<guide>/`, the
names in `guides.json` (Lee's: `mini-robot-arm-full-build`, `mini-robot-arm-part-1` ..., `remote-controlled-car-full-build`,
`remote-controlled-car-part-1` ..., `remote-controlled-car-deconstruction`). An address in the LMS must never change.
The site's own pages, made by `tools/site_pages.py` after every publish (header and footer copied from the LMS, Lee
16 Oct 2026): the landing page `/` shows each kit that has a guide on the site (its Full Build's picture), `/kits/<kit>/`
shows that kit's guides (Full Build, Part 1 ..., Deconstruction), and a guide's card opens the guide. Nothing is offered for
download (the 2D PDF guides will be, later). Each guide's card picture is its Completed View: in the player, after the guide is
final, `await _dev.card()` saves it into the kit's `cards/<steps file>.webp` (cut to the model with a margin, 1440 x 900), and
publish copies it into the release (it warns when a guide has none, or one older than the model).

    python3 tools/publish.py <guide> --note "what changed"   # freeze the guide as its next release and put it in site/<guide>/
    python3 tools/check_site.py                              # site/ is exactly the releases on record (Render runs this before each deploy)
    /usr/bin/python3 tools/serve.py site                     # the site as Render serves it: http://localhost:8797/<guide>/
    python3 tools/publish.py <guide> --restore r3            # put an earlier release back (a roll-back); --take-down removes the guide
    python3 tools/publish.py --list                          # which release each guide has on the website
    python3 tools/site_pages.py                              # the landing and kit pages again (publish does this by itself)
    /usr/bin/python3 tools/serve.py releases                 # every earlier release, on this computer only: http://localhost:8798/<guide>/r<N>/

- **Only the current release is on the website** (Lee, 16 Oct 2026). `site/` holds one copy per guide; every release ever
  published is kept in `releases/<guide>/r<N>/` with its record (`release.json`: when, Lee's reason, the source's git commit,
  every file's checksum) and `releases/<guide>/history.json`, in git but never uploaded (Render serves `site/` only).
  `check_site.py` requires each `site/<guide>/` to be byte for byte the release its `steps.json` names, so only `publish.py`
  can change what goes out.
- **What goes out** is only what a learner's browser needs: the player (as `index.html`), the steps (without Review notes or
  `text_key`), the kit's `model.glb` (without the CAD's own body and file names; the part ids stay, as the player needs them),
  the logo and the part pictures the Parts List shows. Never the CAD, `guide.py`, `materials.json`, wire paths, `decals.json`
  (the printing travels inside the model as shapes) or research.
- **What the model gives away** (told to Lee, 16 Oct 2026): a 3D guide has to send the part shapes to the browser; anyone who
  opens a guide can save the model. Only the STEP and editable CAD stay private. So the laser-cut wood is **roughened** in every
  model (Lee, 16 Oct 2026): `materials.json` `"roughen_mm": 0.1` on the wood rule makes `build_model.py` move each vertex of a
  plate's outline 0.05 - 0.1 mm within the plate's plane (the same for both faces, so the plate stays a straight-sided slab;
  deterministic), so a traced cutting file comes out slightly wrong. Invisible in the guide. It is a deterrent, not a guarantee:
  at 0.1 mm a slot's width changes by 0.04 - 0.14 mm, within laser and plywood tolerances, so most traced joints would still
  fit (an independent review, 16 Oct 2026; told to Lee). Making traced joints reliably fail would take 0.3 - 0.5 mm per slot or
  tab, which can show as gaps or parts passing into each other in close-ups: Lee's call. The collision tests and cameras use the
  exact CAD, not the model, so they are unaffected. Checkpoints made before 16 Oct 2026 15:49 (share/) carry the exact geometry.
- **The order:** commit the checked sources; publish; look at it (`serve.py site`, and `_runthrough()` on `/<guide>/`); run
  `check_site.py`; commit `site/`, `releases/`, `render.yaml` and `guides.json`. Then, **only on Lee's word**, put it live:
  `git push origin main:live` (Render
  deploys the branch `live`; `main` can be pushed at any time as a backup). If Lee declines, `--restore` the previous release
  (or `--take-down`) before committing. Push outside lesson hours: a learner who has a guide open during a deploy could get a
  mix of old and new files.
- **Caching:** every file is served `Cache-Control: no-cache` (render.yaml): browsers re-check each file when a guide opens
  (an unchanged file costs a short "not modified" answer), so a release reaches the next learner who opens the guide and there
  is never a cache to clear. Render needs no routine upkeep: deploys follow the push, the HTTPS certificate renews itself.
- **On Render:** the GitHub repository must be private, with Render's GitHub App limited to it. Do not use Render's Rollback
  button (it switches automatic deploys off): roll back with `--restore` and push. A header deleted from render.yaml must also
  be deleted in Render's dashboard. **A new LMS address** (a staging host, a new domain) goes into `guides.json`
  `embed_origins` (lower case, `https://`, no path), then `python3 tools/site_pages.py` (it rewrites render.yaml's rules and
  `assets/frame-guard.js`), commit, push: no guide needs publishing again.
- **Before the first LMS link goes out:** the custom domain verified, then `renderSubdomainPolicy: disabled` in render.yaml (the
  onrender.com address closed); render.yaml's curl loop answers the same over a few minutes; a real embed from the LMS plays on an
  iPad (Safari) and a Chromebook; a frame from any other site stays blank. Locally, `serve.py site` sends render.yaml's headers,
  so a frame from `http://127.0.0.1:<port>` is refused by the header just as a foreign site would be.
- **The embed** (one guide per LMS page, the address with its closing slash, no `?step=`):
  `<iframe src="https://models.tech-box.io/<guide>/" title="<guide title>" allow="fullscreen" allowfullscreen loading="lazy"
  style="width:100%;height:min(80vh,720px);min-height:420px;border:0"></iframe>`. If the LMS ever adds a `sandbox`, it needs
  `allow-scripts allow-same-origin`. Only the LMS may frame a guide, and nothing may frame the site's own pages, so an embed
  can only ever show the one guide it names: render.yaml sends `X-Frame-Options: DENY` on every path and, for each guide, a
  `Content-Security-Policy: frame-ancestors <embed_origins>` on `/<guide>` and `/<guide>/*` (written by site_pages.py from
  `guides.json` between its "guide framing" lines; browsers obey the CSP over X-Frame-Options). Never put a CSP rule on `/*`:
  when two rules with the same header name match one path, Render sends one at random (check_site.py checks all this). As a
  second guard, each guide's index.html (added by publish.py) and each site page (site_pages.py) shows only a link when framed
  by anything else. The Render Blueprint must be linked to the branch `live`, so header changes ship with the guides.
- A new guide gets an entry in `guides.json` (its kit, its steps file, its card label, and `script` if it is not made by
  `guide.py`) before its first publish; a new kit an entry under `kits` (name, code, folder). The site's own files:
  `site/index.html`, `kits/<kit>/index.html`, `404.html` (made by site_pages.py), `robots.txt`, `assets/` (the style sheet, made
  by site_pages.py, and the TechBox wordmark copied from the LMS).

## Part guides (chapters)

Not built yet (planned: `docs/research/production_architecture.md` section 4, with Lee's decisions of 16 Oct 2026 below).
- A kit's Part guides are cut from one run of its Full Build: the core steps of each Part are the Full Build's steps, the same
  order, wording and cameras. A Part has its own title card / Start view (the model as that Part shows it), its own Completed
  View (the model as that Part leaves it) and its own Parts List, of only the parts new in that Part (not those carried over).
  Step numbers restart at 1 in each Part. All the guides of a kit share the kit's one `model.glb`.
- **When Lee asks for a change to a step in a Part, ask whether it should also be in the Full Build** (and so in every guide
  that shares the step) **or in that Part only**, unless Lee has said; then say which was done. A Part's Start, Completed View,
  title card and Parts List are that Part's alone. Lee may name a step as "Part 2, Step 5" or by its Full Build number.
- A guide that is not a cut of the Full Build (the RCC deconstruction) has its own steps file and must never shrink the kit's
  shared model.
- A published Part guide would carry the kit's whole model (every part, later chapters' too) unless `publish.py` prunes the
  model to the parts that guide shows; to be decided when Part guides are built.

## Checking a change

Every change to a guide is checked in the browser before it is reported as done.

1. Regenerate, then load `player.html` and look at the steps that changed, plus one before and one after.
2. Run the whole guide through the check in `player/js/runthrough.js` (served as `js/runthrough.js`). In the page:
   `(0, eval)(await fetch('js/runthrough.js').then(r => r.text())); _dev.freeze(); _runthrough()`.
   It steps every view forwards (animated), backwards and by jumping, and compares visible parts, where each
   part is, lead lines, arrows, wires, labels, eyes, cautions, close-ups and the parts list with `steps.json`. `_dev.show('Step 12c', 0.5)` and
   `_dev.look(part, direction)` are for looking at one step or half-way through its animation. (The built-in
   browser pauses animation while its pane is hidden, which is why the check draws its own frames; a
   screenshot can lag one frame, so take a small throwaway one first. When the pane's screenshots stay stale,
   draw a frame, copy the canvas (and the `#overlay` labels) into a picture and POST it to
   `/__save/thumbs/<name>.png`: `tools/serve.py` saves it into the kit's `thumbs/` folder, where it can be opened
   as a file (`_cam.snap(name)` in `player/js/camsolve.js` does this). The page's own boxes (caption, caution, parts list, close-up) are HTML: to see them too, clone the page
   with its computed styles into an SVG foreignObject and draw that over the canvas. Delete `thumbs/` afterwards.)
3. Read the generator's log: a step with `hand` motion carries a yellow Review note in the player (in a guide with
   `review_notes=False` the log's WARNING line says the same); a step with `lines=0` that is not the first part or a
   note card needs a look.
4. `tools/build_model.py` prints a warning if one conductor changes colour between two cable pieces.
5. Commit the change (sources and generated files) once it is checked; this folder is a git repository (below).

A published copy is checked the same way: `serve.py site`, open `http://localhost:8797/<guide>/`, run the same check (the
server lends it the check script, which is never published).

The preview launcher cannot read the Desktop folder, so start `tools/serve.py` from the shell (in the
background) rather than through `.claude/launch.json`, which only attaches to it.

## Layout

    docs/                      the rulebook, its evidence, and the research reports (research/mra/ = this kit:
                               build videos, engraved codes, how the arm and claw go together, wires, pins, colours)
    player/                    THE player, for every kit: player.html, parts.html, js/ (core, player, parts; runthrough and camsolve:
                               authoring tools, never published), vendor/three/
    guides.json                the kits and guides on the website: kits (name, code, folder), guides (kit, steps file, card label),
                               embed_origins (the LMS addresses that may frame a guide)
    site/                      the website (Render serves this folder only): the current release of each published guide
    releases/                  every release ever published, frozen, with its record (never uploaded)
    render.yaml                the Render static site's configuration
    tools/                     build_model.py, stepgen.py, wires.py, glbio.py, serve.py, publish.py, check_site.py, site_pages.py,
                               bundle.py, step_text.py, step_to_glb.py, cut_part.py; site_assets/ = the TechBox wordmark (copied from the LMS) for the site's pages
                               cadasio/ = scripts for studying published guides; video/ = stills from a build video
    cad-sources.sha256         checksums of the source STEP files (kept out of git: too big for GitHub)
    MRA_Videos/                the four build videos (Base, Controller, Arm, Claw)
    MRA Build Instructions Prototype/
        guide.py, materials.json, mra.glb                         what the guide is generated from
        colour-atlas-mra.json, wire-paths.json, engraved-codes.json   colours, wire centre lines and engraved codes measured for this kit
        silkscreen.py -> decals.json                              the I/O module's printing, placed from the CAD's pin positions
        usb-mini-b.glb, usb-a-end.glb                             the USB cable's ends, converted from cad_extra/*.STEP (materials.json "extra_parts")
        logo.webp                                                 the title-page logo
        steps.json, parts.json, model.glb, model.report.json, parts/   generated; do not edit by hand
        _v1/                                                      the first prototype's files, for reference
    RCC Build Instructions/    the second kit, the Remote Controlled Car (first draft 15 Oct 2026, Lee's first round 16 Oct): the same
                               layout as the MRA's (guide.py, materials.json, rcc.glb from RCC_Assembly_v1.STEP, colour-atlas-rcc.json,
                               wire-paths.json, silkscreen.py -> decals.json, nano-mra.glb = the MRA's export of the Nano model, for both
                               of the RCC's Nano Boards (tools/cut_part.py), usb-a-end.glb). Research: docs/research/rcc/.
                               Commands as for the MRA with the folder name changed (server on port 8796: "Open Prototype.command").

## Conventions in the code

- Coordinates in `steps.json` are millimetres in assembly space, Y up. Part ids are the CAD's top-level
  instance names (`NAUO10`); student-facing names live in `guide.py`.
- CAD file names for the MRA do not match the codes engraved on the wood for 26 of the 44 wood parts (CAD
  B10 = B3, B8 = B7, B9 = B8, R5 / R6 swapped, and almost all of the arm: the engraved arm set is A1-A13).
  `guide.py` follows the engravings; `docs/research/mra/cad_codes_base.md` has the table.
- Where the CAD has a part out of place, `materials.json` `"adjust_mm"` moves it (`[x, y, z]`) or turns it (a pose,
  `{"t", "r", "at"}`); the model and the collision tests both use it, and `_notes.adjusted` says why. The MRA's base
  horn (moved) and R8 (turned end for end) are the cases so far. It also moves a piece inside a part (the RCC adapter
  board's 2-pin socket, `NAUO70`), in assembly mm all the same; only the model shows that (the collision tests take
  whole parts). `"own_parts"` makes a CAD node inside a part a
  part of its own (the Nano Board, inside the I/O module's assembly in the CAD). `"stickers"` adds round stickers
  that the kit puts on a purchased part (the coloured dots that tell the MRA's motors apart, on their wide faces; or one at
  a spot, `"at"`: the RCC Nano Boards' processors). `"extra_parts"` adds a part
  that comes as a STEP file of its own (the USB cable's two ends): convert it once with `tools/step_to_glb.py` into the
  kit folder, and give the GLB and a pose placing it in the assembly; both tools then treat it as a CAD part. The same
  part from a better export in another kit is cut out with `tools/cut_part.py` (the RCC's Nanos). A rule's
  `"regions"` colours faces by where they are in the mesh's own frame, for a purchased part modelled as one solid; with
  `"cut": true` the triangles crossing the box's faces are split first, so a band ends on a straight line (the RCC battery's).
  `"move_engraving"` moves a wood part's engraved code elsewhere on its face (and can turn it the right way up), for a part
  the CAD has engraved in the wrong place (R8): the pocket is filled in and the code drawn there instead.
- The player renders only when something changes. Do not add per-frame work. (A close-up is drawn once as its view
  opens; the parts list's pictures load only when its page is shown; reading aloud uses the browser's own voice.)
- Every step opens on its own camera (the player swings back to it whatever the viewer did). A camera Lee sends as a
  screenshot is solved by matching renders to it (silhouette and colours, coarse to fine: `player/js/camsolve.js`)
  and written as `view_dir=` + `frame=` (with `one_off_camera=True` where the next step chooses its own). Never change another step's camera unasked: after regenerating, diff
  every view's camera against a copy of steps.json saved before the edit.
- Controls stay real buttons, lists and tick boxes (keyboard and screen reader); on-screen text the student needs is
  in the page or in the announcement made as each step opens, never only in the 3D picture.
- New colours go in `materials.json`'s palette, following the colour library in the rulebook. Colours with
  no published reference are listed under `_notes.unconfirmed` there; colours Lee has ruled on are under
  `_notes.decided` and are not to be changed back.

## How edits are asked for

Lee names a step as the player's step list shows it ("Step 12") and says what should change; the edit is
made in the kit's `guide.py` (order, captions, direction, hover, `lines_to=`, `lines_at=`, labels) or
`materials.json` (a colour or the detail of one part of a model), then regenerated and checked as above.
Option-click in the player copies "step | part (id) | [x, y, z]" for a spot on a part; those points go
straight into `lines_at=[...]` when a lead line has to start or end somewhere exact. One edge threshold
(`defaults.edge_angle`, 40 as in Cadasio) applies to every part; do not set it per part without being asked.
Two per-rule options in `materials.json` deal with purchased-part CAD rather than with the threshold:
`edge_min_spacing_mm` leaves out crease lines packed closer than that (a modelled screw thread turns into a
black patch at guide scale), and `"skin": true` on a component marks a coloured shell laid over a copy of the
body, so the body underneath takes the same colour and the two cannot flicker.

## Open items

Questions for Lee about particular steps are on those steps as yellow Review notes (`review=` in `guide.py`; the MRA guide
hides them now that it is past review, `?review=1` shows any left); the independent
reviews behind them are `docs/research/mra/review_*.md`.
Decisions waiting on TechBox are in section 13 of the rulebook; what the player does not do yet is in section 14;
kit-specific points are in the kit's `README.txt` and under `_notes` in its `materials.json`.
The title page uses `logo.webp` (the picture Lee attached in chat); a `logo.svg` or `logo.png` dropped into the
kit folder takes its place the next time `guide.py` runs.

## Version control

This folder is a git repository (branch `main`). Its data is in `.git.nosync` (`.git` is a pointer file to it), which keeps
it out of iCloud sync, as the `.nosync` suffix does for the Python environment; until a remote is added the history is on this
Mac only. Kept out of git (`.gitignore`): the build videos, `share/`, the source CAD files (STEP and the like; checksums in
`cad-sources.sha256`), kits' `thumbs/`, environments. Commit each checked change. The remote (when Lee adds one) must be a
private GitHub repository; pushing `main` is a backup, pushing to `live` publishes (above).

## This computer

16 GB of memory and a nearly full disk: when memory runs out, swap fills the disk and the machine goes down
(it did on 2026-10-13). Run one heavy job at a time (`build_model.py` peaks near 2 GB), check
`df -h /System/Volumes/Data` and `sysctl vm.swapusage` before starting several agents, and have agents save
their reports into `docs/research/` as they go.
