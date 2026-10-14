#!/usr/bin/env node
'use strict';
/*
 * V0.11-D3 — natural opportunity census (mechanical).
 * Prereg: docs/architecture/V0.11-D3-NATURAL-OPPORTUNITY-CENSUS-PREREG-V1.md (FROZEN, 49482bbf, before aggregation)
 * Zero-run audit over existing real-agent sessions. Shape taxonomy by raw output characteristics, not capability names.
 */
const fs = require('fs');
const path = require('path');

const WT = process.cwd();
const MAIN = 'C:/Users/sunqinghw/Documents/hook\u8fc1\u79fbagent';
const OUT = path.join(WT, 'evidence', 'V1', 'v011-d3-natural-opportunity-census.json');

const SOURCES = [
  { id: 'C1', root: path.join(WT, 'hook_ab_test/results/v010_c1_task_level_20260923'), natural: 'natural', note: 'task-level A/B batch (negative formal, included per prereg)' },
  { id: 'D2', root: path.join(WT, 'hook_ab_test/results/v011_d2_terminal_qualification_20260923'), natural: 'natural', note: 'terminal-state A/B batch (Q1=0 formal, included)' },
  { id: 'P2', root: path.join(WT, 'hook_ab_test/results/v1d_adv1_p2_formal_20260921'), natural: 'natural' },
  { id: 'R2A1', root: path.join(WT, 'hook_ab_test/results/v1d_adv1_r2a1_fresh_20260922'), natural: 'natural' },
  { id: 'R2A2', root: path.join(WT, 'hook_ab_test/results/v1d_adv1_r2a2_fresh_20260922'), natural: 'natural' },
  { id: 'CB0', root: path.join(MAIN, 'hook_ab_test/results/v1cb0_baseline_20260917'), natural: 'natural', note: 'natural-task coverage baseline universe' },
  { id: 'B4VD', root: path.join(MAIN, 'hook_ab_test/results/b4_vd_natural_20260915'), natural: 'natural-capability-watch', note: 'validation-delta default-on observation batch; VD overlap flagged' },
];

function readJson(p) { try { return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '')); } catch (_e) { return null; } }
function listSessions(root) {
  const out = [];
  if (!fs.existsSync(root)) return out;
  const stack = [root];
  while (stack.length) {
    const d = stack.pop();
    let es;
    try { es = fs.readdirSync(d, { withFileTypes: true }); } catch (_e) { continue; }
    for (const e of es) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) {
        const base = e.name;
        if (base.startsWith('_') || base.includes('excluded_infra')) continue;
        stack.push(p);
      } else if (e.name === 'summary.json') {
        // session dir = directory containing summary.json; skip anything under a _work/_smoke/_scratch path segment
        const rel = path.relative(root, d);
        if (/(_work|_smoke|_scratch|excluded_infra)/.test(rel)) continue;
        // session identity = relative dir; dedupe (workdir copies under .tasco-runs are inside _work so already filtered)
        out.push({ id: rel.replace(/\\/g, '/'), dir: d });
      }
    }
  }
  return out;
}
function toolClass(t) {
  const s = (t || '').toLowerCase();
  if (s.includes('shell')) return 'shell';
  if (s.includes('read') || s.includes('file')) return 'read';
  if (s.includes('grep') || s.includes('search')) return 'search';
  return 'other';
}

const sessions = [];
for (const src of SOURCES) {
  for (const s of listSessions(src.root)) sessions.push({ source: src.id, natural: src.natural, ...s });
}

// parse events per session
const parsed = [];
for (const s of sessions) {
  const f = findFirstRecursive(s.dir, 'tasco_compression.ndjson');
  if (!f) { parsed.push({ ...s, events: [], no_telemetry: true }); continue; }
  const events = [];
  for (const ln of fs.readFileSync(f, 'utf8').split(/\r?\n/)) {
    if (!ln.trim()) continue;
    const r = readJsonRaw(ln);
    if (!r) continue;
    events.push({
      tool: r.tool, tclass: toolClass(r.tool), scenario: r.scenario,
      chars: r.before_chars || 0, key: r.access && r.access.key, ts: r.timestamp,
      selected: r.selected === true, applied: r.applied === true,
      eligible: r.eligible === true, reason: r.eligibility_reason,
      recovery: r.recovery_detected === true,
      test_executed: r.test_executed === true, test_exit: r.test_exit_code,
    });
  }
  events.sort((a, b) => (a.ts || '').localeCompare(b.ts || ''));
  parsed.push({ ...s, events });
}
function readJsonRaw(ln) { try { return JSON.parse(ln); } catch (_e) { return null; } }
function findFirstRecursive(dir, name) {
  const stack = [dir];
  while (stack.length) {
    const d = stack.pop(); let es;
    try { es = fs.readdirSync(d, { withFileTypes: true }); } catch (_e) { continue; }
    for (const e of es) { const p = path.join(d, e.name); if (e.isDirectory()) stack.push(p); else if (e.name === name) return p; }
  }
  return null;
}

// ---- shape assignment (frozen rules, prereg section 3) ----------------------
const shapeSessions = {}; // shape -> Set(sessionKey)
const shapeEvents = {};   // shape -> [event records with session context]
function mark(shape, sess, ev, extra) { (shapeSessions[shape] ||= new Set()).add(sess.source + '/' + sess.id); (shapeEvents[shape] ||= []).push({ source: sess.source, session: sess.id, natural: sess.natural, n_events: sess.events.length, ...ev, ...extra }); }

for (const sess of parsed) {
  const evs = sess.events;
  const n = evs.length;
  if (!n) continue;
  evs.forEach((ev, i) => {
    ev.pos = (i + 1) / n;
    ev.turns_after = n - (i + 1);
  });
  // S1 large_tool_output
  for (const ev of evs) if (ev.chars >= 2000) mark('S1_large_tool_output', sess, ev);
  // key repetition maps
  const byKey = {};
  evs.forEach((ev, i) => { if (ev.key) (byKey[ev.key] ||= []).push(i); });
  // S2/S3 repeated command rerun (shell same key)
  for (const k of Object.keys(byKey)) {
    const idxs = byKey[k];
    if (idxs.length >= 2 && evs[idxs[0]].tclass === 'shell') {
      for (const i of idxs) mark('S2_repeated_command_rerun', sess, evs[i], { repeat_count: idxs.length });
      if (idxs.length >= 3) for (const i of idxs) mark('S3_multi_rerun_validation', sess, evs[i], { repeat_count: idxs.length });
    }
    if (idxs.length >= 2 && evs[idxs[0]].tclass !== 'shell') for (const i of idxs) mark('S4_repeated_read', sess, evs[i], { repeat_count: idxs.length });
    // S5 immediate reread: non-shell event followed within <=2 events by same key
    for (let j = 0; j < idxs.length - 1; j++) {
      const i = idxs[j], nxt = idxs[j + 1];
      if (evs[i].tclass !== 'shell' && nxt - i <= 2) mark('S5_immediate_reread', sess, evs[nxt], { gap: nxt - i });
    }
  }
  // S6 terminal summary shape (last shell event >=1000)
  const lastShell = (() => { for (let i = n - 1; i >= 0; i--) if (evs[i].tclass === 'shell') return i; return -1; })();
  if (lastShell >= 0 && evs[lastShell].chars >= 1000) mark('S6_terminal_summary_shape', sess, evs[lastShell]);
  // S7/S7b large failing/passing test output
  for (const ev of evs) {
    if (ev.test_executed && ev.chars >= 3000) {
      if (ev.test_exit !== 0 && ev.test_exit !== null) mark('S7_large_failing_output', sess, ev);
      if (ev.test_exit === 0) mark('S7b_large_passing_output', sess, ev);
    }
  }
  // S8 search fanout
  for (const ev of evs) if (ev.tclass === 'search' && ev.chars >= 2000) mark('S8_search_fanout', sess, ev);
}

// ---- per-shape aggregate stats (frozen fields, prereg section 4) ------------
function med(a) { const s = a.slice().sort((x, y) => x - y); return s.length ? s[Math.floor((s.length - 1) / 2)] : null; }
function p75(a) { const s = a.slice().sort((x, y) => x - y); return s.length ? s[Math.min(s.length - 1, Math.floor(0.75 * s.length))] : null; }
const totalSessions = parsed.filter(s => s.events.length > 0).length;
const census = {};
for (const shape of Object.keys(shapeSessions)) {
  const evs = shapeEvents[shape];
  const sessCount = shapeSessions[shape].size;
  const repeatCounts = evs.filter(e => e.repeat_count).map(e => e.repeat_count);
  const downstreamReread = (() => { // recompute from stored gap/reread markers only where defined
    const withKey = evs.filter(e => e.repeat_count);
    return withKey.length ? +(withKey.filter(e => e.repeat_count >= 2).length / withKey.length).toFixed(3) : null;
  })();
  census[shape] = {
    sessions_with_shape: sessCount,
    session_incidence: +(sessCount / totalSessions).toFixed(3),
    events_with_shape: evs.length,
    median_raw_chars: med(evs.map(e => e.chars)),
    p75_raw_chars: p75(evs.map(e => e.chars)),
    median_position_in_trajectory: +med(evs.map(e => e.pos)).toFixed(3),
    median_turns_after_event: med(evs.map(e => e.turns_after)),
    trajectory_exposure: (() => { const t = med(evs.map(e => e.turns_after)); return t === null ? null : (t <= 1 ? 'LOW' : t <= 5 ? 'MEDIUM' : 'HIGH'); })(),
    repeat_frequency: repeatCounts.length ? +med(repeatCounts).toFixed(2) : null,
    downstream_reread_rate: downstreamReread,
    downstream_recovery_rate: +med(evs.map(e => (e.recovery ? 1 : 0))).toFixed(3),
    existing_compression_overlap: +med(evs.map(e => (e.selected || e.applied ? 1 : 0))).toFixed(3),
    overlap_by_source: Object.fromEntries([...new Set(evs.map(e => e.source))].map(src => [src, +med(evs.filter(e => e.source === src).map(e => (e.selected || e.applied ? 1 : 0))).toFixed(3)])),
    historical_task_level_delta_if_known: { S2: null, S3: null, S7: 'validation/test rerun negative task-level evidence exists only for transport/terminal lines (C1/D2), not for this shape per se' }[shape] ?? null,
    correctness_risk_note: 'oracle pass rate of involved sessions reported at batch level; shape-local correctness risk not derivable mechanically',
  };
  census[shape].candidate_pool = census[shape].session_incidence >= 0.20 && census[shape].median_raw_chars >= 1000;
}

// tool enumeration (mechanical mapping audit)
const toolEnum = {};
for (const sess of parsed) for (const ev of sess.events) toolEnum[ev.tool] = (toolEnum[ev.tool] || 0) + 1;

const pool = Object.entries(census).filter(([, v]) => v.candidate_pool)
  .sort((a, b) => b[1].session_incidence - a[1].session_incidence || b[1].median_raw_chars - a[1].median_raw_chars);

const out = {
  schema_version: 1,
  stage: 'V0.11-D3 natural opportunity census (audit-only zero-run; prereg 49482bbf FROZEN before aggregation)',
  date: '2026-09-23',
  universe: {
    sources: SOURCES.map(s => ({ id: s.id, natural: s.natural, note: s.note })),
    sessions_enumerated: sessions.length,
    sessions_with_telemetry: totalSessions,
    sessions_without_telemetry: parsed.length - totalSessions,
  },
  tool_enumeration: toolEnum,
  shapes: census,
  candidate_pool: pool.map(([k]) => k),
  top3_by_frozen_order: pool.slice(0, 3).map(([k, v]) => ({
    shape: k, session_incidence: v.session_incidence, median_raw_chars: v.median_raw_chars, p75_raw_chars: v.p75_raw_chars,
    trajectory_exposure: v.trajectory_exposure, median_turns_after_event: v.median_turns_after_event,
    existing_compression_overlap: v.existing_compression_overlap, overlap_by_source: v.overlap_by_source,
    repeat_frequency: v.repeat_frequency, downstream_reread_rate: v.downstream_reread_rate,
    known_task_level_evidence: v.historical_task_level_delta_if_known,
    unknowns: 'task-level token delta for this shape is unmeasured; eligibility/threshold fit unmeasured; cross-repo generalization unmeasured',
  })),
  special_directions: {
    validation_rerun_family: ['S2_repeated_command_rerun', 'S3_multi_rerun_validation', 'S7_large_failing_output'].map(k => ({ shape: k, ...(census[k] ? { incidence: census[k].session_incidence, median_chars: census[k].median_raw_chars, exposure: census[k].trajectory_exposure } : { incidence: 0 }) })),
    read_search_repeat_family: ['S4_repeated_read', 'S5_immediate_reread', 'S8_search_fanout'].map(k => ({ shape: k, ...(census[k] ? { incidence: census[k].session_incidence, median_chars: census[k].median_raw_chars, exposure: census[k].trajectory_exposure } : { incidence: 0 }) })),
  },
  verdict: pool.length ? 'PASS — NATURAL_OPPORTUNITY_FOUND' : 'NO_NATURAL_OPPORTUNITY / STOP',
};
fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
console.log('sessions enumerated:', sessions.length, '| with telemetry:', totalSessions);
console.log('tool enum:', JSON.stringify(toolEnum));
console.log('--- shapes:');
for (const [k, v] of Object.entries(census)) console.log(`${k.padEnd(30)} inc=${v.session_incidence} medChars=${v.median_raw_chars} p75=${v.p75_raw_chars} exposure=${v.trajectory_exposure} overlap=${v.existing_compression_overlap} pool=${v.candidate_pool}`);
console.log('candidate pool:', pool.map(([k]) => k).join(', ') || '(empty)');
console.log('verdict:', out.verdict);
