// The judge's player tools (21 Oct 2026). A steps copy is put into the kit's thumbs/ through tools/serve.py
// (curl -X POST --data-binary @copy.json http://localhost:8793/__save/thumbs/judge43_low.json); then, in a tab on any missing page of
// the kit's server (a fresh window: http://localhost:8793/judge43-blank), the player is written in with fetch('steps.json') answered
// from that copy:
//   const which = 'low', html = await fetch('/player.html', {cache: 'no-cache'}).then(r => r.text());
//   const patch = `<script>(()=>{const f=window.fetch.bind(window);window.fetch=(u,o)=>{const s=typeof u==='string'?u:(u&&u.url)||'';
//     if(/(^|\\/)steps\\.json(\\?|$)/.test(s))return f('thumbs/judge43_${which}.json',o);return f(u,o);};})();<\/script>`;
//   document.open(); document.write(html.replace(/<head>/i, '<head>' + patch)); document.close();
// then (after load) eval js/runthrough.js, _dev.freeze(), and these. Delete the copies and pictures from thumbs/ afterwards.

// Where a part is on screen through a view's motion: its highest pixel, its x range, and the share of it behind the caption box.
window.topOf = function (id, ts, view = 'Step 43c') {
  const st = _player.stage, T = st.THREE, o = st.parts.get(id), src = st.renderer.domElement, cr = src.getBoundingClientRect();
  _dev.show(view, 0);
  const cap = document.getElementById('instructions').getBoundingClientRect(), out = [];
  for (const t of ts) {
    _dev.show(view, t); st.invalidate(); st.frame(0, false);
    o.updateMatrixWorld(true);
    let top = 1e9, x0 = 1e9, x1 = -1e9, under = 0, n = 0;
    o.traverse(m => { if (!m.isMesh) return; const p = m.geometry.attributes.position, v = new T.Vector3();
      for (let i = 0; i < p.count; i += 7) { v.fromBufferAttribute(p, i).applyMatrix4(m.matrixWorld).project(st.camera);
        const x = (v.x + 1) / 2 * cr.width, y = (1 - v.y) / 2 * cr.height; n++;
        if (y < top) top = y; x0 = Math.min(x0, x); x1 = Math.max(x1, x);
        if (x > cap.left - cr.left && x < cap.right - cr.left && y < cap.bottom - cr.top) under++; } });
    out.push([t, Math.round(top), Math.round(x0), Math.round(x1), Math.round(100 * under / n)]);
  }
  return {canvas: [cr.width, cr.height], caption: [cap.left - cr.left, cap.top - cr.top, cap.right - cr.left, cap.bottom - cr.top], rows: out};
};

// A view at several moments, cut to one rectangle of the canvas (CSS px), drawn at pixel ratio pr, into thumbs/judge43_<name>.png.
window.gridz = async function (name, ts, rect, cols = 3, view = 'Step 43c', pr = 2) {
  const st = _player.stage, src = st.renderer.domElement, [rx, ry, rw, rh] = rect.map(v => v * pr);
  const old = st.renderer.getPixelRatio(), cr = src.getBoundingClientRect();
  st.renderer.setPixelRatio(pr); st.renderer.setSize(cr.width, cr.height, false);
  const rows = Math.ceil(ts.length / cols), c = document.createElement('canvas');
  c.width = cols * rw; c.height = rows * rh;
  const ctx = c.getContext('2d');
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height);
  for (let i = 0; i < ts.length; i++) {
    _dev.show(view, ts[i]);
    st.invalidate(); st.frame(0, false); st.invalidate(); st.frame(0, false);
    const x = (i % cols) * rw, y = Math.floor(i / cols) * rh;
    ctx.drawImage(src, rx, ry, rw, rh, x, y, rw, rh);
    ctx.strokeStyle = '#888'; ctx.lineWidth = 1; ctx.strokeRect(x + 0.5, y + 0.5, rw - 1, rh - 1);
    ctx.fillStyle = '#000'; ctx.font = 'bold 26px Arial'; ctx.fillText(name + ' t ' + ts[i], x + 10, y + rh - 12);
  }
  st.renderer.setPixelRatio(old); st.renderer.setSize(cr.width, cr.height, false); st.invalidate(); st.frame(0, false);
  const blob = await new Promise(r => c.toBlob(r, 'image/png'));
  return (await fetch('/__save/thumbs/judge43_' + name + '.png', {method: 'POST', body: blob})).status;
};
