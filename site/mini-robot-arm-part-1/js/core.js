// Shared 3D stage for the player and the part-image tool: loads the model, applies the house look
// (flat two-tone colour, black outline edges, white background) and renders only when something changed.
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {Line2} from 'three/addons/lines/Line2.js';
import {LineMaterial} from 'three/addons/lines/LineMaterial.js';
import {LineGeometry} from 'three/addons/lines/LineGeometry.js';

export {THREE};
const LIGHT = new THREE.Vector3(-0.45, 0.8, -0.4).normalize();
const TONE_LIT = 1.38, TONE_SHADE = 0.9;     // linear multipliers: the two flat tones of every colour

// Two flat tones per colour, chosen by whether a face looks toward the light. No per-pixel lighting maths,
// so it is about as cheap as a material can be. fade: the wire's own "alpha" attribute fades it out (a wire
// that runs on beyond what the picture shows).
function toonMaterial(color, {fade = false} = {}) {
  return new THREE.ShaderMaterial({
    uniforms: {color: {value: color}, light: {value: LIGHT}, lit: {value: TONE_LIT}, shade: {value: TONE_SHADE}, opacity: {value: 1}},
    vertexShader: `${fade ? 'attribute float alpha; varying float vA;' : ''} varying vec3 vN;
      void main() { ${fade ? 'vA = alpha;' : ''} vN = normalize(mat3(modelMatrix) * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `uniform vec3 color; uniform vec3 light; uniform float lit; uniform float shade; uniform float opacity; varying vec3 vN; ${fade ? 'varying float vA;' : ''}
      void main() {
        float t = smoothstep(-0.02, 0.02, dot(normalize(vN), light));
        vec3 c = min(color * mix(shade, lit, t), vec3(1.0));
        // Encode to sRGB here (not via the renderer) so on-screen frames and off-screen snapshots get identical colours.
        gl_FragColor = vec4(mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c)), ${fade ? 'vA' : 'opacity'});   // (opacity: a part fading, setFade)
      }`,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1,
    ...(fade ? {transparent: true, depthWrite: false} : {}),
  });
}

// Silhouette for round parts whose sides have no crease edges (wires, caps, screws): the back faces, in black, pushed
// out by a fixed distance on screen, so the outline is as thin as the edge lines however near the camera is.
function hullMaterial({fade = false} = {}) {
  return new THREE.ShaderMaterial({
    uniforms: {width: {value: 0.9}, resolution: {value: new THREE.Vector2(1, 1)}, opacity: {value: 1}},   // width in drawn pixels, to match the edge lines
    vertexShader: `uniform float width; uniform vec2 resolution; ${fade ? 'attribute float alpha; varying float vA;' : ''}
      void main() {
        ${fade ? 'vA = alpha;' : ''}
        vec4 p = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        vec2 n = (projectionMatrix * vec4(normalize(normalMatrix * normal), 0.0)).xy * resolution;
        float len = length(n);
        if (len > 1e-6) p.xy += n / len / resolution * 2.0 * width * p.w;
        gl_Position = p;
      }`,
    fragmentShader: `uniform float opacity; ${fade ? 'varying float vA;' : ''} void main() { gl_FragColor = vec4(0.07, 0.07, 0.07, ${fade ? 'vA * vA * vA' : 'opacity * opacity * opacity'}); }`,   // (fading faster than the wire, which it shows through)
    side: THREE.BackSide,
    ...(fade ? {transparent: true, depthWrite: false} : {}),
  });
}
const outlineMaterial = hullMaterial(), fadeOutlineMaterial = hullMaterial({fade: true});
const HIGHLIGHT = new THREE.Color('#ff8000');  // a part clicked on in the viewer is tinted towards this orange, as in the published viewer

// fov and padding come from steps.json so the generator and the player always frame a view the same way.
export async function createStage(container, {modelUrl, fov = 45, padding = 1.08, pixelRatioCap = 1.5, antialias = true, interactive = true, preserveDrawingBuffer = false} = {}) {
  const renderer = new THREE.WebGLRenderer({antialias, alpha: true, preserveDrawingBuffer, powerPreference: 'default'});
  renderer.setClearColor(0xffffff, 1);
  let pixelRatio = Math.min(devicePixelRatio || 1, pixelRatioCap);
  renderer.setPixelRatio(pixelRatio);
  container.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(fov, 1, 1, 20000);
  const controls = interactive ? new OrbitControls(camera, renderer.domElement) : null;
  if (controls) { controls.enableDamping = true; controls.dampingFactor = 0.12; }

  const gltf = await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).loadAsync(modelUrl);
  const root = gltf.scene;
  // Everything that is in assembly space (the model, lead lines, wires, break marks) hangs under `world`, which is
  // turned over for a view of the underside (see worldFor): the camera, its controls and the light stay upright.
  const world = new THREE.Group();
  scene.add(world);
  world.add(root);
  root.updateMatrixWorld(true);

  // one shared material per colour, one for all edges
  const materials = new Map();
  const edgeMaterial = new THREE.LineBasicMaterial({color: 0x111111});
  const meshNames = o => { const a = gltf.parser.associations.get(o); return a && a.meshes !== undefined ? gltf.parser.json.meshes[a.meshes] : null; };
  const outlined = [];
  root.traverse(o => {
    if (o.isLineSegments) { o.material = edgeMaterial; o.userData.edge = true; o.raycast = () => {}; }   // edges are never picked
    else if (o.isMesh) {
      const key = o.material.name || o.material.color.getHexString();
      if (!materials.has(key)) materials.set(key, toonMaterial(o.material.color.clone()));
      o.material = materials.get(key);
      const def = meshNames(o) || (o.parent && meshNames(o.parent));
      if (def && def.name) o.userData.meshName = def.name;
      if (def && def.extras && def.extras.outline) outlined.push(o);
    }
  });
  // (GLTFLoader copies a mesh's extras into userData, so the screws themselves carry `outline`: the hull is marked `hull`.)
  for (const o of outlined) { const hull = new THREE.Mesh(o.geometry, outlineMaterial); hull.userData.hull = true; hull.raycast = () => {}; o.add(hull); }

  // A part picked in the viewer is drawn in tinted copies of its materials until it is let go.
  const tinted = new Map();                    // mesh -> its own material, while it is drawn tinted
  let picked = [];
  function tintOf(material) {
    const key = 'tint' + material.uuid;
    if (!materials.has(key)) {
      const m = material.clone();
      m.uniforms = THREE.UniformsUtils.clone(material.uniforms);
      m.uniforms.light = material.uniforms.light;                   // (still the one shared light)
      m.uniforms.color.value = material.uniforms.color.value.clone().lerp(HIGHLIGHT, 0.7);
      materials.set(key, m);
    }
    return materials.get(key);
  }
  function setHighlight(objects) {
    for (const [o, material] of tinted) o.material = material;
    tinted.clear();
    picked = [...objects];
    for (const top of picked) top.traverse(o => {
      if (!o.isMesh || o.userData.hull || !o.material.uniforms || !o.material.uniforms.color) return;
      tinted.set(o, o.material); o.material = tintOf(o.material);
    });
    dirty = true;
  }

  // A part fading out as it is taken off (or in again, coming back): drawn in see-through copies of its materials meanwhile,
  // nearest surface only (the copies still write depth), and given its own materials back once the fade is over.
  const fading = new Map();                    // part id -> [[object, its own material, the copy]]
  function setFade(id, a) {
    const top = parts.get(id); if (!top) return;
    let list = fading.get(id);
    if (a >= 1) {
      if (list) { for (const [o, own, copy] of list) { o.material = own; copy.dispose(); } fading.delete(id); dirty = true; }
      return;
    }
    if (!list) {
      list = [];
      top.traverse(o => {
        if (!(o.isMesh || o.isLineSegments) || !o.material) return;
        const own = o.material, copy = own.clone();
        if (own.uniforms) for (const k of ['light', 'map']) if (own.uniforms[k]) copy.uniforms[k] = own.uniforms[k];   // (the one light; the decal's own picture)
        copy.transparent = true;
        list.push([o, own, copy]); o.material = copy;
      });
      fading.set(id, list);
    }
    for (const [, , copy] of list) { if (copy.uniforms && copy.uniforms.opacity) copy.uniforms.opacity.value = a; else copy.opacity = a; }
    dirty = true;
  }
  const clearFades = () => { for (const id of [...fading.keys()]) setFade(id, 1); };

  // parts = the assembly's direct children; steps address them by name
  const assembly = root.children.length === 1 && !root.children[0].isMesh ? root.children[0] : root;
  const parts = new Map();
  for (const o of assembly.children) {
    parts.set(o.name, o);
    o.userData.home = o.position.clone();
    o.userData.box = new THREE.Box3().setFromObject(o);     // seated bounds in assembly space (mm)
    o.userData.sphere = o.userData.box.getBoundingSphere(new THREE.Sphere());
    o.userData.homeWorld = o.matrixWorld.clone();
    o.userData.centre = o.userData.sphere.center.clone();   // where the middle of the part is right now
    o.userData.pose = null;
  }
  const parentInverse = new THREE.Matrix4().copy(assembly.matrixWorld).invert();
  const tmp = new THREE.Vector3(), m4 = new THREE.Matrix4(), q4 = new THREE.Quaternion(), axis = new THREE.Vector3();

  // Print on a part (the silkscreen of a circuit board): flat pictures drawn here, in the browser, from a description the
  // model carries (materials.json "decals", put in the part's extras by build_model.py), so the model file holds no image.
  // A decal: {origin, u, v, size: [w, h]} in seated mm (origin = the picture's top-left corner, u = its "right", v = its
  // "down"; it is seen from the side v x u faces), px_per_mm, colour, and items in picture mm: {text, at: [x, y], size,
  // rot, align, weight, width (squeezed to at most that long)}, {rect: [x, y, w, h], line}, {circle: [x, y, r], line or fill},
  // {fill: [x, y, w, h], colour}, {poly: [[x, y], ...] or a list of such rings, filled even-odd (a ring inside another is a
  // hole), or with `line` drawn as outlines (`open`: not closed)}, {arc: [x, y, r, from, to] (degrees, clockwise from the
  // picture's right), line, or filled as the piece its chord cuts off}.
  const maxAniso = renderer.capabilities.getMaxAnisotropy();
  function addDecal(part, d) {
    const [w, h] = d.size, k = d.px_per_mm || 20, canvas = document.createElement('canvas');
    canvas.width = Math.ceil(w * k); canvas.height = Math.ceil(h * k);
    const ctx = canvas.getContext('2d'), ink = d.colour || '#f2f2f2';
    ctx.scale(k, k); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    for (const it of d.items || []) {
      ctx.save(); ctx.fillStyle = ctx.strokeStyle = it.colour || ink;
      if (it.text != null) {
        ctx.translate(it.at[0], it.at[1]); if (it.rot) ctx.rotate(THREE.MathUtils.degToRad(it.rot));
        ctx.font = `${it.weight || 700} ${it.size}px Arial, Helvetica, sans-serif`; ctx.textAlign = it.align || 'center'; ctx.textBaseline = 'middle';
        if (it.width) ctx.fillText(it.text, 0, 0, it.width); else ctx.fillText(it.text, 0, 0);
      } else if (it.rect) { ctx.lineWidth = it.line || 0.15; ctx.strokeRect(...it.rect); }
      else if (it.fill) { ctx.fillRect(...it.fill); }
      else if (it.circle) { ctx.beginPath(); ctx.arc(it.circle[0], it.circle[1], it.circle[2], 0, Math.PI * 2); if (it.line) { ctx.lineWidth = it.line; ctx.stroke(); } else ctx.fill(); }
      else if (it.poly) {
        ctx.beginPath();
        for (const ring of typeof it.poly[0][0] === 'number' ? [it.poly] : it.poly) {
          ring.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
          if (!it.open) ctx.closePath();
        }
        if (it.line) { ctx.lineWidth = it.line; ctx.stroke(); } else ctx.fill('evenodd');
      } else if (it.arc) {
        const [x, y, r, from, to] = it.arc;
        ctx.beginPath(); ctx.arc(x, y, r, THREE.MathUtils.degToRad(from), THREE.MathUtils.degToRad(to));
        if (it.line) { ctx.lineWidth = it.line; ctx.stroke(); } else { ctx.closePath(); ctx.fill(); }
      }
      ctx.restore();
    }
    const map = new THREE.CanvasTexture(canvas);
    map.anisotropy = Math.min(8, maxAniso);    // (no colour space: the canvas's sRGB values are written out as they are, like toonMaterial, so screen and snapshots match)
    const O = new THREE.Vector3(...d.origin), U = new THREE.Vector3(...d.u).normalize().multiplyScalar(w), V = new THREE.Vector3(...d.v).normalize().multiplyScalar(h);
    const toPart = m4.copy(part.matrixWorld).invert();      // (seated; the model is not turned yet)
    const corners = [O.clone(), O.clone().add(U), O.clone().add(U).add(V), O.clone().add(V)].map(p => p.applyMatrix4(toPart));
    const g = new THREE.BufferGeometry().setFromPoints(corners);
    g.setAttribute('uv', new THREE.Float32BufferAttribute([0, 1, 1, 1, 1, 0, 0, 0], 2));
    g.setIndex([0, 2, 1, 0, 3, 2]);                           // facing v x u
    const mesh = new THREE.Mesh(g, new THREE.ShaderMaterial({uniforms: {map: {value: map}, opacity: {value: 1}},
      vertexShader: 'varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
      fragmentShader: 'uniform sampler2D map; uniform float opacity; varying vec2 vUv; void main() { vec4 c = texture2D(map, vUv); gl_FragColor = vec4(c.rgb, c.a * opacity); }',
      transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -4}));
    mesh.raycast = () => {}; mesh.userData.decal = true; mesh.name = `${part.name} ${d.name || 'decal'}`;
    part.add(mesh);
  }
  for (const o of parts.values()) for (const d of o.userData.decals || []) addDecal(o, d);
  // A pose says where a part is shown relative to where it sits when built: [x, y, z] (moved), or
  // {t: [x, y, z], r: [ax, ay, az, degrees], at: [px, py, pz]} (turned about an axis through `at`, then moved). All in mm.
  function poseMatrix(pose, out = new THREE.Matrix4()) {
    if (!pose) return out.identity();
    if (Array.isArray(pose)) return out.makeTranslation(pose[0], pose[1], pose[2]);
    const t = pose.t || [0, 0, 0], r = pose.r, at = pose.at || [0, 0, 0];
    if (!r || !r[3]) return out.makeTranslation(t[0], t[1], t[2]);
    q4.setFromAxisAngle(axis.set(r[0], r[1], r[2]).normalize(), THREE.MathUtils.degToRad(r[3]));
    out.makeRotationFromQuaternion(q4);
    tmp.set(at[0], at[1], at[2]).applyQuaternion(q4);                    // T(t) T(at) R T(-at)
    return out.setPosition(t[0] + at[0] - tmp.x, t[1] + at[1] - tmp.y, t[2] + at[2] - tmp.z);
  }
  function setPose(id, pose) {
    const o = parts.get(id); if (!o) return;
    o.userData.pose = pose;
    poseMatrix(pose, m4);
    o.userData.centre.copy(o.userData.sphere.center).applyMatrix4(m4);
    m4.multiply(o.userData.homeWorld).premultiply(parentInverse).decompose(o.position, o.quaternion, o.scale);
  }
  const setOffset = setPose;
  function setVisible(ids) { const on = ids instanceof Set ? ids : new Set(ids); for (const [id, o] of parts) o.visible = on.has(id); }
  function boundsOf(ids, offsets = {}) {
    const box = new THREE.Box3();
    for (const id of ids) { const o = parts.get(id); if (!o) continue; const b = o.userData.box.clone(); if (offsets[id]) b.applyMatrix4(poseMatrix(offsets[id], m4)); box.union(b); }
    return box;
  }

  // A view of the underside ({flip: true} on its camera, whose dir then points up from below) is shown with the model
  // turned over rather than with the camera under it: so the light still falls from above and the controls still turn
  // about the vertical. The turn is half a turn about the level line through the target that points at the camera, so
  // the camera itself stays where an ordinary view from that side would put it. worldFor gives {q, at} for `world`.
  // A run of such views shares one turn (camera.flip_axis, camera.pivot, written by the generator), so that the model
  // stays put from one to the next and only the camera moves.
  const ONE = new THREE.Quaternion();
  function worldFor(cam) {
    if (!cam || !cam.flip) return {q: ONE.clone(), at: new THREE.Vector3(...(cam ? cam.target : [0, 0, 0]))};
    const along = cam.flip_axis ? new THREE.Vector3(...cam.flip_axis) : new THREE.Vector3(cam.dir[0], 0, cam.dir[2]);
    if (along.lengthSq() < 1e-8) along.set(1, 0, 0);
    return {q: new THREE.Quaternion().setFromAxisAngle(along.normalize(), Math.PI), at: new THREE.Vector3(...(cam.pivot || cam.target))};
  }
  function setWorld({q, at}) {                // world = turned by q about the point `at`
    world.quaternion.copy(q);
    world.position.copy(at).sub(tmp.copy(at).applyQuaternion(q));
    world.updateMatrixWorld(true); dirty = true;
  }
  const toWorld = p => (Array.isArray(p) ? new THREE.Vector3(p[0], p[1], p[2]) : p.clone()).applyMatrix4(world.matrixWorld);
  const fromWorld = p => p.clone().applyMatrix4(m4.copy(world.matrixWorld).invert());

  // camera placement from a view description {dir, target, radius, flip}: the fit sphere always stays inside the frame
  function cameraPose(view, aspect, pad = padding) {
    const half = THREE.MathUtils.degToRad(fov / 2);
    const fitV = view.radius / Math.sin(half);
    const fitH = view.radius / Math.sin(Math.atan(Math.tan(half) * aspect));
    const dist = Math.max(fitV, fitH) * pad;
    const {q, at} = worldFor(view), target = new THREE.Vector3(...view.target).sub(at).applyQuaternion(q).add(at);   // (where the target is once the model is turned)
    return {position: target.clone().addScaledVector(new THREE.Vector3(...view.dir).normalize().applyQuaternion(q), dist), target};
  }

  // Keep the depth range tight around what is shown. With the near plane fixed at 1 mm, two CAD surfaces a hundredth
  // of a millimetre apart (a coloured skin over a body) land on the same depth value from half a metre away and flicker.
  const wc = new THREE.Vector3();
  function fitDepth(cam) {
    let near = Infinity, far = 0;
    for (const o of parts.values()) {
      if (!o.visible) continue;
      const s = o.userData.sphere, d = wc.copy(o.userData.centre).applyMatrix4(world.matrixWorld).distanceTo(cam.position);
      near = Math.min(near, d - s.radius); far = Math.max(far, d + s.radius);
    }
    if (!far) return;
    near = Math.max(1, near / 4); far = far * 1.5 + 100;     // generous: lead lines and labels' parts sit between the parts
    if (near !== cam.near || far !== cam.far) { cam.near = near; cam.far = far; cam.updateProjectionMatrix(); }
  }

  // red lead lines (3D, hidden where they pass behind a part, like the real thing)
  const lineMaterial = new LineMaterial({color: 0xff0000, linewidth: 2.4});
  const lines = new THREE.Group();
  world.add(lines);
  function setLeadLines(polylines) {
    for (const l of [...lines.children]) { l.geometry.dispose(); lines.remove(l); }
    for (const pts of polylines) { const g = new LineGeometry(); g.setPositions(pts.flat()); lines.add(new Line2(g, lineMaterial)); }
  }

  // fat red arrows, for a move with no mating features (see docs/cadasio-patterns.md, section 5): flat, straight, drawn in
  // 3D. [{tail, head, normal}] in mm; normal: the way the face of the arrow looks. Body : head width : head length = 5 : 20 : 17.
  const arrowMaterial = new THREE.MeshBasicMaterial({color: 0xff0000, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -4});
  const arrows = new THREE.Group();
  world.add(arrows);
  function setArrows(list) {
    for (const a of [...arrows.children]) { a.geometry.dispose(); if (a.material !== arrowMaterial) a.material.dispose(); arrows.remove(a); }
    for (const [index, {tail, head, normal = [0, 1, 0], width = 4}] of (list || []).entries()) {
      const t = new THREE.Vector3(...tail), d = new THREE.Vector3(...head).sub(t), L = d.length();
      if (L < 1e-6) continue;
      d.divideScalar(L);
      const s = new THREE.Vector3(...normal).cross(d).normalize(), b = width / 2, hw = width * 2, hl = Math.min(L * 0.6, width * 3.4);
      const at = (u, v) => t.clone().addScaledVector(d, u).addScaledVector(s, v);
      const g = new THREE.BufferGeometry().setFromPoints([at(0, -b), at(L - hl, -b), at(L - hl, b), at(0, b), at(L - hl, -hw), at(L, 0), at(L - hl, hw)]);
      g.setIndex([0, 1, 2, 0, 2, 3, 4, 5, 6]);
      const m = new THREE.Mesh(g, arrowMaterial);
      m.raycast = () => {}; m.userData.arrow = true; m.userData.index = index;   // (its place in the list: setArrowAlphas)
      arrows.add(m);
    }
    dirty = true;
  }
  // How solid each arrow set by setArrows() is now, in its order (a take-apart's arrows shown in turn as a step plays): an arrow
  // given less than 1 gets a see-through copy of the arrows' look; 1 (or none given) puts the shared one back.
  function setArrowAlphas(alphas) {
    for (const m of arrows.children) {
      const i = m.userData.index, a = alphas[i] == null ? 1 : Math.max(0, Math.min(1, alphas[i]));
      if (a >= 1) { if (m.material !== arrowMaterial) { m.material.dispose(); m.material = arrowMaterial; } m.visible = true; continue; }
      if (m.material === arrowMaterial) { m.material = arrowMaterial.clone(); m.material.transparent = true; m.material.depthWrite = false; }
      m.material.opacity = a; m.visible = a > 0.005;
    }
    dirty = true;
  }

  // ---- wires: round tubes drawn along a centre line the player gives (so they can follow parts and change route)
  const RADIAL = 10, wireGroup = new THREE.Group(), wires = new Map();
  world.add(wireGroup);
  const wn = new THREE.Vector3(), wb = new THREE.Vector3(), wt = new THREE.Vector3(), wp = new THREE.Vector3();
  function makeWire(id, colour, n) {
    const rings = n, g = new THREE.BufferGeometry(), index = [];
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array((rings * RADIAL + 2) * 3), 3));
    g.setAttribute('normal', new THREE.BufferAttribute(new Float32Array((rings * RADIAL + 2) * 3), 3));
    g.setAttribute('alpha', new THREE.BufferAttribute(new Float32Array(rings * RADIAL + 2).fill(1), 1));
    for (let i = 0; i < rings - 1; i++) for (let j = 0; j < RADIAL; j++) {
      const a = i * RADIAL + j, b = i * RADIAL + (j + 1) % RADIAL, c = a + RADIAL, d = b + RADIAL;
      index.push(a, b, c, b, d, c);                              // facing outwards
    }
    const c0 = rings * RADIAL, c1 = c0 + 1;                      // flat caps, so a cut end is not hollow
    for (let j = 0; j < RADIAL; j++) { index.push(c0, (j + 1) % RADIAL, j); index.push(c1, (rings - 1) * RADIAL + j, (rings - 1) * RADIAL + (j + 1) % RADIAL); }
    g.setIndex(index);
    for (const fade of [false, true]) {
      const key = 'wire' + colour + (fade ? ' fade' : '');
      if (!materials.has(key)) materials.set(key, toonMaterial(new THREE.Color(colour), {fade}));
    }
    const mesh = new THREE.Mesh(g, materials.get('wire' + colour)), hull = new THREE.Mesh(g, outlineMaterial);
    hull.raycast = () => {}; mesh.frustumCulled = hull.frustumCulled = false; hull.userData.hull = true;
    mesh.userData.wire = id;                                    // (the pointer can rest on a wire to read its name)
    mesh.add(hull); wireGroup.add(mesh);
    const w = {mesh, hull, n, colour, faded: false}; wires.set(id, w); return w;
  }
  // list: [{id, colour, radius, pts: Float32Array of n points, fade}]; wires not listed are hidden.
  // fade: [from, to] in mm along the wire from its first end: the wire fades out between the two (it runs on, but the
  // picture leaves the rest of it out), and is not drawn beyond `to`.
  function setWires(list) {
    for (const w of wires.values()) w.mesh.visible = false;
    for (const {id, colour, radius, pts, fade} of list) {
      const n = pts.length / 3;
      let w = wires.get(id);
      if (w && w.n !== n) { w.mesh.geometry.dispose(); wireGroup.remove(w.mesh); wires.delete(id); w = null; }
      if (!w) w = makeWire(id, colour, n);
      const P = w.mesh.geometry.attributes.position, N = w.mesh.geometry.attributes.normal, pa = P.array, na = N.array;
      if (fade || w.faded) {                                     // the fade follows the wire's length as it is drawn now
        const A = w.mesh.geometry.attributes.alpha, aa = A.array;
        let d = 0;
        for (let i = 0; i < n; i++) {
          if (i) d += Math.hypot(pts[i * 3] - pts[i * 3 - 3], pts[i * 3 + 1] - pts[i * 3 - 2], pts[i * 3 + 2] - pts[i * 3 - 1]);
          const u = fade ? Math.min(1, Math.max(0, (d - fade[0]) / Math.max(1e-6, fade[1] - fade[0]))) : 0, a = 1 - u * u * (3 - 2 * u);
          for (let j = 0; j < RADIAL; j++) aa[i * RADIAL + j] = a;
          if (i === 0) aa[n * RADIAL] = a;
          if (i === n - 1) aa[n * RADIAL + 1] = a;
        }
        A.needsUpdate = true;
      }
      if (!!fade !== w.faded) {                                  // fading wires are see-through, and drawn after the solid ones
        const own = materials.get('wire' + w.colour + (fade ? ' fade' : ''));
        if (tinted.has(w.mesh)) { tinted.set(w.mesh, own); w.mesh.material = tintOf(own); }   // (a picked wire stays picked)
        else w.mesh.material = own;
        w.hull.material = fade ? fadeOutlineMaterial : outlineMaterial;
        w.hull.renderOrder = fade ? 1 : 0; w.mesh.renderOrder = fade ? 2 : 0;
        w.faded = !!fade;
      }
      // a frame carried along the line without twisting
      wt.set(pts[3] - pts[0], pts[4] - pts[1], pts[5] - pts[2]).normalize();
      wn.set(0, 1, 0); if (Math.abs(wt.y) > 0.9) wn.set(1, 0, 0);
      wn.addScaledVector(wt, -wn.dot(wt)).normalize();
      for (let i = 0; i < n; i++) {
        const a = Math.max(0, i - 1) * 3, b = Math.min(n - 1, i + 1) * 3;
        wp.set(pts[b] - pts[a], pts[b + 1] - pts[a + 1], pts[b + 2] - pts[a + 2]);
        if (wp.lengthSq() > 1e-12) wt.copy(wp).normalize();
        wn.addScaledVector(wt, -wn.dot(wt)); if (wn.lengthSq() < 1e-8) wn.set(wt.y, wt.z, wt.x).addScaledVector(wt, -(wt.y * wt.x + wt.z * wt.y + wt.x * wt.z)); wn.normalize();
        wb.crossVectors(wt, wn);
        for (let j = 0; j < RADIAL; j++) {
          const ang = j / RADIAL * Math.PI * 2, c = Math.cos(ang), s = Math.sin(ang), k = (i * RADIAL + j) * 3;
          const nx = wn.x * c + wb.x * s, ny = wn.y * c + wb.y * s, nz = wn.z * c + wb.z * s;
          na[k] = nx; na[k + 1] = ny; na[k + 2] = nz;
          pa[k] = pts[i * 3] + nx * radius; pa[k + 1] = pts[i * 3 + 1] + ny * radius; pa[k + 2] = pts[i * 3 + 2] + nz * radius;
        }
      }
      for (const [k, i, sign] of [[n * RADIAL * 3, 0, -1], [(n * RADIAL + 1) * 3, n - 1, 1]]) {   // cap centres, facing out along the line
        const a = Math.max(0, i - 1) * 3, b = Math.min(n - 1, i + 1) * 3;
        wp.set(pts[b] - pts[a], pts[b + 1] - pts[a + 1], pts[b + 2] - pts[a + 2]).normalize().multiplyScalar(sign);
        pa[k] = pts[i * 3]; pa[k + 1] = pts[i * 3 + 1]; pa[k + 2] = pts[i * 3 + 2]; na[k] = wp.x; na[k + 1] = wp.y; na[k + 2] = wp.z;
      }
      P.needsUpdate = N.needsUpdate = true; w.mesh.visible = true;
      w.mesh.geometry.boundingSphere = w.mesh.geometry.boundingBox = null;   // worked out afresh if the pointer asks
    }
    dirty = true;
  }

  // dark marks drawn across the cut ends of wires that continue off the picture
  const markMaterial = new LineMaterial({color: 0x111111, linewidth: 2.6});
  const marks = new THREE.Group();
  world.add(marks);
  function setMarks(polylines) {
    for (const l of [...marks.children]) { l.geometry.dispose(); marks.remove(l); }
    for (const pts of polylines) { const g = new LineGeometry(); g.setPositions(pts.flat()); marks.add(new Line2(g, markMaterial)); }
    dirty = true;
  }

  // ---- render on demand
  let dirty = true, width = 1, height = 1;
  const setHullResolution = (w, h) => { for (const m of [outlineMaterial, fadeOutlineMaterial]) m.uniforms.resolution.value.set(w, h); };
  const listeners = [];
  const invalidate = () => { dirty = true; };
  function resize() {
    width = Math.max(1, container.clientWidth); height = Math.max(1, container.clientHeight);
    pixelRatio = Math.min(devicePixelRatio || 1, pixelRatioCap);       // re-read: browser zoom changes it
    renderer.setPixelRatio(pixelRatio);
    renderer.setSize(width, height); camera.aspect = width / height; camera.updateProjectionMatrix();
    lineMaterial.resolution.set(width, height); markMaterial.resolution.set(width, height); setHullResolution(width * pixelRatio, height * pixelRatio); dirty = true;
  }
  let counted = 0, slow = 0, last = 0;
  function frame(now, animating) {
    if (!animating) last = 0;
    const moved = controls ? controls.update() : false;
    if (!(dirty || moved || animating)) return false;
    fitDepth(camera);
    renderer.render(scene, camera);
    dirty = false;
    for (const fn of listeners) fn();
    // If step animations run slowly on this device, give up some sharpness for smoothness. Judged by the time
    // between animation frames (which includes the GPU's share), over every 40 of them; 40 ms allows for 30 Hz screens.
    if (animating && pixelRatio > 1) {
      if (last) { counted++; if (now - last > 40) slow++; }
      last = now;
      if (counted >= 40) { if (slow > 20) { pixelRatioCap = 1; resize(); } counted = slow = 0; }
    }
    return true;
  }
  if (controls) controls.addEventListener('change', invalidate);
  renderer.domElement.addEventListener('webglcontextrestored', invalidate);   // rendering is on demand, so ask for a frame once the GPU is back
  resize();

  // ---- off-screen snapshots (step thumbnails, part images). Returns a canvas; never touches the visible frame.
  function snapshot(w, h, {transparent = false, setup} = {}) {
    const target = new THREE.WebGLRenderTarget(w, h, {samples: 4});
    const cam = camera.clone(); cam.aspect = w / h; cam.updateProjectionMatrix();
    const restore = setup ? setup(cam) : null;
    fitDepth(cam);
    const prevColor = renderer.getClearColor(new THREE.Color()), prevAlpha = renderer.getClearAlpha();
    renderer.setClearColor(transparent ? 0x000000 : 0xffffff, transparent ? 0 : 1);
    lineMaterial.resolution.set(w, h); markMaterial.resolution.set(w, h); setHullResolution(w, h);
    renderer.setRenderTarget(target); renderer.clear(); renderer.render(scene, cam); renderer.setRenderTarget(null);
    const px = new Uint8Array(w * h * 4);
    renderer.readRenderTargetPixels(target, 0, 0, w, h, px);
    target.dispose();
    renderer.setClearColor(prevColor, prevAlpha); lineMaterial.resolution.set(width, height); markMaterial.resolution.set(width, height); setHullResolution(width * pixelRatio, height * pixelRatio);
    if (restore) { restore(); scene.updateMatrixWorld(); }   // no frame may follow, and picking reads these matrices
    const canvas = document.createElement('canvas'); canvas.width = w; canvas.height = h;
    const ctx = canvas.getContext('2d'), img = ctx.createImageData(w, h), row = w * 4;
    for (let y = 0; y < h; y++) img.data.set(px.subarray((h - 1 - y) * row, (h - y) * row), y * row);   // flip: GL rows run bottom-up
    if (transparent) {                                 // soft edge pixels come back premultiplied; canvas wants straight alpha
      const d = img.data;
      for (let i = 0; i < d.length; i += 4) { const a = d[i + 3]; if (a > 0 && a < 255) { const k = 255 / a; d[i] = Math.min(255, d[i] * k); d[i + 1] = Math.min(255, d[i + 1] * k); d[i + 2] = Math.min(255, d[i + 2] * k); } }
    }
    ctx.putImageData(img, 0, 0);
    return {canvas, camera: cam};
  }

  const setLight = v => { LIGHT.copy(v).normalize(); dirty = true; };   // every material shares this one light direction
  return {THREE, renderer, scene, camera, controls, root, assembly, parts, materials, edgeMaterial, lineMaterial, world, worldFor, setWorld, toWorld, fromWorld, setHighlight, highlighted: () => picked,
          setOffset, setPose, poseMatrix, setVisible, setFade, clearFades, boundsOf, cameraPose, setLeadLines, setArrows, setArrowAlphas, arrows, setWires, setMarks, wireGroup, setLight, invalidate, resize, frame, snapshot,
          onRender: fn => listeners.push(fn), get width() { return width; }, get height() { return height; },
          contextLost: () => renderer.getContext().isContextLost(),
          info: () => ({calls: renderer.info.render.calls, triangles: renderer.info.render.triangles, lines: renderer.info.render.lines, pixelRatio})};
}
