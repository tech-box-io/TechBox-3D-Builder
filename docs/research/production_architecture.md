# TechBox build guides: production architecture plan

Status: a plan only, written 16 Oct 2026. Nothing was changed, generated or served to write it; only files were read.
It is for Lee (who runs Render and the LMS) and for the Claude sessions that will build it.

- Paths are under `/Users/lee-johnson/Desktop/Claude_Cadasio/`. `MRA/` means `MRA Build Instructions Prototype/`, `RCC/` means
  `RCC Build Instructions/`.
- Line numbers are from the MRA copy unless marked, as the files stood around midday on 16 Oct. Another session is editing
  `MRA/js/player.js`, `MRA/guide.py` and `tools/stepgen.py`, so some numbers will move.
- Assumptions are marked **[A1]**, **[A2]** ... and listed in Appendix B. Where this plan departs from the architect's draft or
  from the two critiques, Appendix A says so and why.

## Lee's decisions of 16 Oct 2026, and what was built (read this first)

These replace the parts of the plan below that disagree with them:
- **Only the current version of each guide is on the website**, at one fixed address per guide, `https://<domain>/<guide>/`.
  There are no `/embed/`, pinned, preview or `/guides/<guide>/r<N>/` addresses and no year-long caching: `site/<guide>/` is
  replaced by each publish and every file is served `no-cache`. Earlier releases stay in `releases/` on this computer (in git,
  never uploaded); a roll-back puts one back into `site/`.
- **Guide names** (web addresses): `mini-robot-arm-full-build`, `mini-robot-arm-part-1` ..., `remote-controlled-car-full-build`,
  `remote-controlled-car-part-1` ..., `remote-controlled-car-deconstruction` (`guides.json`).
- **The LMS is TechBox's own** and takes iframe embeds: no SCORM, xAPI or LTI. Render is set up by Lee (as for five other
  services). Guides are public (the iframe shows the address); only what a learner's browser needs is published.
- **Part guides:** core steps identical to the Full Build's; each Part's own Start, Completed View and Parts List (new parts
  only); numbering restarts at 1; when a Part's step is edited, ask whether the change also belongs in the Full Build.
- **The authoring folder is the git repository** (data in `.git.nosync`, out of iCloud), not a separate site repository.

Built on 16 Oct 2026: one player (`player/`), `tools/serve.py` lending it to the kits, `tools/publish.py`, `tools/check_site.py`,
`guides.json`, `render.yaml` (Render deploys the branch `live`; `main` is a backup), `site/` (no guide published yet), git. An
independent review of that build (four reviewers, each finding verified) led to: `check_site.py` requiring each guide to match
its release record byte for byte; the CAD's body and file names taken out of the published model; content-based version stamps;
per-guide history; the slash fix added at publish rather than in the shared player; and the finding, told to Lee, that the
published model gives away the exact shapes of the laser-cut parts. See CLAUDE.md "Publishing: the website" and "Part guides".
Later the same day (Lee): the site is `https://models.tech-box.io` and the LMS `https://edu.tech-box.io`; a landing page lists
the kits and a page per kit its guides, header and footer copied from the LMS (`tools/site_pages.py`); only the LMS may frame a
guide and nothing may frame the site's own pages (X-Frame-Options: DENY everywhere, a per-guide CSP frame-ancestors, written into
render.yaml); the wood is roughened by 0.05 - 0.1 mm in every model (`"roughen_mm"` in materials.json, `build_model.py`); the RCC's
title is "Remote Controlled Car (RCC)".
Not built yet: Part guides (section 4, adapted to the decisions above), the heavy-job lock, the daily link check.

## The short version

- **Lee's picture of the code is right.** There is one generic player. The guide content (steps, model, part pictures) is in
  separate files, which the player loads when the page opens. The player has no code for a particular kit.
- **The layout is not like that yet.** Each kit folder holds its own hand-made copy of the player, and the player looks for its
  content in its own folder. Nothing records which player a guide was checked with, and every open takes whatever files are
  on disk at that moment.
- **Today's MRA player edit did not change any RCC file.** The kits are linked by three other routes: player fixes copied
  across by hand, the shared generator in `tools/`, and the shared bundler.
- **The recommended path:**
  1. one player source;
  2. each guide published as a frozen release folder that is never changed;
  3. a stable LMS address per guide that points at one release, so going live or rolling back moves only that pointer;
  4. chapter guides cut from one Full Build run.
- **What waits:** a shared, versioned player (the bigger redesign) waits until there are enough guides to need it.
- **The first useful step** is about two days of Claude's work, plus an hour or two of Lee's account and DNS set-up.

---

## 1. How it works today, and why the MRA player change touched the RCC

### 1.1 The three pieces

| Piece | Where | What it does | Shared between kits? |
|---|---|---|---|
| **Generator** | `tools/` (`stepgen.py`, `build_model.py`, `wires.py`, `glbio.py`) | Reads the CAD, `guide.py` and `materials.json`; writes the guide content | Yes, one copy |
| **Content** | each kit folder | `steps.json` (every view: parts on screen, poses, camera, captions, lead lines, wires), `model.glb` (the small coloured model), `parts/*.png`, `logo.webp` | No, one set per kit |
| **Player** | each kit folder | `player.html`, `js/player.js`, `js/core.js`, `vendor/three/`: reads the content and plays it | **No: a hand-made copy per kit** |

**What happens when a guide opens:**
1. `player.html` loads three.js from `./vendor/three/` (player.html:99-100).
2. It loads `./js/player.js?v=<the time now>` (player.html:141). The changing `?v=` forces a fresh download on every open.
   `player.js` loads `core.js` the same way (player.js:3).
3. It fetches `steps.json` from its own folder, telling the browser to check for a newer copy every time (player.js:12). The
   only other file it accepts is another name in the same folder, `?steps=x.json` (player.js:11).
4. `steps.json` names the model as `model.glb?v=<file time>` (stepgen.py:1206-1207), plus the logo and part pictures
   (`parts/<name>.png`, stepgen.py:1199-1201). All are relative to the page (core.js:69, player.js:413).
5. The player finds each part in the model by its CAD name (core.js:122-126) and plays the views from the data.

There is no server logic and nothing is stored for a learner: no cookies, no local storage, no server calls. The only write
endpoints are in the local development server (serve.py:41-57), which only answers on localhost (serve.py:27-30).

**So, to Lee's question:** yes, it is the same player whatever the kit, and the model files are separate and load when the page
asks for them. The catch is that each kit has its own copy of that player, sitting beside its content.

### 1.2 What makes today's set-up unsuitable for production

- **The copies drift.**
  - `core.js` is byte-identical in both kits; the two were last copied together on 15 Oct at 22:50.
  - `player.js` differs (md5 `44d43c…` MRA, `25e8e9…` RCC), and so does `player.html`. The MRA copy (16 Oct 11:37) has the
    reset-view button and the step-list pictures of the Parts List pages; the RCC copy (15 Oct 21:53) has neither.
- **The player only finds content beside itself.** See player.js:11 and the relative URLs above. One folder holds one guide.
- **Every open plays whatever is on disk now.** `Date.now()` (player.html:141) and `no-cache` (player.js:12) do this on
  purpose, which is right while authoring.
  - In production, any edit would reach every learner at once.
  - A learner part-way through an update could get new steps with the old model: the `?v=` stamp is ignored by the server,
    which sends whatever `model.glb` is there.
- **One guide per kit folder.**
  - The generator always writes `steps.json` and `parts.json` into the kit folder (stepgen.py:1213-1214).
  - It then rebuilds `model.glb` to hold exactly the parts that guide shows (stepgen.py:1218, 1221-1232; exact match at 1229).
  - So a second guide script in the same folder would overwrite the Full Build and strip parts out of its model. Missing
    parts are skipped silently (core.js:203), and a missing riding part crashes the page (player.js:65).
- **No version anywhere.**
  - The top-level keys of `steps.json` are `meta, model, fov, frame_padding, names, mesh_names, wires, routes, views`
    (stepgen.py:1210-1212).
  - An older player silently drops what it does not know. The 14 Oct player, given today's MRA content, loses all 14
    cautions, including "Very important: the brown wire goes on G", with no error (contract report).
- **Authoring tools ship with the player.**
  - Review notes can be forced on with `?review=1`, even when `meta.review_notes` is false (player.js:856).
  - The RCC shows its notes by default: 14 distinct notes on 27 of its 67 views, and no `review_notes` setting.
  - The option-click pick tool is on whenever the page is not inside a frame (player.js:804).
- **The kit folders hold authoring files that must never be uploaded:** the CAD (`mra.glb` 41.8 MB, `rcc.glb` 33 MB),
  `RCC_Assembly_v1.STEP` (101 MB), `guide.py`, `materials.json`, `_v1/`, `thumbs/`.

### 1.3 Why the MRA player change "touched" the RCC

**At file level it did not.** The newest RCC file is from 15 Oct 23:40. Today's MRA player edit (16 Oct 11:37) changed only
`MRA/player.html` and `MRA/js/player.js`.

What does tie the kits together:

1. **Player fixes travel by hand-copying, and half a copy breaks.**
   - The RCC README calls its viewer "the same as the MRA's" (RCC/README.txt:91).
   - The next player fix must be copied to every kit. Copying only some files breaks the page: today's MRA `player.js` next
     to the RCC's `player.html` throws at player.js:474, because the RCC page has no reset-view button.
   - Until someone copies, the kits behave differently, which may be the "effect" Lee saw.
2. **The generator is shared.**
   - Re-running `RCC/guide.py` now uses today's `tools/stepgen.py` (changed 16 Oct 11:36) with the RCC's older player.
   - Today that is harmless: the new output (`text_key`) is ignored by every player. The risk is real but latent. The next
     new feature the generator writes would reach the RCC with nothing to say that the RCC player cannot show it.
3. **The bundler is shared and tied to the player's exact text.** `tools/bundle.py` rewrites the player's source with
   patterns, and refuses to run if `player.js` or `player.html` "changed shape" (bundle.py:49, 77). A player edit made for
   one kit can stop bundling for the other.

**The underlying point:** nothing ties a guide to the player it was checked with. The `share/` checkpoints are the exception.
Each bundle freezes the player of its day; they already hold four or five different, unnamed player builds. Freezing is the
right idea. What is missing is a name, a record, and a stable address in front of it.

---

## 2. What has to change

### 2.1 Essentials, before the first LMS embed

1. **Choose the permanent addresses first.** An address pasted into an LMS page cannot be changed centrally, so this comes
   before anything else.
   - Use a TechBox domain, not an `onrender.com` address. `guides.tech-box.io` is a guess **[A2]**.
   - Name guides by content, not by chapter number: `mra/arm`, not `mra/ch3-arm`. The "Chapter 3" label lives in the guide's
     subtitle (player.js:20), which can change.
2. **One player source.**
   - A single `player/` folder in the authoring project. `tools/serve.py` serves it to every kit, and the per-kit copies of
     `player.html`, `js/` and `vendor/` are deleted.
   - Do this only while no other session is editing the player.
   - Moving the RCC onto the current player is itself a change to check: the RCC gains the reset view and the step-list
     pictures.
3. **Frozen releases.**
   - Each published guide is a release folder, `site/guides/<kit>/<guide>/r<N>/`. It holds exactly the player and content
     it was checked with, and is never changed or deleted afterwards.
   - Today's player works unchanged in such a folder, because all its URLs are relative and the folder never changes.
4. **A pointer per guide.**
   - `/embed/<kit>/<guide>/` is a tiny page that sends the browser on to the live release. Going live, or rolling back, only
     rewrites that page.
   - Pinned pointers (`/embed/<kit>/<guide>/r<N>/`) are for courses that must not change.
   - A preview page (`/preview/<kit>/<guide>/`) is for Lee to approve the next release.
5. **A publish step** (`tools/publish.py`, Python standard library only). It:
   - copies an allowlist of files;
   - removes internal data (review notes, `text_key`);
   - stamps the release number on the title page;
   - records what went out (`release.json`, a ledger of every published file, a snapshot of the sources);
   - moves the pointers.
6. **A way to withdraw a release** that contains a harmful mistake (for example, a wiring error that can damage parts). It
   needs:
   - all pointers, pinned ones included, rewritten to the corrected release;
   - a "this version has been replaced" banner for tabs already open.
7. **Production defaults in the one player:**
   - pick tool off unless `?pick=1`;
   - pictures loaded with `crossOrigin` set, for sandboxed LMS frames;
   - the replaced-version banner.

   That is about 30 lines in total.
8. **Hosting configuration and checks:**
   - `render.yaml` with one caching rule per top-level folder;
   - a site check that Render runs as its build command;
   - a check after each deploy that the live files and headers are right.
9. **One heavy job at a time on this Mac.** A machine-wide lock around `guide.py`, `build_model.py` and `bundle.py`, with
   a memory and disk check first. It took the Mac down on 13 Oct. The disk is at 97%, with 15 GiB free today.

### 2.2 Needed for chapter guides (next)

- **The generator writes several guides from one Full Build run.** Chapter files are written beside the Full Build (or in one
  folder per guide later).
- **One model per kit**, holding every part any of its guides shows.
- **Chapter boundaries are checked**, and there is a map from Full Build step numbers to chapter step numbers.
- **Chapters of a kit are published together from one run**, with a report of what else changed and a check that each
  chapter starts where the previous one ends.

Section 4 has the detail.

### 2.3 What can wait, and what would make it necessary

| Item | Why it can wait | When to do it |
|---|---|---|
| A shared player with version numbers (`/player/1.2.0/`), a format version and `requires` list in `steps.json`, and a compatibility rule | Each release folder already holds the exact player it was checked with, which is the strongest version lock there is. A player fix reaches a guide as that guide's next release | More than about 20 live guides; a player fix that must reach every guide at once; or download size across chapters starts to matter |
| Headless browser checks in GitHub Actions, and a conformance matrix | Untested **[A5]**: a second environment to keep working. Claude runs `_runthrough()` in the built-in browser against the published folder instead | With the shared player |
| Automated pixel-by-pixel comparison of every view on old and new players | Player changes on frozen releases are rare. For now, Claude compares screenshots of a sample of views plus every view with a special feature | With the shared player |
| Stable view ids, and an embed message interface with a version | Only matter inside a SCORM or LTI wrapper. The rule for now: **no `?step=` in LMS embeds** | When completion tracking is wanted |
| Moving the authoring folder into git outside iCloud | Disruptive while sessions are working; it breaks paths and Claude's memory notes (section 3.1). The release snapshots give a history meanwhile | Soon after the first embed, at a quiet moment |
| GitHub pull-request flow and Render pull-request previews | Lee is not reviewing pull requests. A preview is a deployed release that nothing points to yet | Not needed |
| Content-hashed part pictures and logo | Each release's own folder never changes, so a long-open tab already gets the right files | With the shared player |
| SCORM, LTI, xAPI | A plain iframe is enough unless completion tracking or single sign-on is wanted | Section 6.5 |

---

## 3. Target layout

### 3.1 Two folders: authoring stays put, publishing gets its own repository

- **The authoring folder stays where it is for now**, on the Desktop with its kit folders, `tools/`, CAD and videos. Moving
  it has costs:
  - **Claude's memory.** Claude's auto-memory is keyed by the folder path (`~/.claude/projects/-Users-lee-johnson-Desktop-Claude-Cadasio/memory/`).
    It holds "keep step cameras" and the memory limits that crash this Mac, and a moved folder starts with none of it.
  - **Paths.** CLAUDE.md, the READMEs and `Open Prototype.command` name today's paths.
  - **Size.** `MRA_Videos/` is 1.9 GB and must never be committed. `share/` is 80 MB.
- **The published site lives in a new, small, private git repository outside iCloud**, for example
  `~/Code/techbox-guides-site`, pushed to GitHub, which Render deploys.
  - It holds no CAD and uses no Git LFS. That removes a serious trap: an LFS rule such as `*.glb` would also catch the
    published models. If Render did not fetch LFS files, it would serve a 130-byte pointer file as the model, cached for a
    year (failure-modes critique, finding 1).
- **`tools/publish.py` lives in the authoring `tools/`.** It reads a kit folder and writes into the site repository.

When the authoring folder later moves into git (Phase 3):
- copy the memory folder to the new project key, and move the critical rules into CLAUDE.md;
- write `.gitignore` before the first commit (videos, `share/`, `.venv.nosync`, `thumbs/`, `__pycache__`);
- either scope LFS to the CAD folders only (`kits/*/cad/**`, never by extension), or keep the CAD out of git with its sha256
  recorded. GitHub's 100 MiB file limit does not apply to LFS files; the real limit is LFS storage and bandwidth quota;
- move at a time when no other session is running.

### 3.2 The site repository

```
techbox-guides-site/
  render.yaml
  releases.json                     live / preview / pinned / withdrawn / history per guide (written only by publish.py)
  ledger.tsv                        every published file: path, sha256, bytes (append-only)
  tools/check_site.py               Render's build command (Python standard library only)
  hooks/pre-commit                  refuses any commit that changes or removes a ledger line
  sources/<kit>/<guide>/r<N>/       source snapshot per release (not served): guide.py, materials.json,
                                    step-text.json, wire-paths.json, engraved-codes.json, decals.json,
                                    sha256 of the CAD and of tools/*.py
  site/                             the only folder Render serves
    guides/<kit>/<guide>/r<N>/      a frozen release: index.html, js/, vendor/, steps.json, parts/, logo, release.json
    models/<kit>/<sha12>.glb        the kit's model, named by its content; shared by every release that uses it
    embed/<kit>/<guide>/index.html          live pointer
    embed/<kit>/<guide>/r<N>/index.html     pinned pointer
    preview/<kit>/<guide>/index.html        preview page (banner + the release in a frame)
    status/<kit>/<guide>.json               withdrawn releases, read by the replaced-version banner
    index.html                              a plain page; nothing listed
```

**What a release folder holds.** It is copied by allowlist, never by "everything except", so a new authoring file can never
leak:
- `player/player.html` saved as `index.html`;
- `player/js/core.js`, `player/js/player.js` and `player/js/runthrough.js`. `runthrough.js` is the check that matches this
  player (it relies on player internals, runthrough.js:21). The player never loads it, and it is harmless in public;
- `player/vendor/three/**`;
- the guide's steps file, saved as `steps.json`;
- the logo named in `meta.logo`;
- only the `parts/*.png` files that this guide's Parts List names.

**The model** is copied once to `site/models/<kit>/<sha12>.glb`. The published `steps.json` points at that address. The
player uses the `model` value exactly as written (player.js:14 → core.js:69), so this needs no player change. Every chapter
of a kit then shares one download per LMS site. It is on the same site, so no cross-site rules are needed.

**Disk use.** A release is about 5 MB on disk. Git stores identical files once, so an unchanged `vendor/` or player adds
nothing to the repository.

### 3.3 Hosted addresses and caching

Each top-level folder gets exactly one `Cache-Control` rule. Render does not document which rule wins when two match, so the
rules never overlap.

| Address | What it is | Cache-Control |
|---|---|---|
| `/embed/<kit>/<guide>/` | the address given to the LMS: points at the live release | `no-cache` (checked every time; tiny) |
| `/embed/<kit>/<guide>/r<N>/` | a pinned address for one release, for a course that must not change | `no-cache` (so a withdrawal can still redirect it) |
| `/preview/<kit>/<guide>/` | the next release, for Lee to approve | `no-cache` |
| `/status/...` | withdrawn-release list | `no-cache` |
| `/guides/<kit>/<guide>/r<N>/...` | a frozen release | `public, max-age=31536000, immutable` |
| `/models/<kit>/<sha12>.glb` | content-named model | `public, max-age=31536000, immutable` |

- **Teachers only ever get `/embed/...` addresses.** A raw `/guides/.../r<N>/` address is pinned to that release forever and
  cannot be redirected after a withdrawal.
- **Copied addresses.** A student who copies the address bar after the redirect gets the raw address. The replaced-version
  banner covers that case.
- **Do not use `history.replaceState` to show the embed address.** It would change the page's base address, and the part
  pictures, which load later with relative URLs (player.js:413), would then fail.

### 3.4 Pointer and preview pages

**Live or pinned pointer** (written by `publish.py` from `releases.json`):

```html
<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">
<title>TechBox build guide</title>
<script>location.replace('/guides/mra/arm/r3/' + location.search + location.hash);</script>
<noscript><a href="/guides/mra/arm/r3/">Open the build guide</a></noscript>
```

- The target always ends in `/`, so the relative URLs inside the release work.
- The query is passed through (for example `?quality=low`).
- When the shared player arrives (Phase 4), the target becomes `/player/<version>/?guide=...`. The address must then be built
  with `URLSearchParams`. The draft's `'...?guide=mra/ch3-arm/r2' + location.search` produced `?guide=…/r2?step=4`, which
  fails the guide-name check:

  ```js
  const u = new URL('/player/1.2.0/', location.origin);
  new URLSearchParams(location.search).forEach((v, k) => { if (k !== 'guide') u.searchParams.set(k, v); });
  u.searchParams.set('guide', 'mra/arm/r3');
  location.replace(u);
  ```

**Preview page.** A small page with a bar reading "PREVIEW – not yet live for students", and the release in an iframe.
- Lee sees exactly the bytes that will go live, and also sees them inside a frame, as the LMS will.
- No player change is needed.
- Review notes are not on the hosted preview, because they are stripped at publish. Lee reads review notes locally, as today.

### 3.5 The records: `release.json`, `releases.json`, the ledger

**`release.json`** is inside each release folder and is written once. It records facts about the release. The player never
reads it.

```json
{"manifest": 1, "layout": "self-contained",
 "guide": "mra/arm", "kit": "mra", "release": "r3",
 "title": "Mini Robot Arm (MRA)", "subtitle": "Arm",
 "published": "2026-11-02T10:14:00Z", "note": "Step 12 caption reworded (Lee, 2 Nov)",
 "player": {"sha256": {"player.js": "…", "core.js": "…", "index.html": "…"}},
 "steps":  {"sha256": "…", "source_sha256": "…"},
 "model":  {"path": "/models/mra/3f9a1c2e7b4d.glb", "sha256": "…", "bytes": 2130000},
 "sources": {"snapshot": "sources/mra/arm/r3/", "cad_sha256": "…", "tools_sha256": {"stepgen.py": "…"}},
 "checks": {"runthrough": "pass", "camera_diff": "no unasked changes", "by": "Claude, 2 Nov"}}
```

- `layout` tells the self-contained releases of Phase 1 apart from the shared-player releases of Phase 4. Both will live
  under `/guides/` (failure-modes critique, finding 25).
- The model's address appears only once in what the player reads (`steps.json`). `release.json` records it only so that it
  can be checked.

**`releases.json`** is at the repository root and is not served. It is the one record of what is live. `publish.py` edits
it, and every pointer page is generated from it.

```json
{"mra/arm": {"live": "r3", "preview": "r4", "pinned": ["r2"],
             "withdrawn": [{"release": "r1", "replacement": "r2", "reason": "wrong row for the brown wire", "date": "2026-10-30"}],
             "history":   [{"release": "r2", "live_from": "2026-10-30", "live_to": "2026-11-02"}],
             "channels":  {}}}
```

`channels` stays empty until a school needs to be held back on an older release (decision 4).

**`ledger.tsv`** lists every file ever published, with its hash. Only `publish.py` adds to it, and the pre-commit hook refuses
any change to an existing line.

### 3.6 What `publish.py` changes in the published copy of `steps.json`

- It removes `review` and `text_key` from every view and sets `meta.review_notes` to `false`. Internal notes addressed to
  Lee are then not public, whatever URL options anyone adds; `?review=1` now shows an empty switch at most (player.js:856).
- It sets `model` to `/models/<kit>/<sha12>.glb`.
- It adds ` · r3` to `meta.copyright`, which shows on the title page (player.js:22). When a teacher reports a problem, the
  release is on screen.
- It adds `meta.release = {"guide": "mra/arm", "release": "r3"}`, which the replaced-version banner reads.

### 3.7 Versions: now and later

**Now (Phases 1 to 3).**
- The player is frozen inside each release, so a guide cannot meet a player it was not checked with.
- A player fix reaches a guide only when that guide is re-released.
- A **re-release with only the player changed** is how a fix reaches a pinned course. The pin promises fixed content, not
  fixed player bytes (failure-modes critique, finding 4). It still goes through the run-through and a screenshot comparison
  before any pointer moves.

**Later (Phase 4, when triggered): one shared player with version numbers.** This is the draft's design, kept for when it is
needed, with the critiques' corrections:

- **Player releases** go at `/player/<major.minor.patch>/`, never edited.
  - Major = a new content format.
  - Minor = new features, backward compatible.
  - Patch = bug fixes only.
  - Each release carries `PLAYER = {version, format_major, supports: [...]}` and its own `runthrough.js`.
- **The content declares what it needs:**
  - `steps.json` gains `format: {name: "techbox-guide", version: "1.x"}` and a `requires` list, computed from what the
    generator actually wrote (cautions, arrows, close-ups, flip, staged wires, decal shapes...).
  - `build_model.py` writes the model's own `requires` into the model file, because decal types live there (core.js:189)
    and the generator cannot see them (finding 11).
  - `publish.py` combines the two lists into `release.json`.
- **The player checks on load.** It refuses:
  - a different format major;
  - any `requires` entry it does not support, with "This guide needs player 1.3 or later";
  - part ids missing from the model. Today they are skipped silently (core.js:203).
- **Pointers name a player line (`1.2.x`), not an exact version.** A patch that passes the automated checks moves every guide
  on that line. Minor and major versions need a deliberate re-pin.
- **The compatibility rule:**
  1. Additive only within a major: a new optional key means a new minor version and a new feature flag.
  2. Changing what an existing key means needs a new flag or a new major. Hidden rules become data. For example, the wire
     pacing at player.js:571-573 (`vias + 1 === beats`) becomes an explicit `wire_pace: "stops"`.
  3. Support is never removed within a major.
  4. The vocabularies are part of the format:
     - decal item types (an unknown one is silently not drawn, core.js:151-173);
     - Parts List icons (four are hard-coded, player.js:390-395);
     - view kinds;
     - pose and camera forms;
     - the extras in the model;
     - the read-aloud shorthand (player.js:367-369), which should move into the data.
  5. A player reads every `1.x` within its major.
- **Every content URL is resolved against the release folder, in one place,** straight after `steps.json` is fetched:
  `model`, `meta.logo` and every `picture`. Pictures are used at player.js:413, 431, 634 and 667, so patching each use is
  error-prone (finding 10).
- **The guide is named in the address** (`?guide=<kit>/<guide>/r<N>`), and accepted only if it matches
  `^[a-z0-9-]+/[a-z0-9-]+/r\d+$` and lives under `/guides/` on the same site.
- **Embed interface version 1:**
  - outgoing messages `{type: 'techbox-step', v: 1, index, id, name, total}`, plus `techbox-ready`, `techbox-complete` and
    `techbox-error`;
  - incoming `techbox-go` accepts a view id;
  - check `e.origin` as well as `e.source` (player.js:877 checks only the source);
  - stop the duplicate message on resize (player.js:875).

---

## 4. Chapter guides from one Full Build

### 4.1 Why chapters are cut from one Full Build run

The chapters build on one another:
- The arm goes onto R2, R5 and R6 of the base, the claw onto the arm, and the final wiring into the module on the base.
- Riding plugs, wire routes and the previous camera carry from step to step (stepgen.py:553-563: the camera does not swing
  when the previous view is still good).

A chapter written as its own guide would have to replay everything before it anyway. So:
- the Full Build runs once;
- each chapter is a slice of its computed views;
- every step camera in a chapter is identical to the Full Build's.

That keeps the "keep step cameras" rule, and the camera diff can compare chapter views with the matching Full Build views.

### 4.2 How a chapter is defined

- **Mark it in the kit's `guide.py`,** where the chapter begins, for example
  `g.chapter('arm', part='Arm', start_view=..., end_view=..., parts_list=...)`. A chapter runs until the next marker.
- **Existing banners show where the markers would go** (the numbers will move as the guide is edited):

| Kit | Sections | Lines in `guide.py` |
|---|---|---|
| MRA | Electronics test | 596-691 |
| MRA | Rotating base, base plates, controller, electronics (sub-headings, no chapter banner) | 693-815 |
| MRA | Arm | 815-949 |
| MRA | Claw and final wiring | 951-1040 |
| MRA | T1/T2 block | 1047-1058 |
| RCC | The controller | 279-319 |
| RCC | Electronics test | 321-397 |
| RCC | The chassis | 408-448 |
| RCC | Wiring and power | 450-466 |

- **This assumes the curriculum chapters are runs of steps in build order [A3].** Lee confirms the boundaries.
- **`g.chapter` refuses a boundary that splits something that belongs together** (finding 30):
  - a Step N / Step Nc pair;
  - a run of flipped views (30 in the MRA);
  - a staged wire (Steps 98-99);
  - a `put_away` sequence (MRA guide.py:675, 689).

### 4.3 What one run writes

- `steps.json`: the Full Build, as today.
- `steps-<slug>.json` for each chapter. Each chapter contains:
  - a title page, with its own camera (new camera work for Lee);
  - Parts List pages of the parts **new in that chapter**, optionally with a page of "from earlier chapters" (decision 6).
    Today the list is built from every part on screen (stepgen.py:1172-1185);
  - a Start view showing the model as the chapter begins: the visible parts, poses, wires and riding parts at the boundary,
    with `cut=True` so nothing glides in. Its camera is also new;
  - the chapter's steps, with cameras copied exactly from the Full Build;
  - a Completed View with its own camera. Today's is fitted to every part (stepgen.py:1115-1116).
- `chapters.json`, the map. For each chapter: its slug, title, first and last Full Build step, the parts it introduces, and
  for each view its Full Build name and its chapter name.
- **Preview locally** with `player.html?steps=steps-arm.json`. The player already accepts that (player.js:11), so chapters
  need no player change.
- **Separate guides that are not slices** (a deconstruction guide, or "the claw from loose parts") stay separate scripts.
  They need an output-name option, because today the names are fixed (stepgen.py:1213-1214), and they must never shrink the
  model.

### 4.4 Step numbers

- If chapters restart at 1 (decision 6), "Step 12" becomes ambiguous (finding 20).
- Lee can name a step either way: "Arm, Step 12" or the Full Build number. Claude translates using `chapters.json`.
- The step-text spreadsheet (`tools/step_text.py`) stays keyed on the Full Build.
- This goes into the rulebook and CLAUDE.md's "How edits are asked for".

### 4.5 One model per kit

- **One `model.glb` per kit, holding the Full Build's parts.** The Full Build shows a superset of every chapter's parts (MRA:
  108 of 115).
- **Model sync is fed only the Full Build's part list**, never a chapter's (stepgen.py:1218).
  - As a safeguard, the check at stepgen.py:1229 changes from "exactly these parts" to "at least these parts".
  - `build_model.py` keeps the parts shown in `steps.json` (build_model.py:721-741). That stays correct as long as
    `steps.json` is the Full Build.
- **At publish, the model is copied once to `/models/<kit>/<sha12>.glb`.** Every chapter release from that run points at it,
  so a learner moving from one chapter to the next downloads only the next chapter's small `steps.json`.
- **The CAD loads once per run:** one memory peak of about 2 GB, not five.

### 4.6 Part pictures and step text

- **Part pictures:**
  - `parts.html` renders the whole kit's pictures from the Full Build (parts.js:12 reads `steps.json` and `parts.json`,
    which cover every chapter).
  - Each chapter release gets only the pictures its Parts List names.
  - `publish.py` warns if a picture is older than the model it shows. That is a cheap guard against stale pictures. A proper
    record of which model drew them comes in Phase 4 (finding 13).
- **Step text:** one `step-text.json`, keyed on the Full Build (stepgen.py:136-142, 936-963). Chapters inherit the wording,
  so a reworded step can never land on the wrong step in another chapter.

### 4.7 Keeping chapters consistent (failure-modes critique, finding 2)

Any edit regenerates every chapter, and a change early in the build can change cameras later on. Publishing one chapter on
its own would let the published chapters drift apart. So:

- **`publish.py <kit> --chapters` publishes all of a kit's chapters from one run as a batch.**
  - It compares each chapter with its latest release and creates a new release only where the content changed.
  - A colour change rebuilds the model and so changes every chapter, which is correct.
- **It prints a "what else changed" report**: per chapter, the cameras, visible parts, poses, wires and captions that differ
  from the live release.
- **"Go live" moves all changed chapters of the kit together.** Moving one chapter alone needs Lee to accept the differences
  in the others, on purpose.
- **A continuity check runs at go-live:** the live end state of chapter N equals the live Start view of chapter N+1 (visible
  parts, poses, wire routes, riding parts).
- **The Full Build is published alongside the chapters** (decision 6), from the same run.

---

## 5. Release process

### 5.1 How a change Claude makes reaches learners

| # | Who | What |
|---|---|---|
| 1 | Lee | Asks for a change in chat, as today ("Arm, Step 12: ..."). |
| 2 | Claude | Edits `guide.py` or `materials.json`, regenerates, and runs the checks in CLAUDE.md "Checking a change": looks at the changed steps plus one either side, runs `_runthrough()`, diffs every camera against a saved copy, reads the generator log. As today. |
| 3 | Claude | `publish.py mra arm --note "<Lee's words>"` creates the next release (say `r8`), moves `/preview/mra/arm/`, writes the source snapshot and the ledger lines, and prints the links. |
| 4 | Claude | Serves the site folder locally (`serve.py` serves any folder, serve.py:64-69), runs `_runthrough()` against `/guides/mra/arm/r8/`, then commits and pushes the site repository. Render runs `check_site.py` and deploys. |
| 5 | Claude | Post-deploy check: fetches every new file from the live domain and compares its hash; checks one address of each kind for `Cache-Control`, content type and compression. Then tells Lee the preview is ready. |
| 6 | Lee | Opens `/preview/mra/arm/`, and the same embed on a hidden test page in the LMS. |
| 7 | Lee: "go live" | `publish.py --live mra/arm r8`, then push and the post-deploy check (the pointer names r8). **Only on Lee's explicit word.** Claude never moves a live pointer on its own. |

- **Several changes in a day:** release numbers are cheap, and Lee can batch requests into one preview.
- **Chapters:** steps 3 to 7 run for the kit's batch (section 4.7).

### 5.2 Roll back, withdraw, re-release

- **Roll back:** `publish.py --live mra/arm r7`, then push. One guide's pointer changes; nothing else is touched. Learners who
  already have r8 open keep it until they reopen the LMS page.
- **Withdraw** (a harmful mistake): `publish.py --withdraw mra/arm r8 --replacement r9 --reason "..."`. It:
  1. moves `live` if needed;
  2. rewrites every pinned pointer that targets r8 so it redirects to r9;
  3. adds r8 to `/status/mra/arm.json`. Open tabs and copied raw addresses then show "This version has been corrected – reload"
     with a link to `/embed/mra/arm/`. The banner fails silently when offline, as in a bundle;
  4. records the reason.

  The r8 files themselves stay: the site never deletes or edits a release.
- **Player fix:** a player change is its own piece of work. For each guide that should get it:
  1. re-release with unchanged content (`publish.py --player-only`);
  2. run `_runthrough()`;
  3. compare screenshots of the old and new release (every view with a special feature, plus a sample of the rest), and show
     Lee the differences;
  4. go live on Lee's word.

  `_runthrough()` alone cannot see framing, colour, lighting, decals, wire shape or label placement (runthrough.js:7-35),
  hence the screenshots (finding 6).
- **Emergency only: Render's dashboard rollback.** It reverts the whole site, every guide's pointer included. It also turns
  off auto-deploy until someone turns it back on, and does not restore header settings (small-team critique, from Render's
  docs). Use it only when a deploy broke the whole site.

### 5.3 The checks

**`check_site.py`** is Render's build command, standard library only. If it fails, the build fails and Render keeps the
previous deploy live. It checks that:
- every ledger entry exists with the same sha256, so no published file was changed or removed;
- every file under `site/guides` and `site/models` is in the ledger;
- nothing forbidden is under `site/`: `.py`, `.STEP`, `materials.json`, colour atlases, `wire-paths.json`, `thumbs/`, the CAD
  names, `.command` files;
- every `.glb` starts with the `glTF` magic bytes, and no file starts with `version https://git-lfs`;
- no published `steps.json` contains `review` or `text_key`;
- every pointer targets an existing release, every model address in a release exists, and the `releases.json` entries are
  consistent (no live or pinned pointer targets a withdrawn release);
- every release has `index.html`, `js/player.js`, `js/core.js`, `vendor/three/three.module.min.js`, `steps.json` and
  `release.json`, and the hashes in `release.json` match.

**Guards against two sessions publishing at once:**
- `publish.py` refuses a release folder that already exists.
- It runs under the machine-wide lock.
- Releases are published only from the site repository's `main`.
- The pre-commit hook blocks ledger edits.

Two branches both creating `r3` would conflict in `releases.json` and the ledger. Readable `r<N>` numbers are kept rather than
content-hash names (Appendix A).

**Heavy-job lock.** `guide.py`, `build_model.py`, `bundle.py` and `publish.py` take one lock file with Python's `fcntl.flock`
(macOS has no `flock` command). Each run first checks `sysctl vm.swapusage` and free disk space, and stops if either is
low.

**Later, a scheduled link check** (Phase 3). Once a day, fetch every live and pinned pointer and its target files, check the
hashes, and alert on failure. A plain LMS page runs no scripts, so nothing else would notice a broken guide (finding 33).

---

## 6. Hosting on Render and embedding in the LMS

### 6.1 Render set-up

- **A Render static site** in TechBox's existing workspace, deploying the site repository's `main` automatically.
- **Static sites have no service fee.** They count against the workspace's bandwidth and build minutes, so check which plan
  the workspace is on **[A8]**.
- **Never generate on Render.** `build_model.py` peaks near 2 GB and needs the CAD. Ray-test and scoring differences could
  also change an insertion direction or a camera on another machine (stepgen.py:553-563).
- **Each deploy replaces the whole published folder.** That is why the repository keeps every release (append-only).

`render.yaml` (sketch, to be checked on the first deploy):

```yaml
services:
  - type: web
    name: techbox-guides
    runtime: static
    branch: main
    autoDeploy: true
    buildCommand: python3 tools/check_site.py      # checks only; generates nothing
    staticPublishPath: site
    previews: {generation: off}
    domains: [guides.tech-box.io]                  # [A2]
    headers:
      - {path: /*,         name: X-Content-Type-Options,      value: nosniff}
      - {path: /*,         name: Access-Control-Allow-Origin, value: "*"}
      - {path: /*,         name: Referrer-Policy,             value: strict-origin-when-cross-origin}
      - {path: /*,         name: X-Robots-Tag,                value: noindex}          # decision 12
      - {path: /guides/*,  name: Cache-Control, value: "public, max-age=31536000, immutable"}
      - {path: /models/*,  name: Cache-Control, value: "public, max-age=31536000, immutable"}
      - {path: /embed/*,   name: Cache-Control, value: "no-cache"}
      - {path: /preview/*, name: Cache-Control, value: "no-cache"}
      - {path: /status/*,  name: Cache-Control, value: "no-cache"}
```

- **No `X-Frame-Options` and no `frame-ancestors` to begin with.** Framing is then allowed from anywhere. A list of allowed LMS
  sites limits who can frame the guides, not who can fetch them, so it is not access control. Tighten it once the customer
  LMS sites are known, and remember nested content domains such as Blackboard's.
- **Check on the first deploy with `curl -I`, before any teacher gets an address [A6]:**
  - `/guides/*` matches nested paths;
  - `.js` is served as `text/javascript` (module scripts are refused otherwise);
  - `.glb` is served as `model/gltf-binary`;
  - `.glb` and `.json` come back Brotli-compressed. If `.glb` does not, each load costs about 1 MB more;
  - Render adds no `X-Frame-Options` of its own.

  One wrong rule that ever sends `immutable` on a pointer would stay in browsers for a year, so the post-deploy check repeats
  these tests every time.
- **Render's Python [A9].** `check_site.py` assumes Render's static-site build has Python 3. If it does not, run the same
  script as a git pre-push hook instead.

### 6.2 The embed

```html
<iframe src="https://guides.tech-box.io/embed/mra/arm/"
        title="Mini Robot Arm build guide: the arm"
        allow="fullscreen" allowfullscreen loading="lazy"
        style="width:100%;aspect-ratio:16/10;min-height:480px;border:0"></iframe>
```

- `allow="fullscreen"` is needed, or the full-screen button hides itself (player.js:853).
- No clipboard, autoplay or other permissions are needed: read-aloud starts from a click, and the pick tool is off.
- **If the LMS forces a `sandbox` attribute, it needs**
  `sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"`. Without `allow-same-origin`:
  - the frame gets an opaque origin, and every request becomes cross-site. `Access-Control-Allow-Origin: *` covers the
    scripts, steps and model;
  - the step list's Parts List pictures are drawn into a canvas and read back (player.js:667, 672). That throws unless the
    images are loaded with `crossOrigin` set, which is why this is in the Phase 1 player defaults (finding 8);
  - any future use of local storage must be wrapped in try/catch, or it will stop the player.
- **Google Classroom takes links, not iframes.** Use the same `/embed/...` address as a full-page link.
- **One guide per LMS page.** Each embed uses a WebGL context, browsers cap these at about 16, and the player also draws a
  small picture of each of its 211 views in idle time (player.js:712-722).
- **No `?step=` in LMS embeds.** It is a position in the view list (player.js:879), and positions shift when a new release
  goes live: the 14 → 14b round went from 209 to 212 views.

### 6.3 Inside the frame

- **Phones:** the 3D controls take over touch scrolling on the canvas, so a tall frame can trap scrolling of the LMS page.
  Consider a "tap to start" cover with "open in a new tab" below about 700 px. Element full screen has historically not
  worked on iPhone Safari, so test there (finding 23).
- **Reduced motion:** the player does not yet honour `prefers-reduced-motion`. It is a small later fix.
- **Test first in TechBox's real LMS, on the cheapest learner device:** load time, scrolling, full screen, read-aloud, and the
  background drawing of the step pictures.

### 6.4 Messages to the LMS page

- The player already sends `techbox-step` messages to the parent page (player.js:501).
- A plain LMS page runs no scripts, so nothing listens. The messages only matter inside a wrapper TechBox controls (SCORM or
  LTI below).

### 6.5 What SCORM, xAPI and LTI would add, and whether they are needed

| Option | What it adds | What it costs | Needed? |
|---|---|---|---|
| **Plain iframe** | The guide, nothing else. The LMS records at most that the page was viewed | Nothing | **Yes: start here** |
| **SCORM 1.2 "pointer" package** | Completion and last step in the LMS gradebook | A zip per guide, generated by a script: an iframe to `/embed/...` plus a small adapter that turns `techbox-step` and `techbox-complete` into `lesson_location` and `lesson_status`. The zip never changes, and content updates stay central. Needs the embed interface (section 3.7) and a "completed" message. About 1-2 days | Only if completion must show in the gradebook |
| **xAPI / cmi5** | Detailed activity records | A Learning Record Store; LMS support varies | Only for analytics beyond completion |
| **LTI 1.3 with Deep Linking** | Single sign-on launch; teachers pick "MRA – Arm" from a list; grades back to the LMS; signed access if guides go private | A small Render web service (paid, so it does not sleep; about $7+/month) for the launch and key checks. About 1-2 weeks | Only with many schools, private guides, or a wish for teacher pick lists |

---

## 7. Learner isolation and caching

**Why one learner can never affect another:**
- The site is static files. Nothing is computed or stored on the server for a learner.
- The player keeps everything in that browser tab's memory (contract and player reports: no storage, no cookies, no server
  calls).

**Why one release can never affect another:**
- Every release is its own folder, written once and never edited or deleted (enforced by `check_site.py`).
- The only files that change are the pointer pages, the preview pages and the status files. Each guide has its own, so a
  promotion, rollback or withdrawal of one guide touches no other guide's files.
- Chapters of a kit share a model only when their content was built from the same model.

**Why a learner's session stays consistent:**
- After the redirect, every file the open page loads comes from one release (and one content-named model). None of those
  files ever change, so the page can never mix new steps with an old model, as it can today.
- Reopening the LMS page reads the pointer again and picks up the current live release.
- The draft's claim that "a learner who reloads stays on r2" is dropped. Browsers differ on whether a reload keeps the frame's
  last address, and there is no saved position anyway (finding 21).

**Caching:**
- Release and model files are cached for a year, and the browser does not even recheck them. That is safe because they never
  change.
- Pointers are rechecked on every open, which costs about 1 KB.
- **Browsers keep separate caches per top-level site.** A learner using two LMS sites downloads a guide twice. That is
  expected and correct.

**If "resume where I left off" is added later:**
- store it in local storage, keyed by guide and release, holding a view id;
- wrap it in try/catch;
- it works per LMS site and is lost in a sandboxed frame. That is acceptable for a convenience.

Still no cookies and no personal data **[A7]**.

---

## 8. Scaling and cost

**Download per learner.** The figures are from the hosting report; gzip stood in for Brotli.

| Load | Size |
|---|---|
| MRA first load: model 1.0 MB, three.js 0.22 MB, `steps.json` 0.18 MB, code 0.03 MB | about 1.5 MB compressed; up to about 2.5 MB if `.glb` is not compressed |
| Opening the Parts List | plus about 0.9 MB |
| The next chapter of the same kit, on the same LMS site | only its `steps.json` plus its own copy of the player and three.js (about 0.25 MB). The model comes from cache via `/models/` |

**Render [A8]** (prices from the hosting report, after Render's 1 Aug 2026 change; recheck before choosing):
- Hobby: $0, 5 GB a month.
- Pro: $25 a month, 25 GB, about 16,000 MRA first loads.
- Overage: $0.15/GB, about $2-5 per extra 10,000 loads.
- Bandwidth is not the deciding factor; the features of the plan are.
- **Anyone can embed a public guide**, and TechBox pays for that traffic. Anyone can also download `model.glb`, a simplified
  CAD model (decision 3).

**What grows, and what to do about it:**

| What | How it grows | When to act |
|---|---|---|
| Number of guides | Each release adds a few MB on disk. Only changed files grow the repository; a new model is added only when the CAD or `materials.json` changes (about 2 MB) | — |
| Site repository and deploy time | Append-only, so deploys slowly get longer | Past about 1 GB, or when deploys are slow: move `/guides/` and `/models/` to Cloudflare R2 (about $0.015/GB-month, free egress) behind the same domain. Exclude `/embed/`, `/preview/` and `/status/` from edge caching, or purge on promote: Render's deploy purge does not reach Cloudflare (finding 28) |
| Build memory | About 2 GB per kit run on a 16 GB Mac with a nearly full disk. Chapters keep it to one run per kit | With more kits: a dedicated build machine, regenerating every guide on it once and diffing against the published releases before trusting it |
| Reproducibility | Not yet verified byte for byte. Python 3.14.4 from Homebrew can change under `brew upgrade` (finding 29) | Phase 3: build twice and compare; pin Python |
| Checks | Run-throughs grow with guides × player releases | With the shared player: headless checks in parallel |
| Many guides on one player | Re-releasing each guide for a player fix becomes tedious | The trigger for Phase 4 (about 20 live guides) |

**Running costs:**
- Phases 1 to 3: GitHub free tier, plus Render's static site within the workspace's plan.
- Later: an LTI web service at about $7+/month; R2 storage if needed.
- **The real cost is set-up time** (section 9).

---

## 9. Phased roadmap

**Phase 0 – decisions and accounts.** About 1-2 hours of Lee's time; Claude cannot create accounts or enter credentials.
- Decide the domain and the guide slugs (decision 1).
- Create a private GitHub repository for the site, and run `gh auth login` on the Mac.
- Create the Render static site in the existing workspace, and add the DNS record for the domain.
- Make a hidden test page in the LMS.

**Phase 1 – first guides live.** About 2 days of Claude's work, in a window when no other session is editing the player or a
kit.
1. **One player source** (about half a day):
   - `player/` becomes the only copy, and `serve.py` serves it to each kit;
   - the kit copies are deleted;
   - the RCC is checked on the newer player;
   - the production defaults go in: pick tool off unless `?pick=1`, `crossOrigin` on content images, the replaced-version
     banner.
2. **Publishing** (about a day): `publish.py`, `check_site.py`, `render.yaml`, the pointer, preview and status pages, the
   ledger and pre-commit hook, the post-deploy check.
3. **The heavy-job lock** (about an hour).
4. **First releases** (about half a day, plus Lee's testing):
   - publish MRA Full Build r1 and RCC Full Build r1 to preview. The RCC's review notes are stripped, but answer them first
     if they change content;
   - verify the headers on Render;
   - test in the LMS on a real device;
   - go live on Lee's word.
5. **Write the loop down:**
   - in CLAUDE.md: the publish loop, "teachers get only `/embed/` addresses", "no `?step=` in embeds", "go live only on
     Lee's word";
   - in the rulebook: offline bundles do not receive corrections.

**Result:** updating one guide can no longer affect another, and every learner gets a stable guide.

**Phase 2 – chapter guides.** About 2-3 days of Claude's work once Lee has made the chapter decisions, plus Lee's review of
each chapter's title, Start and Completed cameras.
- `g.chapter` markers, with boundary checks.
- One run writes the Full Build, the chapter files and `chapters.json`.
- The model check becomes "at least these parts".
- Per-chapter Parts Lists and Start and Completed views.
- Batch publishing with the "what else changed" report and the continuity check.
- The MRA chapters first, then the RCC's.

**Phase 3 – housekeeping.** About a day, at a quiet time.
- Move the authoring folder into git outside iCloud (section 3.1), with memory copied and CLAUDE.md updated.
- `bundle.py` builds offline copies from a *published* release and the one player source. It stamps the release on the title
  page and in a `<meta>` tag, and adds an entry to a register of bundles handed out (finding 18).
- The scheduled daily link check.
- The reproducibility check, with Python pinned.

**Phase 4 – a shared player with version numbers.** About 4-6 days, only when triggered (section 2.3). Section 3.7 has the
design: `/player/<version>/`, the guide named in the address, format version and `requires` (including the model's own), the
compatibility rule, URLs resolved in one place, view ids from a per-kit ledger, and the embed interface version 1. It also
brings, from the critiques:
- **Generator:** build the model before the steps; write both into a staging folder and swap it in; pair the two by a
  geometry fingerprint, so a colour-only change needs no new steps; and stop `build_model.py` rewriting `steps.json`
  (build_model.py:1019-1023) (finding 12).
- **Pictures:** each picture records which model and player drew it, and is named by part id.
- **Checks:** automated screenshot comparison, and headless checks.

**Phase 5 – LMS depth and growth, as needed.** SCORM pointer packages; LTI 1.3; analytics; access control (signed addresses
after an LTI launch); R2; a build machine; a full Content Security Policy. That last needs hashes for the inline import map
and scripts (player.html:99, 136-141), `wasm-unsafe-eval` for the meshopt decoder, and `data:` images.

Phase 2 does not depend on Phase 4. Chapters ship as Phase 1-style frozen releases.

---

## 10. Decisions for Lee

1. **Domain and guide names**, before the first embed: they cannot be changed once pasted. `guides.tech-box.io`? Slugs such
   as `mra/full-build`, `mra/electronics-test`, `mra/base`, `mra/arm`, `mra/claw`?
2. **Which LMS or LMSs**, and who pastes the embeds (TechBox or teachers). This decides:
   - iframe handling: Moodle needs trusted content, and Google Classroom takes links only;
   - whether SCORM or LTI is ever needed.
3. **Public or private guides.** Public allows a plain static site, but anyone can embed the guides (on TechBox's bandwidth)
   and download the model. Private needs signed addresses, in practice an LTI launch.
4. **Update policy for schools.** Recommended: one live address per guide that Lee moves, plus pinned addresses for a course
   that must not change mid-term. If a school asks to be held back, it gets its own channel (`/embed/<school>/<guide>/`). The
   design allows it at no extra cost, but it is not built until needed.
5. **Who says "go live"**, and whether the preview page plus the hidden LMS test page is the review step. Recommended: Lee
   only.
6. **Chapters:**
   - the exact boundaries (the curriculum may not follow build order **[A3]**);
   - step numbers restarting at 1, or keeping the Full Build numbers;
   - a Parts List of new parts only, or also "from earlier chapters";
   - a "Next: ..." line on the Completed View;
   - whether the Full Build stays published (recommended: yes).
7. **Withdrawals:** agree the replaced-version banner and who can call a withdrawal.
8. **Offline bundles:** still needed (SCORM upload, classrooms without internet)? This decides how much work `bundle.py` gets.
   Bundles never receive corrections.
9. **Tracking:** none, page counts, or completion through SCORM or xAPI. Check the student-privacy obligations **[A7]**.
10. **Retention:** recommended forever for published releases. They are small, and deleting one can break an open tab or a
    pinned course.
11. **Render plan:** which plan TechBox's workspace is on, since the guides' bandwidth counts against it.
12. **Search engines:** recommended `noindex` everywhere. The guides are for the LMS, not for search.
13. **When to move the authoring folder into git outside iCloud.** Until then, the release snapshots are the only history of
    `guide.py`; iCloud keeps no versions.

---

## Appendix A: how the draft and the two critiques were applied

**Taken from the draft:**
- the diagnosis;
- frozen releases with pointers;
- slicing chapters from one Full Build run;
- one superset model per kit;
- the later shared-player design (format version, `requires`, the compatibility rule);
- the LMS and standards analysis.

**Corrected in the draft:**

| Draft claim | Correction |
|---|---|
| Four hypotheses for why the RCC was affected | Settled: no RCC file changed; the links are hand-copying, the shared generator and the shared bundler (section 1.3) |
| Pointer `'…?guide=…/r2' + location.search` | Produces `?guide=…/r2?step=4`, which fails the guide check; build the address with `URLSearchParams` (section 3.4) |
| "A learner who reloads stays on r2" | Browser-dependent, and there is no saved position; dropped |
| Later chapters reuse the cached model | True only if the model has its own content-named address; that is now part of Phase 1 (section 3.2) |
| Temporary file and rename keeps steps and model matched | Each file is atomic but the pair is not: steps are written before the model is rebuilt (stepgen.py:1213 before 1218), then rewritten by build_model.py:1019-1023. Fixed in Phase 4 |
| "RCC has 27 review notes" | 14 distinct notes on 27 of 67 views |
| The STEP file is near GitHub's 100 MiB limit | Not relevant once the file is in LFS; the real limit is LFS quota. In any case, no CAD goes into the site repository |
| `Access-Control-Allow-Origin: *` covers sandboxed frames | Partly: the step-list pictures also need `crossOrigin` (player.js:667, 672) |
| Pictures resolved at player.js:413 | Also used at 431, 634 and 667; resolve every URL in one place |
| The hosting report's "player.js:877 checks the sender" | It checks `e.source`, not `e.origin` |

**Small-team critique: agreed.**
- Ship frozen self-contained releases first, then chapters, and hold the shared player until it is needed.
- Render's build command is the only gate: no GitHub Actions, no Playwright, no pull-request flow.
- A separate small site repository now; the authoring folder moves into git later.
- An allowlist in `publish.py`.
- The model copied to `/models/` for chapter sharing.
- The release number on the title page.
- Pick the domain and content-based slugs first.
- No `?step=` in embeds.
- Account steps are Lee's.
- Check the RCC's move onto the current player.
- A real-device test in the real LMS.
- Write the loop into CLAUDE.md.

**Small-team critique: disagreed.**
- *"Drop pinned `/embed/…/rN/` pointers, `/guides/…/rN/` is already pinned."* Kept. A pinned pointer is `no-cache`, so a
  withdrawal can redirect a pinned course. A raw `/guides/` address can never be redirected.
- *"`runthrough.js` stays out of the release."* It goes in. The check must match the player it tests (runthrough.js:21 relies
  on player internals), and it is harmless in public.
- *"Phase 1 has zero player changes."* Three small production edits are made while consolidating the player anyway: the pick
  tool default, `crossOrigin`, and the replaced-version banner. Without them, a learner opening a full-page link gets the
  pick tool, a sandboxed LMS frame breaks the step list, and a withdrawal cannot reach open tabs.

**Failure-modes critique: agreed.**
- No LFS in the deploy repository, plus the glTF-magic and LFS-pointer checks (finding 1).
- Batch publishing, the "what else changed" report and the continuity check (2).
- The machine-wide lock (3).
- A pin fixes content, not player bytes (4).
- Withdrawal through pointers, a status file and the banner (5).
- Screenshot comparison for player changes (6).
- The `URLSearchParams` fix (7).
- `crossOrigin` and the sandbox flags (8).
- Strip review notes and `text_key` at publish (9).
- Resolve URLs in one place (10).
- The model's own `requires` (11).
- Staged model-then-steps writes and a geometry fingerprint (12).
- A picture freshness warning now and a fingerprint later (13).
- Post-deploy header checks (16).
- The memory and video points about moving folders (17).
- Bundles from published releases, with a register (18).
- Per-school channels as a decision (19).
- The step-number map (20).
- Drop the reload claim (21).
- The copied-address problem (22).
- iPhone full screen (23).
- The `layout` field to tell release kinds apart (25).
- `release.json` records, while pointers pair (26).
- Preview banner and noindex (27).
- Cloudflare edge caching (28).
- The reproducibility check (29).
- Boundary validation (30).
- Chapters before the shared player (31).
- The LFS facts (32).
- The scheduled link check (33).
- Third-party embedding as a decision (34).

**Failure-modes critique: disagreed or scaled down.**
- *Separate git worktrees per session now (3).* Only once the authoring folder is in git. Until then, the lock and "publish
  only from `main`" cover the site repository.
- *Automated pixel comparison as a gate for every player release (6).* Deferred to Phase 4. Player changes on frozen releases
  are rare enough for Claude to compare screenshots and show Lee.
- *Release names by content hash (14).* Kept as `r1, r2, …`: readable for Lee and teachers. A single publisher, the lock and
  ledger conflicts prevent duplicates.
- *Stable view ids now (15).* Deferred; the rule "no `?step=` in embeds" covers the risk until completion tracking is wanted.
- *Calling `history.replaceState` to the embed address (22).* Not in Phase 1: it would break the part pictures' relative URLs.
  The banner and teacher guidance cover the case.
- *Phase 1 releases under `/legacy/` (25).* A `layout` field in `release.json` does the same without a second address scheme.

## Appendix B: assumptions

- **[A2]** The domain `guides.tech-box.io` is a guess from the email domain.
- **[A3]** Curriculum chapters are runs of consecutive steps in Full Build order.
- **[A5]** Headless Chromium could run `_runthrough()` at an acceptable speed. Not tried, hence deferred.
- **[A6]** Render's header globs match nested paths, it Brotli-compresses `.glb` and `.json`, it adds no `X-Frame-Options`,
  and its rule precedence is unknown. All to be checked with `curl -I` before any teacher gets an address.
- **[A7]** Learners may be school-age, so no tracking or personal data by default.
- **[A8]** Render prices and quotas as quoted in the hosting report (2026). Recheck against TechBox's workspace.
- **[A9]** Render's static-site build has Python 3 for `check_site.py`. If not, run it as a pre-push hook.
- LMS embeds are teacher-written HTML with no scripts, so messages to the parent page only matter inside a TechBox wrapper.
- Generation stays on one pinned machine; Render only serves and checks.

## Files read for this plan

All under `/Users/lee-johnson/Desktop/Claude_Cadasio/`:
- `CLAUDE.md`
- `MRA Build Instructions Prototype/player.html`, `js/player.js`, `js/core.js`, `guide.py`, `steps.json`
- `RCC Build Instructions/player.html`, `js/`, `guide.py`, `README.txt`, `steps.json`
- `tools/stepgen.py`, `tools/build_model.py`, `tools/bundle.py`, `tools/serve.py`
- `share/` (listing)

The reader reports (player, pipeline, contract, hosting), the architect's draft and the two critiques were supplied by the
workflow that commissioned this plan.
