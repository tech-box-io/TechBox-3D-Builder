// Step-by-step build guide player. Reads steps.json (written by guide.py) and plays its views:
// "Step N" shows the new part hovering with red lead lines and labels, "Step Nc" shows it seated.
const {createStage, THREE} = await import('./core.js' + new URL(import.meta.url).search);   // (the same fresh copy as player.js)

const $ = id => document.getElementById(id);
const params = new URLSearchParams(location.search);
const ACCENT = '#7fdbff';                    // label underline, leader and anchor ring
const STEP_MS = 800;                         // every transition, as in the published guides
// A part taken off fades out once it has slid out, over a beat of its own, as the published take-aparts do (Lee, 18 Oct 2026:
// slower and smoother than a fade inside the slide); it starts a little before the slide comes to rest, so nothing waits.
const FADE_MS = 800, FADE_OVERLAP_MS = 150;
const fadeCurve = u => 0.5 + 0.5 * Math.cos(Math.PI * Math.min(1, Math.max(0, u)));   // 1 -> 0, gently at both ends

// Always the latest steps (the model URL inside carries its own version). ?steps= may name another steps file in this folder, nothing else.
const stepsFile = /^[\w.-]+\.json$/.test(params.get('steps') || '') ? params.get('steps') : 'steps.json';
const data = await fetch(stepsFile, {cache: 'no-cache'}).then(r => { if (!r.ok) throw new Error(`${stepsFile}: ${r.status}`); return r.json(); });
const views = data.views;
const stage = await createStage($('stage'), {modelUrl: data.model, fov: data.fov, padding: data.frame_padding, pixelRatioCap: params.get('quality') === 'low' ? 1 : 1.5, antialias: params.get('quality') !== 'low'});
const {camera, controls} = stage;
const canvasEl = stage.renderer.domElement;
canvasEl.setAttribute('role', 'img');

// ---------- title page
$('title').textContent = data.meta.title;
$('subtitle').textContent = data.meta.part;
$('copyright').textContent = data.meta.copyright || '';
document.title = `${data.meta.title} - ${data.meta.part}`;
if (data.meta.logo) {                        // a logo file in the kit folder replaces the text badge (guide.py records its name)
  const img = new Image();
  img.onload = () => { img.alt = 'TechBox'; $('logo').replaceChildren(img); $('logo').classList.add('image'); reposeTitle(); };
  img.src = data.meta.logo;
}
// The title page's camera depends on where the logo and title are (see framedPose): look again once the logo and the fonts are in.
function reposeTitle() { if (views[cur] && views[cur].kind === 'start') go(cur, false); }
if (document.fonts) document.fonts.ready.then(reposeTitle);
const flat = v => v.kind === 'card';         // a view with no model on screen: a note card, or the parts list (a card with `parts`)
const stepCount = views.filter(v => /^Step \d+$/.test(v.name)).length;

// ---------- poses: where a part is shown, relative to where it sits when built (see core.js)
const ZERO = [0, 0, 0];
const lerp3 = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const pM = new THREE.Matrix4(), pV = new THREE.Vector3(), qA = new THREE.Quaternion(), qB = new THREE.Quaternion(), pAxis = new THREE.Vector3();
const turn = pose => pose && !Array.isArray(pose) && pose.r && pose.r[3] ? pose.r : null;
const shift = pose => !pose ? ZERO : Array.isArray(pose) ? pose : pose.t || ZERO;
function applyPose(pose, p) {
  if (!turn(pose)) { const t = shift(pose); return [p[0] + t[0], p[1] + t[1], p[2] + t[2]]; }
  pV.set(p[0], p[1], p[2]).applyMatrix4(stage.poseMatrix(pose, pM)); return [pV.x, pV.y, pV.z];
}
function unapplyPose(pose, p) {
  if (!turn(pose)) { const t = shift(pose); return [p[0] - t[0], p[1] - t[1], p[2] - t[2]]; }
  pV.set(p[0], p[1], p[2]).applyMatrix4(stage.poseMatrix(pose, pM).invert()); return [pV.x, pV.y, pV.z];
}
const quat = (pose, q) => { const r = turn(pose); return r ? q.setFromAxisAngle(pAxis.set(r[0], r[1], r[2]).normalize(), THREE.MathUtils.degToRad(r[3])) : q.identity(); };
// The same pose written as a turn about another point.
function about(pose, at, q) { const t = shift(pose), a = pose.at || ZERO; pV.set(at[0] - a[0], at[1] - a[1], at[2] - a[2]); const d = pV.clone().applyQuaternion(q).sub(pV); return [t[0] + d.x, t[1] + d.y, t[2] + d.z]; }
// A pose part of the way from a to b: the turn is spread evenly, about b's pivot (or a's if b has none).
function mixPose(a, b, k) {
  if (!turn(a) && !turn(b)) return lerp3(shift(a), shift(b), k);
  const at = (turn(b) ? b.at : a.at) || ZERO;
  quat(a, qA); quat(b, qB);
  const ta = turn(a) ? about(a, at, qA) : shift(a), tb = turn(b) ? about(b, at, qB) : shift(b);
  qA.slerp(qB, k);
  const s = Math.sqrt(Math.max(0, 1 - qA.w * qA.w)), deg = THREE.MathUtils.radToDeg(2 * Math.acos(Math.min(1, Math.abs(qA.w)))) * (qA.w < 0 ? -1 : 1);
  return {t: lerp3(ta, tb, k), r: s < 1e-6 ? [0, 1, 0, 0] : [qA.x / s, qA.y / s, qA.z / s, deg], at};
}
// Where a part that rides with another is (see `carry` in a view): its own pose `inner`, then the carrier's pose
// `outer` on top. Written as a turn about the part's own middle, so that it glides sensibly once it is let go.
const pN = new THREE.Matrix4(), pC = new THREE.Vector3();
function composePose(outer, inner, id) {
  if (!turn(outer) && !shift(outer).some(Boolean)) return inner || ZERO;
  if (!stage.parts.has(id)) return inner || ZERO;   // (a part the model does not have: nothing to draw, nothing to break)
  const m = pN.copy(stage.poseMatrix(outer, pM)).multiply(stage.poseMatrix(inner || null, pM));
  const c = stage.parts.get(id).userData.sphere.center;
  pC.copy(c).applyMatrix4(m);
  const t = [pC.x - c.x, pC.y - c.y, pC.z - c.z];
  qA.setFromRotationMatrix(m);
  const s = Math.sqrt(Math.max(0, 1 - qA.w * qA.w));
  if (s < 1e-6) return t;
  return {t, r: [qA.x / s, qA.y / s, qA.z / s, THREE.MathUtils.radToDeg(2 * Math.acos(Math.min(1, Math.abs(qA.w)))) * (qA.w < 0 ? -1 : 1)], at: [c.x, c.y, c.z]};
}
// A pose part of the way (k = 0..1) through a list of poses, each stretch taking the same share of the time.
function throughPoses(list, k) { const n = list.length - 1, s = Math.min(n - 1, Math.floor(k * n)); return mixPose(list[s], list[s + 1], k * n - s); }
const further = pose => Array.isArray(pose) ? pose.map(v => v * 1.8) : {...pose, t: shift(pose).map(v => v * 1.8)};   // a new part glides in from a little further out
// The stops of a moving part's way in (the poses it pauses at): its own when it has a way of its own.
const stopsFor = (view, id) => view.paths && view.paths[id] ? (view.path_stops && view.path_stops[id]) || null : view.stops || null;
// A step whose wire passes through routes in between (a lead laid into a slot, the extension onto row 10): going back
// from it plays it backwards, since straight back the wire would cut through the parts it was laid round.
const staged = view => Object.keys(view.wire_via || {}).length > 0;

// ---------- wires: each follows a route (a centre line in seated coordinates) and is tied to the parts at its two
// ends, so it bends along when they move; from one view to the next a wire changes route smoothly.
const wireDefs = data.wires || {};
const routes = (data.routes || []).map(r => {
  const n = r.pts.length, s = new Float32Array(n); let len = 0;
  for (let i = 1; i < n; i++) { len += Math.hypot(r.pts[i][0] - r.pts[i - 1][0], r.pts[i][1] - r.pts[i - 1][1], r.pts[i][2] - r.pts[i - 1][2]); s[i] = len; }
  for (let i = 1; i < n; i++) s[i] /= len || 1;
  return {...r, s, len};
});
const wireSamples = {};                      // points along each wire: enough for its longest route
for (const v of views) for (const [id, nos] of [...Object.entries(v.wires || {}).map(([id, no]) => [id, [no]]), ...Object.entries(v.wire_via || {})])
  for (const no of nos) wireSamples[id] = Math.max(wireSamples[id] || 0, Math.min(160, Math.max(12, Math.ceil(routes[no].len / (routes[no].spacing || 1.5)))));   // (in-between routes too; a route may ask for its tube's rings closer together, `spacing` mm: a tight bend, a resistor's leg)
const ramp = s => { const t = Math.min(1, Math.max(0, (s - 0.1) / 0.8)); return t * t * (3 - 2 * t); };   // the ends stay with their parts
const mA = new THREE.Matrix4(), mB = new THREE.Matrix4(), mR = new THREE.Matrix4();
// How far the part at one end of a route has moved from where it was when the route was drawn (`ref`, normally its seat).
function endMove(part, ref, poses, out) {
  if (!part || !(poses[part] || ref)) return null;
  stage.poseMatrix(poses[part] || null, out);
  return ref ? out.multiply(stage.poseMatrix(ref, mR).invert()) : out;
}
// The route's centre line with its ends carried along by their parts: {pts, cum (distance along it), total}. endsOnly: each part
// carries the wire by the move of the wire's own end point, without turning it (a `stretch` lead changing from one shape to the
// next: its shapes are drawn for each stop, its plug's turn already in them; turned along with the plug, a long lead folds).
function skinned(route, poses, endsOnly = false) {
  const A = endMove(route.a, route.a_ref, poses, mA), B = endMove(route.b, route.b_ref, poses, mB), m = route.pts.length;
  const pts = new Float32Array(m * 3), cum = new Float32Array(m);
  const moveOf = (M, p) => M ? (pV.set(p[0], p[1], p[2]).applyMatrix4(M), [pV.x - p[0], pV.y - p[1], pV.z - p[2]]) : null;
  const dA = endsOnly && moveOf(A, route.pts[0]), dB = endsOnly && moveOf(B, route.pts[m - 1]);
  for (let i = 0; i < m; i++) {
    const p = route.pts[i];
    let x = p[0], y = p[1], z = p[2];
    if (A || B) {
      // how much this point goes with the part at the far end: none at all before `b_from` mm (a lead held in a slot there); or,
      // given `a_whole` / `b_whole` (mm from the first end), wholly with `a` up to the one and wholly with `b` from the other, so that a
      // run lying over a part that turns turns with it (the PMG's Step 42: the dot matrix's wires over the module's USB plug)
      let wb;
      if (route.a_whole != null || route.b_whole != null) {
        const lo = Math.max(route.a_whole || 0, route.b_from || 0), hi = route.b_whole != null ? route.b_whole : route.len;
        const t = Math.min(1, Math.max(0, (route.s[i] * route.len - lo) / Math.max(1e-6, hi - lo)));
        wb = route.b ? t * t * (3 - 2 * t) : 0;
      } else {
        const u = route.b_from ? (route.s[i] * route.len - route.b_from) / Math.max(1e-6, route.len - route.b_from) : route.s[i];
        wb = route.b ? ramp(u) : 0;
      }
      const wa = route.a ? 1 - wb : 0;
      if (endsOnly) {
        if (dA && wa) { x += wa * dA[0]; y += wa * dA[1]; z += wa * dA[2]; }
        if (dB && wb) { x += wb * dB[0]; y += wb * dB[1]; z += wb * dB[2]; }
      } else if (A && wa) { pV.set(p[0], p[1], p[2]).applyMatrix4(A); x += wa * (pV.x - p[0]); y += wa * (pV.y - p[1]); z += wa * (pV.z - p[2]); }
      if (!endsOnly && B && wb) { pV.set(p[0], p[1], p[2]).applyMatrix4(B); x += wb * (pV.x - p[0]); y += wb * (pV.y - p[1]); z += wb * (pV.z - p[2]); }
    }
    pts[i * 3] = x; pts[i * 3 + 1] = y; pts[i * 3 + 2] = z;
    if (i) cum[i] = cum[i - 1] + Math.hypot(x - pts[i * 3 - 3], y - pts[i * 3 - 2], z - pts[i * 3 - 1]);
  }
  return {pts, cum, total: cum[m - 1], m, route};
}
// n points along it, evenly spaced over `span` mm from its first end (points past its own end stay on the end); or from `start`
// mm, kept between lo and hi mm.
function sampled(line, n, span = line.total, start = 0, lo = 0, hi = line.total) {
  const {pts, cum, m} = line, out = new Float32Array(n * 3);
  for (let k = 0, i = 0; k < n; k++) {
    const d = Math.max(lo, Math.min(hi, start + span * k / (n - 1)));
    while (i < m - 2 && cum[i + 1] < d) i++;
    const f = cum[i + 1] > cum[i] ? Math.min(1, (d - cum[i]) / (cum[i + 1] - cum[i])) : 0;
    for (let c = 0; c < 3; c++) out[k * 3 + c] = pts[i * 3 + c] + (pts[i * 3 + 3 + c] - pts[i * 3 + c]) * f;
  }
  return out;
}
// Draw the wires of `view` with parts at `poses`; with `from` and k < 1, part of the way from that view's routes.
// A wire changing route keeps each bit of itself the same distance from its first end, so what both routes share
// (the run from a servo to the slot it passes through) stays put, and a longer route grows out of the wire's tip; unless the
// route says `stretch` (see below).
function drawWires(view, poses, from, k = 1, via = null, alphas = null) {
  const list = [], marks = [];
  for (const id in view.wires || {}) {
    const def = wireDefs[id], route = routes[view.wires[id]], n = wireSamples[id], line = skinned(route, poses);
    const changing = from && from.wires && from.wires[id] != null && from.wires[id] !== view.wires[id] && k < 1;
    let pts, fade = route.fade || null;
    if (changing) {                            // from the old route, through any in-between routes the view names, to the new one
      const way = [from.wires[id], ...(((via || view.wire_via) || {})[id] || []), view.wires[id]], legs = way.length - 1;   // (going back: `via`, the routes the step came through, the other way)
      const leg = Math.min(legs - 1, Math.floor(k * legs)), f = k * legs - leg;
      // (a representative lead, `stretch`: each bit keeps its share of the length instead, so a longer or shorter shape
      // stretches evenly rather than growing out of the tip; and it is carried by its ends' moves only, see skinned)
      const even = !!(routes[way[leg]].stretch || routes[way[leg + 1]].stretch);
      const a = skinned(routes[way[leg]], poses, even), b = leg === legs - 1 && !even ? line : skinned(routes[way[leg + 1]], poses, even);
      const span = Math.max(a.total, b.total);
      let pa;
      const ta = routes[way[leg]].tail_from, tb = routes[way[leg + 1]].tail_from;
      if (!even && ta != null && tb != null) {
        // (`tail_from` in both: the head by distance from the first end, the tail by distance from the last, each measured along the
        // route as drawn: a bit of the run under the matrix then meets the same bit of the other shape, and the two keep pace with it)
        const drawn = (l, r) => ({pts: l.pts, cum: r.s.map(x => x * r.len), total: r.len, m: l.m});
        const A = drawn(a, routes[way[leg]]), B = drawn(b, routes[way[leg + 1]]);
        const head = Math.max(ta, tb), tail = Math.max(A.total - ta, B.total - tb);
        const n1 = Math.max(2, Math.min(n - 2, Math.round(n * head / Math.max(1e-6, head + tail))));
        const two = (l, t, out = new Float32Array(n * 3)) => (out.set(sampled(l, n1, head, 0, 0, t)), out.set(sampled(l, n - n1, tail, l.total - tail, t, l.total), n1 * 3), out);
        pa = two(A, ta); pts = two(B, tb);
      } else { pa = even ? sampled(a, n) : sampled(a, n, span); pts = even ? sampled(b, n) : sampled(b, n, span); }
      for (let i = 0; i < pts.length; i++) pts[i] = pa[i] + (pts[i] - pa[i]) * f;
      const fa = routes[way[leg]].fade, fb = routes[way[leg + 1]].fade;
      if (fa || fb) {                          // a faded end grows out to the whole wire (or back)
        const whole = [span, span + 1], from_ = fa || whole, to_ = fb || whole;
        fade = [from_[0] + (to_[0] - from_[0]) * f, from_[1] + (to_[1] - from_[1]) * f];
      }
    } else {
      pts = sampled(line, n);
      if (route.mark) { const A = endMove(route.a, route.a_ref, poses, mA); marks.push(route.mark.map(p => A ? pV.set(p[0], p[1], p[2]).applyMatrix4(A).toArray() : p)); }
    }
    if (alphas && alphas[id] != null && alphas[id] < 1) fade = [-(1 - alphas[id]) * 1e6, alphas[id] * 1e6];   // (the whole lead see-through: a lead taken off with its parts)
    list.push({id, colour: def.colour, radius: def.radius, pts, fade});
  }
  stage.setWires(list); stage.setMarks(marks);
}

// ---------- scene state for a view
function leadLines(view) {
  if (view.kind !== 'hover' || !view.guides) return [];
  const hops = view.path.some(turn) ? [view.path[0]] : view.path.slice(0, -1);   // a part that is turned on its way in gets one straight line from where it hovers
  return view.guides.map(g => [...hops.map(w => applyPose(w, g.tip)), g.mouth]);
}
const arrowsOf = view => view.kind === 'hover' ? view.arrows || [] : [];
function applyState(view, poses) {
  stage.setVisible(flat(view) ? [] : view.visible);
  for (const id of view.visible) stage.setPose(id, (poses || view.offsets)[id] || ZERO);
  drawWires(flat(view) ? {} : view, poses || view.offsets);
}
// ---------- the title page and the Completed View: their own camera at every shape of window (Lee, 21 Oct 2026)
// The camera a guide gives these two views (one solved from Lee's screenshot, or the finished model's corner) keeps its direction
// whatever the window or the LMS's frame: the player moves it back only as far as the window needs, so that every part is in the
// frame (on the title page clear of the logo, top left, and of the title, bottom left), and moves it sideways where that lets the
// model be bigger. No other camera is switched to, so the view does not jump as the window changes, and the model fills about the
// same share of it. (Measured on points sampled on the parts themselves, made once as the model loads; worked out only when one
// of the two views opens or the window changes size, never per frame.) A guide's `min_aspect` / `otherwise` cameras are no longer
// used here; the bottom may still be cut on a title page whose camera says `clear_title` (Lee's picture of the RCC's).
let partPoints = null;                       // part id -> Float32Array [x, y, z, ...]: a sample of its vertices, seated, assembly mm
function samplePoints() {
  partPoints = new Map();
  const v = new THREE.Vector3();
  for (const [id, o] of stage.parts) {
    const meshes = [];
    o.traverse(m => { if (m.isMesh && !m.userData.hull && !m.userData.decal && m.geometry.attributes.position) meshes.push(m); });
    const total = meshes.reduce((n, m) => n + m.geometry.attributes.position.count, 0), step = Math.max(1, Math.ceil(total / 200));
    const pts = [];
    for (const m of meshes) {
      const pos = m.geometry.attributes.position;
      for (let i = 0; i < pos.count; i += step) { v.fromBufferAttribute(pos, i).applyMatrix4(m.matrixWorld); pts.push(v.x, v.y, v.z); }
    }
    partPoints.set(id, new Float32Array(pts));
  }
}
samplePoints();                              // (now, with every part in its seat and the model the right way up)
// The logo's and the title's boxes on the title page, in half frame heights from the middle of the picture (y up), with a gap.
function titleBoxes() {
  const c = canvasEl.getBoundingClientRect(), W = c.width, H = c.height, gap = 12, out = [], range = document.createRange();
  for (const ids of [['logo'], ['title', 'subtitle', 'copyright']]) {
    let l = Infinity, t = Infinity, r = -Infinity, b = -Infinity;
    for (const id of ids) {
      const el = $(id); if (!el || el.closest('[hidden]')) continue;
      range.selectNodeContents(el);
      const box = id === 'logo' ? el.getBoundingClientRect() : range.getBoundingClientRect();   // (the words themselves, not their line)
      if (!box.width) continue;
      l = Math.min(l, box.left); t = Math.min(t, box.top); r = Math.max(r, box.right); b = Math.max(b, box.bottom);
    }
    if (r > l) out.push([(l - gap - c.left - W / 2) / (H / 2), (H / 2 - (b + gap - c.top)) / (H / 2), (r + gap - c.left - W / 2) / (H / 2), (H / 2 - (t - gap - c.top)) / (H / 2)]);
  }
  return out;                                // [[left, bottom, right, top], ...]
}
const framed = new Map();                    // (one answer per view, shape of window and place of the title)
function framedPose(view, aspect, whole) {
  const c = view.camera, title = view.kind === 'start', boxes = title ? titleBoxes() : [];
  const key = `${views.indexOf(view)}|${view.kind}|${aspect.toFixed(4)}|${whole}|${boxes.map(b => b.map(x => x.toFixed(3)).join()).join(';')}`;
  const pose0 = stage.cameraPose(c, 1e6);    // (as far back as fits the view's sphere top to bottom: the frame's shape is allowed for below)
  if (framed.has(key)) { const {by, k} = framed.get(key); return placed(c, pose0, by, k); }
  const T = pose0.target, D = pose0.position.distanceTo(T);
  const eye = new THREE.PerspectiveCamera(); eye.position.copy(pose0.position); eye.lookAt(T); eye.updateMatrixWorld();
  const right = new THREE.Vector3().setFromMatrixColumn(eye.matrixWorld, 0), up = new THREE.Vector3().setFromMatrixColumn(eye.matrixWorld, 1);
  const fwd = T.clone().sub(pose0.position).normalize(), tanh = Math.tan(THREE.MathUtils.degToRad((data.fov || 45) / 2));
  const {q, at} = stage.worldFor(c), turned = q.angleTo(ONE) > 1e-6, M = new THREE.Matrix4(), p = new THREE.Vector3();
  const A = [], B = [], C = [];              // each point: across, up and away, from the target (mm)
  for (const id of view.visible) {
    const pts = partPoints.get(id); if (!pts) continue;
    stage.poseMatrix(view.offsets[id] || null, M);
    for (let i = 0; i < pts.length; i += 3) {
      p.set(pts[i], pts[i + 1], pts[i + 2]).applyMatrix4(M);
      if (turned) p.sub(at).applyQuaternion(q).add(at);
      p.sub(T); A.push(p.dot(right)); B.push(p.dot(up)); C.push(p.dot(fwd));
    }
  }
  const m = 0.03, cutBottom = title && c.clear_title && !whole, r = c.radius, N = A.length, aR = (aspect - m) * tanh, vR = (1 - m) * tanh;
  // With the camera moved aside by `by` and back k times, a point is at (A + by, B) / ((C + D k) tanh) on screen: in the frame from
  // the least k each of its edges allows, and inside a logo or title box for a range of k, worked out exactly (no search).
  const frameK = by => {
    let k = 1;
    for (let i = 0; i < N; i++) {
      const X = A[i] + by, Y = B[i], c0 = C[i];
      const kx = ((X < 0 ? -X : X) / aR - c0) / D, ky = ((Y > 0 ? Y : cutBottom ? 0 : -Y) / vR - c0) / D;
      if (kx > k) k = kx;
      if (ky > k) k = ky;
    }
    return k;
  };
  const boxK = (by, rects, k) => {           // the least k, from k up, with no point inside a box
    const bad = [];
    for (let i = 0; i < N; i++) {
      const X = A[i] + by, Y = B[i];
      for (let j = 0; j < rects.length; j++) {   // inside while l < gX < rr and b < gY < t, g = 1 / ((C + D k) tanh) > 0
        const [l, b, rr, t] = rects[j];
        let lo = 0, hi = Infinity;
        if (X > 0) { lo = l / X; hi = rr / X; } else if (X < 0) { lo = rr / X; hi = l / X; } else if (!(l < 0 && rr > 0)) continue;
        if (Y > 0) { lo = Math.max(lo, b / Y); hi = Math.min(hi, t / Y); } else if (Y < 0) { lo = Math.max(lo, t / Y); hi = Math.min(hi, b / Y); } else if (!(b < 0 && t > 0)) continue;
        if (lo < 0) lo = 0;
        if (hi <= lo) continue;
        const k2 = lo > 0 ? (1 / (lo * tanh) - C[i]) / D : Infinity;   // (g falls as k grows: the larger g ends the range)
        if (k2 > k) bad.push((1 / (hi * tanh) - C[i]) / D, k2);
      }
    }
    const order = [...Array(bad.length / 2).keys()].sort((x, y) => bad[2 * x] - bad[2 * y]);
    for (const n of order) { if (bad[2 * n] > k) break; if (bad[2 * n + 1] > k) k = bad[2 * n + 1] + 1e-4; }
    return k;
  };
  const prefer = title ? (c.shift ?? 0) : 0;
  let best = null;
  for (const rects of boxes.length ? [boxes, []] : [[]]) {   // (if the logo and title leave no room at all, the frame alone)
    const shifts = [...Array(53).keys()].map(n => Math.round((n * 0.05 - 1) * 100) / 100).sort((x, y) => Math.abs(x - prefer) - Math.abs(y - prefer));
    for (const sr of shifts) {               // (nearest the shift the guide asks first: the others then rarely need the boxes worked out)
      const by = sr * r, nudge = 0.002 * Math.abs(sr - prefer);   // (the biggest model; then the shift the guide asks)
      let k = frameK(by);
      if (k > 8 || (best && k + nudge >= best.score)) continue;   // (it cannot do better than the best so far)
      if (rects.length) k = boxK(by, rects, k);
      if (k <= 8 && (!best || k + nudge < best.score)) best = {by, k, score: k + nudge};
    }
    if (best) break;
  }
  if (!best) best = {by: 0, k: 1};
  framed.set(key, best);
  return placed(c, pose0, best.by, best.k);
}
function placed(c, pose0, by, k) {         // the view's camera moved aside by `by` mm and back k times as far
  const side = new THREE.Vector3().crossVectors(new THREE.Vector3(...c.dir).normalize(), new THREE.Vector3(0, 1, 0)).normalize();
  const {q} = stage.worldFor(c); side.applyQuaternion(q);
  const target = pose0.target.clone().addScaledVector(side, by);
  return {target, position: target.clone().add(pose0.position.clone().sub(pose0.target).multiplyScalar(k))};
}
function poseFor(view, aspect, whole = false) {
  if (view.kind === 'start' || view.kind === 'end') return framedPose(view, aspect, whole);
  return stage.cameraPose(view.camera, aspect);
}

// ---------- labels: a fixed spot on screen for each, chosen once per step; only the leader follows the part
const svg = $('overlay');
const NS = 'http://www.w3.org/2000/svg';
let callouts = [];                           // {el parts..., box, anchor fn}
const measureCtx = document.createElement('canvas').getContext('2d');
function textWidth(text, size) { measureCtx.font = `700 ${size}px Arial, Helvetica, sans-serif`; return measureCtx.measureText(text).width; }
let projWorld = null;                         // the turn of the model to project with (the one on screen unless a picture is being drawn)
function project(p, cam, W, H) { const v = new THREE.Vector3(p[0], p[1], p[2]).applyMatrix4(projWorld || stage.world.matrixWorld).project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }
function anchorOf(item, view, poses) { return applyPose((poses || view.offsets)[item.id], item.anchor); }

// Where the model sits on screen, so labels can go in the white space around it.
function screenRect(view, cam, W, H) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const id of view.visible) {
    const part = stage.parts.get(id); if (!part) continue;
    const b = part.userData.box, o = view.offsets[id];
    for (let k = 0; k < 8; k++) {
      const [x, y] = project(applyPose(o, [k & 1 ? b.max.x : b.min.x, k & 2 ? b.max.y : b.min.y, k & 4 ? b.max.z : b.min.z]), cam, W, H);
      x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);
    }
  }
  for (const id in view.wires || {}) {       // wires reach beyond the parts they join
    const {pts, m} = skinned(routes[view.wires[id]], view.offsets);
    for (let i = 0; i < m; i += 4) {
      const [x, y] = project([pts[i * 3], pts[i * 3 + 1], pts[i * 3 + 2]], cam, W, H);
      x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);
    }
  }
  return {x0, y0, x1, y1};
}
// The box of instructions on screen, for labels and close-ups to keep clear of (null when it is not shown).
const onScreenInstructions = () => { const el = $('instructions'); if (el.hidden) return null; const r = el.getBoundingClientRect(); return r.height ? r : null; };
// Returns [{text|eye, x, y, w, h, side}] in pixels for a W x H frame.
const NEAR = {'up-right': [1, -1], 'up-left': [-1, -1], 'down-right': [1, 1], 'down-left': [-1, 1],
              'near-left': [-1.25, 0], 'near-right': [1.25, 0], 'near-above': [0, -1.25], 'near-below': [0, 1.25]};
function layoutCallouts(view, cam, W, H, {top = 64, bottom = 12, keepClear = null} = {}) {
  const size = Math.max(15, Math.min(28, W * 0.027)), pad = 10, gap = Math.max(14, W * 0.02);
  const R = screenRect(view, cam, W, H);
  const items = [...labelsOf(view).map(l => ({...l, w: textWidth(l.text, size) + 2 * pad, h: size + 12})),
                 ...(view.eye || []).map(e => ({...e, eye: true, w: Math.max(44, W * 0.07), h: Math.max(44, W * 0.07) * 0.56}))];
  for (const it of items) {
    const [ax, ay] = project(anchorOf(it, view), cam, W, H);
    it.ay = ay;
    const room = {right: W - R.x1 - gap - it.w - 8, left: R.x0 - gap - it.w - 8, top: R.y0 - gap - it.h - top, bottom: H - R.y1 - gap - it.h - bottom};
    const reach = {right: R.x1 - ax, left: ax - R.x0, top: ay - R.y0, bottom: R.y1 - ay};
    const sides = Object.keys(room).filter(s => room[s] >= 0).sort((a, b) => reach[a] - reach[b]);
    // A callout may ask for its place (`side`): a side of the model ('left', 'right', 'top', 'bottom'), or a place beside its own spot
    // ('up-right', 'up-left', 'down-right', 'down-left', 'near-left', 'near-right', 'near-above', 'near-below'; `reach`: how far, as a
    // share of the view's width, default 0.07): the PMG's module-pin labels up and to the right of their pins (Lee, 19 Oct 2026).
    const near = NEAR[it.side];
    it.side = near || ['left', 'right', 'top', 'bottom'].includes(it.side) ? it.side : sides[0] || 'float';
    if (near) {
      const d = (it.reach || 0.07) * W;
      it.x = ax + near[0] * d - (near[0] < 0 ? it.w : near[0] === 0 ? it.w / 2 : 0);
      it.y = ay + near[1] * d - (near[1] < 0 ? it.h : near[1] === 0 ? it.h / 2 : 0);
    } else if (it.side === 'right') { it.x = R.x1 + gap; it.y = ay - it.h - gap * 1.6; }           // a little above the part, so the leader slopes
    else if (it.side === 'left') { it.x = R.x0 - gap - it.w; it.y = ay - it.h - gap * 1.6; }
    else if (it.side === 'top') { it.x = ax + gap; it.y = R.y0 - gap - it.h; }
    else if (it.side === 'bottom') { it.x = ax + gap; it.y = R.y1 + gap; }
    else { it.x = ax + (ax > W / 2 ? -1 : 1) * 90 - (ax > W / 2 ? it.w : 0); it.y = ay - 90; }   // no white space: sit near the part
    it.x = Math.max(8, Math.min(W - it.w - 8, it.x)); it.y = Math.max(top, Math.min(H - it.h - bottom, it.y));
  }
  // never under the instructions at the top left (caption and caution can be tall, on a phone most of all)
  const box = keepClear && keepClear();
  if (box) for (const it of items) if (it.x < box.right + 8 && it.x + it.w > box.left - 8 && it.y < box.bottom + 8) it.y = Math.min(H - it.h - bottom, box.bottom + 12);
  // keep labels on the same side from overlapping; down a side in the order of the spots they name, so that their leaders do not cross
  // when some have been moved down out of the instructions' way (the LSM's Step 14 in a narrow window)
  for (const side of ['right', 'left', 'top', 'bottom', 'float']) {
    const group = items.filter(i => i.side === side), horizontal = side === 'top' || side === 'bottom';
    group.sort((a, b) => horizontal ? a.x - b.x : a.ay - b.ay || a.y - b.y);
    for (let i = 1; i < group.length; i++) {
      const a = group[i - 1], b = group[i];
      if (horizontal) { if (b.x < a.x + a.w + 14) b.x = a.x + a.w + 14; }
      else if (b.y < a.y + a.h + 10) b.y = a.y + a.h + 10;
    }
  }
  return {items, size, pad};
}
// The "look here" eye, drawn in a 100 x 56 box.
const EYE = {outline: 'M0 28C18 4 82 4 100 28 82 52 18 52 0 28Z', circles: [[50, 28, 17, '#fff'], [50, 28, 11, '#111'], [56, 23, 4.5, '#fff']]};
const EYE_PAD = 6;                           // the white box round the eye (as round a label: Lee, 18 Oct 2026, the eye alone had too little contrast)
const showLabels = params.get('labels') !== '0';
const labelsOf = view => showLabels ? (view.labels || []) : (view.labels || []).filter(l => /^\d+x$/.test(l.text));   // quantities always show
// Every label sits on a white box, which cannot be seen in white space and keeps the text readable where a label has to
// go over the model (a close-up, where the model fills the frame: Lee, 14 Oct 2026).
const BACKING = 'rgba(255,255,255,0.92)';
function buildCallouts(view) {
  svg.replaceChildren(); callouts = [];
  if (!(view.kind === 'hover' || view.kind === 'done') || !(labelsOf(view).length || (view.eye && view.eye.length))) return;   // (Step Nc: labels_done)
  const W = stage.width, H = stage.height;
  camera.updateMatrixWorld(true);
  const {items, size, pad} = layoutCallouts(view, camera, W, H, {keepClear: onScreenInstructions});   // laid out once, for the view as the step opens
  const stroke = Math.max(3, size * 0.16);
  const make = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); return e; };
  for (const it of items) {
    const leader = make('line', {stroke: ACCENT, 'stroke-width': stroke, 'stroke-linecap': 'round'});
    const ring = it.ring === false ? null : make('circle', {r: size * 0.36, fill: 'none', stroke: ACCENT, 'stroke-width': stroke, 'stroke-dasharray': `${size * 0.2} ${size * 0.13}`});   // (no ring on a label for an exact spot, such as a pin)
    if (it.eye) {
      make('rect', {x: it.x - EYE_PAD, y: it.y - EYE_PAD, width: it.w + 2 * EYE_PAD, height: it.h + 2 * EYE_PAD, rx: 6, fill: BACKING});
      const g = make('g', {transform: `translate(${it.x} ${it.y}) scale(${it.w / 100})`});
      const p = document.createElementNS(NS, 'path'); p.setAttribute('d', EYE.outline); p.setAttribute('fill', '#111'); g.appendChild(p);
      for (const [cx, cy, r, fill] of EYE.circles) { const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', r); c.setAttribute('fill', fill); g.appendChild(c); }
    } else {
      make('rect', {x: it.x - 2, y: it.y + 2, width: it.w + 4, height: it.h - 2 + stroke / 2, rx: 5, fill: BACKING});
      make('line', {x1: it.x, y1: it.y + it.h, x2: it.x + it.w, y2: it.y + it.h, stroke: ACCENT, 'stroke-width': stroke, 'stroke-linecap': 'round'});
      const t = make('text', {x: it.x + pad, y: it.y + it.h - 9, 'font-size': size, 'font-weight': 700, 'font-family': 'Arial, Helvetica, sans-serif', fill: '#111'});
      t.textContent = it.text;
    }
    callouts.push({it, leader, ring});
  }
}
function updateCallouts() {
  if (insetLeader) placeLeader(insetLeader);
  if (!callouts.length) return;
  const view = views[cur], W = stage.width, H = stage.height;
  for (const {it, leader, ring} of callouts) {
    const [ax, ay] = project(anchorOf(it, view, liveOffsets), camera, W, H);
    // leader leaves from whichever end of the underline (or the eye) is nearer the part
    const y = it.eye ? it.y + it.h / 2 : it.y + it.h;
    const x = Math.abs(ax - it.x) < Math.abs(ax - (it.x + it.w)) ? it.x : it.x + it.w;
    leader.setAttribute('x1', x); leader.setAttribute('y1', y); leader.setAttribute('x2', ax); leader.setAttribute('y2', ay);
    if (ring) { ring.setAttribute('cx', ax); ring.setAttribute('cy', ay); }
  }
}
stage.onRender(updateCallouts);

// ---------- a close-up picture (an inset) with a blue frame and a lead line to the place it shows: drawn once as the
// view opens, with some parts left out (to show what is inside), and placed in the white space beside the model.
let insetLeader = null;
function placeLeader(L) {
  const [ax, ay] = project(L.anchor, camera, stage.width, stage.height);
  const x = Math.max(L.box.x, Math.min(L.box.x + L.box.w, ax)), y = Math.max(L.box.y, Math.min(L.box.y + L.box.h, ay));
  L.line.setAttribute('x1', x); L.line.setAttribute('y1', y); L.line.setAttribute('x2', ax); L.line.setAttribute('y2', ay);
  L.ring.setAttribute('cx', ax); L.ring.setAttribute('cy', ay);
}
function buildInset(view) {
  const I = view.inset, box = $('inset');
  insetLeader = null;
  if (!I) { box.hidden = true; return; }
  // A close-up is a picture of the model drawn as the view opens, or a picture made outside (`image`, a file beside the steps, with
  // its shape `image_aspect`, height over width: the LSM's capacitor card), no taller than half the view.
  const W = stage.width, H = stage.height, aspect = I.image ? (I.image_aspect || 1) : 0.72;
  let w = Math.round(Math.max(200, Math.min(400, W * 0.28))), h = Math.round(w * aspect);
  if (I.image && h > H * 0.5) { h = Math.round(H * 0.5); w = Math.round(h / aspect); }
  const ratio = Math.min(2, devicePixelRatio || 1), picked = stage.highlighted();
  const shown = view.visible.filter(id => !(I.hide || []).includes(id));
  if (I.image) $('insetimg').src = I.image;
  else {
  const {canvas, camera: cam} = stage.snapshot(Math.round(w * ratio), Math.round(h * ratio), {setup: c => {
    stage.setHighlight([]); stage.setVisible(shown); stage.setLeadLines([]); stage.setArrows(I.arrows ? arrowsOf(view).filter(a => I.arrows === true || I.arrows.includes(a.part)) : []);   // (arrows: [parts] whose arrow it shows: one seen only here)
    for (const id in I.ghost || {}) stage.setFade(id, I.ghost[id]);   // (parts drawn faintly, `ghost`: {id: alpha}, to show what is under them)
    const at = stage.toWorld(I.target), d = new THREE.Vector3(...I.dir).normalize().applyQuaternion(stage.world.quaternion);
    const up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion);   // the picture is turned as the main view is
    up.addScaledVector(d, -up.dot(d)); if (up.lengthSq() < 1e-6) up.set(0, 0, 1);
    c.up.copy(up.normalize());
    c.position.copy(at).addScaledVector(d, I.radius / Math.sin(THREE.MathUtils.degToRad((data.fov || 45) / 2)) * 1.05);
    c.lookAt(at); c.updateMatrixWorld(true);
    return () => { for (const id in I.ghost || {}) stage.setFade(id, (view.ghost || {})[id] ?? 1);
                   stage.setVisible(view.visible); stage.setHighlight(picked); stage.setLeadLines(leadLines(view)); stage.setArrows(arrowsOf(view)); };
  }});
  // a thin red box round the exact detail, as in the published guides; or several (`marks`: [{at, half}], each round its own spot)
  const boxes = I.marks ? I.marks.map(m => ({at: m.at, half: m.half})) : I.mark ? [{at: I.target, half: I.mark}] : [];
  for (const b of boxes) {
    const ctx = canvas.getContext('2d'), v = stage.toWorld(b.at).project(cam);
    const half = THREE.MathUtils.degToRad((data.fov || 45) / 2), across = I.radius * 1.05 / Math.cos(half);   // (half the picture's height at the detail, in mm)
    const cx = (v.x + 1) / 2 * canvas.width, cy = (1 - v.y) / 2 * canvas.height, r = b.half / across * canvas.height * 0.5;
    ctx.strokeStyle = '#ff0000'; ctx.lineWidth = 2 * ratio; ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(cx - r, cy - r, 2 * r, 2 * r, 4 * ratio); else ctx.rect(cx - r, cy - r, 2 * r, 2 * r);
    ctx.stroke();
  }
  $('insetimg').src = canvas.toDataURL('image/png');
  }
  $('insetimg').alt = I.alt || '';
  $('insetcap').textContent = I.caption || '';
  // where: the side of the model with the most room, level with the place it shows
  camera.updateMatrixWorld(true);
  const R = screenRect(view, camera, W, H), [ax, ay] = project(I.target, camera, W, H), capH = I.caption ? 24 : 0;
  let boxH = h + 12 + capH + 8, boxW = w + 20;
  const room = {right: W - R.x1, left: R.x0, top: R.y0 - 70, bottom: H - R.y1};
  // the sides by room; a close-up may ask for its side (`side`: the LSM's capacitor picture, right of the capacitor, so that its leader
  // does not cross it: Lee, 20 Oct 2026), tried first wherever it fits
  const sides = Object.keys(room).sort((a, b) => (b === I.side) - (a === I.side) || room[b] - room[a]);
  const side = sides[0];
  const clear = onScreenInstructions();         // (not over the instructions)
  const placeAt = s => {
    let x = s === 'right' ? R.x1 + Math.max(24, (W - R.x1 - boxW) / 2) : s === 'left' ? Math.min(R.x0 - boxW - 24, (R.x0 - boxW) / 2) : ax - boxW / 2;   // (in the middle of the free space)
    let y = s === 'top' ? 70 : s === 'bottom' ? H - boxH - 16 : ay - boxH / 2;
    x = Math.max(12, Math.min(W - boxW - 12, x)); y = Math.max(70, Math.min(H - boxH - 12, y));
    if (clear && x < clear.right + 8 && x + boxW > clear.left - 8 && y < clear.bottom + 8) y = Math.min(H - boxH - 12, clear.bottom + 12);
    return [x, y];
  };
  let [x, y] = placeAt(side);
  // Not over the step's labels and eyes or their leaders either (a view with both, such as the LSM's Steps 6 and 14: Lee, 19 Oct
  // 2026): if it would be, the first other place that is clear of them (the other sides, or this side higher or lower), or else
  // the one that covers least. A close-up that covers none stays where it was.
  const marks = [];
  for (const {it} of callouts) {
    marks.push([it.x - 8, it.y - 8, it.x + it.w + 8, it.y + it.h + 8]);
    const [px, py] = project(anchorOf(it, view), camera, W, H), lx = it.x + it.w / 2, ly = it.y + it.h;
    for (let k = 1; k < 12; k++) { const qx = lx + (px - lx) * k / 12, qy = ly + (py - ly) * k / 12; marks.push([qx - 3, qy - 3, qx + 3, qy + 3]); }
  }
  if (marks.length && clear) marks.push([clear.left - 8, clear.top - 8, clear.right + 8, clear.bottom + 8]);   // (nor, moved, over the instructions)
  marks.push([ax - 2, ay - 2, ax + 2, ay + 2]);   // (nor over the place it shows: asked for the side where that is, with no room beside it in a
  //                                                 narrow window, it covered it, the PMG's Steps 19c - 20c at 760 px; it is then made smaller there)
  const covered = (x, y) => marks.reduce((s, [x0, y0, x1, y1]) => s + Math.max(0, Math.min(x + boxW, x1) - Math.max(x, x0)) * Math.max(0, Math.min(y + boxH, y1) - Math.max(y, y0)), 0);
  if (marks.length && covered(x, y) > 0) {
    // (and if nowhere is clear at full size, a little smaller, down to 60%: a view with labels on both sides in a narrow window, the
    // LSM's Step 6 at 1000 px)
    // (a side asked for is tried at every size before any other side)
    let best = [x, y, covered(x, y), boxW, boxH];
    const passes = [...(I.side ? [1, 0.85, 0.72, 0.6].map(k => [k, [I.side]]) : []), ...[1, 0.85, 0.72, 0.6].map(k => [k, sides])];
    for (const [k, these] of passes) {
      boxW = Math.round(w * k) + 20; boxH = Math.round(h * k) + 12 + capH + 8;
      const tries = [];
      for (const s of these) {
        const [sx, sy] = placeAt(s);
        tries.push([sx, sy]);
        if (s === 'left' || s === 'right') tries.push([sx, Math.max(70, clear && sx < clear.right + 8 && sx + boxW > clear.left - 8 ? clear.bottom + 12 : 70)], [sx, H - boxH - 12]);
        else tries.push([12, sy], [W - boxW - 12, sy]);
      }
      for (const [tx, ty] of tries) { const c = covered(tx, ty); if (c < best[2]) best = [tx, ty, c, boxW, boxH]; if (!c) break; }
      if (!best[2]) break;
    }
    [x, y, , boxW, boxH] = best;
  }
  Object.assign(box.style, {left: x + 'px', top: y + 'px', width: boxW + 'px'});
  box.hidden = false;
  const stroke = Math.max(3, Math.min(28, W * 0.027) * 0.16), make = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); return e; };
  insetLeader = {anchor: I.target, box: {x, y, w: boxW, h: boxH},
                 line: make('line', {stroke: ACCENT, 'stroke-width': stroke, 'stroke-linecap': 'round'}),
                 ring: make('circle', {r: 9, fill: 'none', stroke: ACCENT, 'stroke-width': stroke, 'stroke-dasharray': '5 3.4'})};
  placeLeader(insetLeader);
}

// ---------- the instructions: caption and caution in a box at the top left, read aloud on request, and announced to a screen reader
const speech = 'speechSynthesis' in window && typeof SpeechSynthesisUtterance === 'function' ? window.speechSynthesis : null;   // (built into the browser: nothing to load)
const speakButtons = [$('speak'), $('cardspeak')];
if (!speech) for (const b of speakButtons) b.hidden = true;
const partsText = view => view.parts.map(g => `${g.title}: ` + g.items.map(p => `${p.qty} ${p.name}${p.tag ? ` (${p.tag})` : ''}`).join(', ')).join('. ');
function wordsOf(view) {
  if (view.kind === 'start') return `${data.meta.title}. ${data.meta.part}.`;
  if (view.parts) return `${view.name}. ${partsText(view)}.`;
  if (view.kind === 'end') return 'The finished model.';
  return [view.caption, view.caution && `Caution: ${view.caution}`].filter(Boolean).join(' ');
}
// What the speech engine is given: the same words, with the build's shorthand spelled out.
const sayable = text => text.replace(/•/g, '').replace(/\b([A-Z]\d+) - ([A-Z]\d+)\b/g, '$1 to $2').replace(/\b([A-Z]\d+) \/ ([A-Z]\d+)\b/g, '$1 and $2')
  .replace(/I\/O/g, 'I O').replace(/\+5V/g, 'plus 5 volts').replace(/(\d)mm\b/g, '$1 millimetre')
  .replace(/([.:;!?])[ \t]*\n+\s*/g, '$1 ').replace(/\s*\n+\s*/g, '. ');   // (one pause between the lines of a list)
let reading = null;                          // the utterance being read now
function setSpeaking(on) { for (const b of speakButtons) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.title = on ? 'Stop reading' : 'Read aloud'; } }
function speak() {
  if (!speech) return;
  if (speech.speaking || speech.pending) { speech.cancel(); setSpeaking(false); return; }
  const u = new SpeechSynthesisUtterance(sayable(wordsOf(views[cur])));
  u.lang = document.documentElement.lang || 'en'; u.rate = 0.95;
  u.onend = u.onerror = () => { if (reading === u) { reading = null; setSpeaking(false); } };   // (a cancelled one ends later, after a new one may have started)
  reading = u; speech.speak(u); setSpeaking(true);
}
for (const b of speakButtons) b.onclick = speak;
function announce(view, i) {
  const where = view.kind === 'start' ? 'Title page' : view.kind === 'end' ? 'Completed View' : view.name;
  const labels = view.kind === 'hover' || view.kind === 'done' ? labelsOf(view).map(l => l.text) : [];
  const words = view.kind === 'start' ? wordsOf(view) : view.parts ? `${view.parts.reduce((n, g) => n + g.items.length, 0)} kinds of part; the list is on the page.` : wordsOf(view);
  $('announce').textContent = `${where}, ${i + 1} of ${views.length}. ${words}${labels.length ? ` Labels: ${labels.join(', ')}.` : ''}`;
  canvasEl.setAttribute('aria-label', flat(view) ? 'No model on this page' : `3D view of the model, ${where}${labels.length ? ': ' + labels.join(', ') : ''}. Drag to turn it.`);
}

// ---------- the parts list: one band per part (quantity, name, size or dot, picture), grouped by kind as in the published guides
const ICONS = {
  electronics: '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 2 36 11v18L20 38 4 29V11z" fill="#e5484d"/><rect x="13" y="13" width="14" height="14" rx="2" fill="#fff"/><path d="M16 9v4M20 9v4M24 9v4M16 27v4M20 27v4M24 27v4M9 16h4M9 20h4M9 24h4M27 16h4M27 20h4M27 24h4" stroke="#fff" stroke-width="2"/></svg>',
  motors: '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18" fill="#6ab04c"/><path d="M20 9l2.4 3.6 4.2-1.2.2 4.4 4 1.8-2.2 3.4 2.2 3.4-4 1.8-.2 4.4-4.2-1.2L20 31l-2.4-3.6-4.2 1.2-.2-4.4-4-1.8 2.2-3.4-2.2-3.4 4-1.8.2-4.4 4.2 1.2z" fill="#fff"/><circle cx="20" cy="20" r="4" fill="#6ab04c"/></svg>',
  screws: '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 2 38 35H2z" fill="#22a39f"/><rect x="15" y="12" width="10" height="5" rx="1" fill="#fff"/><path d="M18 17h4v13l-2 3-2-3z" fill="#fff"/><path d="M17.5 21l5 1.5M17.5 24.5l5 1.5" stroke="#22a39f" stroke-width="1.2"/></svg>',
  wood: '<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="2" y="2" width="36" height="36" rx="6" fill="#f08c3a"/><rect x="8" y="12" width="24" height="16" rx="2" fill="#fff"/><circle cx="13" cy="20" r="2" fill="#f08c3a"/><path d="M19 17h9M19 20h9M19 23h6" stroke="#f08c3a" stroke-width="1.6"/></svg>',
};
const builtParts = new Map();                // view index -> its groups, made the first time it is shown (so no picture loads before then)
function showParts(view, i) {
  if (!builtParts.has(i)) {
    const groups = [];
    for (const g of view.parts) {
      const section = document.createElement('section'); section.className = 'pgroup';
      section.style.setProperty('--band', g.colour); section.style.setProperty('--halo', g.halo || g.colour);
      const h = document.createElement('h3'); h.innerHTML = ICONS[g.icon] || ''; h.append(g.title); section.appendChild(h);
      const ul = document.createElement('ul');
      for (const p of g.items) {
        const li = document.createElement('li'), band = document.createElement('button');
        band.type = 'button'; band.className = 'pband'; band.title = 'Show this part larger';
        band.setAttribute('aria-label', `${p.qty} ${p.name}${p.tag ? ` (${p.tag})` : ''}: show the picture larger`);
        const q = document.createElement('span'); q.className = 'pqty'; q.textContent = `${p.qty}x`;
        const name = document.createElement('span'); name.className = 'pname';
        if (p.tag) { const t = document.createElement('span'); t.className = 'ptag'; t.textContent = p.tag; name.appendChild(t); }
        name.append(p.name);
        const img = new Image(); img.alt = ''; img.decoding = 'async'; img.src = p.picture;   // (the name is right beside it)
        band.append(q, name, img); band.onclick = () => zoomPart(p, band);
        li.appendChild(band); ul.appendChild(li);
      }
      section.appendChild(ul); groups.push(section);
    }
    builtParts.set(i, groups);
  }
  $('partsgroups').replaceChildren(...builtParts.get(i));
  $('partstitle').textContent = view.name;
  $('partsview').scrollTop = 0;
}

// A part's picture, large (the 500 x 500 px picture from parts.html), with its name: a click on its band, Escape or a click
// outside closes it and puts the keyboard back on the band.
let zoomFrom = null;
function zoomPart(p, from) {
  zoomFrom = from;
  $('partzoomimg').src = p.picture; $('partzoomimg').alt = p.name;
  $('partzoomname').textContent = `${p.qty}x ${p.name}${p.tag ? ` (${p.tag})` : ''}`;
  $('partzoom').hidden = false; $('partzoomclose').focus();
}
function unzoomPart(refocus = true) {
  if ($('partzoom').hidden) return false;
  $('partzoom').hidden = true;
  if (refocus && zoomFrom && zoomFrom.isConnected) zoomFrom.focus();   // (not on a change of view: its band is about to go)
  zoomFrom = null; return true;
}
$('partzoomclose').onclick = () => unzoomPart();
$('partzoom').onclick = e => { if (e.target === $('partzoom')) unzoomPart(); };

// ---------- stepping and animation
let cur = 0, anim = null, liveOffsets = null, camSwing = null;   // (camSwing: the view reset's swing, below)
const ease = k => k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
// How far apart two poses are, for pacing: millimetres moved plus half a millimetre per degree turned.
function poseGap(a, b) { const s = shift(a), t = shift(b); quat(a, qA); quat(b, qB); return Math.hypot(t[0] - s[0], t[1] - s[1], t[2] - s[2]) + THREE.MathUtils.radToDeg(qA.angleTo(qB)) * 0.5; }
// A pose along a path at time t (0..1). The path is played stop to stop, one beat each, easing in and out of every
// stop; poses between two stops are passed through at a steady pace.
function alongPath(pts, t, stops) {
  if (pts.length < 2) return pts[0];
  stops = stops || pts.map((_, i) => i);
  const beats = stops.length - 1, beat = Math.min(beats - 1, Math.floor(t * beats)), from = stops[beat], to = stops[beat + 1];
  const k = ease(t * beats - beat);
  if (to - from === 1) return mixPose(pts[from], pts[to], k);
  const gaps = []; let total = 0;
  for (let i = from; i < to; i++) { gaps.push(poseGap(pts[i], pts[i + 1])); total += gaps[gaps.length - 1]; }
  let d = k * total, i = 0;
  while (i < gaps.length - 1 && d > gaps[i]) d -= gaps[i++];
  return mixPose(pts[from + i], pts[from + i + 1], gaps[i] ? Math.min(1, d / gaps[i]) : 1);
}

// A view taking parts off, played forwards over moveDur ms of motion: when each part's way starts and comes to rest, and when it
// starts to fade out (FADE_OVERLAP_MS before it rests, so nothing waits); a part riding on another, and a lead, go with what
// carries them. dur: the whole, the last fade included.
function awayTiming(view, moveDur) {
  const ids = view.moving || [], overlap = Math.min(FADE_OVERLAP_MS, moveDur / 4);
  const wayOf = id => ((view.paths && view.paths[id]) || view.path), stopsOf = id => stopsFor(view, id) || wayOf(id).map((_, k) => k);
  const moveFrom = {}, restAt = {};
  for (const id of ids) {
    const way = wayOf(id), s = stopsOf(id), beat = moveDur / Math.max(1, s.length - 1);   // (each way's stops share the whole motion)
    let first = -1, last = -1;
    for (let b = 0; b < s.length - 1; b++) if (way.slice(s[b] + 1, s[b + 1] + 1).some(p => poseGap(way[s[b]], p) > 1e-3)) { if (first < 0) first = b; last = b; }
    moveFrom[id] = first < 0 ? 0 : first * beat; restAt[id] = last < 0 ? 0 : (last + 1) * beat;
  }
  const carrier = id => { for (let c = id, n = 0; n < 8; n++) { if (c in restAt) return c; c = view.carry && view.carry[c] && view.carry[c].by; if (!c) break; } return null; };
  const fadeAt = {}, wireFadeAt = {};
  for (const id of new Set([...ids, ...(view.leaving || [])])) { const c = carrier(id); fadeAt[id] = Math.max(0, (c ? restAt[c] : moveDur) - overlap); if (c && !(id in moveFrom)) { moveFrom[id] = moveFrom[c]; restAt[id] = restAt[c]; } }
  for (const [w, no] of Object.entries(view.leaving_wires || {})) {
    const ends = [routes[no].a, routes[no].b].filter(e => e && e in fadeAt);
    wireFadeAt[w] = ends.length ? Math.max(...ends.map(e => fadeAt[e])) : Math.max(0, moveDur - overlap);
  }
  const dur = Math.max(moveDur, ...Object.values(fadeAt).map(a => a + FADE_MS), ...Object.values(wireFadeAt).map(a => a + FADE_MS));
  return {moveFrom, restAt, fadeAt, wireFadeAt, dur};
}

function go(i, animate = true) {
  i = Math.max(0, Math.min(views.length - 1, i));
  const from = views[cur], to = views[i], sameView = i === cur;
  const flying = new Set((anim && anim.leaving) || []);   // (parts still on their way out of a removal that is being played)
  // (a `reappear` step cut short: as if it had played, so that the next step does not move its parts from where they were through
  // everything, the very move the fade is there to avoid: a review, 21 Oct 2026)
  if (anim && anim.reappear && liveOffsets) for (const id in anim.end) liveOffsets[id] = anim.end[id];
  // After the bench test is put away the build starts afresh: no part glides over from the view before (`cut`).
  if ((i === cur + 1 && to.cut) || (i === cur - 1 && from.cut)) animate = false;
  const forward = animate && i === cur + 1, backward = animate && i === cur - 1;
  // Turned round half-way through a deconstruction step (Prev while its parts are still going, or Next while Prev brings them
  // back): the step plays the other way from the very point it had reached, rather than starting again (where each part is, how
  // far it has faded, which part of a screw-then-part step is moving).
  const prev = anim, turnAround = !!(prev && prev.dur && prev.to === from && prev.src === to && (backward ? from.away : forward && to.away));
  const elapsed = turnAround ? Math.min(performance.now() - prev.t0, prev.dur) : 0;
  cur = i;
  camSwing = null;
  sel.value = i;
  const focused = document.activeElement;
  $('resetview').hidden = flat(to);          // (no view to reset on a note card or the parts list; after `focused`, so that focus on it moves on below)
  $('prev').disabled = $('first').disabled = i === 0;
  $('next').disabled = $('last').disabled = i === views.length - 1;
  if (focused && focused.disabled) ({next: $('prev'), last: $('prev'), prev: $('next'), first: $('next')})[focused.id]?.focus();   // (keyboard focus never falls off a button that turns off)
  if (!sameView && speech && (speech.speaking || speech.pending)) { reading = null; speech.cancel(); setSpeaking(false); }
  $('start').hidden = to.kind !== 'start';
  $('card').hidden = !flat(to) || !!to.parts;
  $('partsview').hidden = !to.parts;
  if (!sameView) unzoomPart(false);
  if (to.parts && !sameView) showParts(to, i);
  $('cardtext').textContent = flat(to) && !to.parts ? to.caption : '';
  $('cardbox').classList.toggle('list', flat(to) && !to.parts && to.caption.includes('\n'));   // a checklist: one item a line, ranged left
  $('cardcaution').hidden = !(flat(to) && to.caution); $('cardcautiontext').textContent = flat(to) && to.caution || '';
  const showCaption = to.caption && !flat(to) && params.get('captions') !== '0';
  $('caption').hidden = !showCaption; $('captiontext').textContent = to.caption || '';
  $('caution').hidden = !(to.caution && !flat(to)); $('cautiontext').textContent = to.caution || '';
  $('instructions').hidden = $('caption').hidden && $('caution').hidden;
  fitCaption();
  $('flag').hidden = !(to.review && $('rv').checked); $('flag').textContent = to.review ? 'Review: ' + to.review : '';
  stage.setLeadLines([]); stage.setArrows([]); stage.setMarks([]); svg.replaceChildren(); callouts = []; insetLeader = null; $('inset').hidden = true; tip.hidden = true; select(null);
  if (!sameView) marks = [];                 // (a resize redraws the same view: its picked dots stay)
  for (const c of grid.children) { const on = +c.dataset.i === i; c.classList.toggle('active', on); if (on) c.setAttribute('aria-current', 'step'); else c.removeAttribute('aria-current'); }
  if (!sameView) announce(to, i);
  const shown = el => el.getClientRects().length > 0;   // (not inside something hidden)
  if (focused && focused !== document.body && !focused.disabled && !shown(focused)) {   // its box was hidden: e.g. the caption's speaker, on a card
    const speakNow = flat(to) && !to.parts ? $('cardspeak') : $('speak');
    (shown(speakNow) ? speakNow : $('next').disabled ? $('prev') : $('next')).focus();
  }
  if (window.parent !== window) window.parent.postMessage({type: 'techbox-step', index: i, name: to.name, total: views.length}, '*');

  // A part taken off in a deconstruction (`leaving` on Step Nc) stays on screen while it travels out, and goes at the end.
  const leaving = forward && from.kind === 'hover' && to.kind === 'done' ? (to.leaving || []).filter(id => from.visible.includes(id)) : [];
  stage.clearFades();                        // (a fade cut short by this step)
  stage.setVisible(flat(to) ? [] : leaving.length ? [...to.visible, ...leaving] : to.visible);
  const was = id => !flat(from) && from.kind !== 'start' && from.visible.includes(id) && animate;
  const start = {}, end = {}, ways = {};
  for (const id of to.visible) {
    end[id] = to.offsets[id] || ZERO;
    start[id] = was(id) ? (!turnAround && liveOffsets && liveOffsets[id]) || from.offsets[id] || ZERO : end[id];
  }
  for (const id of leaving) { end[id] = to.offsets[id] || ZERO; start[id] = (!turnAround && liveOffsets && liveOffsets[id]) || from.offsets[id] || ZERO; }
  // A way starts from where the part is now; where the way begins by waiting (a part whose turn comes after a screw's), it waits there.
  const fromHere = (way, here) => { const w = way.slice(), w0 = JSON.stringify(w[0]); for (let k = 1; k < w.length - 1 && JSON.stringify(w[k]) === w0; k++) w[k] = here; w[0] = here; return w; };
  // seat the part along its path (may have more than one leg); a wiggle on the spot (`wiggle`) also plays as its step opens
  // (the wiggle plays however its step is reached: stepping forward or back, or jumping to it)
  let wayStops = null, wireVia = null;
  if ((forward && to.kind === 'done' && from.kind === 'hover') || (to.wiggle && !sameView)) {
    for (const id of to.moving) ways[id] = fromHere((to.paths && to.paths[id]) || to.path, start[id]);   // from wherever it is now (a part may have a way of its own)
  } else if (backward && from.kind === 'done' && to.kind === 'hover' && from.away) {
    // Back from a deconstruction step (`away`): the parts come back the way they went, a part that was taken off from where its
    // way out ends (or from where it had got to, if it was still on its way out).
    wayStops = {};
    for (const id of from.moving) {
      if (!(id in end)) continue;
      const back = ((from.paths && from.paths[id]) || from.path).slice().reverse(), n = back.length - 1, s = stopsFor(from, id);
      if (!from.visible.includes(id)) start[id] = !turnAround && flying.has(id) && liveOffsets && liveOffsets[id] ? liveOffsets[id] : back[0];
      const way = fromHere(back, start[id]);
      way[n] = end[id];
      ways[id] = way;
      if (s) wayStops[id] = s.map(k => n - k).reverse();
    }
    for (const id of from.leaving || []) if (id in end && !(id in ways) && !from.visible.includes(id))   // (one that rode on another: it comes back with it)
      start[id] = !turnAround && flying.has(id) && liveOffsets && liveOffsets[id] ? liveOffsets[id] : from.offsets[id] || end[id];
    if (from.wire_via) { wireVia = {}; for (const id in from.wire_via) wireVia[id] = from.wire_via[id].slice().reverse(); }   // (a lead laid in stages: back through them)
  } else if (backward && from.kind === 'done' && to.kind === 'hover' && staged(from)) {
    // Back from a step whose wire goes in by stages (Steps 97 and 100: the extension past R4 and the jumper wires): the
    // part's way backwards, stop by stop, its wire back through the same routes and a riding plug back the way it came.
    wayStops = {};
    for (const id of from.moving) {
      const way = ((from.paths && from.paths[id]) || from.path).slice().reverse(), n = way.length - 1, s = stopsFor(from, id);
      way[0] = start[id]; way[n] = end[id];
      ways[id] = way;
      if (s) wayStops[id] = s.map(k => n - k).reverse();
    }
    if (from.wire_via) { wireVia = {}; for (const id in from.wire_via) wireVia[id] = from.wire_via[id].slice().reverse(); }
  }
  if (forward && to.kind === 'hover') {                               // a new part glides in from a little further out
    for (const id of to.moving) if (!was(id) && !(to.still || []).includes(id)) start[id] = further(end[id]);   // (`still`: on screen where it starts)
  }
  if (from.isolated && !to.isolated) for (const id of to.visible) start[id] = end[id];   // leaving a sub-assembly close-up: the model is simply there
  // Every step opens on its own camera, whatever the viewer has turned or zoomed to since (Lee, 14 Oct 2026): the camera
  // swings back from where it is now, or is simply there when the step is jumped to.
  if (controls) { controls.enableDamping = false; controls.update(); controls.enableDamping = true; }   // (drop any spin still running from a drag)
  const pose = poseFor(to, stage.width / stage.height);
  const stopsOf = id => wayStops ? wayStops[id] || null : stopsFor(to, id);
  // A step that carries a riding part through in-between places and asks for it (`ride_beats`: the PMG's display slid under the dot
  // matrix's wires, lifted behind the case and over it) gives each stretch a beat of its own, as a moving part's stops have; the
  // riding part and its wires then keep pace stop by stop (paced(), below). Coming back, the same from the step being left.
  const rideView = backward ? from : to;
  const rideLegs = rideView.ride_beats ? Math.max(1, ...Object.values(rideView.carry || {}).map(c => (c.via || []).length + 1)) : 1;
  const legs = Math.max(rideLegs, Object.keys(ways).length ? Math.max(1, ...Object.keys(ways).map(id => (stopsOf(id) || ways[id]).length - 1)) : 1);
  // Parts taken off slide out, then fade out over a beat of their own (FADE_MS), each once its own way has come to rest (a screw,
  // then the part it held); coming back, the same played backwards: each fades in where its way out ended, then slides back.
  // Their leads go with them.
  let fade = null;
  const playing = animate || Object.keys(ways).length > 0;   // (a jump is at once, except for a wiggle, which still plays)
  const moveDur = playing ? STEP_MS * legs : 0;
  let moveAt = 0, dur = moveDur;
  const away = playing && leaving.length ? to : playing && backward && from.away && (from.leaving || []).length ? from : null;
  if (away) {
    const T = awayTiming(away, moveDur), out = away === to;
    const parts = out ? leaving : from.leaving.filter(id => id in end);
    const wires = out ? Object.keys(to.leaving_wires || {}) : Object.keys(from.leaving_wires || {}).filter(w => (to.wires || {})[w] != null);
    fade = {out, parts: Object.fromEntries(parts.map(id => [id, T.fadeAt[id]])), wires: Object.fromEntries(wires.map(w => [w, T.wireFadeAt[w]]))};
    dur = T.dur;
    if (!out) moveAt = dur - moveDur;                                 // (backwards: the whole played the other way round)
  }
  // the model is turned over (or back) for a view of its underside: about the new view's target, as the camera moves
  const w0 = {q: worldLive.q.clone(), at: worldLive.at.clone()}, w1 = flat(to) ? w0 : stage.worldFor(to.camera);   // (from the turn on screen, which may be half done)
  const moved = w0.q.angleTo(w1.q) > 1e-6 || (w1.q.angleTo(ONE) > 1e-6 && w0.at.distanceTo(w1.at) > 1e-3);   // turned, or turned about another point
  const turning = moved && animate && !flat(from) && from.kind !== 'start';   // (after a card the model is simply the other way up)
  anim = {t0: performance.now() - (turnAround ? Math.max(0, dur - elapsed) : 0), dur, moveAt, moveDur, src: from, start, end, ways, stops: Object.fromEntries(Object.keys(ways).map(id => [id, stopsOf(id)])), wireVia, to, leaving, fade, fresh: new Set(to.visible.filter(id => !was(id))), from: flat(from) || from.kind === 'start' || (from.isolated && !to.isolated) || !animate ? null : from,
          cam: animate ? {p0: camera.position.clone(), t0: controls.target.clone(), p1: pose.position, t1: pose.target} : {p0: pose.position.clone(), t0: pose.target.clone(), p1: pose.position, t1: pose.target},
          world: turning ? {q0: w0.q.clone(), q1: w1.q.clone(), at0: (w0.q.angleTo(ONE) < 1e-6 ? w1.at : w0.at).clone(), at1: (w1.q.angleTo(ONE) < 1e-6 ? w0.at : w1.at).clone()} : null};
  if (!turning) turnWorld(w1.q, w1.at);
  // A step that asks for it (`reappear`: the PMG's Step 42, the I/O module lifted onto H4 with all its wires, whose way there
  // could not be shown without the wires passing through one another: Lee, 21 Oct 2026) does not move anything: what changes
  // place, and its wires, fade out where they are, then fade in where they end, a beat each; back, the same the other way.
  const rv = forward && from.kind === 'hover' && to.kind === 'done' && to.reappear ? to : backward && from.kind === 'done' && to.kind === 'hover' && from.reappear ? from : null;
  if (rv && playing) {
    const mA = new THREE.Matrix4(), mB = new THREE.Matrix4();   // (where a part is, to a thousandth: a turned pose worked out again on the way, a part
    const same = (a, b) => { stage.poseMatrix(a || null, mA); stage.poseMatrix(b || null, mB); return mA.elements.every((x, k) => Math.abs(x - mB.elements[k]) < 1e-3); };   //  lying still, is not moving)
    const parts = Object.keys(end).filter(id => !same(start[id], end[id]));
    const wires = Object.keys(to.wires || {}).filter(w => (from.wires || {})[w] !== to.wires[w] || [routes[to.wires[w]].a, routes[to.wires[w]].b].some(e => parts.includes(e)));
    anim.reappear = {parts, wires};
    anim.dur = anim.moveDur = 2 * FADE_MS; anim.moveAt = 0;
    if (turnAround) anim.t0 = performance.now() - Math.max(0, anim.dur - elapsed);   // (a take-apart's fade turned round half-way: on from there)
  }
  // A part that comes off in stages (the PMG's H11 and H12: slid toward H1, then lifted, as TechBox's published take-apart shows it):
  // Step N's arrow is the first stage's; as the step plays, the arrow of each later stage shows while the stage before it plays,
  // and goes as its own plays (`staged_arrows` on Step Nc). Played backwards, none: Step N's arrow comes back as the step is reached.
  if (forward && playing && !anim.reappear && from.kind === 'hover' && to.kind === 'done' && to.staged_arrows) {
    const list = [...arrowsOf(from).map(a => [a.stage || 0, true, a]), ...to.staged_arrows.flatMap(g => g.arrows.map(a => [g.stage, false, a]))];
    anim.staged = {list: list.map(x => x[2]), at: list.map(x => x[0]), shown: list.map(x => x[1])};
    stage.setArrows(anim.staged.list);
  }
  stage.invalidate();
}
const vA = new THREE.Vector3(), vB = new THREE.Vector3(), sA = new THREE.Spherical(), sB = new THREE.Spherical();
const ONE = new THREE.Quaternion(), qW = new THREE.Quaternion(), aW = new THREE.Vector3();
const worldLive = {q: new THREE.Quaternion(), at: new THREE.Vector3()};   // how the model is turned on screen right now
function turnWorld(q, at) { worldLive.q.copy(q); worldLive.at.copy(at); stage.setWorld(worldLive); }
function stepAnimation(now) {
  if (!anim) return false;
  const t = Math.max(0, now - anim.t0);      // (a frame can be stamped just before the click)
  const k = anim.dur ? Math.min(1, t / anim.dur) : 1;   // the whole: the motion, and a fade before or after it
  let km = anim.moveDur ? Math.min(1, Math.max(0, (t - anim.moveAt) / anim.moveDur)) : 1, e = ease(km);   // the motion
  const ec = anim.reappear ? ease(k) : e;    // (the camera and the model's turn: over the whole, even where nothing moves)
  let shown = null;                          // (`reappear`: where it was until half-way, then where it ends; how solid it is now)
  if (anim.reappear && k < 1) { const half = t < FADE_MS; km = e = half ? 0 : 1; shown = half ? fadeCurve(t / FADE_MS) : 1 - fadeCurve((t - FADE_MS) / FADE_MS); }
  if (anim.world) { const w = anim.world; turnWorld(qW.slerpQuaternions(w.q0, w.q1, ec), aW.lerpVectors(w.at0, w.at1, ec)); }
  liveOffsets = {};
  for (const id in anim.end) { const o = anim.ways[id] ? alongPath(anim.ways[id], km, anim.stops[id]) : mixPose(anim.start[id], anim.end[id], e); liveOffsets[id] = o; stage.setPose(id, o); }
  // Something passing through as many stretches as the step has beats keeps pace with the moving parts' stops, stop by stop: a
  // wire through its in-between routes (the servo extension wire onto row 10), and a riding part through its in-between places
  // (the LSM's LED matrix lifted over D4, carried across and laid down, its wires keeping pace); anything else over the whole step.
  const beats = anim.moveDur ? Math.max(1, Math.round(anim.moveDur / STEP_MS)) : 1;
  const paced = n => { if (beats > 1 && n === beats) { const b = Math.min(beats - 1, Math.floor(km * beats)); return (b + ease(km * beats - b)) / beats; } return e; };
  if (anim.staged) {                         // (the arrows of a part coming off in stages, in turn: see go())
    const b = Math.min(beats - 1, Math.floor(km * beats)), u = km >= 1 ? 1 : km * beats - b, ramp = x => ease(Math.max(0, Math.min(1, x)));
    stage.setArrowAlphas(anim.staged.at.map((s, i) => s === b ? 1 - ramp(u / 0.6) : s > b && (anim.staged.shown[i] || s === b + 1) ? (anim.staged.shown[i] ? 1 : ramp(u / 0.4)) : 0));   // (Step N's: until its stage plays)
  }
  const carry = anim.to.carry || {}, before = (anim.from && anim.from.carry) || {}, back = !!anim.wireVia;
  for (const id in carry) {                  // a part riding with another goes wherever that part is in this frame
    if (!(id in anim.end)) continue;
    const c = carry[id], was = before[id] && before[id].by === c.by ? before[id].pose : null;
    if (!was && anim.ways[id]) continue;     // (a part with a way of its own that did not ride on it before: it follows its way, which ends where it rides)
    const via = back ? ((was && before[id].via) || []).slice().reverse() : c.via || [];
    if (was) liveOffsets[id] = composePose(liveOffsets[c.by], JSON.stringify(was) === JSON.stringify(c.pose) ? c.pose : throughPoses([was, ...via, c.pose], paced(via.length + 1)), id);   // (it may be moved to a new place on its carrier)
    else if (anim.fresh.has(id)) liveOffsets[id] = composePose(liveOffsets[c.by], c.pose, id);        // new with its carrier: it rides from the start
    else liveOffsets[id] = mixPose(anim.start[id], composePose(liveOffsets[c.by], c.pose, id), e);   // it was not riding before: it glides there
    stage.setPose(id, liveOffsets[id]);
  }
  // (A wire that passes through as many routes as the moving part has stops keeps pace with it, stop by stop: see `paced`.)
  const wireVia = anim.wireVia || anim.to.wire_via;
  const vias = wireVia ? Math.max(0, ...Object.values(wireVia).map(v => v.length)) : 0;
  const we = paced(vias + 1);
  const leads = anim.leaving.length && k < 1 && anim.to.leaving_wires ? {...anim.to, wires: {...anim.to.wires, ...anim.to.leaving_wires}} : anim.to;   // (a lead taken off goes with its parts)
  let alphas = null;
  if (anim.fade && k < 1) {                  // (parts taken off, fading out; or fading in again, coming back: the same, backwards)
    const f = anim.fade, alpha = at => fadeCurve(((f.out ? t : anim.dur - t) - at) / FADE_MS);
    for (const id in f.parts) stage.setFade(id, alpha(f.parts[id]));
    alphas = Object.fromEntries(Object.entries(f.wires).map(([w, at]) => [w, alpha(at)]));
  }
  if (shown != null) {
    for (const id of anim.reappear.parts) stage.setFade(id, shown);
    alphas = Object.fromEntries(anim.reappear.wires.map(w => [w, shown]));
  }
  // A part shown see-through on a view (`ghost`: {id: alpha}, to see what is behind it: the posts' tabs through D1 from below),
  // blending from the view before's value to this view's over the motion (a Step Nc without it: the part fades back to solid).
  const g0 = (anim.from && anim.from.ghost) || {}, g1 = anim.to.ghost || {};
  for (const id of new Set([...Object.keys(g0), ...Object.keys(g1)])) {
    const a0 = anim.from ? (g0[id] != null ? g0[id] : 1) : (g1[id] != null ? g1[id] : 1), a1 = g1[id] != null ? g1[id] : 1;
    if (!(anim.fade && id in anim.fade.parts)) stage.setFade(id, a0 + (a1 - a0) * e);
  }
  drawWires(flat(anim.to) ? {} : leads, liveOffsets, anim.from, we, anim.wireVia, alphas);
  if (anim.cam) {                            // swing around the target rather than cutting through the model
    const c = anim.cam;
    controls.target.lerpVectors(c.t0, c.t1, ec);
    vA.subVectors(c.p0, c.t0); vB.subVectors(c.p1, c.t1);
    if (k >= 1 || vA.length() < 1e-6) camera.position.copy(c.p1);
    else {                                   // turn about the vertical and tilt separately, so a big swing never goes over the top
      sA.setFromVector3(vA); sB.setFromVector3(vB);
      let turn = sB.theta - sA.theta;
      if (turn > Math.PI) turn -= 2 * Math.PI; else if (turn < -Math.PI) turn += 2 * Math.PI;
      camera.position.setFromSphericalCoords(sA.radius + (sB.radius - sA.radius) * ec, sA.phi + (sB.phi - sA.phi) * ec, sA.theta + turn * ec).add(controls.target);
    }
    camera.lookAt(controls.target);
  }
  if (k >= 1) {
    const view = anim.to, gone = anim.leaving.length > 0, faded = !!anim.fade || !!anim.reappear, inTurn = !!anim.staged; anim = null;
    if (gone) stage.setVisible(view.visible);   // (the parts taken off have gone)
    if (inTurn && view.kind !== 'hover') stage.setArrows([]);   // (the arrows shown in turn have all gone with their stages)
    if (faded) stage.clearFades();
    for (const id in view.ghost || {}) stage.setFade(id, view.ghost[id]);   // (see-through as the view has it, once the step has played)
    if (view.kind === 'hover') { stage.setLeadLines(leadLines(view)); stage.setArrows(arrowsOf(view)); buildCallouts(view); }
    else if (view.kind === 'done' && view.labels) buildCallouts(view);   // (labels on Step Nc, once it has played: the PMG's buttons in the case)
    if (view.inset) buildInset(view);
  }
  return true;
}

// ---------- all-steps grid with a picture of every step
const grid = $('grid');
const thumbs = new Array(views.length).fill(null);
function drawCalloutsOn(ctx, view, cam, W, H) {
  const {items, size, pad} = layoutCallouts(view, cam, W, H, {top: 6, bottom: 6});
  if (!items.length) return;
  const stroke = Math.max(2, size * 0.16);
  ctx.lineCap = 'round'; ctx.lineWidth = stroke; ctx.strokeStyle = ACCENT; ctx.fillStyle = '#111'; ctx.font = `700 ${size}px Arial, Helvetica, sans-serif`;
  for (const it of items) {
    const [ax, ay] = project(anchorOf(it, view), cam, W, H);
    const y = it.eye ? it.y + it.h / 2 : it.y + it.h, x = Math.abs(ax - it.x) < Math.abs(ax - (it.x + it.w)) ? it.x : it.x + it.w;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(ax, ay); ctx.stroke();
    if (it.ring !== false) { ctx.beginPath(); ctx.arc(ax, ay, size * 0.36, 0, Math.PI * 2); ctx.stroke(); }
    if (it.eye) { ctx.fillStyle = BACKING; ctx.fillRect(it.x - EYE_PAD, it.y - EYE_PAD, it.w + 2 * EYE_PAD, it.h + 2 * EYE_PAD); ctx.save(); ctx.translate(it.x, it.y); ctx.scale(it.w / 100, it.w / 100); ctx.fillStyle = '#111'; ctx.fill(new Path2D(EYE.outline)); for (const [cx, cy, r, fill] of EYE.circles) { ctx.fillStyle = fill; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); } ctx.restore(); ctx.fillStyle = '#111'; }
    else { ctx.fillStyle = BACKING; ctx.fillRect(it.x - 2, it.y + 2, it.w + 4, it.h - 2); ctx.fillStyle = '#111'; ctx.beginPath(); ctx.moveTo(it.x, it.y + it.h); ctx.lineTo(it.x + it.w, it.y + it.h); ctx.stroke(); ctx.fillText(it.text, it.x + pad, it.y + it.h - 9); }
  }
}
function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  const lines = [];
  for (const para of text.split('\n')) {
    let line = '';
    for (const word of para.split(' ')) { const t = line ? line + ' ' + word : word; if (ctx.measureText(t).width > maxWidth && line) { lines.push(line); line = word; } else line = t; }
    lines.push(line);
  }
  lines.forEach((l, i) => ctx.fillText(l, x, y + (i - (lines.length - 1) / 2) * lineHeight));
}
// The step list's picture of a Parts List page: the page itself, small (its bands, names, icons and part pictures), drawn the
// way the page lays them out on a 1100 px wide window. The part pictures load only once the step list is opened (until then
// the bands are drawn without them), as the page itself loads them only when it is shown.
const thumbImages = new Map();               // picture or icon -> Image
function thumbImage(src) { let im = thumbImages.get(src); if (!im) { im = new Image(); im.decoding = 'async'; im.src = src; thumbImages.set(src, im); } return im; }
const iconSrc = name => ICONS[name] ? 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(ICONS[name].replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" ')) : null;
const bareParts = new Set();                 // Parts List pictures drawn without their part pictures so far
function roundedBand(ctx, x, y, w, h) { const r = h / 2; ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + w, y); ctx.lineTo(x + w, y + h); ctx.lineTo(x + r, y + h); ctx.arc(x + r, y + r, r, Math.PI / 2, Math.PI * 1.5); ctx.closePath(); }
function renderPartsThumb(i) {
  const view = views[i], W = 960, H = 600, canvas = document.createElement('canvas'), ctx = canvas.getContext('2d');
  canvas.width = W; canvas.height = H;
  const withPictures = !$('gridwrap').hidden;
  const srcs = [...new Set(view.parts.flatMap(g => [iconSrc(g.icon), ...g.items.map(p => p.picture)]).filter(Boolean))];   // (each once: a group icon recurs)
  if (withPictures) {
    const waiting = srcs.map(thumbImage).filter(im => !im.complete);
    if (waiting.length) { let n = waiting.length; const done = () => { if (--n === 0) renderPartsThumb(i); }; for (const im of waiting) { im.addEventListener('load', done, {once: true}); im.addEventListener('error', done, {once: true}); } }
    bareParts.delete(i);
  } else bareParts.add(i);
  const pic = src => { const im = withPictures && src && thumbImages.get(src); return im && im.complete && im.naturalWidth ? im : null; };
  const PW = 1100, PAD = 24, GAPX = 40, GAPY = 26, COLGAP = 18, ROWGAP = 12, ROW = 66, HEAD = 50, TITLE = 40;   // (the page's own sizes)
  const groups = view.parts, avail = PW - 2 * PAD;
  const perRow = Math.max(1, Math.min(groups.length, Math.floor((avail + GAPX) / (300 + GAPX))));
  const gw = Math.min(640, (avail - GAPX * (perRow - 1)) / perRow), cols = Math.max(1, Math.floor((gw + COLGAP) / (250 + COLGAP))), cw = (gw - COLGAP * (cols - 1)) / cols;
  const heights = groups.map(g => HEAD + Math.ceil(g.items.length / cols) * (ROW + ROWGAP) - ROWGAP), rows = [];
  let y = PAD + TITLE;
  for (let r = 0; r < groups.length; r += perRow) { const h = Math.max(...heights.slice(r, r + perRow)); rows.push({y, from: r}); y += h + GAPY; }
  const s = Math.min(W / PW, H / (y - GAPY + PAD));
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.translate((W - PW * s) / 2, 0); ctx.scale(s, s); ctx.textAlign = 'left';
  ctx.fillStyle = '#55606a'; ctx.font = '700 22px Arial, Helvetica, sans-serif'; ctx.textBaseline = 'top'; ctx.fillText(view.name, PAD, PAD);
  for (const row of rows) groups.slice(row.from, row.from + perRow).forEach((g, k) => {
    const x0 = PAD + k * (gw + GAPX), icon = pic(iconSrc(g.icon));
    if (icon) ctx.drawImage(icon, x0, row.y, 40, 40);
    ctx.fillStyle = '#333'; ctx.font = '700 16px Arial, Helvetica, sans-serif'; ctx.textBaseline = 'middle'; ctx.fillText(g.title, x0 + 50, row.y + 20);
    g.items.forEach((p, j) => {
      const bx = x0 + (j % cols) * (cw + COLGAP), by = row.y + HEAD + Math.floor(j / cols) * (ROW + ROWGAP) + 10, mid = by + 23;
      ctx.fillStyle = g.colour; roundedBand(ctx, bx, by, cw, 46); ctx.fill();
      ctx.fillStyle = '#111'; ctx.font = '700 20px Arial, Helvetica, sans-serif'; ctx.fillText(`${p.qty}x`, bx + 12, mid);
      let ny = mid;
      if (p.tag) {
        ctx.font = '700 11px Arial, Helvetica, sans-serif'; const tw = ctx.measureText(p.tag).width + 12;
        ctx.fillStyle = '#333'; ctx.beginPath(); ctx.roundRect ? ctx.roundRect(bx + 56, mid - 16, tw, 15, 7) : ctx.rect(bx + 56, mid - 16, tw, 15); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.fillText(p.tag, bx + 62, mid - 8.5); ny = mid + 8;
      }
      ctx.fillStyle = '#222'; ctx.font = '13px Arial, Helvetica, sans-serif'; ctx.fillText(p.name, bx + 56, ny, cw - 56 - 96);
      const im = pic(p.picture);
      if (im) { ctx.save(); ctx.shadowColor = g.halo || g.colour; ctx.shadowBlur = 3; ctx.drawImage(im, bx + cw - 92, mid - 46, 92, 92); ctx.restore(); }
    });
  });
  ctx.restore();
  thumbs[i] = canvas.toDataURL('image/webp', 0.86);
  const img = grid.children[i] && grid.children[i].querySelector('img');
  if (img) img.src = thumbs[i];
}
// A still picture of a step whose part comes off in stages (the step list, the 2D PDF: player/js/pages.js) shows every stage's arrow at
// once, Step N's own with those shown in turn as the step plays (`staged_arrows`): a still cannot play them one after the other.
const stillArrows = i => { const v = views[i], d = views[i + 1]; return v.kind === 'hover' && d && d.kind === 'done' && d.staged_arrows ? [...arrowsOf(v), ...d.staged_arrows.flatMap(g => g.arrows)] : arrowsOf(v); };
function renderThumb(i, size) {               // (size [w, h]: a picture of that size, returned and not kept: the website's card picture)
  const view = views[i], W = size ? size[0] : 480, H = size ? size[1] : 300;
  if (view.parts && !size) return renderPartsThumb(i);
  let turn = null;
  const {canvas, camera: cam} = stage.snapshot(W, H, {setup: c => {
    const before = {q: stage.world.quaternion.clone(), position: stage.world.position.clone()}, picked = stage.highlighted();
    stage.setHighlight([]);                  // (a part picked on screen is not picked in the pictures)
    applyState(view); stage.setLeadLines(leadLines(view)); stage.setArrows(stillArrows(i));
    if (!flat(view)) stage.setWorld(stage.worldFor(view.camera));
    turn = stage.world.matrixWorld.clone();
    const pose = poseFor({...view, kind: view.kind === 'start' ? 'end' : view.kind}, W / H, !!size);   // (the card: the whole model)
    c.position.copy(pose.position); c.lookAt(pose.target); c.updateMatrixWorld(true);
    return () => {
      const now = views[cur]; applyState(now, liveOffsets); stage.setLeadLines(anim ? [] : leadLines(now)); stage.setArrows(anim ? (anim.staged ? anim.staged.list : []) : arrowsOf(now));
      stage.world.quaternion.copy(before.q); stage.world.position.copy(before.position); stage.world.updateMatrixWorld(true);
      stage.setHighlight(picked);
    };
  }});
  const ctx = canvas.getContext('2d');
  if (flat(view)) {
    const text = view.parts ? view.name : view.caption, list = !view.parts && text.includes('\n');
    ctx.fillStyle = '#111'; ctx.font = `600 ${list ? 13 : 22}px Arial, Helvetica, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; wrapText(ctx, text, W / 2, H / 2, W - 40, list ? 16 : 28);
  }
  else if (view.kind === 'hover' || (view.kind === 'done' && view.labels)) { projWorld = turn; drawCalloutsOn(ctx, view, cam, W, H); projWorld = null; }   // (uses the same label switch as the main view)
  if (size) return canvas;
  thumbs[i] = canvas.toDataURL('image/webp', 0.82);
  const img = grid.children[i] && grid.children[i].querySelector('img');
  if (img) img.src = thumbs[i];
}
views.forEach((v, i) => {
  const card = document.createElement('button');
  card.className = 'tile'; card.dataset.i = i;
  card.innerHTML = '<span class="pic"><img alt=""></span><span class="name"></span>';
  card.querySelector('.name').textContent = v.name;
  card.setAttribute('aria-label', v.kind === 'start' ? 'Title page' : v.caption && !v.parts ? `${v.name}: ${v.caption.split('\n')[0]}` : v.name);
  grid.appendChild(card);
});
// Pictures are drawn one at a time in spare moments after the guide has loaded, and never during a step
// animation, so stepping stays smooth on slow laptops. Opening the grid finishes whatever is left at once.
let thumbQueue = views.map((_, i) => i), lastDraw = 0;
stage.onRender(() => { lastDraw = performance.now(); });
const quiet = () => !anim && !stage.contextLost() && performance.now() - lastDraw > 200;   // not animating, rotating or zooming
function pumpThumbs() {
  if (thumbQueue.length && quiet()) renderThumb(thumbQueue.shift());
  if (thumbQueue.length) schedule();
}
const schedule = () => window.requestIdleCallback ? requestIdleCallback(pumpThumbs, {timeout: 400}) : setTimeout(pumpThumbs, 60);
setTimeout(schedule, 900);
let focusBeforeGrid = null;
function openGrid(open) {
  if (open === !$('gridwrap').hidden) return;
  $('gridwrap').hidden = !open;
  if (!open) { if (focusBeforeGrid) focusBeforeGrid.focus(); return; }
  focusBeforeGrid = document.activeElement.id === 'partzoomclose' ? zoomFrom || $('gridbtn') : document.activeElement;
  unzoomPart(false);                         // (the step list opens over the parts list: the large picture closes; closing the list goes back to its band)
  const active = grid.querySelector('.active');
  if (active) { active.scrollIntoView({block: 'center'}); active.focus({preventScroll: true}); }
  for (const k of [...bareParts]) renderPartsThumb(k);   // (now with their part pictures)
  (function finish() { if ($('gridwrap').hidden || !thumbQueue.length) return; if (!anim && !stage.contextLost()) for (let k = 0; k < 3 && thumbQueue.length; k++) renderThumb(thumbQueue.shift()); setTimeout(finish, 0); })();
}
grid.onclick = e => { const b = e.target.closest('.tile'); if (b) { openGrid(false); go(+b.dataset.i, false); } };
$('gridclose').onclick = () => openGrid(false);
$('gridwrap').onclick = e => { if (e.target === $('gridwrap')) openGrid(false); };

// ---------- part names on hover (the published viewer does the same)
const tip = $('tip'), ray = new THREE.Raycaster(), pointer = new THREE.Vector2();
let tipTimer = 0;
function hitUnder(x, y) {                     // {id, point} of the part surface under a screen position, or null
  const r = canvasEl.getBoundingClientRect();
  pointer.set((x - r.left) / r.width * 2 - 1, 1 - (y - r.top) / r.height * 2);
  ray.setFromCamera(pointer, camera);
  const shown = [...stage.parts.values()].filter(o => o.visible);
  for (const hit of ray.intersectObjects(shown, true)) {
    if (!hit.object.isMesh || hit.object.userData.hull) continue;
    let o = hit.object; while (o && !stage.parts.has(o.name)) o = o.parent;
    return o ? {id: o.name, point: stage.fromWorld(hit.point)} : null;      // (in assembly space, whichever way up the model is shown)
  }
  return null;
}
const partUnder = (x, y) => { const hit = hitUnder(x, y); return hit && hit.id; };
const meshNames = Object.entries(data.mesh_names || {});   // CAD mesh name (its start) -> name, for a part inside a part (the Nano on its module)
function thingUnder(x, y) {                   // what the pointer is on: {name, object} for a wire, a named sub-part or a part
  const r = canvasEl.getBoundingClientRect();
  pointer.set((x - r.left) / r.width * 2 - 1, 1 - (y - r.top) / r.height * 2);
  ray.setFromCamera(pointer, camera);
  const shown = [...stage.parts.values()].filter(o => o.visible);
  for (const hit of ray.intersectObjects([...shown, ...stage.wireGroup.children.filter(o => o.visible)], true)) {
    if (!hit.object.isMesh || hit.object.userData.hull) continue;
    if (hit.object.userData.wire) return {name: (wireDefs[hit.object.userData.wire] || {}).name || null, object: hit.object};
    let o = hit.object; while (o && !stage.parts.has(o.name)) o = o.parent;
    const sub = meshNames.find(([start]) => (hit.object.userData.meshName || '').startsWith(start));
    if (sub) return {name: sub[1], object: o};
    return o ? {name: data.names[o.name] || null, object: o} : null;
  }
  return null;
}
const nameUnder = (x, y) => { const t = thingUnder(x, y); return t && t.name; };
canvasEl.addEventListener('pointermove', e => {
  tip.hidden = true; clearTimeout(tipTimer);
  if (e.buttons || e.pointerType === 'touch') return;        // not while rotating
  tipTimer = setTimeout(() => {                               // only once the pointer rests, so it costs nothing while moving
    if (anim || camSwing) return;                             // (not while a step opens or the view swings back: the part would slide away from its name)
    const name = nameUnder(e.clientX, e.clientY);
    if (!name) return;
    tip.textContent = name; tip.style.left = e.clientX + 14 + 'px'; tip.style.top = e.clientY + 14 + 'px'; tip.hidden = false;
  }, 160);
});
canvasEl.addEventListener('pointerleave', () => { tip.hidden = true; clearTimeout(tipTimer); });
// A click on a part (or a wire) picks it out, as in the published viewer: it is tinted and its name stays up until the
// next click, or the next step. A click on nothing lets it go. (A drag still turns the view; Option-click is the pick tool.)
// The name stays where the pointer was, so as soon as the view moves (a drag that turns, slides or pinches it, the wheel, the
// view reset) the part is let go and a name shown on hover goes too: it would point at the wrong place (Lee, 17 Oct 2026).
const chosen = $('chosen');
function select(thing, x, y) {
  stage.setHighlight(thing && thing.object ? [thing.object] : []);
  chosen.hidden = !(thing && thing.name);
  if (thing && thing.name) { chosen.textContent = thing.name; chosen.style.left = x + 14 + 'px'; chosen.style.top = y + 14 + 'px'; }
}
function letGo() {
  tip.hidden = true; clearTimeout(tipTimer);
  if (!chosen.hidden || stage.highlighted().length) select(null);   // (only when something is picked: a drag calls this on every move)
}
// The view coasts on for a moment after a drag (and a click's own small wobble sets it going): a click stops it where it is,
// so that the part it picks stays under its name; and whatever moves the view after that lets the part go.
function stopCoasting() {
  if (!controls) return;
  const p = camera.position.clone(), t = controls.target.clone();
  controls.enableDamping = false; controls.update(); controls.enableDamping = true;   // (spends what is left of the coast and clears it...)
  camera.position.copy(p); controls.target.copy(t); controls.update();                // (...then puts the view back where it was)
}
if (controls) {
  const lastP = camera.position.clone(), lastT = controls.target.clone();
  controls.addEventListener('change', () => {
    if (camera.position.distanceToSquared(lastP) + controls.target.distanceToSquared(lastT) > 0.01) letGo();   // (moved more than 0.1 mm)
    lastP.copy(camera.position); lastT.copy(controls.target);
  });
}
{
  let down = null;
  const pressed = new Map();                   // each pointer held on the picture (any button, any finger) -> where it went down
  canvasEl.addEventListener('pointerdown', e => { pressed.set(e.pointerId, [e.clientX, e.clientY]); down = !e.altKey && e.button === 0 ? [e.clientX, e.clientY] : null; });
  canvasEl.addEventListener('pointermove', e => {             // further than a click may move: the view is being turned, slid or pinched
    const p = pressed.get(e.pointerId);
    if (p && e.buttons && Math.hypot(e.clientX - p[0], e.clientY - p[1]) > 4) { down = null; letGo(); }
  });
  canvasEl.addEventListener('pointercancel', e => pressed.delete(e.pointerId));
  canvasEl.addEventListener('wheel', letGo, {passive: true});   // zoom (a trackpad's scroll and pinch come as the wheel)
  canvasEl.addEventListener('pointerup', e => {
    pressed.delete(e.pointerId);
    const from = down; down = null;
    if (!from || Math.hypot(e.clientX - from[0], e.clientY - from[1]) > 4) return;
    if (anim || camSwing) return;              // (not while a step opens or the view swings back)
    stopCoasting();
    select(thingUnder(e.clientX, e.clientY), e.clientX, e.clientY);
    tip.hidden = true;
  });
}

// ---------- pick tool, for whoever is writing the guide: Option-click (Alt-click) a spot on a part to note
// "step | part | [x, y, z]". The numbers are where that spot is once the part is seated, in mm, which is what
// lines_at=[...] in guide.py takes. Not offered to students: only on this computer (the local server, or a guide opened as a
// file, such as a checkpoint), never embedded, and never on the hosted site, unless ?pick=1.
const authoring = location.protocol === 'file:' || ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname);
const pickOn = params.get('pick') === '1' || (params.get('pick') !== '0' && window.parent === window && authoring);
const picked = [];
let marks = [];                              // dots on the spots picked in this view: {id, p, el}
const offsetNow = id => (liveOffsets && liveOffsets[id]) || views[cur].offsets[id] || ZERO;
function updateMarks() {
  for (const m of marks) {
    if (!m.el.isConnected) svg.appendChild(m.el);            // the overlay is redrawn when a step finishes opening
    const [x, y] = project(applyPose(offsetNow(m.id), m.p), camera, stage.width, stage.height);
    m.el.setAttribute('cx', x); m.el.setAttribute('cy', y);
  }
}
function showPicks() {
  $('picks').hidden = !picked.length;
  $('picklist').textContent = picked.join('\n');
  if (!picked.length) return;
  const say = ok => { $('pickstate').textContent = ok ? '(copied to the clipboard)' : '(not copied: select the lines and copy them)'; };
  if (navigator.clipboard) navigator.clipboard.writeText(picked.join('\n')).then(() => say(true), () => say(false)); else say(false);
}
if (pickOn) {
  const el = canvasEl;
  let down = null;
  stage.onRender(updateMarks);
  el.addEventListener('pointerdown', e => { down = e.altKey && e.button === 0 ? [e.clientX, e.clientY] : null; });
  el.addEventListener('pointerup', e => {
    const from = down; down = null;
    if (!from || Math.hypot(e.clientX - from[0], e.clientY - from[1]) > 4) return;   // a drag rotates the view as usual
    const hit = hitUnder(e.clientX, e.clientY);
    if (!hit) return;
    const p = unapplyPose(offsetNow(hit.id), [hit.point.x, hit.point.y, hit.point.z]).map(v => Math.round(v * 10) / 10 + 0);
    picked.push(`${views[cur].name} | ${data.names[hit.id] || hit.id} (${hit.id}) | [${p.join(', ')}]`);
    const dot = document.createElementNS(NS, 'circle');
    for (const [k, v] of Object.entries({r: 5, fill: '#e6007e', stroke: '#fff', 'stroke-width': 1.5})) dot.setAttribute(k, v);
    marks.push({id: hit.id, p, el: dot});
    updateMarks(); showPicks();
  });
  $('pickcopy').onclick = showPicks;
  $('pickclear').onclick = () => { picked.length = 0; for (const m of marks) m.el.remove(); marks = []; showPicks(); };
}

// ---------- controls (every one is a button, a list or a tick box: Tab reaches it, Enter or Space works it)
const sel = $('sel');
sel.add(new Option('--- View all steps ---', 'all'));
views.forEach((v, i) => sel.add(new Option(v.name, i)));
sel.onchange = () => { if (sel.value === 'all') { sel.value = cur; openGrid(true); } else go(+sel.value, false); };
$('next').onclick = () => go(cur + 1);
$('prev').onclick = () => go(cur - 1);          // going back is animated too, as in the published viewer
$('first').onclick = () => go(0, false);
$('last').onclick = () => go(views.length - 1, false);
$('gridbtn').onclick = () => openGrid($('gridwrap').hidden);
if (!document.fullscreenEnabled) { $('fs').hidden = true; document.body.classList.add('nofs'); }   // e.g. embedded without permission to go full screen (the reset moves into the corner)
$('fs').onclick = () => document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
$('rv').onchange = () => { const v = views[cur]; $('flag').hidden = !(v.review && $('rv').checked); };
const reviewsOff = params.get('review') === '0' || (params.get('review') !== '1' && (data.meta.review_notes === false || !views.some(v => v.review)));
if (reviewsOff) { $('rv').checked = false; $('review').hidden = true; }   // (a guide past review shows neither the notes nor their switch)
else document.body.classList.add('reviewing');   // (the caption box keeps clear of the switch)
addEventListener('keydown', e => {
  if (e.key === 'Escape') return unzoomPart() || openGrid(false);
  if (!$('partzoom').hidden) { if (e.key === 'Tab') { e.preventDefault(); $('partzoomclose').focus(); } return; }   // (the large picture has one control)
  if (!$('gridwrap').hidden && e.key === 'Tab') {             // while the list of steps is open, Tab stays inside it
    const inside = [$('gridclose'), ...grid.querySelectorAll('.tile')], first = inside[0], last = inside[inside.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    else if (!$('gridwrap').contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    return;
  }
  if (e.altKey || e.ctrlKey || e.metaKey || !$('gridwrap').hidden) return;
  const key = {ArrowRight: () => go(cur + 1), ArrowLeft: () => go(cur - 1), Home: () => go(0, false), End: () => go(views.length - 1, false)}[e.key];
  if (!key) return;
  e.preventDefault();                        // otherwise a focused step list would move a second time on its own
  key();
});
addEventListener('resize', () => { stage.resize(); go(cur, false); });

// ---------- in a frame (the LMS's embed), not full screen: two pills down the left, one for the instruction and one for the caution
// when the step has one, each opening its box beside it and closing it again (Lee, 21 Oct 2026, with TechBox's curriculum director);
// what the learner opens stays open from step to step. Full screen from the embed (the guide's own button, an iPad's included), or
// the guide on a page of its own, shows both boxes whole and no pills, as before; leaving full screen gives the pills back. The
// player tells it is in a frame by itself (the LMS's iframe needs nothing added); ?embed=1 shows a guide so outside one, for
// checking. The announcement and reading aloud always give the whole of both.
let captionOpen = false, cautionOpen = false;
const fullScreen = () => document.fullscreenElement || document.webkitFullscreenElement;
function setCompact() {
  const inFrame = params.get('embed') === '1' || (() => { try { return window.top !== window.self; } catch (e) { return true; } })();
  const was = document.documentElement.classList.contains('compact'), focused = document.activeElement;
  document.documentElement.classList.toggle('compact', inFrame && !fullScreen());
  fitCaption();
  if (was !== document.documentElement.classList.contains('compact') && views[cur]) relayout();   // (the size may have changed first)
  if (focused && focused !== document.body && !focused.getClientRects().length)   // (keyboard focus never falls off a box that closes)
    ($('caption').contains(focused) ? $('captionpill') : $('caution').contains(focused) ? $('cautionpill') : $('fs').hidden ? $('next') : $('fs')).focus();
}
function fitCaption() {
  const compact = document.documentElement.classList.contains('compact');
  const say = (id, text) => { $(id).title = text; $(id).setAttribute('aria-label', text); };
  $('caption').classList.toggle('open', !compact || captionOpen);
  $('caution').classList.toggle('open', !compact || cautionOpen);
  $('captionpill').hidden = $('caption').hidden;   // (a pill only for a box the step has)
  $('cautionpill').hidden = $('caution').hidden;
  $('captionpill').setAttribute('aria-expanded', String(captionOpen));
  $('cautionpill').setAttribute('aria-expanded', String(cautionOpen));
  say('captionpill', captionOpen ? 'Instructions: hide them' : 'Instructions: show them');
  say('cautionpill', cautionOpen ? 'Caution: hide it' : 'Caution: show it');
}
function relayout() {                        // (labels and a close-up keep clear of the instructions: place them again)
  const view = views[cur];
  if (anim || flat(view)) return;
  // laid out for the step's own camera, as when the step opened, whatever the learner has turned the view to since (its leaders
  // follow the live camera as always); the camera is put back before anything is drawn
  const pose = poseFor(view, stage.width / stage.height), p = camera.position.clone(), q = camera.quaternion.clone();
  camera.position.copy(pose.position); camera.lookAt(pose.target); camera.updateMatrixWorld(true);
  if (view.kind === 'hover' || view.kind === 'done') buildCallouts(view);
  if (view.inset) buildInset(view);
  camera.position.copy(p); camera.quaternion.copy(q); camera.updateMatrixWorld(true);
  updateCallouts();
  stage.invalidate();
}
$('captionpill').onclick = () => { captionOpen = !captionOpen; fitCaption(); relayout(); };
$('cautionpill').onclick = () => { cautionOpen = !cautionOpen; fitCaption(); relayout(); };
document.addEventListener('fullscreenchange', setCompact);
document.addEventListener('webkitfullscreenchange', setCompact);
setCompact();
// The page that embeds the player (and only that page) may ask it to jump to a step.
addEventListener('message', e => { if (e.source === window.parent && e.data && e.data.type === 'techbox-go' && Number.isInteger(e.data.index)) go(e.data.index, false); });

go(Math.max(0, Math.min(views.length - 1, +(params.get('step') || 0))), false);
announce(views[cur], cur);
$('loading').remove();
// The view reset (top right): the camera swings back to the step's own view, as when the step is opened, from wherever the
// viewer has turned or zoomed it (Lee, 16 Oct 2026). Dragging the view again stops the swing.
function resetView() {
  const view = views[cur];
  if (flat(view) || anim || !controls) return;   // (a step that is still opening is on its way to its own view already)
  letGo();                                       // (the view is about to swing: a picked part's name would be left behind)
  if (controls) { controls.enableDamping = false; controls.update(); controls.enableDamping = true; }   // (drop any spin still running from a drag)
  const pose = poseFor(view, stage.width / stage.height);
  camSwing = {t0: performance.now(), p0: camera.position.clone(), t0v: controls.target.clone(), p1: pose.position.clone(), t1: pose.target.clone()};
  stage.invalidate();
}
function swingCamera(now) {
  if (!camSwing) return false;
  const c = camSwing, k = Math.min(1, Math.max(0, (now - c.t0) / STEP_MS)), e = ease(k);
  controls.target.lerpVectors(c.t0v, c.t1, e);
  vA.subVectors(c.p0, c.t0v); vB.subVectors(c.p1, c.t1);
  if (k >= 1 || vA.length() < 1e-6) camera.position.copy(c.p1);
  else {
    sA.setFromVector3(vA); sB.setFromVector3(vB);
    let turn = sB.theta - sA.theta;
    if (turn > Math.PI) turn -= 2 * Math.PI; else if (turn < -Math.PI) turn += 2 * Math.PI;
    camera.position.setFromSphericalCoords(sA.radius + (sB.radius - sA.radius) * e, sA.phi + (sB.phi - sA.phi) * e, sA.theta + turn * e).add(controls.target);
  }
  camera.lookAt(controls.target);
  if (k >= 1) camSwing = null;
  return true;
}
$('resetview').onclick = resetView;
if (controls) controls.addEventListener('start', () => { camSwing = null; });
const frame = now => stage.frame(now, stepAnimation(now) || swingCamera(now));
(function tick(now) { requestAnimationFrame(tick); frame(now); })(performance.now());
window._player = {views, go, stage, frame, renderThumb, poseFor, thumbs, speak, get index() { return cur; },
                  get timing() { return anim ? {dur: anim.dur, moveAt: anim.moveAt, moveDur: anim.moveDur, fade: anim.fade} : null; }, awayTiming};   // handle for tests and debugging
