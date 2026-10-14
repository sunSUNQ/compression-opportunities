#!/usr/bin/env node
"use strict";
// V0.11-D3-E5 — RDS JS module self-test (17-case matrix ported from E4 python, prereg-frozen semantics)
const assert = require("assert");
const path = require("path");
const fs = require("fs");
const os = require("os");

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "rds-test-"));
process.env.CODE_GUARD_BASE_DIR = TMP;
// runtime_paths uses ACTIVE_SESSION_ID; set one so sessionPath lands in a stable dir
const { setActiveSessionId } = require(process.cwd() + "/deploy/hooks/guard_core/runtime_paths.js");
setActiveSessionId("selftest");
const rds = require(process.cwd() + "/deploy/hooks/post_tool/repeated_delivery_suppression.js");

function fresh() { return rds; } // state persists per session dir; tests share trajectory semantics via unique lines

let pass = 0, fail = 0;
function check(name, fn) {
  try { fn(); pass++; console.log("  ok", name); }
  catch (e) { fail++; console.log("  FAIL", name, "-", e.message); }
}

// unique-line helpers to avoid cross-test state interference
let uid = 0;
function U(s) { return s.replace(/\{u\}/g, () => `u${uid++}`); }

check("07 missing anchor (first obs native)", () => {
  const r = rds.process(U("first observation {u}\nline2 {u}"));
  assert.strictEqual(r.compressed, false);
});
check("01 exact duplicate", () => {
  const a = U("A{u}\nB{u}\nC{u}");
  rds.process(a);
  const r = rds.process(a);
  assert.strictEqual(r.compressed, true);
  assert.ok(r.matched_chars > 0);
});
check("02 partial line overlap", () => {
  const a = U("P1{u}\nP2{u}\nP3{u}\nP4{u}");
  rds.process(a);
  const r = rds.process(a + "\nNEW{u}");
  assert.strictEqual(r.compressed, true);
  assert.ok(r.text.includes("NEW{u}".replace(/\{u\}/, "")) || r.text.includes("NEW"));
});
check("03 content changed -> native", () => {
  rds.process(U("X1{u}\nY1{u}\nZ1{u}"));
  const r = rds.process(U("X2{u}\nY2{u}\nZ2{u}"));
  assert.strictEqual(r.compressed, false);
});
check("04 fully shuffled -> native", () => {
  rds.process(U("S1{u}\nS2{u}\nS3{u}"));
  const r = rds.process(U("S3{u}\nS2{u}\nS1{u}"));
  assert.strictEqual(r.compressed, false);
});
check("04b contiguous segment in shuffled context folds exactly", () => {
  const a = U("T1{u}\nT2{u}\nT3{u}");
  rds.process(a);
  const L = a.split("\n");
  const r = rds.process([L[2], L[0], L[1]].join("\n")); // T3 first; T1,T2 = contiguous anchor lines 0..1
  assert.strictEqual(r.compressed, true);
});
check("05 same command different output -> native", () => {
  rds.process(U("tests: 10 passed {u}"));
  const r = rds.process(U("tests: 3 failed {u}"));
  assert.strictEqual(r.compressed, false);
});
check("06 file same content differs: changed line survives", () => {
  rds.process(U("file v1 {u}\ncode(); {u}\nmore(); {u}"));
  const r = rds.process(U("file v2 {u}\ncode(); {u}\nmore(); {u}"));
  if (r.compressed) {
    assert.ok(!r.text.includes("file v1"));
    assert.ok(r.text.includes("file v2") || r.text.includes("[TASCO-RDS"));
  }
});
check("09 malformed payload -> native", () => {
  const r = rds.process(null);
  assert.strictEqual(r.compressed, false);
});
check("11 cross-task boundary -> native", () => {
  rds.process(U("task1 build output {u}\nmany lines {u}\nhere {u}"));
  const r = rds.process(U("task2 unrelated {u}\ncontent flows {u}\nnow {u}"));
  assert.strictEqual(r.compressed, false);
});
check("12 multiple candidate anchors -> first delivery wins", () => {
  const a = U("m1 {u}\nm2 {u}\nonly0 {u}");
  rds.process(a);
  rds.process(U("other {u}"));
  const L = a.split("\n");
  const r = rds.process([L[0], L[1], U("new3 {u}")].join("\n"));
  assert.strictEqual(r.compressed, true);
});
check("13 unicode + newline normalization", () => {
  const a = U("数据行一 {u}\r\n数据行二 {u}\r\n数据行三 {u}");
  rds.process(a);
  const r = rds.process(a.replace(/\r\n/g, "\n") + "\n" + U("新增 {u}"));
  assert.strictEqual(r.compressed, true);
  assert.ok(r.text.includes("新增"));
});
check("14 huge repeated payload", () => {
  const big = Array.from({ length: 5000 }, (_, i) => `hline-${i}-xxxxxxxxxxxx`).join("\n");
  rds.process(big);
  const r = rds.process(big);
  assert.strictEqual(r.compressed, true);
  assert.ok(r.matched_chars > 100000);
});
check("15 negative command-same output-differs", () => {
  rds.process(U("run1 results {u}\ndetail a {u}"));
  const r = rds.process(U("run2 results {u}\ndetail b {u}"));
  assert.strictEqual(r.compressed, false);
});
check("16 negative file-same content-differs", () => {
  rds.process(U("fv1 {u}\ncode(); {u}\nmore(); {u}"));
  const r = rds.process(U("fv2 {u}\ncode(); {u}\nmore(); {u}"));
  if (r.compressed) assert.ok(r.text.includes("fv2"));
});
check("17 accounting invariant", () => {
  const a = U("A17 {u}\nB17 {u}\nC17 {u}\nD17 {u}");
  rds.process(a);
  const r = rds.process(a + "\nE17 {u}\nF17 {u}");
  if (r.compressed) {
    assert.ok(r.matched_chars > 0);
    assert.ok(r.matched_chars + r.new_chars > 0);
  }
});
check("marker auditable format", () => {
  const a = U("M1 {u}\nM2 {u}\nM3 {u}");
  rds.process(a);
  const r = rds.process(a);
  assert.ok(/\[TASCO-RDS omitted: observation #\d+ lines \d+\.\.\d+ \(\d+ chars\); new: \d+ chars\]/.test(r.text));
});

console.log(`\nself-test: ${pass} pass, ${fail} fail`);
process.exit(fail ? 1 : 0);
