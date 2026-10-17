// Run-through check for the player: every view forwards (animated to its end) and backwards, comparing what is on
// screen with steps.json. Paste into the page (it defines window._runthrough and returns its result as JSON).
window._runthrough = () => {
  const P = window._player, st = P.stage, T = st.THREE, problems = [], n = P.views.length;
  const m = new T.Matrix4(), v = new T.Vector3();
  const at = (pose, p) => v.copy(p).applyMatrix4(st.poseMatrix(pose || null, m)).clone();
  const check = (i, tag) => {
    const view = P.views[i];
    for (let k = 0; k < 3; k++) P.frame(performance.now() + 1e6 + k);
    const shown = [...st.parts].filter(([, o]) => o.visible).map(([id]) => id).sort().join();
    const want = (view.kind === 'card' ? [] : [...view.visible]).sort().join();
    if (shown !== want) problems.push(`${tag} ${view.name}: visible parts differ`);
    if (view.kind !== 'card') for (const id of view.visible) {
      const o = st.parts.get(id); if (!o) { problems.push(`${tag} ${view.name}: ${id} is not in the model`); continue; }
      const c = o.userData.sphere.center, far = c.clone().add(new T.Vector3(10, 20, 30));
      const here = o.userData.pose, there = view.offsets[id];
      if (at(here, c).distanceTo(at(there, c)) > 0.05 || at(here, far).distanceTo(at(there, far)) > 0.1) problems.push(`${tag} ${view.name}: ${id} is not where the view puts it`);
    }
    let red = 0, tubes = 0;
    st.scene.traverse(o => { if (o.isLine2 && o.material.color.getHex() === 0xff0000) red++; });
    st.scene.traverse(o => { if (o.isMesh && o.visible && o.parent === st.wireGroup && o.geometry.index && o.material.uniforms && o.frustumCulled === false) tubes++; });
    const wantLines = view.kind === 'hover' ? (view.guides || []).length : 0;
    if (red !== wantLines) problems.push(`${tag} ${view.name}: ${red} lead lines, expected ${wantLines}`);
    const wantWires = view.kind === 'card' ? 0 : Object.keys(view.wires || {}).length;
    if (tubes !== wantWires) problems.push(`${tag} ${view.name}: ${tubes} wires drawn, expected ${wantWires}`);
    const texts = document.querySelectorAll('#overlay text').length, eyes = document.querySelectorAll('#overlay g').length;
    const wantTexts = view.kind === 'hover' ? (view.labels || []).length : 0, wantEyes = view.kind === 'hover' ? (view.eye || []).length : 0;
    if (texts !== wantTexts || eyes !== wantEyes) problems.push(`${tag} ${view.name}: ${texts} labels and ${eyes} eyes, expected ${wantTexts} and ${wantEyes}`);
    const arrows = st.arrows.children.length, wantArrows = view.kind === 'hover' ? (view.arrows || []).length : 0;
    if (arrows !== wantArrows) problems.push(`${tag} ${view.name}: ${arrows} arrows, expected ${wantArrows}`);
    if (document.getElementById('inset').hidden !== !view.inset) problems.push(`${tag} ${view.name}: the close-up picture is ${view.inset ? 'missing' : 'shown'}`);
    const caution = view.kind === 'card' ? document.getElementById('cardcaution') : document.getElementById('caution');
    if (caution.hidden !== !view.caution) problems.push(`${tag} ${view.name}: the caution is ${view.caution ? 'missing' : 'shown'}`);
    if (view.parts && document.getElementById('partsview').hidden) problems.push(`${tag} ${view.name}: the parts list is not shown`);
  };
  P.go(0, false); check(0, 'fwd');
  for (let i = 1; i < n; i++) { P.go(i, true); check(i, 'fwd'); }
  for (let i = n - 2; i >= 0; i--) { P.go(i, true); check(i, 'back'); }
  for (let i = 0; i < n; i += 3) { P.go(i, false); check(i, 'jump'); }
  return {views: n, problems: problems.length, first: problems.slice(0, 12)};
};

// Helpers for looking at a guide by hand from a script (the browser pane pauses animation when it is hidden, and a
// running animation would fight a script, so freeze() stops the page's own frame loop and frames are drawn on request).
//   _dev.freeze()                 stop the page's own animation loop (call once after the page has loaded)
//   _dev.show('Step 12')          go to that view as if "next" had been pressed on the one before, and finish the animation
//   _dev.show('Step 12c', 0.5)    the same, stopped part of the way through the animation (0..1)
//   _dev.look('NAUO45', [1, 0.6, 0.4], 2)   then put the camera on one part: direction to look from, and how wide (1 = tight)
//   await _dev.card()             the guide's picture for its card on the website: its Completed View, 1440 x 900, saved through
//                                 tools/serve.py into the kit's cards/<steps file>.webp (publish.py copies it into the release)
window._dev = {
  async card() {
    const P = window._player, i = P.views.findIndex(v => v.kind === 'end'), W = 1440, H = 900;
    if (i < 0) throw new Error('this guide has no Completed View to picture');
    const big = P.renderThumb(i, [2 * W, 2 * H]);              // (drawn large, then cut to the model with a margin, so every card is filled)
    const d = big.getContext('2d').getImageData(0, 0, big.width, big.height).data;
    let x0 = big.width, y0 = big.height, x1 = 0, y1 = 0;
    for (let y = 0; y < big.height; y++) for (let x = 0; x < big.width; x++) {
      const k = 4 * (y * big.width + x);
      if (d[k] < 245 || d[k + 1] < 245 || d[k + 2] < 245) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    if (x1 < x0) throw new Error('the Completed View came out empty: nothing to picture');
    let w = (x1 - x0) * 1.12, h = (y1 - y0) * 1.12;              // (a 6% margin all round, then widened or heightened to the card's shape)
    if (w / h < W / H) w = h * W / H; else h = w * H / W;
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, canvas = document.createElement('canvas');
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(big, cx - w / 2, cy - h / 2, w, h, 0, 0, W, H);
    const blob = await new Promise(r => canvas.toBlob(r, 'image/webp', 0.9));
    const steps = (new URLSearchParams(location.search).get('steps') || 'steps.json').replace(/\.json$/, '');
    const r = await fetch(`/__save/cards/${steps}.webp`, {method: 'POST', body: blob});
    if (!r.ok) throw new Error(`saving the card picture failed: ${r.status}`);
    const model = (await fetch(`${steps}.json`, {cache: 'no-cache'}).then(x => x.json())).model.split('?v=')[1] || '';
    const n = await fetch(`/__save/cards/${steps}.json`, {method: 'POST', body: JSON.stringify({model, made: new Date().toISOString()})});   // (the model it shows: publish.py checks it)
    if (!n.ok) throw new Error(`saving the card's record failed: ${n.status}`);
    return `cards/${steps}.webp (${Math.round(blob.size / 1024)} kB)`;
  },
  freeze() { window.requestAnimationFrame = () => 0; },
  show(name, k) {
    const P = window._player, i = P.views.findIndex(v => v.name === name);
    if (i < 0) throw new Error('no view called ' + name);
    P.go(Math.max(0, i - 1), false); P.frame(performance.now() + 1e6);
    P.go(i, true);
    const t = performance.now(), v = P.views[i];
    const stops = id => v.paths && v.paths[id] ? (v.path_stops && v.path_stops[id]) || v.paths[id] : v.stops || v.path;   // (as the player counts them)
    const beats = (v.kind === 'done' || v.wiggle) && v.moving && v.moving.length ? Math.max(1, ...v.moving.map(id => stops(id).length - 1)) : 1;
    const at = k == null ? 1e6 : k * 800 * beats;
    P.frame(t + at); P.stage.invalidate(); P.frame(t + at);
    return {index: i, kind: v.kind, caption: v.caption, moving: v.moving, lines: (v.guides || []).length, labels: (v.labels || []).map(l => l.text), review: v.review || null};
  },
  look(id, dir, wide = 1.6) {
    const st = window._player.stage, o = st.parts.get(id), c = st.toWorld(o.userData.centre);       // (dir in assembly space, as the model is shown)
    const d = new st.THREE.Vector3(...dir).normalize().applyQuaternion(st.world.quaternion);
    st.camera.position.copy(c).addScaledVector(d, o.userData.sphere.radius * wide / Math.sin(Math.PI / 8));
    st.controls.target.copy(c); st.camera.lookAt(c);
    st.invalidate(); st.frame(0, false); st.invalidate(); st.frame(0, false);
  },
};
