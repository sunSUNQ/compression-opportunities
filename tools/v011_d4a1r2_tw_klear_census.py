#!/usr/bin/env python3
"""
V0.11-D4-A1R2 — klear parser recovery & discovery census amendment.
Prereg: evidence/V1/v011-d4a1r2-klear-amendment-prereg.json (FROZEN before recompute).
Adapter (schema-adapter only, verbatim semantics from v011_d3e4_rds_prototype.py):
  user message without OBSERVATION prefix but with <returncode>N</returncode> + <output>..</output>
  -> obs = output inner text, exit = N.
E1-E15 predicates/thresholds/groupings: IDENTICAL to evidence/tools/opportunity_census.py (A0).
Regression gate: non-klear 10,000 sessions must reproduce v011-d3e1 exactly.
"""
import hashlib, json, os, re, statistics, sys
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREREG = os.path.join(ROOT, 'evidence/V1/v011-d4a1r2-klear-amendment-prereg.json')
D3E1 = os.path.join(ROOT, 'evidence/V1/v011-d3e1-external-census.json')
D4A1 = os.path.join(ROOT, 'evidence/V1/v011-d4a1-census-results.json')
OUT = os.path.join(ROOT, 'evidence/V1/v011-d4a1r2-tw-klear-census.json')
PARQUET = 'D:/tasco-temp/d3_hf_data/sessions.parquet'
KLEAR = 'kwai-klear-swe-smith-mini'

SHAPES = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15']
FULLNAME = {'E1': 'E1_repeated_exact_command', 'E2': 'E2_repeated_similar_command', 'E3': 'E3_same_file_reread',
            'E4': 'E4_overlapping_file_read', 'E5': 'E5_same_search', 'E6': 'E6_large_test_success',
            'E7': 'E7_large_test_failure', 'E8': 'E8_large_lint_output', 'E9': 'E9_large_build_output',
            'E10': 'E10_repeated_validation', 'E11': 'E11_unchanged_validation', 'E12': 'E12_large_diagnostic',
            'E13': 'E13_large_output_near_terminal', 'E14': 'E14_output_followed_by_reread',
            'E15': 'E15_output_followed_by_rederivation'}
CLASSES = {'E1': 'A', 'E2': 'A', 'E3': 'A', 'E4': 'A', 'E5': 'D', 'E6': 'D', 'E7': 'C', 'E8': 'A',
           'E9': 'E', 'E10': 'D', 'E11': 'D', 'E12': 'C', 'E13': 'B', 'E14': 'A', 'E15': 'D'}
UNSAFE = {'E7', 'E12'}
IDX = {s: i for i, s in enumerate(SHAPES)}
NUMTOK = re.compile(r'\d+')

TEST_PAT = re.compile(r'^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|go\s+test|cargo\s+test|make\s+test|tox|python\s+-m\s+unittest)\b', re.I)
LINT_PAT = re.compile(r'^\s*(eslint|ruff|flake8|pylint|mypy|tsc|pyright|pre-commit)\b', re.I)
BUILD_PAT = re.compile(r'^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)', re.I)
SEARCH_PAT = re.compile(r'^\s*(grep|rg|ag|ack|find)\b', re.I)
VIEW_WORDS = {'view', 'open', 'cat', 'head', 'tail', 'less', 'sed', 'str_replace_editor'}
EXIT_PAT = re.compile(r'\[The command completed with exit code (\d+)[^\]]*\]')
FAIL_PAT = re.compile(r'FAILED|ERROR|Traceback|AssertionError|✖|failing', re.I)
PASS_PAT = re.compile(r'PASSED|passed|all tests passed|✓|ok\.?\s*$|\d+ passed', re.I)
DIAG_PAT = re.compile(r'Traceback|Exception|ERROR:|error:', re.I)
RC_PAT = re.compile(r'<returncode>(\d+)</returncode>')
OUT_PAT = re.compile(r'<output>\n?(.*?)\n?</output>\s*$', re.S)

def norm_cmd(c): return ' '.join(c.split()).strip()
def sim_cmd(c): return ' '.join(NUMTOK.sub('#', norm_cmd(c)).split())

def cmd_class(c):
    if TEST_PAT.match(c): return 'test'
    if LINT_PAT.match(c): return 'lint'
    if BUILD_PAT.match(c): return 'build'
    if SEARCH_PAT.match(c): return 'search'
    first = c.split(' ', 1)[0].strip('`')
    return 'view' if first in VIEW_WORDS else 'other'

def parse_events(msgs):
    """opportunity_census.py parse + D3-E4 klear observation adapter (schema-adapter only)."""
    events = []; pending = None
    for idx, m in enumerate(msgs):
        role = m.get('role'); content = m.get('content') or ''
        if role == 'assistant':
            tc = m.get('tool_calls_json'); cmd = None; path = None; vrange = None
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
                            cmd = norm_cmd(a.splitlines()[0])
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
                pending = {'cmd': cmd, 'cnorm': norm_cmd(cmd), 'csim': sim_cmd(cmd), 'cclass': cmd_class(cmd),
                           'path': path, 'vrange': vrange, 'turn_index': idx}
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; pending['obs_chars'] = len(content)
            em = EXIT_PAT.search(content)
            pending['exit'] = int(em.group(1)) if em else None
            events.append(pending); pending = None
        elif role == 'user' and pending is not None:
            c = content if content.startswith('OBSERVATION:') else (content[content.find('OBSERVATION:'):] if 'OBSERVATION:' in content[:200] else None)
            if c is not None:
                body = c[len('OBSERVATION:'):].strip()
                pending['obs'] = body; pending['obs_chars'] = len(body); pending['exit'] = None
                events.append(pending); pending = None
            else:
                rm = RC_PAT.search(content)          # <- D3-E4 klear adapter (verbatim semantics)
                om = OUT_PAT.search(content)
                if rm and om:
                    pending['obs'] = om.group(1)
                    pending['obs_chars'] = len(om.group(1))
                    pending['exit'] = int(rm.group(1))
                    events.append(pending); pending = None
    return events

def jaccard_lines(a, b):
    if not a and not b: return 0.0
    return len(a & b) / max(1, len(a | b))

def main():
    prereg_sha = hashlib.sha256(open(PREREG, 'rb').read()).hexdigest()
    input_sha = hashlib.sha256(open(PARQUET, 'rb').read()).hexdigest()
    script_sha = hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()
    d3e1 = json.load(open(D3E1, encoding='utf-8'))
    d4a1 = json.load(open(D4A1, encoding='utf-8'))
    official = {s: d3e1['shapes'][FULLNAME[s]]['sessions'] for s in SHAPES if FULLNAME[s] in d3e1['shapes']}
    osw_counts = {s: d4a1['shape_results'][FULLNAME[s]]['event_sessions'] for s in SHAPES}

    shape_sess = {s: set() for s in SHAPES}
    src_shape_sess = {}
    shape_events = {s: 0 for s in SHAPES}
    shape_chars = {s: 0.0 for s in SHAPES}
    ev_pair = {}
    resid = {k: {'events': 0, 'chars': 0} for k in ['detected', 'small-no-repeat', 'large-uncovered-other',
             'below-large-threshold', 'large-classed-ambiguous-features', 'detected-unsafe-only', 'orphan-observation']}
    klear_stats = {'sessions': 0, 'sessions_with_events': 0, 'events': 0, 'empty_obs_events': 0,
                   'exit_extracted': 0, 'zero_event_sessions': 0,
                   'zero_event_with_fence_commands': 0, 'zero_event_without_commands': 0}
    klear_samples = []
    sessions = 0; total_events = 0
    tot_obs = 0.0; labeled_chars = 0.0; qualified_chars = 0.0
    class_chars = {c: 0.0 for c in 'ABCDE'}
    src_obs = {}; src_events = {}
    nonklear_shape_sess = {s: set() for s in SHAPES}
    nonklear_obs = 0.0

    pf = pq.ParquetFile(PARQUET)
    for batch in pf.iter_batches(batch_size=250):
        for row in batch.to_pylist():
            sessions += 1
            src = row.get('source_dataset')
            try: msgs = json.loads(row['messages_json'])
            except Exception: continue
            events = parse_events(msgs)
            n = len(events)
            for i, e in enumerate(events):
                e['pos'] = (i + 1) / n if n else 0; e['turns_after'] = n - (i + 1)
            total_events += n
            obs_total = sum(e['obs_chars'] for e in events)
            tot_obs += obs_total
            src_obs[src] = src_obs.get(src, 0) + obs_total
            src_events[src] = src_events.get(src, 0) + n
            skey = row['session_id']
            is_klear = (src == KLEAR)
            if is_klear:
                klear_stats['sessions'] += 1
                klear_stats['events'] += n
                if n:
                    klear_stats['sessions_with_events'] += 1
                    klear_stats['exit_extracted'] += sum(1 for e in events if e.get('exit') is not None)
                else:
                    klear_stats['zero_event_sessions'] += 1
                    has_fence = any('```' in (m.get('content') or '') for m in msgs if m.get('role') == 'assistant')
                    if has_fence: klear_stats['zero_event_with_fence_commands'] += 1
                    else: klear_stats['zero_event_without_commands'] += 1
                if len(klear_samples) < 5 and n >= 2:
                    e0 = events[0]
                    klear_samples.append({'session': skey, 'cmd': e0['cmd'][:120], 'cclass': e0['cclass'],
                                          'path': e0.get('path'), 'exit': e0.get('exit'),
                                          'obs_chars': e0['obs_chars'],
                                          'obs_head': (e0.get('obs') or '')[:200]})
            if not is_klear:
                nonklear_obs += obs_total
            # orphan accounting (mirrors parse_events pending semantics: commands come
            # from tool_calls_json OR fenced code blocks; pending survives unmatched user msgs)
            pend = False
            for m in msgs:
                role = m.get('role'); content = m.get('content') or ''
                if role == 'assistant':
                    if m.get('tool_calls_json') or re.search(r'```[a-z]*\s*\n(.+?)\n```', content, re.S):
                        pend = True
                elif role == 'tool':
                    if not pend:
                        resid['orphan-observation']['events'] += 1
                        resid['orphan-observation']['chars'] += len(content)
                    else:
                        pend = False
                elif role == 'user':
                    if not pend:
                        resid['orphan-observation']['events'] += 1
                        resid['orphan-observation']['chars'] += len(content)
                    elif content.startswith('OBSERVATION:') or RC_PAT.search(content):
                        pend = False
            # detection (verbatim A0 grouping)
            masks = [0] * n
            by_cnorm = {}; by_csim = {}; by_path = {}
            for i, e in enumerate(events):
                by_cnorm.setdefault(e['cnorm'], []).append(i)
                by_csim.setdefault(e['csim'], []).append(i)
                if e['path']: by_path.setdefault(e['path'], []).append(i)
            def mk(short, i): masks[i] |= 1 << IDX[short]
            for grp, sh in ((by_cnorm, 'E1'), (by_csim, 'E2')):
                for k, idxs in grp.items():
                    if len(idxs) >= 2:
                        for i in idxs: mk(sh, i)
            for p, idxs in by_path.items():
                if len(idxs) < 2: continue
                for i in idxs: mk('E3', i)
                vr = [events[i]['vrange'] for i in idxs if events[i]['vrange']]
                if len(vr) >= 2:
                    for a in range(len(vr)):
                        for b in range(a + 1, len(vr)):
                            s1, e1 = vr[a][0], vr[a][1] if len(vr[a]) > 1 else vr[a][0]
                            s2, e2 = vr[b][0], vr[b][1] if len(vr[b]) > 1 else vr[b][0]
                            if s1 <= e2 and s2 <= e1:
                                for i in (idxs[a], idxs[b]): mk('E4', i)
                                break
            search_keys = {}
            for i, e in enumerate(events):
                if e['cclass'] == 'search': search_keys.setdefault(e['cnorm'], []).append(i)
            for k, idxs in search_keys.items():
                if len(idxs) >= 2:
                    for i in idxs: mk('E5', i)
            for i, e in enumerate(events):
                if e['obs_chars'] < 3000: continue
                is_pass = (e['exit'] == 0) or (e['exit'] is None and bool(PASS_PAT.search(e['obs'])) and not FAIL_PAT.search(e['obs']))
                is_fail = (e['exit'] is not None and e['exit'] != 0) or (e['exit'] is None and bool(FAIL_PAT.search(e['obs'])))
                if e['cclass'] == 'test':
                    if is_pass: mk('E6', i)
                    elif is_fail: mk('E7', i)
                elif e['cclass'] == 'lint': mk('E8', i)
                elif e['cclass'] == 'build': mk('E9', i)
                if DIAG_PAT.search(e['obs']): mk('E12', i)
            for k, idxs in by_cnorm.items():
                cls = events[idxs[0]]['cclass']
                if cls not in ('test', 'lint') or len(idxs) < 2: continue
                for i in idxs: mk('E10', i)
                for a, b in zip(idxs, idxs[1:]):
                    j = jaccard_lines(frozenset(events[a]['obs'].splitlines()), frozenset(events[b]['obs'].splitlines()))
                    if j >= 0.8:
                        for i in (a, b): mk('E11', i)
            for i, e in enumerate(events):
                if e['obs_chars'] >= 2000 and e['pos'] >= 0.75 and e['turns_after'] <= 3: mk('E13', i)
            for i, e in enumerate(events):
                for j in range(i + 1, min(i + 4, n)):
                    if e['path'] and events[j]['path'] == e['path'] and events[j]['cclass'] == 'view':
                        mk('E14', j); break
                for j in range(i + 1, min(i + 4, n)):
                    if events[j]['csim'] == e['csim'] and events[j]['cclass'] in ('test', 'lint', 'build'):
                        mk('E15', j); break
            # aggregates
            for i, e in enumerate(events):
                shapes = [SHAPES[bi] for bi in range(15) if masks[i] >> bi & 1]
                if e['obs_chars'] == 0 and is_klear: klear_stats['empty_obs_events'] += 1
                if shapes:
                    labeled_chars += e['obs_chars']
                    share = e['obs_chars'] / len(shapes)
                    for s in shapes:
                        shape_chars[s] += share
                        if s not in UNSAFE: qualified_chars += share
                        class_chars[CLASSES[s]] += share
                    for a in range(len(shapes)):
                        for b in range(a + 1, len(shapes)):
                            k2 = f'{shapes[a]}|{shapes[b]}' if IDX[shapes[a]] < IDX[shapes[b]] else f'{shapes[b]}|{shapes[a]}'
                            ev_pair[k2] = ev_pair.get(k2, 0) + 1
                    for s in shapes:
                        shape_sess[s].add(skey); shape_events[s] += 1
                        src_shape_sess.setdefault(src, {}).setdefault(s, set()).add(skey)
                        if not is_klear: nonklear_shape_sess[s].add(skey)
                    if set(shapes) <= UNSAFE:
                        resid['detected-unsafe-only']['events'] += 1; resid['detected-unsafe-only']['chars'] += e['obs_chars']
                    resid['detected']['events'] += 1; resid['detected']['chars'] += e['obs_chars']
                else:
                    if e['obs_chars'] < 2000:
                        resid['small-no-repeat']['events'] += 1; resid['small-no-repeat']['chars'] += e['obs_chars']
                    elif e['obs_chars'] < 3000 and e['cclass'] in ('test', 'lint', 'build'):
                        resid['below-large-threshold']['events'] += 1; resid['below-large-threshold']['chars'] += e['obs_chars']
                    elif e['cclass'] == 'test':
                        resid['large-classed-ambiguous-features']['events'] += 1
                        resid['large-classed-ambiguous-features']['chars'] += e['obs_chars']
                    else:
                        resid['large-uncovered-other']['events'] += 1; resid['large-uncovered-other']['chars'] += e['obs_chars']
            if not is_klear and n == 0:
                pass
    # ---- regression gate (non-klear 10,000) ----
    regression = {}
    ok_all = True
    for s in SHAPES:
        mine = len(nonklear_shape_sess[s])
        off = official.get(s)
        ok = (off == mine) if off is not None else (mine == 0)
        regression[s] = {'official': off, 'nonklear_mine': mine, 'match': ok}
        ok_all = ok_all and ok
    regression['_nonklear_obs_chars'] = {'official_15000_ctx_sum': 1134133251, 'nonklear_mine': round(nonklear_obs, 1),
                                         'match': abs(nonklear_obs - 1134133251) < 0.5}
    ok_all = ok_all and regression['_nonklear_obs_chars']['match']
    # ---- delta ledger + full-precision bands ----
    delta = {}
    bands = {}
    for s in SHAPES:
        old = official.get(s, 0)
        new = len(shape_sess[s])
        old_inc = old / 15000.0
        new_inc = new / 15000.0
        osw_c = osw_counts[s]
        def band(tw, osw):
            if not tw or not osw: return 'NOT_MEASURABLE' if not tw else 'MEASURABLE_ONLY'
            r = osw / tw
            if 0.5 <= r <= 2.0: return 'REPLICATED'
            if 0.2 <= r < 0.5 or 2.0 < r <= 5.0: return 'PARTIAL_REPLICATION'
            return 'DATASET_SPECIFIC'
        r_old = (osw_c / 20000.0) / old_inc if old else None
        r_new = (osw_c / 20000.0) / new_inc if new else None
        delta[s] = {'old_sessions': old, 'new_sessions': new, 'delta': new - old,
                    'old_inc': round(old_inc, 4), 'new_inc': round(new_inc, 4), 'delta_pp': round((new_inc - old_inc) * 100, 2),
                    'new_events': shape_events[s], 'new_chars_split': round(shape_chars[s], 1)}
        bands[s] = {'osw_exact': osw_c, 'tw_old_exact': old, 'tw_new_exact': new,
                    'ratio_old_fullprec': round(r_old, 4) if r_old else None,
                    'ratio_new_fullprec': round(r_new, 4) if r_new else None,
                    'band_old_fullprec': band(old_inc, osw_c / 20000.0) if old else 'NOT_MEASURABLE',
                    'band_new_fullprec': band(new_inc, osw_c / 20000.0) if new else 'NOT_MEASURABLE',
                    'band_stored_d4a1': d4a1['shape_results'][FULLNAME[s]]['replication_band']}
    out = {
        'meta': {'stage': 'V0.11-D4-A1R2 klear recovery discovery census amendment',
                 'prereg_sha256_16': prereg_sha[:16], 'input_parquet_sha256_16': input_sha[:16],
                 'script_sha256_16': script_sha[:16], 'sessions': sessions, 'events': total_events,
                 'adapter': 'D3-E4 user-role <returncode>/<output> branch (schema-adapter only)'},
        'regression_gate': {'pass': ok_all, 'detail': regression},
        'klear_verification': {**klear_stats, 'samples': klear_samples},
        'amended': {'per_shape_sessions': {s: len(shape_sess[s]) for s in SHAPES},
                    'per_shape_events': dict(shape_events),
                    'session_incidence': {s: round(len(shape_sess[s]) / sessions, 4) for s in SHAPES},
                    'total_obs_chars': round(tot_obs, 1), 'labeled_chars': round(labeled_chars, 1),
                    'qualified_chars': round(qualified_chars, 1),
                    'per_class_chars': {c: round(v, 1) for c, v in class_chars.items()},
                    'per_source': {str(src): {'sessions_obs_chars': round(v, 1), 'events': src_events.get(src, 0)} for src, v in src_obs.items()}},
        'delta_ledger': delta,
        'bands_full_precision': bands,
        'overlap_event_pairs_top': dict(sorted(ev_pair.items(), key=lambda kv: -kv[1])[:12]),
        'residual': resid,
    }
    json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
    print('REGRESSION GATE:', 'PASS' if ok_all else 'FAIL')
    if not ok_all:
        for s, v in regression.items():
            if isinstance(v, dict) and not v['match']: print('  DRIFT:', s, v)
    print('klear:', json.dumps({k: v for k, v in klear_stats.items()}))
    print('--- delta ledger (old -> new, sessions):')
    for s in SHAPES:
        d = delta[s]
        b = bands[s]
        print(f"  {s:4s} {d['old_sessions']:5d} -> {d['new_sessions']:5d} ({d['delta_pp']:+6.2f}pp)  "
              f"band old={b['band_old_fullprec']:18s} new={b['band_new_fullprec']:18s} ratio_new={b['ratio_new_fullprec']}")
    print('total obs chars:', round(tot_obs, 1), '(old official ctx sum 1,134,133,251)')
    print('saved:', OUT)

if __name__ == '__main__':
    main()
