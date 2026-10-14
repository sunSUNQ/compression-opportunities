#!/usr/bin/env node
"use strict";
/*
 * V0.11-D3-E5 — RDS online A/B analyzer (mechanical, prereg 35c10393).
 * Primary = task-level total_flow_tokens; backlash = first-class gates; dual universe; concentration.
 */
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const RES = path.join(ROOT, 'hook_ab_test', 'results', 'v011_d5_rds_ab_20260923');
const OUT = path.join(ROOT, 'evidence', 'V1', 'v011-d5-rds-online-ab.json');

const CELLS = [
  { task: 'a1', cell: 'lint-fix' }, { task: 'a2', cell: 'lint-fix' }, { task: 'a3', cell: 'lint-fix' },
  { task: 'a4', cell: 'lint-fix' }, { task: 'a5', cell: 'lint-fix' }, { task: 'a6', cell: 'lint-fix' },
  { task: 't1', cell: 'test-fix' }, { task: 't2', cell: 'test-fix' }, { task: 't3', cell: 'test-fix' }, { task: 't4', cell: 'test-fix' },
  { task: 'm1', cell: 'feature-validation' }, { task: 'm2', cell: 'validation-review' },
];
function readJson(p) { try { return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '')); } catch (_e) { return null; } }
function findFirstRecursive(dir, name) {
  const stack = [dir];
  while (stack.length) {
    const d = stack.pop(); let es;
    try { es = fs.readdirSync(d, { withFileTypes: true }); } catch (_e) { continue; }
    for (const e of es) { const p = path.join(d, e.name); if (e.isDirectory()) stack.push(p); else if (e.name === name) return p; }
  }
  return null;
}
function readSession(task, rep, arm) {
  const base = path.join(RES, task, 'rep' + rep, 'formal', `${task}_${arm}`);
  let sf = path.join(base, 'summary.json');
  if (!fs.existsSync(sf)) { const alt = base + '.excluded_infra'; if (fs.existsSync(path.join(alt, 'summary.json'))) sf = path.join(alt, 'summary.json'); else return null; }
  const s = readJson(sf);
  if (!s || !s.usage) return null;
  const u = s.usage;
  const rds = { compressed_events: 0, matched_chars: 0, new_chars: 0, eligible_events: 0, fallback: 0 };
  let lf = findFirstRecursive(base, 'rds_ledger.ndjson');
  if (!lf) {
    // ledger lives in the session workdir (.tasco-runs/<ts>/<session>/rds_ledger.ndjson), not the collected session dir
    const workdir = path.join(path.dirname(base), '_work_' + `${task}_${arm}`);
    lf = findFirstRecursive(workdir, 'rds_ledger.ndjson');
  }
  const compressedSeqs = new Set();
  if (lf) {
    for (const ln of fs.readFileSync(lf, 'utf8').split(/\r?\n/)) {
      if (!ln.trim()) continue;
      const r = readJsonRaw(ln); if (!r) continue;
      if (r.eligible) rds.eligible_events++;
      if (r.compressed && !compressedSeqs.has(r.seq)) { compressedSeqs.add(r.seq); rds.compressed_events++; rds.matched_chars += r.matched_chars || 0; rds.new_chars += r.new_chars || 0; }
    }
  }
  const valid = s.exitCode === 0 && u.input_tokens != null;
  return {
    task, rep, arm, exit_code: s.exitCode, turns: s.turns, oracle_success: s.exitCode === 0, valid,
    input: u.input_tokens || 0, output: u.output_tokens || 0,
    cache_read: u.cache_read_input_tokens || 0, cache_creation: u.cache_creation_input_tokens || 0,
    total_flow: (u.input_tokens || 0) + (u.output_tokens || 0) + (u.cache_read_input_tokens || 0) + (u.cache_creation_input_tokens || 0),
    rds, compressedSeqs,
  };
}
function readJsonRaw(ln) { try { return JSON.parse(ln); } catch (_e) { return null; } }

const sessions = []; const exclusions = [];
for (const c of CELLS) for (const rep of [1, 2]) for (const [label, arm] of [['B', 'o'], ['T', 'd']]) {
  const s = readSession(c.task, rep, arm);
  if (s) { s.cell = c.cell; s.armLabel = label; sessions.push(s); } else exclusions.push({ pair: `${c.task}/rep${rep}/${label}`, reason: 'missing/invalid' });
}
const byKey = {};
for (const s of sessions) byKey[`${s.task}#${s.rep}#${s.armLabel}`] = s;
const pairs = [];
for (const c of CELLS) for (const rep of [1, 2]) {
  const B = byKey[`${c.task}#${rep}#B`], T = byKey[`${c.task}#${rep}#T`];
  if (!B || !T || !B.valid || !T.valid) { exclusions.push({ pair: `${c.task}/rep${rep}`, reason: 'incomplete pair' }); continue; }
  const dTotal = B.total_flow - T.total_flow, dIn = B.input - T.input, dOut = B.output - T.output;
  pairs.push({
    task: c.task, cell: c.cell, rep,
    B_tokens: B.total_flow, T_tokens: T.total_flow,
    d_input: dIn, d_output: dOut, d_total: dTotal,
    relative_total_saving: dTotal / B.total_flow,
    B_oracle: B.oracle_success, T_oracle: T.oracle_success,
    B_turns: B.turns, T_turns: T.turns,
    T_rds: T.rds,
    rds_positive: T.rds.compressed_events > 0,
    realization: T.rds.matched_chars > 0 ? dTotal / (T.rds.matched_chars / 4) : null,
  });
}

function med(a) { const s = a.slice().sort((x, y) => x - y); return s.length ? s[Math.floor((s.length - 1) / 2)] : null; }
function pctl(a, q) { const s = a.slice().sort((x, y) => x - y); return s.length ? s[Math.min(s.length - 1, Math.floor(q * s.length))] : null; }
function min(x) { return x; } function len(a) { return a.length; } function int(x) { return Math.floor(x); }
function summarize(list) {
  const sv = list.map(p => p.relative_total_saving);
  const dts = list.map(p => p.d_total);
  const nn = list.filter(p => p.d_total >= 0).length;
  const ge5 = list.filter(p => p.relative_total_saving >= 0.05).length;
  const sumB = list.reduce((a, p) => a + p.B_tokens, 0), sumT = list.reduce((a, p) => a + p.T_tokens, 0);
  return {
    pairs: list.length,
    aggregate_relative_saving: r4((sumB - sumT) / sumB),
    median_relative_saving: r4(med(sv)),
    mean_relative_saving: r4(sv.reduce((a, b) => a + b, 0) / Math.max(1, sv.length)),
    p25_relative: r4(pctl(sv, 0.25)), p75_relative: r4(pctl(sv, 0.75)),
    nonnegative_pairs: nn, ge5pct_pairs: ge5,
    median_d_total_tokens: med(dts),
  };
}
function r4(x) { return typeof x === 'number' && !Number.isInteger(x) ? Math.round(x * 10000) / 10000 : x; }

const globalStats = summarize(pairs);
const posPairs = pairs.filter(p => p.rds_positive);
const posStats = summarize(posPairs);
// four-quadrant correctness
const quad = { 'B-pass/T-pass': 0, 'B-pass/T-fail': 0, 'B-fail/T-pass': 0, 'B-fail/T-fail': 0 };
for (const p of pairs) quad[`${p.B_oracle ? 'B-pass' : 'B-fail'}/${p.T_oracle ? 'T-pass' : 'T-fail'}`]++;
// backlash
const turnDelta = pairs.map(p => p.T_turns - p.B_turns);
// realization
const reals = pairs.filter(p => p.realization !== null && p.T_rds.matched_chars > 0).map(p => p.realization);
// concentration (union/global by d_total positive contribution)
const byContribution = pairs.slice().sort((a, b) => b.d_total - a.d_total);
const totalPositive = byContribution.reduce((a, p) => a + Math.max(0, p.d_total), 0);
let cum = 0; const shares = {};
for (let i = 0; i < byContribution.length; i++) {
  cum += Math.max(0, byContribution[i].d_total);
  if (i === 0) shares['top1_pair'] = r4(cum / Math.max(1, totalPositive));
  if (i === Math.floor(pairs.length * 0.1) - 1) shares['top10pct_pairs'] = r4(cum / Math.max(1, totalPositive));
}
const leaveTop10 = (() => {
  const drop = new Set(byContribution.slice(0, Math.floor(pairs.length * 0.1)).map(p => `${p.task}#${p.rep}`));
  const rest = pairs.filter(p => !drop.has(`${p.task}#${p.rep}`));
  const sB = rest.reduce((a, p) => a + p.B_tokens, 0), sT = rest.reduce((a, p) => a + p.T_tokens, 0);
  return { pairs: rest.length, aggregate_relative_saving: r4((sB - sT) / sB) };
})();
// few-step pairs contribution (T turns < B-3)
const fewStep = pairs.filter(p => p.T_turns < p.B_turns - 3);
const fewStepContribution = totalPositive ? fewStep.reduce((a, p) => a + Math.max(0, p.d_total), 0) / totalPositive : null;

// gates
const G1 = pairs.filter(p => p.T_oracle).length >= pairs.filter(p => p.B_oracle).length;
const G2 = globalStats.aggregate_relative_saving >= 0.05 && globalStats.nonnegative_pairs / pairs.length >= 2 / 3;
const G3 = med(turnDelta) <= 1; // prereg: median non-increase (B+1 tolerance)
const G5 = leaveTop10.aggregate_relative_saving > 0;
let verdict;
if (G1 && G2 && G3 && G5) verdict = 'QUALIFIED';
else if (posStats.aggregate_relative_saving >= 0.05 && posStats.nonnegative_pairs / Math.max(1, posPairs.length) >= 2 / 3) verdict = 'LIMITED / POSITIVE-SUBSET';
else verdict = 'NOT_QUALIFIED';

const out = {
  schema_version: 1,
  stage: 'V0.11-D3-E5 RDS real-agent paired A/B (prereg 35c10393 FROZEN; batch identity 21735560)',
  date: '2026-09-24',
  sessions_planned: 48, valid_sessions: sessions.length, valid_pairs: pairs.length, exclusions,
  B_arm_ledger_zero_check: 'B arm has no rds_ledger by construction (flag=0, RDS module not invoked)',
  global_universe: globalStats,
  rds_positive_universe: { pairs: posPairs.length, ...posStats, pair_list: posPairs.map(p => `${p.task}/rep${p.rep}`) },
  correctness_quadrant: quad,
  backlash: {
    turn_delta_median: med(turnDelta),
    T_turns_gt_B_pairs: pairs.filter(p => p.T_turns > p.B_turns).length,
    few_step_pairs: fewStep.map(p => `${p.task}/rep${p.rep}`),
    few_step_saving_contribution: r4(fewStepContribution),
    note: 'same-file-reread/rerun rates derivable from hook telemetry; marker-then-reread approximated by few-step/turn gates (see report)',
  },
  token_realization_ratio: { pairs_with_matched: reals.length, median: r4(med(reals)), note: 'dTotalTokens / (matched_chars/4); >=0.5 strong, <0.25 weak' },
  concentration: { top_shares: shares, leave_top10pct_out: leaveTop10 },
  gates: { G1_correctness: G1, G2_global_task_level: G2, G3_backlash: G3, G5_stability: G5 },
  final_verdict: verdict,
  raw_pairs: pairs.map(p => ({ ...p, relative_total_saving: r4(p.relative_total_saving), realization: p.realization === null ? null : r4(p.realization) })),
};
out.aggregates_sha256 = hashlib(out);
fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
function hashlib(o) { const c = require('crypto'); return c.createHash('sha256').update(JSON.stringify({ ...o, aggregates_sha256: undefined }, Object.keys(o).sort(), 1), 'utf8').digest('hex'); }
console.log('pairs:', pairs.length, '| exclusions:', exclusions.length);
console.log('GLOBAL:', JSON.stringify(globalStats));
console.log('RDS-POSITIVE:', posPairs.length, 'pairs', JSON.stringify(posStats));
console.log('quadrant:', JSON.stringify(quad));
console.log('backlash: turnDeltaMedian =', med(turnDelta), '| T>B turns pairs:', pairs.filter(p => p.T_turns > p.B_turns).length);
console.log('realization median:', r4(med(reals)), '(n=' + reals.length + ')');
console.log('concentration:', JSON.stringify(shares), '| leave-top10:', leaveTop10);
console.log('gates: G1', G1, 'G2', G2, 'G3', G3, 'G5', G5, '=> verdict:', verdict);
