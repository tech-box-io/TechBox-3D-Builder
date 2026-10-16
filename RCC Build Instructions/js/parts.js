// Part-image tool: renders one picture per part in the same look as the build guide, for the parts
// list ("recipe") in the LMS. Reads parts.json (written by guide.py). Saves into the kit's parts/
// folder when opened through tools/serve.py; otherwise offers the pictures as a single zip download.
const {createStage, THREE} = await import('./core.js' + new URL(import.meta.url).search);   // (the same fresh copy as parts.js)

const $ = id => document.getElementById(id);
const params = new URLSearchParams(location.search);
const SIZE = Math.max(128, Math.min(2048, +(params.get('size') || 500)));
const TRANSPARENT = params.get('bg') !== 'white';
const HOUSE = new THREE.Vector3(-0.5417, 0.6428, -0.5417);            // the guide's three-quarter view

const [steps, list] = await Promise.all(['steps.json', 'parts.json'].map(f => fetch(f, {cache: 'no-cache'}).then(r => r.json())));
const stage = await createStage($('stage'), {modelUrl: steps.model, fov: steps.fov, interactive: false, pixelRatioCap: 1});
const slug = name => name.trim().replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '');

// A flat panel is best shown face-on (slightly turned so its thickness reads), from the side that
// carries its engraved code. Everything else gets the guide's three-quarter view.
function viewFor(part, object) {
  const roll = v => part.view && part.view.roll ? {dir: v.dir, up: v.up.clone().applyAxisAngle(v.dir, THREE.MathUtils.degToRad(part.view.roll))} : v;
  if (part.view && part.view.dir) return roll({dir: new THREE.Vector3(...part.view.dir).normalize(), up: new THREE.Vector3(...(part.view.up || [0, 1, 0]))});
  const box = object.userData.box, size = box.getSize(new THREE.Vector3());
  const dims = [size.x, size.y, size.z], thin = dims.indexOf(Math.min(...dims));
  const mid = dims.slice().sort((a, b) => a - b)[1];
  if (dims[thin] > 0.25 * mid) return roll({dir: HOUSE.clone(), up: new THREE.Vector3(0, 1, 0)});
  const normal = new THREE.Vector3().setComponent(thin, 1);
  // which face has the engraving? (its dark "ink" faces sit just under that surface)
  const ink = new THREE.Box3(); let hasInk = false;
  object.traverse(o => { if (o.isMesh && o.material === stage.materials.get('ink')) { ink.expandByObject(o); hasInk = true; } });
  const centre = box.getCenter(new THREE.Vector3());
  if (hasInk && ink.getCenter(new THREE.Vector3()).getComponent(thin) < centre.getComponent(thin)) normal.negate();
  else if (!hasInk && normal.dot(HOUSE) < 0) normal.negate();
  // "up" for the picture: upright panels keep the model's up; a panel lying flat is turned so its engraved
  // code reads across (codes are wider than tall), or failing that so its long side runs across.
  const inPlane = [0, 1, 2].filter(a => a !== thin);
  let across = thin === 1 ? (size.x >= size.z ? 0 : 2) : inPlane.find(a => a !== 1);
  if (thin === 1 && hasInk) { const t = ink.getSize(new THREE.Vector3()); across = t.x >= t.z ? 0 : 2; }
  const upAxis = inPlane.find(a => a !== across);
  const up = new THREE.Vector3().setComponent(upAxis, upAxis === 1 ? 1 : -1);
  const right = new THREE.Vector3().crossVectors(up, normal).normalize();
  return roll({dir: normal.clone().addScaledVector(right, 0.28).addScaledVector(up, 0.22).normalize(), up});
}

function render(part) {
  const object = stage.parts.get(part.ids[0]);
  if (!object) return null;
  const {dir, up} = viewFor(part, object);
  // a part that comes with others fitted (a motor with its horn) is pictured with them
  const shown = [...new Set([part.ids[0], ...(part.picture_ids || []), ...(part.with || [])])].filter(id => stage.parts.has(id));
  const poses = part.poses || {};                       // (pieces laid out as in a step: an extension wire's two ends)
  const box = stage.boundsOf(shown, poses);
  for (const w of part.wires || []) for (const p of w.pts) box.expandByPoint(new THREE.Vector3(...p));   // (a wire drawn in the picture: a breadboard wire)
  const centre = box.getCenter(new THREE.Vector3());
  // camera distance at which every corner of the part's box is inside the picture (a long part pointing at the camera needs more room)
  const tanHalf = Math.tan(THREE.MathUtils.degToRad((steps.fov || 45) / 2)), corner = new THREE.Vector3();
  let distance = 0;
  for (let k = 0; k < 8; k++) {
    corner.set(k & 1 ? box.max.x : box.min.x, k & 2 ? box.max.y : box.min.y, k & 4 ? box.max.z : box.min.z).sub(centre);
    const depth = corner.dot(dir);
    distance = Math.max(distance, depth + corner.addScaledVector(dir, -depth).length() / tanHalf);
  }
  const {canvas} = stage.snapshot(SIZE, SIZE, {transparent: TRANSPARENT, setup: cam => {
    stage.setVisible(shown); for (const id of shown) stage.setOffset(id, poses[id] || [0, 0, 0]); stage.setLeadLines([]); stage.setMarks([]);
    stage.setWires((part.wires || []).map((w, k) => ({id: `${part.name} ${k}`, colour: w.colour, radius: w.radius, pts: new Float32Array(w.pts.flat()), fade: null})));
    cam.up.copy(up); cam.position.copy(centre).addScaledVector(dir, distance * 1.06); cam.lookAt(centre); cam.updateMatrixWorld(true);
    // light from over the camera's left shoulder, so the face being shown is the bright one
    stage.setLight(dir.clone().addScaledVector(up, 0.45).addScaledVector(new THREE.Vector3().crossVectors(up, dir).normalize(), -0.35));
    return null;
  }});
  return canvas;
}

const toBlob = canvas => new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
const results = [];
for (const part of list.parts) {
  const canvas = render(part);
  if (!canvas) continue;
  const file = slug(part.name) + '.png';
  const blob = await toBlob(canvas);
  results.push({name: part.name, qty: part.qty, file, blob});
  const tile = document.createElement('figure');
  const img = new Image(); img.src = URL.createObjectURL(blob); img.alt = part.name;
  const cap = document.createElement('figcaption'); cap.textContent = part.qty > 1 ? `${part.name}  ×${part.qty}` : part.name;
  const link = document.createElement('a'); link.href = img.src; link.download = file; link.textContent = file;
  tile.append(img, cap, link); $('gallery').appendChild(tile);
}
const manifest = {kit: list.meta.title, part: list.meta.part, image_size: SIZE, parts: results.map(r => ({name: r.name, quantity: r.qty, image: r.file}))};
const csv = 'name,quantity,image\n' + results.map(r => `"${r.name.replace(/"/g, '""')}",${r.qty},${r.file}`).join('\n') + '\n';

// ---- save into the kit folder (local server) or hand over a zip (anywhere else)
async function saveToFolder() {
  const put = (path, body) => fetch('/__save/parts/' + path, {method: 'POST', body}).then(r => { if (!r.ok) throw new Error(r.status); });
  for (const r of results) await put(r.file, r.blob);
  await put('parts.json', JSON.stringify(manifest, null, 1));
  await put('parts.csv', csv);
}
const crcTable = new Uint32Array(256).map((_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
const crc32 = bytes => { let c = 0xFFFFFFFF; for (let i = 0; i < bytes.length; i++) c = crcTable[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
async function zip(files) {                  // stored (no compression): PNGs are already compressed
  const enc = new TextEncoder(), chunks = [], central = []; let offset = 0;
  for (const f of files) {
    const name = enc.encode(f.name), data = new Uint8Array(await f.blob.arrayBuffer()), crc = crc32(data);
    const head = new DataView(new ArrayBuffer(30));
    head.setUint32(0, 0x04034b50, true); head.setUint16(4, 20, true); head.setUint32(14, crc, true); head.setUint32(18, data.length, true); head.setUint32(22, data.length, true); head.setUint16(26, name.length, true);
    chunks.push(new Uint8Array(head.buffer), name, data);
    const cen = new DataView(new ArrayBuffer(46));
    cen.setUint32(0, 0x02014b50, true); cen.setUint16(4, 20, true); cen.setUint16(6, 20, true); cen.setUint32(16, crc, true); cen.setUint32(20, data.length, true); cen.setUint32(24, data.length, true); cen.setUint16(28, name.length, true); cen.setUint32(42, offset, true);
    central.push(new Uint8Array(cen.buffer), name);
    offset += 30 + name.length + data.length;
  }
  const size = central.reduce((a, c) => a + c.length, 0), end = new DataView(new ArrayBuffer(22));
  end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true); end.setUint32(12, size, true); end.setUint32(16, offset, true);
  return new Blob([...chunks, ...central, new Uint8Array(end.buffer)], {type: 'application/zip'});
}
$('zip').onclick = async () => {
  const blob = await zip([...results.map(r => ({name: r.file, blob: r.blob})), {name: 'parts.json', blob: new Blob([JSON.stringify(manifest, null, 1)])}, {name: 'parts.csv', blob: new Blob([csv])}]);
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = slug(`${list.meta.title} ${list.meta.part} parts`) + '.zip'; a.click();
};
$('status').textContent = `${results.length} part images at ${SIZE} × ${SIZE} px${TRANSPARENT ? ', transparent background' : ''}.`;
// Only the standard pictures are written to the kit folder; a trial size or background is a preview.
if (params.has('size') || params.has('bg')) $('status').textContent += ' Preview only, not saved to the parts folder; use the zip button.';
else if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
  try { await saveToFolder(); $('status').textContent += ' Saved to the parts folder (with parts.json and parts.csv).'; }
  catch (e) { $('status').textContent += ' Could not save to the folder from here; use the zip button.'; }
}
window._parts = {results: results.map(r => ({name: r.name, qty: r.qty, file: r.file, bytes: r.blob.size})), manifest};
