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
  screenshot, with the narrowest window it suits, `min_aspect`, and `otherwise=` for narrower ones; or `otherwise=[...]`, wider
  cameras closest first: the generator notes where the parts reach on screen with each (`fit`), and the player takes the first
  that keeps them within the frame's sides and top (the card picture: the bottom too), on the title page (`clear_title=True`)
  moved aside just enough to clear the title, which is a fixed size on the page: the RCC's title page and Completed View, punched
  in yet right in the LMS's frame),
  can leave parts off them (`hide=`) and can show parts turned or moved there (`poses={id: pose}`; the Completed View then cuts
  in rather than gliding from the last step). The RCC's controller is instead turned in the build itself from Step 29
  (`rest_at` + `carry`), so that the Completed View glides.
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
  as it blends between them (Steps 98 and 99). Or (the RCC's motor leads) give every stop of the plug a smooth shape of its own,
  drawn with `W.smooth` (a spline through a few points, no corners), all lying flat the same way (`W.ribbon(twist=)`), with the
  plug turning no more than a quarter turn per beat: the player blends shapes bit by bit along their length, and very unlike
  shapes (one bending back, the next forward) or shapes twisted the opposite way fold or cross their wires as they blend. A lead
  whose length does not matter says `stretch` (W.route): it then stretches evenly between shapes of different lengths instead of
  growing out of its tip, and while it changes shape it is carried by its ends' moves only, not turned with its plug. A part in both `move` and `appear` is on screen where its path starts
  as the step opens (a plug at the end of a lead laid out on the bench) instead of gliding in.
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
- **More guides from one kit.** Part guides cut from the Full Build (`g.chapter()`; `g.in_part()` and `g.note(only_in=)` for
  what one Part has of its own) and a deconstruction guide (`g.take_apart()`, then `remove()`, `unplug()`, `lift()`): see "A kit's
  guides" below.
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
    .venv.nosync/bin/python "MRA Build Instructions Prototype/deconstruction.py"   # then the deconstruction, made from the Full Build
    .venv.nosync/bin/python "RCC Build Instructions/deconstruction.py"            # (the RCC's, likewise, after its guide.py)
    .venv.nosync/bin/python tools/build_model.py "MRA Build Instructions Prototype" # after editing materials.json or replacing the CAD
    .venv.nosync/bin/python "MRA Build Instructions Prototype/silkscreen.py"       # after editing the module's printing (then build_model)
    /usr/bin/python3 tools/serve.py "MRA Build Instructions Prototype" 8791         # local server; then open http://localhost:8791/player.html

`guide.py` rebuilds the model by itself when the set of parts shown changes. Opening
`http://localhost:8791/parts.html` re-renders the part pictures and saves them into `parts/`.

    python3 tools/step_text.py export "MRA Build Instructions Prototype" "share/<folder>/MRA step text.csv"   # step text for editing
    python3 tools/step_text.py import "MRA Build Instructions Prototype" "<edited>.csv"                       # then run guide.py

(`step_text.py` takes a steps file as a fourth argument, for a Part or a guide of its own such as a deconstruction: a Part's sheet
is imported with `--only-this-part` or `--everywhere`, see "A kit's guides".)

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
names in `guides.json` (Lee's: `mini-robot-arm-full-build`, `mini-robot-arm-part-1` ..., `mini-robot-arm-deconstruction`, `remote-controlled-car-full-build`,
`remote-controlled-car-part-1` ..., `remote-controlled-car-deconstruction`). An address in the LMS must never change.
The site's own pages, made by `tools/site_pages.py` after every publish (header and footer copied from the LMS, Lee
16 Oct 2026): the landing page `/` shows each kit that has a guide on the site (its Full Build's picture), `/kits/<kit>/`
shows that kit's guides (Full Build, Part 1 ..., Deconstruction), and a guide's card opens the guide. Nothing is offered for
download (the 2D PDF guides will be, later). Each guide's card picture is its Completed View (a deconstruction's is its Full
Build's card, the same picture: Lee, 18 Oct 2026; make the Full Build's first): in the player, after the guide is final, `await _dev.card()` saves it into the kit's `cards/<steps file>.webp` (cut to the model with a margin, 1440 x 900; for a
Part, `player.html?steps=steps-part-1.json`), with `cards/<steps file>.json`, the model it shows; publish copies it into the
release (it warns when a guide has none, or one drawn from another model; `parts.html` notes its model in `parts/parts.json`
the same way, and publish warns about part pictures drawn from another model).

    python3 tools/publish.py <guide> --note "what changed"   # freeze the guide as its next release and put it in site/<guide>/
    python3 tools/publish.py --kit <kit> --note "..."        # the same for every guide of a kit that has changed (the rest are left)
    python3 tools/check_site.py                              # site/ is exactly the releases on record (Render runs this before each deploy)
    /usr/bin/python3 tools/serve.py site                     # the site as Render serves it: http://localhost:8797/<guide>/
    python3 tools/publish.py <guide> --restore r3            # put an earlier release back (a roll-back); --take-down removes the guide
    python3 tools/publish.py --list                          # which release each guide has on the website
    python3 tools/site_pages.py                              # the landing and kit pages again (publish does this by itself)
    /usr/bin/python3 tools/serve.py releases                 # every earlier release, on this computer only: http://localhost:8798/<guide>/r<N>/

- **A local copy of the website**, for Lee between sessions and to look at before anything is published: publish every guide
  with `--to "share/Website preview"` (a practice run: it writes only there, never `site/`, `releases/` or `render.yaml`, and needs
  no commit), check it with `python3 tools/check_site.py "share/Website preview/site"`, serve it on 8797; `Open Website
  Preview.command` (top folder) starts it by double-click. Make it again after each round, and for every guide after a player
  change (a published copy keeps the player it was published with).
- **iCloud** (the Desktop is synced, `site/` and `share/` with it): `publish.py` updates a guide's folder where it is, file by
  file (an unchanged file is not touched, anything not in the release is removed and listed), and never swaps the folder for a
  new one: swapped folders left iCloud's copies beside them ("index 2.html", "js 2/": 18 Oct 2026), which `check_site.py`
  refuses, naming them as iCloud copies. Publishing the guide again (or `--restore` of its release) clears any that remain.
- **Only the current release is on the website** (Lee, 16 Oct 2026). `site/` holds one copy per guide; every release ever
  published is kept in `releases/<guide>/r<N>/` with its record (`release.json`: when, Lee's reason, the source's git commit,
  every file's checksum) and `releases/<guide>/history.json`, in git but never uploaded (Render serves `site/` only).
  `check_site.py` requires each `site/<guide>/` to be byte for byte the release its `steps.json` names, so only `publish.py`
  can change what goes out.
- **What goes out** is only what a learner's browser needs: the player (as `index.html`), the steps (without Review notes,
  `text_key` or the generator's own records), the kit's `model.glb` cut down to the parts that guide shows (a Part guide downloads
  only its own: Lee, 17 Oct 2026; without the CAD's own body and file names; the part ids stay, as the player needs them), the logo
  and the part pictures the Parts List shows. Never the CAD, `guide.py`, `materials.json`, wire paths, `decals.json`
  (the printing travels inside the model as shapes) or research. `check_site.py` refuses any other kind of file in a guide's
  folder (only .html, .js, .glb, .png, .webp, .jpg, .svg, steps.json and the three.js licence) and a CAD name left in its model.
- **What the model gives away** (told to Lee, 16 Oct 2026): a 3D guide has to send the part shapes to the browser; anyone who
  opens a guide can save the model. Only the STEP and editable CAD stay private. So the laser-cut wood is **roughened** in every
  model (Lee, 16 Oct 2026): `materials.json` `"roughen_mm": 0.1` on the wood rule makes `build_model.py` move each vertex of a
  plate's outline 0.05 - 0.1 mm within the plate's plane (the same for both faces, so the plate stays a straight-sided slab;
  deterministic), so a traced cutting file comes out slightly wrong. Invisible in the guide. It is a deterrent, not a guarantee:
  at 0.1 mm a slot's width changes by 0.04 - 0.14 mm, within laser and plywood tolerances, so most traced joints would still
  fit (an independent review, 16 Oct 2026; told to Lee). Making traced joints reliably fail would take 0.3 - 0.5 mm per slot or
  tab, which can show as gaps or parts passing into each other in close-ups: Lee's call. The collision tests and cameras use the
  exact CAD, not the model, so they are unaffected. `publish.py` refuses to publish a kit whose laser-cut meshes (the colour of a
  rule with `roughen_mm`) are not all roughened (`model.report.json`), or whose materials.json has no `roughen_mm` rule at all
  unless it says `"no_laser_cut_parts": true`: a new kit cannot go out with exact shapes by leaving it out. Checkpoints made before 16 Oct 2026 15:49 (share/) carry the exact geometry.
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
- **The first deploy, in stages** (so that Render, the domain and the headers are tried with no guide online): create the GitHub
  repository private and empty (no README, licence or .gitignore), push `main`; push the site as it is, with no guide in it, to
  `live` (`git push origin main:live`: its landing page says "No guides are published yet"); in Render, New > Blueprint from this
  repository, branch `live`, Render's GitHub App limited to this repository; read the build log (`python3 --version`, then
  check_site's OK); add the CNAME `models` at tech-box.io's DNS (DreamHost) to the onrender.com host Render shows; check the headers
  (render.yaml's curl loop, on every kind of path, a few times over some minutes: one Cache-Control, an ETag or Last-Modified, .js
  as JavaScript, a 404 for a missing page); only then publish the guides for real and push them to `live`, on Lee's word. Push
  with `git -c pack.threads=1 push` on this Mac (memory). As set up, the raw CAD meshes (mra.glb, rcc.glb, nano-mra.glb: exact,
  unroughened) go to the private repository, since a guide cannot be regenerated without them; keeping them out of GitHub
  instead means taking them out of the history before the first push (Lee's call).
- **Before the first LMS link goes out:** the custom domain verified, then `renderSubdomainPolicy: disabled` in render.yaml (the
  onrender.com address closed); render.yaml's curl loop answers the same over a few minutes; a real embed from the LMS plays on an
  iPad (Safari: iOS 16.4 or later, for the player's import map) and a Chromebook; a frame from any other site stays blank. Locally, `serve.py site` sends render.yaml's headers,
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

## A kit's guides: Full Build, Parts, Deconstruction

A kit's guides live side by side in its folder, each with its own steps file, `guides.json` entry, address and releases, and
all of them use the kit's one `model.glb`, which holds every part any of them shows (`build_model.py` keeps the parts of every
steps file in the folder, so no guide ever shrinks it below what another needs). Steps files name the model by its content
(`model.glb?v=<checksum>`), so the stamp is the same on any computer and after any checkout.

- **The Full Build**: `guide.py` -> `steps.json` (and `parts.json`, from which the part pictures are made).
- **Part guides** are cut from the Full Build by the same run (Lee, 16 Oct 2026): in `guide.py`, `g.chapter('part-1',
  part='Part 1: The Controller')` just before the first step of each Part (optional `start_view=` / `end_view=`, as
  `Guide`'s). Running guide.py then also writes `steps-part-1.json` ... and `chapters.json`, the map: each Part's first and last
  step in the Full Build, the parts it brings in, and its step names -> the Full Build's (for "Part 2, Step 5"; null for a card
  only the Part has). A Part's steps are the Full Build's, with their order, wording and cameras, numbered from Step 1. It has its
  own title page and Completed View, both showing the model as that Part leaves it (by default from the finished model's corner,
  framed on what the Part shows), and a Parts List of only the parts new in it (a Part with none has no Parts List). Take a
  `chapter()` line out and the next run removes that Part's file. The log notes a Part that begins inside a turned-over run or a
  sub-assembly built in the hand, and a caption that names a step by its (Full Build) number.
- **A change in one Part only** (Lee, 17 Oct 2026): `g.in_part(caption=, caution=, view_dir= / frame= / look_from=)`, written just
  after the step in guide.py, is that step as its Part shows it (wording, or a camera of its own for both its views; not for a
  turned-over step or a `rest()` step); the Full Build keeps the step as written. `g.note(..., only_in='part')` is a card only the
  Part shows ("Part 1 must be finished first"), `only_in='full'` one only the Full Build shows; each guide numbers its own steps.
  A Part's spreadsheet (`step_text.py export <kit> <csv> steps-part-2.json`) is imported with `--only-this-part` (into
  `step-text-part-2.json`, applied over the Full Build's wording and `in_part()`) or `--everywhere` (into `step-text.json`: the
  Full Build and every guide with the step; a step with wording of its own in the Part keeps it, and the import says so). What a
  Part cannot have on its own: different parts, moves or wires (those carry on into the steps after), or a step left out.
- **When Lee asks for a change to a step in a Part, ask whether it should also be in the Full Build** (and so in every guide
  that shares the step) **or in that Part only**, unless Lee has said; then say which was done. A Part's Start, Completed View,
  title card and Parts List are that Part's alone. Lee may name a step as "Part 2, Step 5" or by its Full Build number.
- **A deconstruction guide** (the MRA's and the RCC's, first drafts 18 Oct 2026) is a script of its own in the kit folder (e.g. `deconstruction.py`, named in its
  `guides.json` entry as `"script"`): `Guide(..., part='Deconstruction', steps_file='steps-deconstruction.json')`, then
  `g.take_apart()`, which starts it from the Full Build as it ends (read from its steps.json: run the Full Build first), with the
  Full Build's title page. Then, as a rule the build in reverse (rulebook section 11 and Lee's conventions there: parts may go in
  unison, every step has its own wording, a part once off is gone for good):
  - `g.remove(caption, ids)`: the parts leave and disappear. Step N shows them where they are with one red arrow per unit (parts the
    Full Build put on together are one unit; two of a kind get an arrow each); Next plays them out the way the Full Build put them
    in, reversed (to where they hovered, by that step's camera), and they are gone; Prev brings them back. A part the Full Build
    did not move in, or one not in its seat, is pulled straight out the first free way. Parts riding on them go too, and so does a
    lead whose ends both go; a lead left with one end on screen is refused (unplug it first). `path=` / `paths=` / `direction=`
    and `hover=` by hand; `arrows=`, `eye=`, `inset=` (on Step N: a catch to release), `alone=[ids]` (taken apart on its own),
    `new_camera=True` or `view_dir=` / `frame=` / `look_from=`; `wires={id: route or None}`; `in_turn=[[ids], ...]` (in order, each
    group once the one before has slid out and faded); `units=[[ids], ...]` (the arrows by
    hand: an arrow on the joystick, not the walls it carries); `wires_here={id: route}` (leads as drawn on this step only);
    `keep_camera=True` (the step before's camera: two steps on one sub-assembly). Two of a kind get an arrow each only if they do
    not touch (a motor and its horn, named alike, are one). A sub-assembly taken apart in the hand after sliding off (not turned)
    keeps the Full Build's in-hand cameras, moved with it. Arrows (Lee, 18 Oct 2026: smaller than the published ones): sized to the
    part, 15 - 40 mm long and 1.6 - 3.2 mm thick; along the longest stage of its way (the module's slide, not the nudge before it);
    moved on along it until the camera can see it; and one that would point at the camera becomes an eye on the part. A plug moved
    on its lead (walked back) has an eye, no arrow, as an unplug; several things at once can have an eye each (the eight breadboard
    wires: one at each joystick's ends and one at the module's). A part the camera cannot see gets a close-up from the other side
    (`inset=`, with its own arrow in it: `inset=dict(..., arrows=[ids])` and that arrow's `face=` towards the close-up), not an eye.
    By hand, per step (Lee's third round, 18 Oct 2026): `arrow_scale=k` (every arrow of the step), `arrow_style={id: dict(scale=,
    like=id2 (as big as id2's own arrow: a screw's as its part's), at=[x, y, z] (where its tail is: the top of R7, the edge of B2's
    cut-out), shift=[dx, dy, dz] (raised clear of wires), face=, keep=True (an arrow even towards the camera: the A9s), stage=k (along stage k
    of its way, 0 the first, not the longest: the RCC's joysticks pulled back out of their sockets))}`.
  - `g.unplug(caption, plugs)`: each plug comes out the way it went in, its lead back on the route it had before, and dangles from
    the part it rode on in the Full Build (or `ride_on=`) until that part is removed. An eye on each plug, no arrow.
  - `g.lift(caption, ids, to=pose)`: set aside beside the model, still wired, to be unplugged later; or `path=`; or neither: the
    Full Build's way in, reversed (a group lifted off to be taken apart in the hand). With `ride_on=` each part rides on that part
    again where it ends: a Full Build step that moved only a plug on its lead (into a slot, a hook, a hole), walked back with its
    poses as `via()` and its lead's stages as `wire_via={wire: [route, ...]}` (last route in `wires=`); the player then moves the
    plug as the Full Build did, at an even pace with its lead (the MRA's `walked_back()`).
  - `g.note(...)` as in a build; `put_away(ids)` for what is left of a sub-assembly taken apart on its own.
  It writes only its steps file (its wording: `step-text-deconstruction.json`), never `parts.json` or the Part files, and it can add
  parts to the model but not take any away. The log warns where a way out passes through a part still there (the order differs
  from the build's reverse), and notes a camera copied from the Full Build that leaves out a part lying aside. It ends on what is
  left (the base), closer in. No Parts List unless asked for. Its card picture on the website is its Full Build's card (Lee, 18 Oct
  2026: `_dev.card()` copies it for a guide made by `take_apart()`); its title page is the Full Build's. Parts taken off slide out, then fade out over a
  beat of their own (800 ms, starting just before the slide comes to rest), leads with them, as Cadasio does (Lee, 18 Oct 2026:
  slower and smoother than the fade inside the slide of 17 Oct), each part once its own way has come to rest; Prev plays the whole
  backwards (each fades in where its way out ended, then slides back). `in_turn=[[screw], [part]]` takes a screw and the part it
  held off in one step, one after the other: the screw out and gone, then the part (Lee, 18 Oct 2026). An `alone=` view shows
  what rides on its parts too. The arrow of parts spread apart (six screws round a plate) starts on the one nearest their middle.
  The MRA's (`deconstruction.py`, 73 steps): the Full Build reversed except where Lee said (the eight breadboard wires at once;
  no electronics test; A12, A13, A11, A5 and the lever each a screw then its part; with B8 off, the breadboard wires, the I/O module and the Nano
  Board come out before the joysticks' walls), and it ends on R1. Run it after every Full Build change.
  The RCC's (`deconstruction.py`, 22 steps, Lee's order of 18 Oct 2026): the controller first, on its own (its USB cable, one arrow
  on the Mini-B plug clear of the cable; then the joysticks, the radio module and the Nano Board, by the Full Build's camera for
  the right joystick turned round with the controller, one camera for the run); the barrel plug and the battery; the 9V adapter off the battery on its own; the wheel motors unplugged
  (the Full Build's four beats, reversed) before L6, L7 and the I/O module; the module taken apart on its own; L4 and L5 lifted
  off L1 with the motors, the leads straightened back as in the hand so that L4 slides off over the plugs, the motors out of L5;
  L3 and L2; it ends on L1. Run it after every Full Build change.
- **Publishing:** `publish.py --kit <kit>` publishes every guide of the kit that has changed since its release (steps, model,
  pictures, card or player) and leaves the rest; publishing one guide alone warns when others of its kit have changed. A Part
  whose steps are not from the run that wrote `chapters.json` is refused; a deconstruction made from an earlier Full Build is
  published with a warning (run its script again). Each guide's model goes out cut down to the parts it shows (`only_parts`; the
  RCC: Part 1 0.98 MB of 1.98), and `bundle.py` packs a Part the same way.
- A new guide gets an entry in `guides.json` before its first publish (above); a new kit, an entry under `kits` and a folder
  laid out as the MRA's.

## Checking a change

Every change to a guide is checked in the browser before it is reported as done.

1. Regenerate, then load `player.html` and look at the steps that changed, plus one before and one after.
2. Run the whole guide through the check in `player/js/runthrough.js` (served as `js/runthrough.js`). In the page:
   `(0, eval)(await fetch('js/runthrough.js').then(r => r.text())); _dev.freeze(); _runthrough()`. A kit with Parts or a
   guide of its own: run it on each of them too (`player.html?steps=steps-part-1.json`).
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
    Open Website Preview.command   serves the local copy of the website (share/Website preview/site) on 8797, by double-click
    tools/                     build_model.py, stepgen.py, wires.py, glbio.py, serve.py, publish.py, check_site.py, site_pages.py,
                               bundle.py, step_text.py, step_to_glb.py, cut_part.py, step_tree.py (a STEP's assembly tree, read as text), wirecheck.py
                               (wires passing into parts, view by view); site_assets/ = the TechBox wordmark (copied from the LMS) for the site's pages
                               cadasio/ = scripts for studying published guides; video/ = stills from a build video
    cad-sources.sha256         checksums of the source STEP files (kept out of git: too big for GitHub)
    MRA_Videos/                the four build videos (Base, Controller, Arm, Claw)
    MRA Build Instructions Prototype/
        guide.py, materials.json, mra.glb                         what the guide is generated from
        colour-atlas-mra.json, wire-paths.json, engraved-codes.json   colours, wire centre lines and engraved codes measured for this kit
        silkscreen.py -> decals.json                              the I/O module's printing, placed from the CAD's pin positions
        usb-mini-b.glb, usb-a-end.glb                             the USB cable's ends, converted from cad_extra/*.STEP (materials.json "extra_parts")
        logo.webp                                                 the title-page logo
        steps.json, parts.json, model.glb, model.report.json, parts/   generated; do not edit by hand (and, once a guide has
                                                                  Parts, steps-part-*.json and chapters.json)
        cards/                                                    each guide's card picture for the website (_dev.card())
        _v1/                                                      the first prototype's files, for reference
    RCC Build Instructions/    the second kit, the Remote Controlled Car (first draft 15 Oct 2026, Lee's first round 16 Oct): the same
                               layout as the MRA's (guide.py, materials.json, rcc.glb from RCC_Assembly_v1.STEP, colour-atlas-rcc.json,
                               wire-paths.json, silkscreen.py -> decals.json, nano-mra.glb = the MRA's export of the Nano model, for both
                               of the RCC's Nano Boards (tools/cut_part.py), usb-a-end.glb). Research: docs/research/rcc/.
                               Commands as for the MRA with the folder name changed (server on port 8796: "Open Prototype.command").
    LAC Build Instructions/    the LCD Alarm Clock (first draft 19 Oct 2026): guide.py, materials.json, colour-atlas-lac.json, wire-paths.json,
                               lac.glb from "LAC Full Build.STEP" (the engineer's export, every part in several posed copies), cut down by the
                               kit's trim_source.py to lac-guide.glb (the parts the guide uses: the source both tools read); nano-mra.glb and
                               usb-a-end.glb (the MRA's), f4.glb (F4 seated: the STEP has it only lying beside the base). The STEP has no
                               F2, F5, F6 yet (README.txt). Research: docs/research/lac/. Server on port 8793 ("Open Prototype.command").
    LSM Build Instructions/    the Laser Stem Matrix (first draft 19 Oct 2026): guide.py, materials.json, colour-atlas-lsm.json (make_atlas.py),
                               lsm.glb made by the kit's assemble.py: Lee's STEPs hold no working assembly (the loose parts files
                               LSM_WoodSteps / LSM_Electronics, a Full Build export missing the Nano, D4 - D10 and the stems), so each part is
                               taken from them in its own frame and placed where TechBox's published Cadasio guide has it (the same SolidWorks
                               parts, same coordinates), or into the breadboard holes the guide names; the Nano and USB A end are the MRA's;
                               the stems are drawn from Cadasio's box until their CAD comes. docs/research/lsm/cad_study.md has the
                               sub-millimetre corrections. Server on port 8805 ("Open Prototype.command").
    PMG Build Instructions/    the Piano Memory Game (first draft 19 Oct 2026): guide.py, materials.json, colour-atlas-pmg.json, silkscreen.py ->
                               decals.json, wire-paths.json (the CAD's wire shapes guide.py reuses). pmg.glb (167 MB, from "PMG Full 3D Cadasio
                               Build.STEP": the engineer's pose copies of most parts; kept out of git, over GitHub's limit) is cut down by the kit's
                               make_source.py to pmg-guide.glb (one copy of each part, built; the source both tools read; the MRA's Nano grafted in)
                               and cad-geometry.json (every other copy as a pose, the jumper caps, the USB cable's ends). The STEP is older than the
                               published Cadasio guide's model, which the draft follows (three wires per button, the I/O module USB end up:
                               README.txt). Research: docs/research/pmg/. Server on port 8792 ("Open Prototype.command").

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
  the CAD has engraved in the wrong place (R8): the pocket is filled in and the code drawn there instead. `"fill_holes"`
  ({instance: [points on the holes' axes, assembly mm]}) fills round pin holes in a plate that nothing passes through any
  more, in the mesh itself, so that neither hole nor line shows, picked or not (the RCC adapter board's two holes left empty
  when its socket was moved; a painted-over disc showed a grey ring and stayed white when the board was picked).
- The player renders only when something changes. Do not add per-frame work. (A close-up is drawn once as its view
  opens; the parts list's pictures load only when its page is shown; reading aloud uses the browser's own voice.)
- Every step opens on its own camera (the player swings back to it whatever the viewer did). A camera Lee sends as a
  screenshot is solved by matching renders to it (silhouette and colours, coarse to fine: `player/js/camsolve.js`)
  and written as `view_dir=` + `frame=` (with `one_off_camera=True` where the next step chooses its own). Never change another step's camera unasked: after regenerating, diff
  every view's camera against a copy of steps.json saved before the edit.
- Controls stay real buttons, lists and tick boxes (keyboard and screen reader); on-screen text the student needs is
  in the page or in the announcement made as each step opens, never only in the 3D picture.
- A part picked by a click (or named on hover) is let go as soon as the view moves (drag, pinch, wheel, the view reset):
  its name is placed once on the page and would no longer point at it (Lee, 17 Oct 2026).
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
