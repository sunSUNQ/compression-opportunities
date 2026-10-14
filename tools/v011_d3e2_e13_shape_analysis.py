#!/usr/bin/env python3
"""
V0.11-D3-E2 — E13 natural shape decomposition (mechanical, offline).
Prereg: docs/architecture/V0.11-D3-E2-E13-DECOMPOSITION-PREREG-V1.md (FROZEN cf604d54)
E13 membership rebuilt from UNCHANGED E1 definition (obs>=2000, last-25% position, <=3 subsequent observations).
Deterministic: stable sorting, no randomness; aggregates hash recorded for rerun verification.
"""
import json, re, statistics, hashlib
import pyarrow.parquet as pq

PARQUET = 'D:/tasco-temp/d3_hf_data/sessions.parquet'
OUT = 'evidence/V1/v011-d3e2-e13-shape-analysis.json'

TEST_PAT = re.compile(r'^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|go\s+test|cargo\s+test|make\s+test|tox|python\s+-m\s+unittest)\b', re.I)
LINT_PAT = re.compile(r'^\s*(eslint|ruff|flake8|pylint|pre-commit)\b', re.I)
TYPECHECK_PAT = re.compile(r'^\s*(mypy|tsc|pyright|pyre)\b', re.I)
BUILD_PAT = re.compile(r'^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)', re.I)
GIT_PAT = re.compile(r'^\s*git\s+(diff|status|log|show|branch|commit)\b', re.I)
PKG_PAT = re.compile(r'^\s*(pip3?\s+install|npm\s+install|yarn\s+add|poetry\s+(add|install)|conda\s+install)\b', re.I)
SEARCH_PAT = re.compile(r'^\s*(grep|rg|ag|ack|find)\b', re.I)
VIEW_WORDS = {'view', 'open', 'cat', 'head', 'tail', 'less', 'sed', 'str_replace_editor'}
RUNTIME_PAT = re.compile(r'^\s*(python3?|node|perl|ruby)\b', re.I)
GENERIC_PAT = re.compile(r'^\s*(cd|ls|echo|pwd|mkdir|touch|mv|cp|rm|export|which|env)\b', re.I)

def norm_cmd(c): return ' '.join(c.split()).strip()
def sim_cmd(c): return ' '.join(re.sub(r'\d+', '#', norm_cmd(c)).split())

def producer(c, path_kind=False):
    if path_kind: return 'file-read'
    if TEST_PAT.match(c): return 'test'
    if LINT_PAT.match(c): return 'lint'
    if TYPECHECK_PAT.match(c): return 'typecheck'
    if BUILD_PAT.match(c): return 'build'
    if GIT_PAT.match(c): return 'git'
    if PKG_PAT.match(c): return 'package-install'
    if SEARCH_PAT.match(c): return 'search'
    if RUNTIME_PAT.match(c): return 'runtime-execute'
    if GENERIC_PAT.match(c): return 'generic-shell'
    first = c.split(' ', 1)[0].strip('`')
    if first in VIEW_WORDS: return 'file-read'
    return 'other'

# ---- frozen structure rules (prereg section 2) ----
STACK_PAT = re.compile(r'File "[^"]+", line \d+|^\s+at .+\(|Traceback|Caused by', re.M)
TCASE_PAT = re.compile(r'^[✓✖×]|PASSED|FAILED|PASS\b|FAIL\b|test_.*\.\.\.|passed|failed', re.M)
DIFF_PAT = re.compile(r'^@@|diff --git|^\+\+\+|^--- |^Index:', re.M)
COLS_PAT = re.compile(r'\S(\s{2,}\S)+|\S(\s*\|\s*\S)+')
CODE_PAT = re.compile(r'\bdef |\bclass |\bfunction |\bimport |\bfrom |\breturn |=\s|\{|\}')

def structure_ratios(obs):
    lines = obs.splitlines()
    n = max(1, len(lines))
    stack = sum(1 for l in lines if STACK_PAT.search(l)) / n
    tcase = sum(1 for l in lines if TCASE_PAT.search(l)) / n
    diff = sum(1 for l in lines if DIFF_PAT.search(l)) / n
    table = sum(1 for l in lines if COLS_PAT.search(l)) / n
    indent = sum(1 for l in lines if re.match(r'^\s+\S', l)) / n
    code = sum(1 for l in lines if CODE_PAT.search(l)) / n
    src = indent * (code >= 0.15)  # source-code-like requires both
    labels = {'stacktrace-diagnostic': stack >= 0.10, 'test-case-list': tcase >= 0.15,
              'diff-like': diff >= 0.05, 'table-list-like': table >= 0.30,
              'source-code-like': src >= 0.40}
    primary = max(labels.items(), key=lambda kv: kv[1])[0] if any(labels.values()) else 'unstructured'
    dup = n - len(set(lines))
    # consecutive repeated block chars (runs beyond first occurrence line)
    block_chars = 0
    run = 1
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1]: run += 1
        else:
            if run > 1: block_chars += sum(len(l) + 1 for l in lines[i - run + 1:i])
            run = 1
    if run > 1: block_chars += sum(len(l) + 1 for l in lines[len(lines) - run + 1:])
    seen = set(); dedup_chars = 0
    for l in lines:
        if l in seen: dedup_chars += len(l) + 1
        else: seen.add(l)
    collapse = dedup_chars + block_chars
    return {
        'line_count': len(lines),
        'unique_line_ratio': round(len(set(lines)) / n, 4),
        'exact_duplicate_line_ratio': round(dup / n, 4),
        'repeated_block_chars_ratio': round(block_chars / max(1, len(obs)), 4),
        'prefix_suffix_repeat': (lines[:5] == lines[-5:] and len(lines) >= 10),
        'labels': {k: round(v, 4) for k, v in [('stacktrace-diagnostic', stack), ('test-case-list', tcase), ('diff-like', diff), ('table-list-like', table), ('source-code-like', src)]},
        'primary_structure': primary,
        'dedup_only_removable_chars': dedup_chars,
        'structure_collapse_removable_chars': collapse,
        'removable_ratio_dedup': round(dedup_chars / max(1, len(obs)), 4),
        'removable_ratio_collapse': round(collapse / max(1, len(obs)), 4),
    }

# ---- parse + E13 membership rebuild (E1 definition unchanged) ----
def parse_events(msgs):
    events = []; pending = None
    for idx, m in enumerate(msgs):
        role = m.get('role'); content = m.get('content') or ''
        if role == 'assistant':
            tc = m.get('tool_calls_json'); cmd = None; path = None
            if tc:
                try:
                    calls = json.loads(tc)
                    if isinstance(calls, dict): calls = [calls]
                    for call in calls:
                        fn = (call.get('function') or {})
                        try: args = json.loads(fn.get('arguments') or '{}')
                        except Exception: args = {}
                        a = args.get('command')
                        if isinstance(a, str) and a.strip(): cmd = norm_cmd(a.splitlines()[0])
                        if args.get('path'): path = args['path']
                except Exception: pass
            if cmd is None:
                mm = re.search(r'```[a-z]*\s*\n(.+?)\n```', content, re.S)
                if mm:
                    first = mm.group(1).strip().splitlines()[0]
                    cmd = norm_cmd(first)
                    pm = re.search(r'(/[^\s`]+)', first)
                    if pm: path = pm.group(1)
            if cmd: pending = {'cmd': cmd, 'path': path, 'turn_index': idx}
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; em = EXIT_PAT.search(content)
            pending['exit'] = int(em.group(1)) if em else None
            events.append(pending); pending = None
        elif role == 'user' and pending is not None:
            c = content if content.startswith('OBSERVATION:') else (content[content.find('OBSERVATION:'):] if 'OBSERVATION:' in content[:200] else None)
            if c is not None:
                body = c[len('OBSERVATION:'):].strip()
                pending['obs'] = body; pending['exit'] = None
                events.append(pending); pending = None
    return events

EXIT_PAT = re.compile(r'\[The command completed with exit code (\d+)[^\]]*\]')

E13 = []
SESSIONS_TOTAL = 0
pf = pq.ParquetFile(PARQUET)
for batch in pf.iter_batches(batch_size=250):
    for row in batch.to_pylist():
        SESSIONS_TOTAL += 1
        try: msgs = json.loads(row['messages_json'])
        except Exception: continue
        events = parse_events(msgs)
        n = len(events)
        if not n: continue
        for i, e in enumerate(events):
            e['obs_chars'] = len(e.get('obs') or '')
            e['pos'] = (i + 1) / n
            e['turns_after'] = n - (i + 1)
        # E13 membership (E1 definition unchanged)
        for i, e in enumerate(events):
            if e['obs_chars'] >= 2000 and e['pos'] >= 0.75 and e['turns_after'] <= 3:
                e13 = dict(e)
                e13['producer'] = producer(e['cmd'], path_kind=(e['cclass'] if False else None) or (e['cmd'].split(' ', 1)[0].strip('`') in VIEW_WORDS))
                e13['session'] = row['session_id']; e13['source'] = row['source_dataset']
                try: e13['resolved'] = json.loads(row.get('ground_truth_meta_json') or '{}').get('resolved')
                except Exception: e13['resolved'] = None
                # future consumption within remaining events
                rest = events[i + 1:]
                e13['future'] = {
                    'has_subsequent_tool_call': len(rest) > 0,
                    'subsequent_obs_count': len(rest),
                    'reread_same_artifact': any(x.get('path') and x['path'] == e['path'] for x in rest),
                    'rerun_same_similar_command': any(sim_cmd(x['cmd']) == sim_cmd(e['cmd']) for x in rest),
                    'subsequent_output_chars': sum(x['obs_chars'] for x in rest),
                }
                e13['structure'] = structure_ratios(e['obs'])
                E13.append(e13)

def pctl(a, q):
    if not a: return None
    s = sorted(a); return s[min(len(s) - 1, int(q * len(s)))]

def med(a): return statistics.median(a) if a else None

def r4(x): return round(x, 4) if isinstance(x, float) else x

# ---- aggregate: producer taxonomy ----
producers = {}
for e in E13:
    producers.setdefault(e['producer'], []).append(e)
prod_out = {}
for p, evs in sorted(producers.items(), key=lambda kv: -len(kv[1])):
    sess = set(e['session'] for e in evs)
    chars = [e['obs_chars'] for e in evs]
    td = [e['turns_after'] for e in evs]
    prod_out[p] = {
        'events': len(evs), 'sessions': len(sess), 'session_incidence': r4(len(sess) / SESSIONS_TOTAL),
        'median_chars': med(chars), 'p75_chars': pctl(chars, 0.75), 'p90_chars': pctl(chars, 0.90),
        'terminal_turn_distance_median': med(td),
        'removable_ratio_dedup': {'p25': pctl([e['structure']['removable_ratio_dedup'] for e in evs], 0.25), 'median': med([e['structure']['removable_ratio_dedup'] for e in evs]), 'p75': pctl([e['structure']['removable_ratio_dedup'] for e in evs], 0.75)},
        'removable_ratio_collapse': {'p25': pctl([e['structure']['removable_ratio_collapse'] for e in evs], 0.25), 'median': med([e['structure']['removable_ratio_collapse'] for e in evs]), 'p75': pctl([e['structure']['removable_ratio_collapse'] for e in evs], 0.75)},
    }

# ---- aggregate: structure (primary label distribution) ----
struct_dist = {}
for e in E13:
    s = e['structure']['primary_structure']
    struct_dist.setdefault(s, {'count': 0, 'sessions': set(), 'median_chars': [], 'removable_dedup': [], 'removable_collapse': []})
    struct_dist[s]['count'] += 1
    struct_dist[s]['sessions'].add(e['session'])
    struct_dist[s]['median_chars'].append(e['obs_chars'])
    struct_dist[s]['removable_dedup'].append(e['structure']['removable_ratio_dedup'])
    struct_dist[s]['removable_collapse'].append(e['structure']['removable_ratio_collapse'])
struct_out = {}
for s, v in sorted(struct_dist.items(), key=lambda kv: -kv[1]['count']):
    struct_out[s] = {
        'events': v['count'], 'sessions': len(v['sessions']),
        'median_chars': med(v['median_chars']),
        'removable_ratio_dedup_median': med(v['removable_dedup']),
        'removable_ratio_collapse_median': med(v['removable_collapse']),
    }

# ---- aggregate: global removable ratios + future consumption ----
all_chars = [e['obs_chars'] for e in E13]
all_dedup = [e['structure']['removable_ratio_dedup'] for e in E13]
all_collapse = [e['structure']['removable_ratio_collapse'] for e in E13]
td_all = [e['turns_after'] for e in E13]
future = {
    'has_subsequent_tool_call_rate': r4(sum(1 for e in E13 if e['future']['has_subsequent_tool_call']) / len(E13)),
    'reread_same_artifact_rate': r4(sum(1 for e in E13 if e['future']['reread_same_artifact']) / len(E13)),
    'rerun_same_similar_command_rate': r4(sum(1 for e in E13 if e['future']['rerun_same_similar_command']) / len(E13)),
    'terminal_distance_distribution': {d: r4(sum(1 for e in E13 if min(e['future']['subsequent_obs_count'], 3) == (3 if d == '3+' else int(d))) / len(E13)) for d in ['0', '1', '2', '3+']},
    'subsequent_output_chars_median': med([e['future']['subsequent_output_chars'] for e in E13]),
    'subsequent_output_chars_p75': pctl([e['future']['subsequent_output_chars'] for e in E13], 0.75),
}
global_out = {
    'e13_events': len(E13), 'e13_sessions': len(set(e['session'] for e in E13)),
    'session_incidence': r4(len(set(e['session'] for e in E13)) / SESSIONS_TOTAL),
    'median_chars': med(all_chars), 'p75_chars': pctl(all_chars, 0.75), 'p90_chars': pctl(all_chars, 0.90),
    'terminal_turn_distance_median': med(td_all),
    'removable_ratio_dedup': {'p25': pctl(all_dedup, 0.25), 'median': med(all_dedup), 'p75': pctl(all_dedup, 0.75)},
    'removable_ratio_collapse': {'p25': pctl(all_collapse, 0.25), 'median': med(all_collapse), 'p75': pctl(all_collapse, 0.75)},
    'future_consumption': future,
}

out = {
    'schema_version': 1,
    'stage': 'V0.11-D3-E2 E13 natural shape decomposition (prereg cf604d54 FROZEN before analysis)',
    'date': '2026-09-23',
    'dataset': {'pin': 'D:/tasco-temp/d3_hf_data/sessions.parquet', 'sessions_total': SESSIONS_TOTAL},
    'e13_definition_unchanged': True,
    'producer_taxonomy': prod_out,
    'payload_structure_distribution': struct_out,
    'global': global_out,
    'wording_note': 'LOW exposure = significantly reduced trajectory-backfire risk per frozen prereg; NOT immune/safe',
}
blob = json.dumps(out, sort_keys=True, indent=1, ensure_ascii=False).encode('utf-8')
out['aggregates_sha256'] = hashlib.sha256(json.dumps({k: v for k, v in out.items()}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print('E13 events:', len(E13), '| sessions:', out['global']['e13_sessions'], '| incidence:', out['global']['session_incidence'])
print('--- producers:')
for p, v in sorted(prod_out.items(), key=lambda kv: -kv[1]['events']):
    print(f"  {p:18s} ev={v['events']:<5} sess={v['sessions']:<5} inc={v['session_incidence']:<7} med={v['median_chars']:<8} p75={v['p75_chars']:<8} dedupMed={v['removable_ratio_dedup']['median']} collapseMed={v['removable_ratio_collapse']['median']}")
print('--- structure:')
for s, v in struct_out.items(): print(f"  {s:22s} ev={v['events']:<5} med={v['median_chars']:<8} dedup={v['removable_ratio_dedup_median']} collapse={v['removable_ratio_collapse_median']}")
print('--- global removable: dedup', global_out['removable_ratio_dedup'], 'collapse', global_out['removable_ratio_collapse'])
print('--- future consumption:', json.dumps(future))
print('hash:', out['aggregates_sha256'][:16], '...')
