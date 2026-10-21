// Authoring tool, never published (publish.py copies only core.js and player.js): the pictures for a guide's 2D PDF
// (tools/make_pdf.py, Lee 21 Oct 2026). Every view that shows the model (the title page, each Step N and Step Nc, the Completed
// View) is drawn as the player draws it, by the player's own renderThumb: its wires, lead lines, arrows, labels and eyes, all at
// one print size and shape. A close-up is framed in the corner farthest from the spot it shows, with its leader and ring, as the
// player shows it on screen. Each picture goes into the kit's pages/<steps file>/ folder (tools/serve.py; not kept in git), with
// pages.json, the list of what was drawn. Parts List pages and note cards are not drawn here: make_pdf.py lays them out itself.
// In the page, for a kit served by tools/serve.py (player.html?steps=<file> for a guide other than steps.json):
//   (0, eval)(await fetch('js/pages.js').then(r => r.text())); _pages()
// It works in the background (a guide of 200 views takes a few minutes); _pages.progress says how far it has got.
window._pages = (() => {
  const ACCENT = '#7fdbff', progress = {running: false, done: 0, total: 0, finished: false, errors: []};
  const steps = new URLSearchParams(location.search).get('steps') || 'steps.json';
  const folder = steps.replace(/\.json$/, '');
  const save = async (name, blob) => {
    const r = await fetch(`/__save/pages/${folder}/${name}`, {method: 'POST', body: blob});
    if (!r.ok) throw new Error(`saving ${name}: ${r.status}`);
  };
  const loaded = img => new Promise(ok => { if (img.complete && img.naturalWidth) ok(); else { img.onload = ok; img.onerror = ok; } });

  // The close-up of a view, as the player built it on screen, framed on the picture (W x H) in the corner farthest from its spot.
  async function drawInset(view, canvas) {
    const P = window._player, st = P.stage, T = st.THREE, I = view.inset, W = canvas.width, H = canvas.height;
    await _dev.show(view.name);
    const img = document.getElementById('insetimg'), cap = document.getElementById('insetcap');
    await loaded(img);
    if (!img.naturalWidth) return;
    const pose = P.poseFor(view, W / H, true), cam = new T.PerspectiveCamera(45, W / H, 1, 10000);
    cam.position.copy(pose.position); cam.lookAt(pose.target); cam.updateMatrixWorld(true);
    const at = st.toWorld(I.target).project(cam), ax = (at.x + 1) / 2 * W, ay = (1 - at.y) / 2 * H;
    const k = W / 1000, pad = 12 * k, border = 7 * k, captionH = cap && cap.textContent ? 34 * k : 0;
    const w = Math.round(W * 0.3), h = Math.round(w * img.naturalHeight / img.naturalWidth);
    const boxW = w + 2 * pad, boxH = h + 2 * pad + captionH, m = 26 * k;
    const corners = [[m, m], [W - boxW - m, m], [m, H - boxH - m], [W - boxW - m, H - boxH - m]];
    const [x, y] = corners.reduce((best, c) => Math.hypot(c[0] + boxW / 2 - ax, c[1] + boxH / 2 - ay) > Math.hypot(best[0] + boxW / 2 - ax, best[1] + boxH / 2 - ay) ? c : best);
    const ctx = canvas.getContext('2d');
    const lx = Math.max(x, Math.min(x + boxW, ax)), ly = Math.max(y, Math.min(y + boxH, ay));
    ctx.strokeStyle = ACCENT; ctx.lineCap = 'round'; ctx.lineWidth = 5 * k;
    ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(ax, ay); ctx.stroke();
    ctx.setLineDash([10 * k, 7 * k]); ctx.beginPath(); ctx.arc(ax, ay, 18 * k, 0, 2 * Math.PI); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#fff'; ctx.strokeStyle = ACCENT; ctx.lineWidth = border;
    ctx.beginPath(); ctx.roundRect(x, y, boxW, boxH, 22 * k); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.beginPath(); ctx.roundRect(x + pad, y + pad, w, h, 10 * k); ctx.clip(); ctx.drawImage(img, x + pad, y + pad, w, h); ctx.restore();
    if (captionH) {
      ctx.fillStyle = '#333'; ctx.font = `600 ${24 * k}px Arial, Helvetica, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(cap.textContent, x + boxW / 2, y + pad + h + captionH / 2 + 2 * k);
    }
  }

  async function run({width = 2000, aspect = 1.72} = {}) {
    if (progress.running) return progress;
    const P = window._player;
    if (!window._dev) (0, eval)(await fetch('js/runthrough.js').then(r => r.text()));
    _dev.freeze();
    const W = width, H = Math.round(width / aspect), drawn = P.views.map((v, i) => [v, i]).filter(([v]) => ['start', 'hover', 'done', 'end'].includes(v.kind));
    Object.assign(progress, {running: true, done: 0, total: drawn.length, finished: false, errors: []});
    const list = [];
    // (the red lead lines are drawn so many pixels wide: as wide, for the picture's size, as on a screen 1000 px wide)
    const lead = P.stage.lineMaterial, leadWidth = lead.linewidth;
    lead.linewidth = leadWidth * W / 1000;
    try {
    for (const [view, i] of drawn) {
      try {
        if (view.inset) await _dev.show(view.name);     // (renderThumb draws the view on screen's state for what it leaves out)
        const canvas = P.renderThumb(i, [W, H]);
        if (view.inset) await drawInset(view, canvas);
        const file = String(i).padStart(3, '0') + '.png';
        await save(file, await new Promise(ok => canvas.toBlob(ok, 'image/png')));
        list.push({index: i, name: view.name, kind: view.kind, file});
      } catch (e) {
        progress.errors.push(`${view.name}: ${e.message}`);
      }
      progress.done += 1;
    }
    } finally {
      lead.linewidth = leadWidth;
    }
    const data = await fetch(steps).then(r => r.json());
    await save('pages.json', new Blob([JSON.stringify({steps, model: data.model, run: (data.meta || {}).run || null, width: W, height: H,
                                                       views: P.views.length, pictures: list}, null, 1)], {type: 'application/json'}));
    Object.assign(progress, {running: false, finished: true});
    return progress;
  }
  const start = opts => { run(opts).catch(e => { progress.errors.push(e.message); progress.running = false; progress.finished = true; }); return progress; };
  start.progress = progress;
  return start;
})();
