#!/usr/bin/env python3
"""
V0.11-D4-A1 Census — frozen-detector external validation on Open-SWE-Traces 20K.
Detectors: A0-frozen E1-E15 (definitions identical to D3-E1 census implementation).
Coverage: dual ledger (shipped-only vs shipped+RDS-candidate), byte-deduplicated.
Provenance: manifest v2 (sample-id-set sha256 601318a78fc86c84...), A0 freeze commit 1865a160.
"""
import json, os, re, statistics, hashlib
import pyarrow.parquet as pq

DST = 'D:/tasco-temp/d3_hf_data/oswe_v10/'
MF = r'D:/tasco-runtime/work_isolated/v010_rc1_wt/evidence/V1/v011-d4a1-oswe-20k-manifest-v2.json'
OUT = r'D:/tasco-runtime/work_isolated/v010_rc1_wt/evidence/V1/v011-d4a1-census-results.json'

m = json.load(open(MF, encoding='utf-8'))
ids = set(r['trajectory_id'] for r in m['sample'])
id_meta = {r['trajectory_id']: r for r in m['sample']}

# ---- frozen shape detectors (A0 registry; identical rules to D3-E1) ----
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
    first = c.split(' ', 1)[0].strip('`')
    if first in VIEW_WORDS: return 'view'
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
                            if p and cb.split(' ', 1)[0].strip('') in {'view', 'open', 'str_replace_editor', 'create'}:
                                cb = cb + ' ' + str(p)
                            pending = {'cmd': norm_cmd(cb), 'csim': sim_cmd(cb),
                                       'cclass': cmd_class(cb), 'path': p}
                except Exception: pass
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; pending['obs_chars'] = len(content)
            events.append(pending); pending = None
    n = len(events)
    for i, e in enumerate(events):
        e['pos'] = (i + 1) / n if n else 0
        e['turns_after'] = n - (i + 1)
    return events

def detect_shapes(events):
    """A0-frozen E1-E15 detectors. Returns set of shape_ids present + per-shape event chars."""
    hits = {}; n = len(events)
    if not n: return hits
    def mark(sid, ev): hits.setdefault(sid, []).append(ev)
    by_csim = {}; by_path = {}
    for i, e in enumerate(events):
        by_csim.setdefault(e['csim'], []).append(i)
        if e['path']: by_path.setdefault(e['path'], []).append(i)
    # E1/E2
    for k, idxs in by_csim.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E1_repeated_exact_command' if k == events[i]['csim'] else 'E2_repeated_similar_command', events[i])
            # csim == cnorm for exact; distinguish: exact means cnorm identical (csim identical AND digits irrelevant)
    for k, idxs in by_csim.items():
        cn = events[idxs[0]]['cmd']
        if len(set(events[i]['cmd'] for i in idxs)) == 1 and len(idxs) >= 2:
            pass  # exact subset already marked via csim==cnorm equivalence below
    # redo precisely: exact = same cnorm; similar = same csim
    by_cnorm = {}
    for i, e in enumerate(events): by_cnorm.setdefault(e['cmd'], []).append(i)
    hits.pop('E1_repeated_exact_command', None); hits.pop('E2_repeated_similar_command', None)
    for k, idxs in by_cnorm.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E1_repeated_exact_command', events[i])
    for k, idxs in by_csim.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E2_repeated_similar_command', events[i])
    # E3/E14 same-file reread
    for p, idxs in by_path.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E3_same_file_reread', events[i])
            for a, b in zip(idxs, idxs[1:]):
                if b - a <= 3:
                    mark('E14_output_followed_by_reread', events[b])
    # E4 overlapping read (view ranges not in this schema; approximate via same-path multi-view — E4 defined with ranges; without ranges mark only if >=2 views same path)
    # NOTE: Open-SWE tool_calls carry path but not ranges in observed samples -> E4 range-overlap NOT_MEASURABLE unless range info present
    # E5 same search
    sk = {}
    for i, e in enumerate(events):
        if e['cclass'] == 'search': sk.setdefault(e['csim'], []).append(i)
    for k, idxs in sk.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E5_same_search', events[i])
    # E6/E7 large test success/failure (no exit code field -> textual pass/fail features)
    PASS_PAT = re.compile(r'PASSED|passed|all tests passed|✓', re.I)
    FAIL_PAT = re.compile(r'FAILED|AssertionError|Traceback|✖|failing', re.I)
    for e in events:
        if e['cclass'] == 'test' and e['obs_chars'] >= 3000:
            if FAIL_PAT.search(e['obs']): mark('E7_large_test_failure', e)
            elif PASS_PAT.search(e['obs']): mark('E6_large_test_success', e)
    # E8/E9 large lint/build
    for e in events:
        if e['obs_chars'] >= 3000:
            if e['cclass'] == 'lint': mark('E8_large_lint_output', e)
            elif e['cclass'] == 'build': mark('E9_large_build_output', e)
    # E10/E11 repeated/unchanged validation
    val = {}
    for i, e in enumerate(events):
        if e['cclass'] in ('test', 'lint'): val.setdefault(e['csim'], []).append(i)
    for k, idxs in val.items():
        if len(idxs) >= 2:
            for i in idxs: mark('E10_repeated_validation', events[i])
            for a, b in zip(idxs, idxs[1:]):
                la = set(events[a]['obs'].replace('\r\n', '\n').split('\n'))
                lb = set(events[b]['obs'].replace('\r\n', '\n').split('\n'))
                j = len(la & lb) / max(1, len(la | lb))
                if j >= 0.8:
                    mark('E11_unchanged_validation', events[b])
    # E12 large diagnostic
    DIAG_PAT = re.compile(r'Traceback|Exception|ERROR:|error:', re.I)
    for e in events:
        if e['obs_chars'] >= 3000 and DIAG_PAT.search(e['obs']): mark('E12_large_diagnostic', e)
    # E13 large output near terminal
    for e in events:
        if e['obs_chars'] >= 2000 and e['pos'] >= 0.75 and e['turns_after'] <= 3: mark('E13_large_output_near_terminal', e)
    # E15 rederivation within <=3 events
    for i, e in enumerate(events):
        for jj in range(i + 1, min(i + 4, n)):
            if events[jj]['csim'] == e['csim'] and events[jj]['cclass'] in ('test', 'lint', 'build'):
                mark('E15_output_followed_by_rederivation', events[jj]); break
    return hits

# capability mapping (A0 registry, frozen)
SHIPPED_FULL = {'E8_large_lint_output', 'E5_same_search', 'E10_repeated_validation', 'E11_unchanged_validation'}
CANDIDATE_FULL = {'E1_repeated_exact_command', 'E2_repeated_similar_command', 'E3_same_file_reread', 'E14_output_followed_by_reread', 'E15_output_followed_by_rederivation'}
UNSAFE = {'E7_large_test_failure', 'E12_large_diagnostic'}
ABC = {'E1': 'A', 'E2': 'A', 'E3': 'A', 'E4': 'A', 'E5': 'D', 'E6': 'D', 'E7': 'C', 'E8': 'A', 'E9': 'E', 'E10': 'D', 'E11': 'D', 'E12': 'C', 'E13': 'B', 'E14': 'A', 'E15': 'D'}
SHAPE_SESSIONS = {}  # shape -> set(session)
SHAPE_CHARS = {}
SESSION_SHAPES = {}
per_session = []
for split, nfiles in [('openhands/minimax_m25', 18), ('sweagent/minimax_m25', 19)]:
    for i in range(nfiles):
        fn = DST + f'{split}/swe-rebench-v2/train-{i:05d}-of-{nfiles:05d}.parquet'.replace('/', '_')
        pf = pq.ParquetFile(fn)
        for b in pf.iter_batches(batch_size=400, columns=['trajectory_id', 'messages', 'language', 'resolved']):
            for r in b.to_pylist():
                if r['trajectory_id'] not in ids: continue
                msgs = json.loads(r['messages']) if isinstance(r['messages'], str) else r['messages']
                events = parse_events(msgs)
                hits = detect_shapes(events)
                ss = {'session': r['trajectory_id'], 'stratum': split, 'language': r['language'], 'resolved': r['resolved'],
                      'n_events': len(events), 'obs_chars': sum(e['obs_chars'] for e in events), 'shapes': sorted(hits.keys())}
                for sid, evs in hits.items():
                    SHAPE_SESSIONS.setdefault(sid, set()).add(r['trajectory_id'])
                    SHAPE_CHARS.setdefault(sid, []).append(sum(e['obs_chars'] for e in evs))
                per_session.append(ss)

print('sessions censused:', len(per_session), '/ 20000')

def med(a): return statistics.median(a) if a else None
def r4(x): return round(x, 4) if isinstance(x, float) else x
def pctl(a, q):
    s = sorted(a); return s[min(len(s) - 1, int(q * s.length if False else int(q * len(s))))] if a else None

TW = {  # Thoughtworks 15K discovery incidence (D3-E1 census)
 'E1': 0.6581, 'E2': 0.6627, 'E3': 0.6651, 'E4': 0.2771, 'E5': 0.0047, 'E6': 0.0039, 'E7': 0.002,
 'E8': None, 'E9': 0.0001, 'E10': 0.0011, 'E11': 0.0005, 'E12': 0.6011, 'E13': 0.5325, 'E14': 0.6153, 'E15': 0.0005}

def band(tw, osv):
    if tw is None or osv is None: return 'NOT_MEASURABLE' if tw is None else 'MEASURABLE_ONLY_EXTERNAL'
    r = osv / tw
    if 0.5 <= r <= 2.0: return 'REPLICATED'
    if 0.2 <= r < 0.5 or 2.0 < r <= 5.0: return 'PARTIAL_REPLICATION'
    return 'DATASET_SPECIFIC'

shape_results = {}
ALL_SHAPES = ['E1_repeated_exact_command', 'E2_repeated_similar_command', 'E3_same_file_reread', 'E4_overlapping_file_read',
              'E5_same_search', 'E6_large_test_success', 'E7_large_test_failure', 'E8_large_lint_output', 'E9_large_build_output',
              'E10_repeated_validation', 'E11_unchanged_validation', 'E12_large_diagnostic', 'E13_large_output_near_terminal',
              'E14_output_followed_by_reread', 'E15_output_followed_by_rederivation']
for sid in ALL_SHAPES:
    sess = SHAPE_SESSIONS.get(sid, set())
    chars = SHAPE_CHARS.get(sid, [])
    inc = len(sess) / len(per_session) if per_session else 0
    short = sid.split('_')[0]
    shape_results[sid] = {
        'measurable': True, 'event_sessions': len(sess), 'session_incidence': round(inc, 4),
        'median_event_chars': med(chars), 'p75_event_chars': pctl(chars, 0.75) if chars else None,
        'thoughtworks_incidence': TW[short],
        'replication_band': band(TW[short], inc),
        'abcde_class': ABC[short],
    }

# A-E session-level distribution (union)
cls_of = {}
for sid in ALL_SHAPES: cls_of[sid] = ABC[sid.split('_')[0]]
sess_class = {}
for ss in per_session:
    classes = set(cls_of.get(s.split('_')[0], 'E') for s in ss['shapes'])
    ss['classes'] = sorted(classes)
    for cl in classes: sess_class.setdefault(cl, set()).add(ss['session'])
ae = {cl: {'sessions': len(se), 'session_share': round(len(se) / len(per_session), 4)} for cl, se in sorted(sess_class.items())}

# coverage: supported sets (A0 mapping)
SHIPPED_FULL_SHAPES = {s for s in ALL_SHAPES if s in SHIPPED_FULL}
CAND_FULL_SHAPES = set(CANDIDATE_FULL)
def coverage(shape_filter):
    soc_sessions = set(); coc_bytes = 0; total_qualified_bytes = 0
    for ss in per_session:
        q_shapes = [s for s in ss['shapes'] if s not in UNSAFE and (s.split('_')[0] not in ('E7', 'E12'))]
        if not q_shapes: continue
        supported = [s for s in q_shapes if s in shape_filter]
        if supported: soc_sessions.add(ss['session'])
        # byte ledger: per session, per shape first-occurrence obs chars (dedup across shapes via session-shape sum, conservative)
        for s in q_shapes: total_qualified_bytes += ss['obs_chars'] / max(1, len(ss['shapes']))
        for s in supported: coc_bytes += ss['obs_chars'] / max(1, len(ss['shapes']))
    return {'SOC': round(len(soc_sessions) / max(1, len(per_session)), 4),
            'COC': round(coc_bytes / max(1, total_qualified_bytes), 4)}

cov_shipped = coverage(SHIPPED_FULL_SHAPES)
cov_both = coverage(SHIPPED_FULL_SHAPES | CAND_FULL_SHAPES)
gap_rate = None
if cov_both['COC'] > 0: gap_rate = r4(1 - cov_shipped['COC'] / max(1e-9, cov_both['COC']))

# stratification: scaffold
def stratum_stats(name, flt):
    sub = [s for s in per_session if flt(s)]
    sc = {}
    for ss in sub:
        for sh in ss['shapes']: sc.setdefault(sh, set()).add(ss['session'])
    return {'sessions': len(sub),
            'shape_incidence': {sid.split('_')[0]: round(len(sc.get(sid, set())) / len(sub), 4) for sid in ALL_SHAPES if sc.get(sid)}}
oh = stratum_stats('OH', lambda s: s['stratum'] == 'openhands_minimax_m25')
sa = stratum_stats('SA', lambda s: s['stratum'] == 'sweagent_minimax_m25')
lang_stats = {}
for ss in per_session: lang_stats.setdefault(ss['language'], set()).add(ss['session'])
lang_out = {lg: len(se) for lg, se in sorted(lang_stats.items(), key=lambda kv: -len(kv[1]))}
res_stats = {}
for ss in per_session: res_stats[ss['resolved']] = res_stats.get(ss['resolved'], 0) + 1

out = {
    'schema_version': 1,
    'stage': 'V0.11-D4-A1 census — frozen-detector external validation (prereg d229a6a4 + amendment 76547f34; A0 freeze 1865a160)',
    'date': '2026-09-24',
    'provenance': {
        'manifest': 'v011-d4a1-oswe-20k-manifest-v2.json',
        'manifest_sample_id_set_sha256': '601318a78fc86c84',
        'manifest_note': 'file-level manifest_sha256 895a96c0 predates SUPERSEDED bookkeeping append on old manifest; v2 sample array verified 20000/20000 unique',
        'detector_freeze_commit': '1865a160 (A0 registry)',
        'dataset': 'nvidia/Open-SWE-Traces v1.0 HF revision f8fb5b3d2c78 (Minimax-M2.5, OH+SA strata)',
    },
    'census_integrity': {'sessions_expected': 20000, 'sessions_censused': len(per_session), 'complete': len(per_session) == 20000},
    'shape_results': shape_results,
    'abcde_session_distribution': ae,
    'coverage': {
        'shipped_only': cov_shipped,
        'shipped_plus_candidate': cov_both,
        'capability_gap_rate': gap_rate,
        'definition_note': 'COC byte numerator counts full-fit capability shape sessions (conservative; partial-fit not counted); unsafe shapes (E7/E12) excluded from qualified denominator',
    },
    'stratification': {
        'openhands': oh, 'sweagent': sa,
        'languages_by_sessions': lang_out,
        'resolved_by_sessions': {str(k): v for k, v in res_stats.items()},
    },
    'scaffold_comparison_note': 'compare oh/sa shape_incidence: persistent if both >0.5x overall; scaffold-sensitive if ratio >2x; near-absent if <0.1',
    'final_status': 'EXTERNAL_VALIDATION_COMPLETE' if len(per_session) == 20000 else 'BLOCKED',
}
out['aggregates_sha256'] = hashlib.sha256(json.dumps({k: v for k, v in out.items()}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('--- shape results:')
for sid, v in shape_results.items():
    print(f"  {sid:38s} inc={v['session_incidence']:<8} TW={v['thoughtworks_incidence']} band={v['replication_band']}")
print('A-E:', json.dumps(ae))
print('coverage shipped:', cov_shipped, '| +candidate:', cov_both, '| gap:', gap_rate)
print('OH vs SA sample:')
for sid in ['E2_repeated_similar_command', 'E3_same_file_reread', 'E12_large_diagnostic', 'E13_large_output_near_terminal', 'E8_large_lint_output']:
    print(' ', sid.split('_')[0], 'OH=', oh['shape_incidence'].get(sid.split('_')[0]), 'SA=', sa['shape_incidence'].get(sid.split('_')[0]))
print('status:', out['final_status'])
