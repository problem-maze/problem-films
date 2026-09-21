#!/usr/bin/env node
'use strict';

const fs = require('fs');
const crypto = require('crypto');

const [r0Path, buildPath, probePath] = process.argv.slice(2);
if (!r0Path || !buildPath || !probePath) {
  throw new Error('usage: validate_v8_r1_cinematic_reality.js R0_BUILD R1_BUILD R1_PROBE');
}

const read = path => fs.readFileSync(path, 'utf8');
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const slice = (value, start, end) => {
  const a = value.indexOf(start);
  if (a < 0) throw new Error(`missing start marker: ${start}`);
  const b = value.indexOf(end, a + start.length);
  if (b < 0) throw new Error(`missing end marker: ${end}`);
  return value.slice(a, b);
};
const templateProperty = (value, objectName, propertyName) => {
  const a = value.indexOf(`const ${objectName}=`);
  const b = value.indexOf(` ${propertyName}:\``, a);
  if (a < 0 || b < 0) throw new Error(`missing ${objectName}.${propertyName}`);
  const c = b + ` ${propertyName}:\``.length;
  return value.slice(c, value.indexOf('`', c));
};
const balanced = source => {
  const pairs = {')': '(', ']': '[', '}': '{'};
  const stack = [];
  for (const ch of source) {
    if ('([{'.includes(ch)) stack.push(ch);
    else if (')]}'.includes(ch) && stack.pop() !== pairs[ch]) return false;
  }
  return stack.length === 0;
};

const r0 = read(r0Path);
const build = read(buildPath);
const probe = read(probePath);

function runtime(value) {
  const authoredSource = slice(
    value,
    'function makeAuthoredSharkGeometry(){',
    'const OCEAN_SHADERS={'
  );
  const oceanSource = slice(value, 'function makeOceanGeometry(){', "if(typeof module!=='undefined')module.exports=makeOceanGeometry;");
  const mathSource = slice(value, 'const OceanMath=(()=>{', "if(typeof module!=='undefined')module.exports=OceanMath;");
  const OceanMath = new Function(`${mathSource};return OceanMath;`)();
  const makeAuthoredSharkGeometry = new Function(`${authoredSource};return makeAuthoredSharkGeometry;`)();
  const makeOceanGeometry = new Function(`${oceanSource};return makeOceanGeometry;`)();
  const poseSource = slice(value, ' function g1Pose(t){', ' function g1Bank(t){');
  const bankSource = slice(value, ' function g1Bank(t){', ' function render(){');
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const g1Pose = new Function('OceanMath', 'clamp', `${poseSource};return g1Pose;`)(OceanMath, clamp);
  const g1Bank = new Function('clamp', `${bankSource};return g1Bank;`)(clamp);
  return {authoredSource, oceanSource, mathSource, OceanMath, makeAuthoredSharkGeometry, makeOceanGeometry, g1Pose, g1Bank, poseSource, bankSource};
}

const r0Runtime = runtime(r0);
const r1Runtime = runtime(build);
const whale = r1Runtime.makeAuthoredSharkGeometry();
const generatedScene = r1Runtime.makeOceanGeometry();

let finiteValues = 0;
let nonFiniteValues = 0;
for (const values of [...Object.values(generatedScene), whale]) {
  for (const value of values) {
    finiteValues++;
    if (!Number.isFinite(value)) nonFiniteValues++;
  }
}

const transform = (m, x, y, z) => [
  m[0] * x + m[4] * y + m[8] * z + m[12],
  m[1] * x + m[5] * y + m[9] * z + m[13],
  m[2] * x + m[6] * y + m[10] * z + m[14],
  m[3] * x + m[7] * y + m[11] * z + m[15],
];

function projectAt(rt, t, region = () => true) {
  const aspect = 390 / 844;
  const cam = rt.OceanMath.shot(t, aspect, 0, 0, 1);
  const model = rt.g1Pose(t);
  let total = 0;
  let inside = 0;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (let i = 0; i < whale.length; i += 10) {
    const x = whale[i], y = whale[i + 1], z = whale[i + 2];
    if (!region(x, y, z, whale[i + 8], whale[i + 9])) continue;
    const world = transform(model, x, y, z);
    const clip = transform(cam.vp, world[0], world[1], world[2]);
    const nx = clip[0] / clip[3], ny = clip[1] / clip[3];
    if (!Number.isFinite(nx) || !Number.isFinite(ny)) continue;
    total++;
    minX = Math.min(minX, nx); maxX = Math.max(maxX, nx);
    minY = Math.min(minY, ny); maxY = Math.max(maxY, ny);
    if (clip[3] > 0 && nx >= -1 && nx <= 1 && ny >= -1 && ny <= 1) inside++;
  }
  return {
    t,
    percent: total ? +(inside / total * 100).toFixed(1) : 0,
    bounds: [minX, maxX, minY, maxY].map(value => +value.toFixed(3)),
    eye: cam.eye.map(value => +value.toFixed(3)),
    target: cam.target.map(value => +value.toFixed(3)),
    fovDegrees: +(Math.atan(cam.tan) * 2 * 180 / Math.PI).toFixed(3),
    deep: +cam.deep.toFixed(3),
  };
}

const regions = {
  head: x => x < -4.15,
  shoulder: x => x >= -4.15 && x < -1.15,
  torso: x => x >= -1.15 && x < 3.10,
  posterior: x => x >= 2.25,
  full: () => true,
};
const times = [0, 1.25, 2.5, 4.25, 5.5, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10.2, 10.7, 11.2, 11.6, 12];
const framing = {};
for (const t of times) {
  framing[t] = {};
  for (const [name, region] of Object.entries(regions)) framing[t][name] = projectAt(r1Runtime, t, region);
}

let cameraNonFinite = 0;
let maxEyeSpeed = 0;
let maxTargetSpeed = 0;
let maxFovRate = 0;
let previous = null;
const hz = 240;
for (let i = 0; i <= 12 * hz; i++) {
  const t = i / hz;
  const cam = r1Runtime.OceanMath.shot(t, 390 / 844, 0, 0, 1);
  const numbers = [...cam.eye, ...cam.target, cam.tan, cam.deep];
  if (numbers.some(value => !Number.isFinite(value))) cameraNonFinite++;
  if (previous) {
    const speed = (a, b) => Math.hypot(...a.map((value, index) => value - b[index])) * hz;
    maxEyeSpeed = Math.max(maxEyeSpeed, speed(cam.eye, previous.eye));
    maxTargetSpeed = Math.max(maxTargetSpeed, speed(cam.target, previous.target));
    maxFovRate = Math.max(maxFovRate, Math.abs(cam.tan - previous.tan) * hz);
  }
  previous = cam;
}

const protectedSpans = {
  authoredGeometry: [r0Runtime.authoredSource, r1Runtime.authoredSource],
  fullPropulsionVertexShader: [templateProperty(r0, 'VM4_SHARK_SHADERS', 'meshVS'), templateProperty(build, 'V8R1_SHARK_SHADERS', 'meshVS')],
  safePropulsionVertexShader: [templateProperty(r0, 'VM4_SHARK_SHADERS_SAFE', 'meshVS'), templateProperty(build, 'V8R1_SHARK_SHADERS_SAFE', 'meshVS')],
  sharkPose: [r0Runtime.poseSource, r1Runtime.poseSource],
  sharkBank: [r0Runtime.bankSource, r1Runtime.bankSource],
};
const protectedResults = {};
for (const [name, [before, after]] of Object.entries(protectedSpans)) {
  protectedResults[name] = {pass: before === after, sha256: sha(after), bytes: Buffer.byteLength(after)};
}

const shaderSets = [
  ['fullEnvironment', 'OCEAN_SHADERS', ['meshVS', 'meshFS', 'backVS', 'backFS', 'beamVS', 'beamFS', 'dustVS', 'dustFS', 'bubbleVS', 'bubbleFS', 'postVS', 'postFS']],
  ['safeEnvironment', 'OCEAN_SHADERS_SAFE', ['meshFS', 'backFS', 'postFS']],
  ['fullShark', 'V8R1_SHARK_SHADERS', ['meshVS', 'meshFS']],
  ['safeShark', 'V8R1_SHARK_SHADERS_SAFE', ['meshVS', 'meshFS']],
];
const shaderSanity = {};
for (const [label, objectName, properties] of shaderSets) {
  shaderSanity[label] = {};
  for (const property of properties) {
    const source = templateProperty(build, objectName, property);
    shaderSanity[label][property] = {balanced: balanced(source), main: /void\s+main\s*\(/.test(source), bytes: Buffer.byteLength(source)};
  }
}
for (const [label, constantName] of [['cornea', 'V8R1_CORNEA_FS'], ['waterShell', 'V8R1_WATER_SHELL_FS']]) {
  const marker = `const ${constantName}=\``;
  const start = build.indexOf(marker) + marker.length;
  const source = build.slice(start, build.indexOf('`', start));
  shaderSanity[label] = {balanced: balanced(source), main: /void\s+main\s*\(/.test(source), bytes: Buffer.byteLength(source)};
}

const identitySpans = [
  ['geometry', 'function makeAuthoredSharkGeometry(){', 'const OCEAN_SHADERS={'],
  ['math', 'const OceanMath=(()=>{', "if(typeof module!=='undefined')module.exports=OceanMath;"],
  ['fullEnvironment', 'const OCEAN_SHADERS={', "if(typeof module!=='undefined')module.exports=OCEAN_SHADERS;"],
  ['safeEnvironment', 'const OCEAN_SHADERS_SAFE={', 'const V8R1_SHARK_SHADERS='],
  ['fullShark', 'const V8R1_SHARK_SHADERS={', 'const V8R1_SHARK_SHADERS_SAFE='],
  ['safeShark', 'const V8R1_SHARK_SHADERS_SAFE={', 'const V8R1_CORNEA_FS='],
  ['render', ' function common(p,cam){', ' function updateUI(){'],
];
const probeIdentity = {};
for (const [label, start, end] of identitySpans) {
  const buildSpan = slice(build, start, end);
  const probeSpan = slice(probe, start, end);
  probeIdentity[label] = {pass: buildSpan === probeSpan, sha256: sha(buildSpan), bytes: Buffer.byteLength(buildSpan)};
}

const r0Comparison = {};
for (const t of [0, 2.5, 7, 8, 9, 10.2, 10.7, 11.6, 12]) {
  r0Comparison[t] = {};
  for (const [name, region] of Object.entries(regions)) {
    const r0Frame = projectAt(r0Runtime, t, region);
    const r1Frame = projectAt(r1Runtime, t, region);
    r0Comparison[t][name] = {r0: r0Frame.percent, r1: r1Frame.percent, r0Bounds: r0Frame.bounds, r1Bounds: r1Frame.bounds};
  }
  r0Comparison[t].camera = {r0: projectAt(r0Runtime, t), r1: projectAt(r1Runtime, t)};
}

const result = {
  files: {
    build: {bytes: Buffer.byteLength(build), sha256: sha(build)},
    probe: {bytes: Buffer.byteLength(probe), sha256: sha(probe)},
  },
  geometry: {
    authoredTriangles: whale.length / 10 / 3,
    authoredVertices: whale.length / 10,
    authoredFloats: whale.length,
    allSceneValues: finiteValues,
    nonFiniteValues,
  },
  camera: {
    samples: 12 * hz + 1,
    nonFiniteSamples: cameraNonFinite,
    maxEyeSpeed: +maxEyeSpeed.toFixed(6),
    maxTargetSpeed: +maxTargetSpeed.toFixed(6),
    maxFovTangentRate: +maxFovRate.toFixed(8),
  },
  framing,
  r0Comparison,
  protectedResults,
  shaderSanity,
  probeIdentity,
  architecture: {
    buildCanvas2DCalls: (build.match(/getContext\(['"]2d['"]\)/g) || []).length,
    probeCanvas2DCalls: (probe.match(/getContext\(['"]2d['"]\)/g) || []).length,
    buildRequestAnimationFrameOccurrences: (build.match(/requestAnimationFrame/g) || []).length,
    probeRequestAnimationFrameOccurrences: (probe.match(/requestAnimationFrame/g) || []).length,
    fullPath: build.includes("state.renderer='v8r1-full'"),
    safePath: build.includes("state.renderer='v8r1-webgl-safe'"),
    reducedMotion: build.includes("prefers-reduced-motion: reduce") && build.includes('state.reduced=media.matches'),
    fullCompileFixUCine: templateProperty(build, 'V8R1_SHARK_SHADERS', 'meshFS').includes('uniform float uCine;'),
    fullCompileFixMouthMask: templateProperty(build, 'OCEAN_SHADERS', 'meshFS').includes('float mouthMask=0.;'),
  },
};

console.log(JSON.stringify(result, null, 2));
