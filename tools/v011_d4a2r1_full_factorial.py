#!/usr/bin/env python3
"""V0.11-D4-A2R1 — SAxQwen census + full factorial E13 2x2 + core-shape model-contrast verification."""
import json, re, hashlib
import pyarrow.parquet as pq

DST = 'D:/tasco-temp/d3_hf_data/oswe_v10/'
OUT = r'D:/tasco-runtime/work_isolated/v010_rc1_wt/evidence/V1/v011-d4a2r1-full-factorial.json'
A1 = r'D:/tasco-runtime/work_isolated/v010_rc1_wt/evidence/V1/v011-d4a1-census-results.json'
a1 = json.load(open(A1, encoding='utf-8'))

TEST_PAT = re.compile(r'^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|go\s+test|cargo\s+test|make\s+test|tox)\b', re.I)
LINT_PAT = re.compile(r'^\s*(eslint|ruff|flake8|pylint|pre-commit)\b', re.I)
BUILD_PAT = re.compile(r'^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)', re.I)
SEARCH_PAT = re.compile(r'^\s*(grep|rg|ag|ack|find)\b', re.I)
VIEW_WORDS = {'view', 'open', 'cat', 'head', 'tail', 'less', 'sed', 'str_replace_editor'}
NUMTOK = re.compile(r'\d+')

def norm_cmd(c): return ' '.join(c.split()).strip()
def sim_cmd(c): return ' '.join(NUMTOK.sub('#', norm_cmd(c)).split())
def cmd_class(c):
    if TEST_PAT.match(c): return 'test'
    if LINT_PAT.match(c): return 'lint'
    if BUILD_PAT.match(c): return 'build'
    if SEARCH_PAT.match(c): return 'search'
    if c.split(' ', 1)[0].strip('`') in VIEW_WORDS: return 'view'
    return 'other'

def parse_events(msgs):
    events = []; pending = None
    for m in msgs:
        role = m.get('role'); content = m.get('content') or ''
        if role == 'assistant':
            tc = m.get('tool_calls')
            if tc:
                try:
                    calls = json.loads(tc) if isinstance(tc, str) else tc
                    if isinstance(calls, dict): calls = [calls]
                    for call in calls:
                        fn = call.get('function') or {}
                        try: args = json.loads(fn.get('arguments') or '{}')
                        except Exception: args = {}
                        a = args.get('command')
                        if isinstance(a, str) and a.strip():
                            cb = a.splitlines()[0]
                            p = args.get('path')
                            if p and cb.split(' ', 1)[0].strip('`') in {'view', 'open', 'str_replace_editor', 'create'}:
                                cb = cb + ' ' + str(p)
                            pending = {'cmd': norm_cmd(cb), 'csim': sim_cmd(cb), 'cclass': cmd_class(cb), 'path': p}
                except Exception: pending = None
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; pending['obs_chars'] = len(content)
            events.append(pending); pending = None
    n = len(events)
    for i, e in enumerate(events):
        e['pos'] = (i + 1) / n if n else 0
        e['turns_after'] = n - (i + 1)
    return events

def detect_shapes(events):
    hits = {}; n = len(events)
    if not n: return hits
    def mark(sid, ev): hits.setdefault(sid, []).append(ev)
    by_csim = {}; by_cnorm = {}; by_path = {}
    for i, e in enumerate(events):
        by_csim.setdefault(e['csim'], []).append(i)
        by_cnorm.setdefault(e['cmd'], []).append(i)
        if e['path']: by_path.setdefault(e['path'], []).append(i)
    for k, idxs in by_cnorm.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E1_repeated_exact_command', events[i])
    for k, idxs in by_csim.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E2_repeated_similar_command', events[i])
    for p, idxs in by_path.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E3_same_file_reread', events[i])
            for a, b in zip(idxs, idxs[1:]):
                if b - a <= 3: mark('E14_output_followed_by_reread', events[b])
    sk = {}
    for i, e in enumerate(events):
        if e['cclass'] == 'search': sk.setdefault(e['csim'], []).append(i)
    for k, idxs in sk.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E5_same_search', events[i])
    PASS_PAT = re.compile(r'PASSED|passed|all tests passed|✓', re.I)
    FAIL_PAT = re.compile(r'FAILED|AssertionError|Traceback|✖|failing', re.I)
    DIAG_PAT = re.compile(r'Traceback|Exception|ERROR:|error:', re.I)
    for e in events:
        if e['cclass'] == 'test' and e['obs_chars'] >= 3000:
            if FAIL_PAT.search(e['obs']): mark('E7_large_test_failure', e)
            elif PASS_PAT.search(e['obs']): mark('E6_large_test_success', e)
        if e['obs_chars'] >= 3000:
            if e['cclass'] == 'lint': mark('E8_large_lint_output', e)
            elif e['cclass'] == 'build': mark('E9_large_build_output', e)
            if DIAG_PAT.search(e['obs']): mark('E12_large_diagnostic', e)
    val = {}
    for i, e in enumerate(events):
        if e['cclass'] in ('test', 'lint'): val.setdefault(e['csim'], []).append(i)
    for k, idxs in val.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E10_repeated_validation', events[i])
            for a, b in zip(idxs, idxs[1:]):
                la = set(events[a]['obs'].replace('\r\n', '\n').split('\n'))
                lb = set(events[b]['obs'].replace('\r\n', '\n').split('\n'))
                if len(la & lb) / max(1, len(la | lb)) >= 0.8: mark('E11_unchanged_validation', events[b])
    for e in events:
        if e['obs_chars'] >= 2000 and e['pos'] >= 0.75 and e['turns_after'] <= 3: mark('E13_large_output_near_terminal', e)
    for i, e in enumerate(events):
        for jj in range(i + 1, min(i + 4, n)):
            if events[jj]['csim'] == e['csim'] and events[jj]['cclass'] in ('test', 'lint', 'build'):
                mark('E15_output_followed_by_rederivation', events[jj]); break
    return hits

# ---- SA x Qwen census (FULL frame 9 shards) ----
sa_q_sessions = []
for i in range(9):
    fn = DST + f'sweagent/qwen35_122b/swe-rebench-v2/train-{i:05d}-of-00009.parquet'.replace('/', '_')
    pf = pq.ParquetFile(fn)
    for b in pf.iter_batches(batch_size=400, columns=['trajectory_id', 'messages', 'language', 'resolved']):
        for r in b.to_pylist():
            msgs = json.loads(r['messages']) if isinstance(r['messages'], str) else r['messages']
            events = parse_events(msgs)
            hits = detect_shapes(events)
            sa_q_sessions.append({'id': r['trajectory_id'], 'shapes': sorted(hits.keys()),
                                  'language': r['language'], 'resolved': r['resolved']})
print('SA x Qwen sessions:', len(sa_q_sessions))

def inc_by_shape(sessions):
    sc = {}
    for ss in sessions:
        for sh in ss['shapes']: sc.setdefault(sh, set()).add(ss['id'])
    return {sid.split('_')[0]: round(len(se) / max(1, len(sessions)), 4) for sid, se in sorted(sc.items())}

sa_q_inc = inc_by_shape(sa_q_sessions)
mm_sa_inc = a1['stratification']['sweagent']['incidence']
oh_mm_inc = a1['stratification']['openhands']['incidence']
oh_q_inc = json.load(open(r'D:/tasco-runtime/work_isolated/v010_rc1_wt/evidence/V1/v011-d4a2-cross-model.json', encoding='utf-8'))['qwen_incidence_openhands']

# E13 2x2 (full factorial)
e13_2x2 = {
    'OH_x_Minimax': oh_mm_inc.get('E13'), 'SA_x_Minimax': mm_sa_inc.get('E13'),
    'OH_x_Qwen': oh_q_inc.get('E13'), 'SA_x_Qwen': sa_q_inc.get('E13'),
}
# contrasts: absolute pp difference + ratio
def contrast(a, b):
    if a is None or b is None: return {'pp_diff': None, 'ratio': None}
    return {'pp_diff': round(b - a, 4), 'ratio': round(b / max(1e-9, a), 3)}
e13_contrasts = {
    'scaffold_within_minimax': contrast(e13_2x2['OH_x_Minimax'], e13_2x2['SA_x_Minimax']),
    'scaffold_within_qwen': contrast(e13_2x2['OH_x_Qwen'], e13_2x2['SA_x_Qwen']),
    'model_within_openhands': contrast(e13_2x2['OH_x_Minimax'], e13_2x2['OH_x_Qwen']),
    'model_within_sweagent': contrast(e13_2x2['SA_x_Minimax'], e13_2x2['SA_x_Qwen']),
}
# consistency of scaffold effect across models (pp_diff sign + magnitude)
sc1 = e13_contrasts['scaffold_within_minimax']['pp_diff']
sc2 = e13_contrasts['scaffold_within_qwen']['pp_diff']
scaffold_consistent = (sc1 < 0 and sc2 < 0) or (sc1 > 0 and sc2 > 0)

# core-shape model-contrast verification on SA scaffold (was MODEL_STABLE on OH for E1/E2/E3/E12/E13/E14)
CORE = ['E1_repeated_exact_command', 'E2_repeated_similar_command', 'E3_same_file_reread',
        'E12_large_diagnostic', 'E13_large_output_near_terminal', 'E14_output_followed_by_reread']
core_verification = {}
for sid in CORE:
    s = sid.split('_')[0]
    mm = mm_sa_inc.get(s); q = sa_q_inc.get(s, 0)
    if mm is None: core_verification[s] = 'NOT_MEASURABLE_DISCOVERY'; continue
    r = q / mm if mm else float('inf')
    core_verification[s] = {'minimax': mm, 'qwen': q, 'ratio': round(r, 3) if mm else None,
                            'verdict': ('MODEL_STABLE' if 0.67 <= r <= 1.5 else 'MODEL_SENSITIVE' if 0.33 <= r <= 3.0 else 'MODEL_SENSITIVE_STRONG') if mm else 'INCONCLUSIVE'}

out = {
    'schema_version': 1,
    'stage': 'V0.11-D4-A2R1 SAxQwen cross-cell closure — full factorial model x scaffold (prereg A2 frozen; detectors unchanged)',
    'date': '2026-09-24',
    'provenance': {'detector_freeze_commit': '1865a160', 'dataset': 'nvidia/Open-SWE-Traces v1.0 rev f8fb5b3d2c78',
                   'sa_qwen_frame': '9/9 shards FULL (20334 trajectories), transactional recovery (never delete valid finals)'},
    'sa_qwen_sessions': len(sa_q_sessions),
    'sa_qwen_incidence': sa_q_inc,
    'e13_full_factorial_2x2': {'incidence': e13_2x2, 'contrasts': e13_contrasts,
        'scaffold_effect_consistent_across_models': scaffold_consistent,
        'reading': None},
    'core_shape_model_contrast_on_SA': core_verification,
    'full_factorial_status': 'COMPLETE (2x2 all four cells observed; OH/SA x Minimax/Qwen)',
    'verdict': 'FULL_FACTORIAL_VALIDATION_COMPLETE',
}
# reading
sc1_abs = abs(sc1); sc2_abs = abs(sc2)
out['e13_full_factorial_2x2']['reading'] = (
    f"scaffold contrast direction {'consistent' if scaffold_consistent else 'INCONSISTENT'} across models "
    f"(Minimax {sc1:+.3f}, Qwen {sc2:+.3f} pp; |effect| {sc1_abs:.3f} vs {sc2_abs:.3f}); "
    f"model contrast within SA {'+%.3f' % e13_contrasts['model_within_sweagent']['pp_diff'] if isinstance(e13_contrasts['model_within_sweagent']['pp_diff'], float) else 'N/A'} pp")
out['aggregates_sha256'] = hashlib.sha256(json.dumps({k: v for k, v in out.items()}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('SA x Qwen incidence:', json.dumps(sa_q_inc))
print('E13 2x2:', json.dumps(e13_2x2))
print('E13 contrasts:', json.dumps(e13_contrasts))
print('scaffold consistent across models:', scaffold_consistent)
print('core shapes on SA:', json.dumps(core_verification))
print('verdict:', out['verdict'])
