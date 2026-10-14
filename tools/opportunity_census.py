#!/usr/bin/env python3
"""
V0.11-D3-E1 — external dataset opportunity census (mechanical, offline).
Prereg: docs/architecture/V0.11-D3-E1-EXTERNAL-DATASET-CENSUS-PREREG-V1.md (FROZEN 55494bce)
Dataset: thoughtworks/agentic-coding-trajectories sessions.parquet (15,000 sessions, pinned D:/tasco-temp/d3_hf_data).
Zero model calls. Candidate-discovery only.
"""
import json, re, sys, statistics
import pyarrow.parquet as pq

PARQUET = 'D:/tasco-temp/d3_hf_data/sessions.parquet'
OUT = 'evidence/V1/v011-d3e1-external-census.json'

TEST_PAT = re.compile(r'^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|go\s+test|cargo\s+test|make\s+test|tox|python\s+-m\s+unittest)\b', re.I)
LINT_PAT = re.compile(r'^\s*(eslint|ruff|flake8|pylint|mypy|tsc|pyright|pre-commit)\b', re.I)
BUILD_PAT = re.compile(r'^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)', re.I)
SEARCH_PAT = re.compile(r'^\s*(grep|rg|ag|ack|find)\b', re.I)
VIEW_WORDS = {'view', 'open', 'cat', 'head', 'tail', 'less', 'sed', 'str_replace_editor'}
EXIT_PAT = re.compile(r'\[The command completed with exit code (\d+)[^\]]*\]')
FAIL_PAT = re.compile(r'FAILED|ERROR|Traceback|AssertionError|✖|failing', re.I)
PASS_PAT = re.compile(r'PASSED|passed|all tests passed|✓|ok\.?\s*$|\d+ passed', re.I)
DIAG_PAT = re.compile(r'Traceback|Exception|ERROR:|error:', re.I)
NUMTOK = re.compile(r'\d+')

def norm_cmd(c):
    c = ' '.join(c.split()).strip()
    return c

def sim_cmd(c):
    return ' '.join(NUMTOK.sub('#', norm_cmd(c)).split())

def cmd_class(c):
    if TEST_PAT.match(c): return 'test'
    if LINT_PAT.match(c): return 'lint'
    if BUILD_PAT.match(c): return 'build'
    if SEARCH_PAT.match(c): return 'search'
    first = c.split(' ', 1)[0].strip('`')
    if first in VIEW_WORDS: return 'view'
    return 'other'

def parse_events(msgs, framework):
    """Return list of events: {cmd, cnorm, csim, cclass, path, vrange, obs_chars, obs_lines, obs, exit, turn_index}"""
    events = []
    pending = None  # assistant command awaiting observation
    for idx, m in enumerate(msgs):
        role = m.get('role')
        content = m.get('content') or ''
        if role == 'assistant':
            tc = m.get('tool_calls_json')
            cmd = None; path = None; vrange = None
            if tc:
                try:
                    calls = json.loads(tc)
                    if isinstance(calls, dict): calls = [calls]
                    for call in calls:
                        fn = (call.get('function') or {})
                        name = fn.get('name') or ''
                        try: args = json.loads(fn.get('arguments') or '{}')
                        except Exception: args = {}
                        a = args.get('command')
                        if isinstance(a, str) and a.strip():
                            cmd = norm_cmd(a.splitlines()[0] if name.lower().find('edit') == -1 else a.splitlines()[0])
                        elif name.lower().find('view') != -1 or (isinstance(args.get('command'), str) and args.get('command') in ('view', 'open')):
                            cmd = norm_cmd(str(args.get('command', name)))
                        if args.get('path'): path = args['path']
                        if args.get('view_range'): vrange = args['view_range']
                except Exception:
                    pass
            if cmd is None:
                mm = re.search(r'```[a-z]*\s*\n(.+?)\n```', content, re.S)
                if mm:
                    first = mm.group(1).strip().splitlines()[0]
                    cmd = norm_cmd(first)
                    if first.strip().startswith(('view ', 'open ')):
                        parts = first.split()
                        if len(parts) > 1: path = parts[1]
                        m2 = re.search(r'\[(\d+),\s*(\d+)\]', first)
                        if m2: vrange = [int(m2.group(1)), int(m2.group(2))]
                    else:
                        pm = re.search(r'(/[^\s`]+)', first)
                        if pm and cmd_class(first) == 'view': path = pm.group(1)
            if cmd:
                pending = {'cmd': cmd, 'cnorm': norm_cmd(cmd), 'csim': sim_cmd(cmd), 'cclass': cmd_class(cmd), 'path': path, 'vrange': vrange, 'turn_index': idx}
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; pending['obs_chars'] = len(content)
            pending['obs_lines'] = len(content.splitlines())
            em = EXIT_PAT.search(content)
            pending['exit'] = int(em.group(1)) if em else None
            events.append(pending); pending = None
        elif role == 'user' and pending is not None:
            c = content if content.startswith('OBSERVATION:') else (content[content.find('OBSERVATION:'):] if 'OBSERVATION:' in content[:200] else None)
            if c is not None:
                body = c[len('OBSERVATION:'):].strip()
                pending['obs'] = body; pending['obs_chars'] = len(body)
                pending['obs_lines'] = len(body.splitlines())
                pending['exit'] = None
                events.append(pending); pending = None
    return events

def line_set(obs):
    return frozenset(obs.splitlines())

def jaccard(a, b):
    if not a and not b: return 0.0
    return len(a & b) / max(1, len(a | b))

def pctl(a, q):
    if not a: return None
    s = sorted(a); i = min(len(s) - 1, int(q * len(s)))
    return s[i]

def med(a):
    return statistics.median(a) if a else None

SHAPES = {}
SESSIONS_TOTAL = 0
CTX_TOTAL = 0
session_records = []

pf = pq.ParquetFile(PARQUET)
for batch in pf.iter_batches(batch_size=250):
    for row in batch.to_pylist():
        SESSIONS_TOTAL += 1
        try: msgs = json.loads(row['messages_json'])
        except Exception: continue
        events = parse_events(msgs, row.get('agent_framework'))
        obs_total = sum(e['obs_chars'] for e in events)
        CTX_TOTAL += obs_total
        resolved = None
        try:
            gt = json.loads(row.get('ground_truth_meta_json') or '{}')
            resolved = gt.get('resolved')
        except Exception: pass
        skey = row['session_id']
        sess_shaped = set()
        # per-shape event collection
        def mark(shape, ev, extra=None):
            sess_shaped.add(shape)
            SHAPES.setdefault(shape, []).append({'session': skey, 'source': row['source_dataset'], 'resolved': resolved, 'ctx_chars': obs_total, **ev, **(extra or {})})
        by_cnorm = {}; by_csim = {}; by_path = {}
        for i, e in enumerate(events):
            by_cnorm.setdefault(e['cnorm'], []).append(i)
            by_csim.setdefault(e['csim'], []).append(i)
            if e['path']: by_path.setdefault(e['path'], []).append(i)
        n = len(events)
        for i, e in enumerate(events):
            e['pos'] = (i + 1) / n if n else 0
            e['turns_after'] = n - (i + 1)
        # E1/E2
        for grp, shape in ((by_cnorm, 'E1_repeated_exact_command'), (by_csim, 'E2_repeated_similar_command')):
            for k, idxs in grp.items():
                if len(idxs) >= 2:
                    for i in idxs: mark(shape, events[i], {'repeat_count': len(idxs)})
        # E3/E4 same file reread / overlapping read
        for p, idxs in by_path.items():
            if len(idxs) < 2: continue
            for i in idxs: mark('E3_same_file_reread', events[i], {'repeat_count': len(idxs)})
            vr = [events[i]['vrange'] for i in idxs if events[i]['vrange']]
            if len(vr) >= 2:
                for a in range(len(vr)):
                    for b in range(a + 1, len(vr)):
                        s1, e1 = vr[a][0], vr[a][1] if len(vr[a]) > 1 else vr[a][0]
                        s2, e2 = vr[b][0], vr[b][1] if len(vr[b]) > 1 else vr[b][0]
                        if s1 <= e2 and s2 <= e1:
                            for i in (idxs[a], idxs[b]): mark('E4_overlapping_file_read', events[i], {'overlap': [max(s1, s2), min(e1, e2)]})
                            break
        # E5 same search
        search_keys = {}
        for i, e in enumerate(events):
            if e['cclass'] == 'search': search_keys.setdefault(e['cnorm'], []).append(i)
        for k, idxs in search_keys.items():
            if len(idxs) >= 2:
                for i in idxs: mark('E5_same_search', events[i], {'repeat_count': len(idxs)})
        # E6-E9 large outputs by class + exit/feature
        for e in events:
            if e['obs_chars'] < 3000: continue
            is_pass = (e['exit'] == 0) or (e['exit'] is None and bool(PASS_PAT.search(e['obs'])) and not FAIL_PAT.search(e['obs']))
            is_fail = (e['exit'] is not None and e['exit'] != 0) or (e['exit'] is None and bool(FAIL_PAT.search(e['obs'])))
            if e['cclass'] == 'test':
                if is_pass: mark('E6_large_test_success', e)
                elif is_fail: mark('E7_large_test_failure', e)
            elif e['cclass'] == 'lint': mark('E8_large_lint_output', e)
            elif e['cclass'] == 'build': mark('E9_large_build_output', e)
            if DIAG_PAT.search(e['obs']): mark('E12_large_diagnostic', e)
        # E10/E11 repeated validation + unchanged (adjacent same-cnorm test/lint pairs, Jaccard)
        for k, idxs in by_cnorm.items():
            cls = events[idxs[0]]['cclass']
            if cls not in ('test', 'lint') or len(idxs) < 2: continue
            for i in idxs: mark('E10_repeated_validation', events[i], {'repeat_count': len(idxs)})
            for a, b in zip(idxs, idxs[1:]):
                j = jaccard(line_set(events[a]['obs']), line_set(events[b]['obs']))
                if j >= 0.8:
                    overlap_chars = sum(len(l) + 1 for l in (line_set(events[a]['obs']) & line_set(events[b]['obs'])))
                    for i in (a, b): mark('E11_unchanged_validation', events[i], {'jaccard': round(j, 3), 'overlap_chars': overlap_chars})
        # E13 large output near terminal
        for e in events:
            if e['obs_chars'] >= 2000 and e['pos'] >= 0.75 and e['turns_after'] <= 3:
                mark('E13_large_output_near_terminal', e)
        # E14/E15 reread/rederivation within <=3 assistant turns after
        for i, e in enumerate(events):
            for j in range(i + 1, min(i + 4, n)):
                if e['path'] and events[j]['path'] == e['path'] and events[j]['cclass'] == 'view':
                    mark('E14_output_followed_by_reread', events[j], {'gap': j - i}); break
            for j in range(i + 1, min(i + 4, n)):
                if events[j]['csim'] == e['csim'] and events[j]['cclass'] in ('test', 'lint', 'build'):
                    mark('E15_output_followed_by_rederivation', events[j], {'gap': j - i}); break
        session_records.append({'session': skey, 'source': row['source_dataset'], 'framework': row.get('agent_framework'), 'model': row.get('recorded_model'), 'resolved': resolved, 'n_events': n, 'obs_total_chars': obs_total, 'total_tokens_field': row.get('total_tokens'), 'shapes': sorted(sess_shaped)})

# aggregate per shape
def agg(shape):
    evs = SHAPES.get(shape, [])
    if not evs: return None
    sess_set = set(e['session'] for e in evs)
    chars = [e['obs_chars'] for e in evs]
    pot = [e.get('overlap_chars', 0) for e in evs]
    resolved_map = {}
    for e in evs:
        resolved_map.setdefault(e['session'], e['resolved'])
    succ = [1 if v else 0 for v in resolved_map.values() if v is not None]
    return {
        'sessions': len(sess_set),
        'session_incidence': round(len(sess_set) / SESSIONS_TOTAL, 4),
        'events': len(evs),
        'median_chars': med(chars), 'p75_chars': pctl(chars, 0.75),
        'median_tokens_est': round(med(chars) / 4, 1) if med(chars) else None,
        'median_turn_index': round(med([e['pos'] for e in evs]), 3),
        'median_turns_after': med([e['turns_after'] for e in evs]),
        'trajectory_exposure': (lambda t: None if t is None else ('LOW' if t <= 1 else 'MEDIUM' if t <= 5 else 'HIGH'))(med([e['turns_after'] for e in evs])),
        'repeat_rate': round(med([e.get('repeat_count', 1) for e in evs]), 2),
        'later_reread_rate': None,
        'success_session_rate': round(sum(succ) / len(succ), 3) if succ else None,
        'potential_compressible_chars_median': med(pot) if any(pot) else None,
        'by_source': {src: len([e for e in evs if e['source'] == src]) for src in set(e['source'] for e in evs)},
    }

result_shapes = {s: agg(s) for s in sorted(SHAPES)}
POOL_GATES = {'min_incidence': 0.20, 'min_median_chars': 1000}
pool = sorted([s for s, v in result_shapes.items() if v and v['session_incidence'] >= POOL_GATES['min_incidence'] and (v['median_chars'] or 0) >= POOL_GATES['min_median_chars']],
              key=lambda s: (-result_shapes[s]['session_incidence'], -result_shapes[s]['median_chars']))

out = {
    'schema_version': 1,
    'stage': 'V0.11-D3-E1 external dataset opportunity census (prereg 55494bce FROZEN before aggregation)',
    'date': '2026-09-23',
    'dataset': {'name': 'thoughtworks/agentic-coding-trajectories', 'sessions': SESSIONS_TOTAL, 'pin': 'D:/tasco-temp/d3_hf_data/sessions.parquet', 'bytes': 325563194},
    'context_proxy': {'whole_session_context_chars_sum': CTX_TOTAL, 'mean_obs_chars_per_session': round(CTX_TOTAL / max(1, SESSIONS_TOTAL), 1)},
    'shapes': result_shapes,
    'pool_gates': POOL_GATES,
    'candidate_pool': pool,
    'top3': [{'shape': s, **{k: result_shapes[s][k] for k in ('session_incidence', 'events', 'median_chars', 'p75_chars', 'median_turns_after', 'trajectory_exposure', 'repeat_rate', 'success_session_rate', 'potential_compressible_chars_median', 'by_source')}} for s in pool[:3]],
    'special_directions': {k: result_shapes.get(k) for k in ('E10_repeated_validation', 'E11_unchanged_validation', 'E3_same_file_reread', 'E4_overlapping_file_read', 'E13_large_output_near_terminal')},
    'verdict': 'PASS — NATURAL_OPPORTUNITY_FOUND' if pool else 'NO_NATURAL_OPPORTUNITY / STOP',
}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)

print('sessions:', SESSIONS_TOTAL, '| ctx proxy chars/session:', out['context_proxy']['mean_obs_chars_per_session'])
print('--- shapes:')
for s, v in result_shapes.items():
    if v: print(f"{s:38s} inc={v['session_incidence']:<7} med={v['median_chars']:<8} p75={v['p75_chars']:<8} expo={str(v['trajectory_exposure']):<7} repeat={v['repeat_rate']} succ={v['success_session_rate']} pool={s in pool}")
print('candidate pool:', pool)
print('verdict:', out['verdict'])
