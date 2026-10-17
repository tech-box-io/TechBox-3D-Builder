// Authoring tool, never published (publish.py copies only core.js and player.js). A camera from a screenshot Lee sends: renders
// the step with candidate cameras and compares them with the picture (silhouette, then colour), coarse to fine. In the page:
//   (0, eval)(await fetch('js/camsolve.js').then(r => r.text())); _dev.freeze(); _dev.show('Step 27');
//   const T = await _cam.target('thumbs/lee.png', {crop: [0, 0, 1, 0.95], exclude: [[x0, y0, x1, y1]]});   // (fractions: the step bar,
//                                                                                                          //  label text)
//   const d = await _cam.solveDir('Step 27', T);                 // {az, el, dir, score}: view_dir=
//   const f = await _cam.solveFrame('Step 27', T, d.dir);        // {target, radius}: frame=, framing it as in the picture
//   await _cam.snap('name')                                      // the view on screen with its labels, into thumbs/name.png
// Put the picture in the kit's thumbs/ folder first. Match the scene to the picture before solving (a part posed differently
// pulls the framing: _player.stage.setPose(id, pose)), and check the result beside the picture. A screenshot cut off under the
// caption puts the model too high: let it down a little (the battery step of the RCC). A view of the underside renders the same
// whatever the turn-over axis, since the player turns the camera with the model.
window._cam = (() => {
  const P = window._player, st = P.stage, T3 = st.THREE, deg = Math.PI / 180;
  const dirOf = (az, el) => [Math.cos(el * deg) * Math.sin(az * deg), Math.sin(el * deg), Math.cos(el * deg) * Math.cos(az * deg)];
  const azel = d => { const n = Math.hypot(...d); return [Math.atan2(d[0], d[2]) / deg, Math.asin(d[1] / n) / deg]; };

  function features(d, W, H, exclude = []) {
    const mask = new Uint8Array(W * H), rgb = new Float32Array(W * H * 3);
    let n = 0, cx = 0, cy = 0, x0 = W, y0 = H, x1 = 0, y1 = 0;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = y * W + x, r = d[4 * i], g = d[4 * i + 1], b = d[4 * i + 2];
      let ex = false;
      for (const [a0, b0, a1, b1] of exclude) if (x >= a0 * W && x < a1 * W && y >= b0 * H && y < b1 * H) ex = true;
      const blue = b > 200 && b - r > 50 && g > 170;          // label leaders
      const red = r > 200 && g < 70 && b < 70;                 // lead lines
      const fg = !ex && !blue && !red && (r < 236 || g < 236 || b < 236);
      if (fg) { mask[i] = 1; n++; cx += x; cy += y; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      rgb[3 * i] = r / 255; rgb[3 * i + 1] = g / 255; rgb[3 * i + 2] = b / 255;
    }
    return {W, H, mask, rgb, n, cx: cx / Math.max(1, n), cy: cy / Math.max(1, n), box: [x0, y0, x1, y1]};
  }

  async function target(url, {crop = [0, 0, 1, 1], exclude = [], W = 200} = {}) {
    const img = new Image(); img.src = url; await img.decode();
    const sx = crop[0] * img.width, sy = crop[1] * img.height, sw = (crop[2] - crop[0]) * img.width, sh = (crop[3] - crop[1]) * img.height;
    const H = Math.round(W * sh / sw), c = document.createElement('canvas'); c.width = W; c.height = H;
    const ctx = c.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, W, H);
    return features(ctx.getImageData(0, 0, W, H).data, W, H, exclude);
  }

  const index = name => { const i = P.views.findIndex(v => v.name === name); if (i < 0) throw new Error('no view ' + name); return i; };
  let freeAxis = false;                                        // true: a view of the underside turns the model about its own camera's level direction
  function camFor(name, cam) {
    const v = P.views[index(name)], vc = {...v.camera, ...cam};
    if (v.camera.flip && freeAxis) { const h = Math.hypot(vc.dir[0], vc.dir[2]); vc.flip_axis = [vc.dir[0] / h, 0, vc.dir[2] / h]; vc.pivot = vc.target; }
    return vc;
  }
  function withWorld(vc, fn) {
    const q = st.world.quaternion.clone(), p = st.world.position.clone();
    st.setWorld(st.worldFor(vc));
    try { return fn(); } finally { st.world.quaternion.copy(q); st.world.position.copy(p); st.world.updateMatrixWorld(true); }
  }
  function render(name, cam, W, H) {
    const vc = camFor(name, cam);
    return withWorld(vc, () => {
      const pose = st.cameraPose(vc, W / H);
      const {canvas} = st.snapshot(W, H, {setup: c => { c.position.copy(pose.position); c.lookAt(pose.target); c.updateMatrixWorld(true); return null; }});
      return {f: features(canvas.getContext('2d').getImageData(0, 0, W, H).data, W, H), pose, canvas, toWorld: st.toWorld(cam.target ?? vc.target), world: st.world.matrixWorld.clone()};
    });
  }

  function score(T, R) {                                       // after matching centroid and area
    if (!R.n) return -1;
    const s = Math.sqrt(T.n / R.n);
    let inter = 0, err = 0;
    for (let y = 0; y < T.H; y++) for (let x = 0; x < T.W; x++) {
      if (!T.mask[y * T.W + x]) continue;
      const rx = Math.round((x - T.cx) / s + R.cx), ry = Math.round((y - T.cy) / s + R.cy);
      if (rx < 0 || ry < 0 || rx >= R.W || ry >= R.H || !R.mask[ry * R.W + rx]) continue;
      inter++;
      const a = 3 * (y * T.W + x), b = 3 * (ry * R.W + rx);
      err += Math.abs(T.rgb[a] - R.rgb[b]) + Math.abs(T.rgb[a + 1] - R.rgb[b + 1]) + Math.abs(T.rgb[a + 2] - R.rgb[b + 2]);
    }
    return inter / (2 * T.n - inter) - 0.25 * (inter ? err / inter / 3 : 1);
  }

  async function solveDir(name, T, {az = null, el = null, span = 180, flip = null} = {}) {
    const v = P.views[index(name)], below = flip ?? !!v.camera.flip, cam0 = v.camera;
    const W = T.W, H = T.H, tryOne = (a, e) => ({az: a, el: e, score: score(T, render(name, {dir: dirOf(a, e), target: cam0.target, radius: cam0.radius}, W, H).f)});
    let best = {score: -2}, results = [];
    const els = below ? [-75, -65, -55, -45, -35, -25, -15, -5] : [5, 15, 25, 35, 45, 55, 65, 75];
    const az0 = az ?? 0;
    for (let a = az0 - span; a < az0 + span; a += 10) for (const e of (el == null ? els : [el - 10, el, el + 10])) {
      const r = tryOne(a, e); results.push(r); if (r.score > best.score) best = r;
    }
    for (const step of [3, 1, 0.4]) {
      const c = best;
      for (let da = -3; da <= 3; da++) for (let de = -3; de <= 3; de++) {
        if (!da && !de) continue;
        const r = tryOne(c.az + da * step, c.el + de * step); if (r.score > best.score) best = r;
      }
    }
    results.sort((a, b) => b.score - a.score);
    return {...best, dir: dirOf(best.az, best.el).map(x => +x.toFixed(4)), runnersUp: results.slice(0, 5).map(r => [r.az, r.el, +r.score.toFixed(3)])};
  }

  async function solveFrame(name, T, dir, {iters = 4} = {}) {
    let cam = {dir, target: [...P.views[index(name)].camera.target], radius: P.views[index(name)].camera.radius};
    const W = T.W, H = T.H, half = Math.tan((P.data ? P.data.fov : 45) / 2 * deg);
    for (let k = 0; k < iters; k++) {
      let {f: R, pose} = render(name, cam, W, H);
      cam.radius = cam.radius / Math.sqrt(T.n / R.n);
      ({f: R, pose} = render(name, cam, W, H));
      const dist = pose.position.distanceTo(pose.target), px = 2 * dist * half / H;
      const fwd = pose.target.clone().sub(pose.position).normalize(), right = fwd.clone().cross(new T3.Vector3(0, 1, 0)).normalize(), up = right.clone().cross(fwd).normalize();
      const shift = right.multiplyScalar(-(T.cx - R.cx) * px).add(up.multiplyScalar((T.cy - R.cy) * px));
      const tw = pose.target.clone().add(shift), vc = camFor(name, cam), tm = withWorld(vc, () => st.fromWorld(tw));
      cam.target = [tm.x, tm.y, tm.z];
    }
    const {f: R} = render(name, cam, W, H);
    return {target: cam.target.map(x => +x.toFixed(1)), radius: +cam.radius.toFixed(1), score: +score(T, R).toFixed(3), offset: [+(T.cx - R.cx).toFixed(1), +(T.cy - R.cy).toFixed(1)], area: +(R.n / T.n).toFixed(3)};
  }

  async function save(name, cam, W, H, file) {
    const {canvas} = render(name, cam, W, H);
    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
    return (await fetch(`/__save/thumbs/${file}.png`, {method: 'POST', body: blob})).status;
  }

  async function snap(name, {scale = 1} = {}) {             // the 3D view on screen and its labels (the #overlay SVG), as a picture in thumbs/
    st.invalidate(); st.frame(0, false); st.invalidate(); st.frame(0, false);
    const src = st.renderer.domElement, W = src.width, H = src.height, c = document.createElement('canvas');
    c.width = Math.round(W * scale); c.height = Math.round(H * scale);
    const ctx = c.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height); ctx.drawImage(src, 0, 0, c.width, c.height);
    const ov = document.getElementById('overlay');
    if (ov && ov.children.length) {
      const clone = ov.cloneNode(true), r = ov.getBoundingClientRect(), cr = src.getBoundingClientRect();
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg'); clone.setAttribute('width', r.width); clone.setAttribute('height', r.height);
      const a = ov.querySelectorAll('*'), b = clone.querySelectorAll('*');
      a.forEach((el, k) => { const cs = getComputedStyle(el); b[k].setAttribute('style', ['fill', 'stroke', 'stroke-width', 'font-family', 'font-size', 'font-weight', 'stroke-dasharray', 'paint-order', 'opacity', 'stroke-linecap'].map(p => `${p}:${cs.getPropertyValue(p)}`).join(';')); });
      const img = new Image();
      await new Promise((ok, bad) => { img.onload = ok; img.onerror = bad; img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(new XMLSerializer().serializeToString(clone)); });
      const k = c.width / cr.width;
      ctx.drawImage(img, (r.left - cr.left) * k, (r.top - cr.top) * k, r.width * k, r.height * k);
    }
    const blob = await new Promise(r => c.toBlob(r, 'image/png'));
    return (await fetch(`/__save/thumbs/${name}.png`, {method: 'POST', body: blob})).status;
  }
  return {dirOf, azel, target, render, score, solveDir, solveFrame, save, snap, set freeAxis(v) { freeAxis = v; }};
})();
'camsolve ready';
