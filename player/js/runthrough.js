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
window._dev = {
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
