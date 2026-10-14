#!/usr/bin/env python3
"""
V0.11-D3-E3 — repetition-class task-level savings census (mechanical, offline).
Prereg: docs/architecture/V0.11-D3-E3-REPEAT-CLASS-CENSUS-PREREG-V1.md (FROZEN 0b16c0c6)
E2/E3/E14 definitions reused UNCHANGED from E1. Deterministic: stable sort, no randomness, SHA256 recorded.
Ledger semantic: anchor (first observation in a repeat group) never counts; repeat events count only line-exact
chars already seen in the group context (union of prior observations). Event removable computed once (max over
its group contexts), never summed across shapes.
"""
import json, re, statistics, hashlib
import pyarrow.parquet as pq

PARQUET = 'D:/tasco-temp/d3_hf_data/sessions.parquet'
OUT = 'evidence/V1/v011-d3e3-repeat-class-census.json'

TEST_PAT = re.compile(r'^\s*(pytest|python\s+-m\s+pytest|npm\s+(run\s+)?test|mocha|jest|vitest|go\s+test|cargo\s+test|make\s+test|tox|python\s+-m\s+unittest)\b', re.I)
LINT_PAT = re.compile(r'^\s*(eslint|ruff|flake8|pylint|pre-commit)\b', re.I)
TYPECHECK_PAT = re.compile(r'^\s*(mypy|tsc|pyright|pyre)\b', re.I)
BUILD_PAT = re.compile(r'^\s*(make\b(?!.*test)|npm\s+run\s+build|gradle|mvn\b|cmake|cargo\s+build|gcc|g\+\+)', re.I)
SEARCH_PAT = re.compile(r'^\s*(grep|rg|ag|ack|find)\b', re.I)
VIEW_WORDS = {'view', 'open', 'cat', 'head', 'tail', 'less', 'sed', 'str_replace_editor'}
EXIT_PAT = re.compile(r'\[The command completed with exit code (\d+)[^\]]*\]')
NUMTOK = re.compile(r'\d+')

def norm_cmd(c): return ' '.join(c.split()).strip()
def sim_cmd(c): return ' '.join(NUMTOK.sub('#', norm_cmd(c)).split())

def cmd_class(c):
    if TEST_PAT.match(c) or LINT_PAT.match(c) or TYPECHECK_PAT.match(c) or BUILD_PAT.match(c): return 'check'
    if SEARCH_PAT.match(c): return 'search'
    first = c.split(' ', 1)[0].strip('`')
    if first in VIEW_WORDS: return 'view'
    return 'other'  # shell/other

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
            if cmd: pending = {'cmd': cmd, 'cnorm': norm_cmd(cmd), 'csim': sim_cmd(cmd), 'cclass': cmd_class(cmd), 'path': path, 'turn_index': idx}
        elif role == 'tool' and pending is not None:
            pending['obs'] = content; events.append(pending); pending = None
        elif role == 'user' and pending is not None:
            c = content if content.startswith('OBSERVATION:') else (content[content.find('OBSERVATION:'):] if 'OBSERVATION:' in content[:200] else None)
            if c is not None:
                pending['obs'] = c[len('OBSERVATION:'):].strip(); events.append(pending); pending = None
    for e in events:
        e['obs_chars'] = len(e.get('obs') or '')
        e['lines'] = frozenset((e.get('obs') or '').splitlines())
        e['assistant_chars'] = 0
    # assistant chars for wide denominator
    for m in msgs:
        if m.get('role') == 'assistant': pass
    return events

def inter_chars(line_set, seen_union):
    return sum(len(l) + 1 for l in line_set if l in seen_union)

SESSIONS_TOTAL = 0
sess_ledger = []  # per-session record
CTX = {'obs': 0, 'obs_plus_assistant': 0}
for batch in [None]:
    pass

pf = pq.ParquetFile(PARQUET)
assistant_char_cache = []
for batch in pf.iter_batches(batch_size=250):
    for row in batch.to_pylist():
        SESSIONS_TOTAL += 1
        try: msgs = json.loads(row['messages_json'])
        except Exception: continue
        events = parse_events(msgs)
        n = len(events)
        if not n: continue
        obs_total = sum(e['obs_chars'] for e in events)
        asst_total = sum(len(m.get('content') or '') for m in msgs if m.get('role') == 'assistant')
        CTX['obs'] += obs_total; CTX['obs_plus_assistant'] += obs_total + asst_total
        try: resolved = json.loads(row.get('ground_truth_meta_json') or '{}').get('resolved')
        except Exception: resolved = None

        # group construction (E1 definitions unchanged)
        csim_groups = {}; path_groups = {}
        for i, e in enumerate(events):
            csim_groups.setdefault(e['csim'], []).append(i)
            if e['cclass'] != 'other' or True:
                pass
            if e['path'] and e['cclass'] != 'other':
                path_groups.setdefault(e['path'], []).append(i)
            elif e['path']:
                path_groups.setdefault(e['path'], []).append(i)

        # per-event removable: compute in each group context, take max (single counting)
        ev_removable = {}
        ev_shapes = {i: set() for i in range(n)}
        for grp in (csim_groups, path_groups):
            for k, idxs in grp.items():
                if len(idxs) < 2: continue
                is_path_group = grp is path_groups
                seen = set()
                for j, i in enumerate(idxs):
                    e = events[i]
                    if j == 0:
                        seen |= e['lines']; continue
                    rem = inter_chars(e['lines'], seen)
                    prev = ev_removable.get(i, 0)
                    ev_removable[i] = max(prev, rem)
                    seen |= e['lines']
                    if is_path_group:
                        ev_shapes[i].add('E3')
                        # E14: reread within <=3 events of previous same-path event
                        if idxs[j] - idxs[j - 1] <= 3: ev_shapes[i].add('E14')
                    else:
                        ev_shapes[i].add('E2')
        # E14 anchor-reread pairs: mark reread events (already above via path group indexing)
        # session ledger per shape + union
        def ledger_for(shape=None):
            evs = [i for i in range(n) if (shape is None or shape in ev_shapes[i]) and i in ev_removable]
            if shape is None: evs = sorted(ev_removable.keys())
            q = len(evs)
            qchars = sum(events[i]['obs_chars'] for i in evs)
            gross = sum(events[i]['obs_chars'] for i in evs if ev_removable[i] >= 0)  # repeat events all counted (anchor never in ev_removable)
            rem = sum(ev_removable[i] for i in evs)
            return {'qualifying_events': q, 'qualifying_chars': qchars, 'gross_repeated_chars': gross, 'conservative_removable_chars': rem}

        u = ledger_for(None)
        e2 = ledger_for('E2'); e3 = ledger_for('E3'); e14 = ledger_for('E14')
        sess_ledger.append({
            'session': row['session_id'], 'source': row['source_dataset'], 'resolved': (json.loads(row.get('ground_truth_meta_json') or '{}').get('resolved') if row.get('ground_truth_meta_json') else None),
            'n_events': n, 'obs_total': obs_total, 'obs_plus_assistant': obs_total + asst_total,
            'union': u, 'E2': e2, 'E3': e3, 'E14': e14,
        })

def pctl(a, q):
    if not a: return None
    s = sorted(a); return s[min(len(s) - 1, int(q * len(s)))]
def med(a): return statistics.median(a) if a else None
def r4(x): return round(x, 4) if isinstance(x, float) else x

def shape_stats(key, denom='obs'):
    lk = 'union' if key is None else key
    hit = [s for s in sess_ledger if s[lk]['qualifying_events'] > 0]
    rem = [s[lk]['conservative_removable_chars'] for s in hit]
    gross = [s[lk]['gross_repeated_chars'] for s in hit]
    qev = [s[lk]['qualifying_events'] for s in hit]
    d = 'obs_total' if denom == 'obs' else 'obs_plus_assistant'
    ratios = [s[lk]['conservative_removable_chars'] / max(1, s[d]) for s in hit]
    out = {
        'sessions_with_shape': len(hit),
        'session_incidence': r4(len(hit) / SESSIONS_TOTAL),
        'qualifying_events_median': med(qev),
        'qualifying_chars': {'p25': pctl([s[lk]['qualifying_chars'] for s in hit], 0.25), 'median': med([s[lk]['qualifying_chars'] for s in hit]), 'p75': pctl([s[lk]['qualifying_chars'] for s in hit], 0.75), 'p90': pctl([s[lk]['qualifying_chars'] for s in hit], 0.90)},
        'gross_repeated_chars_median': med(gross),
        'conservative_removable_chars': {'p25': pctl(rem, 0.25), 'median': med(rem), 'p75': pctl(rem, 0.75), 'p90': pctl(rem, 0.90)},
        'cumulative_removable_thresholds': {f'>= {t} chars': r4(sum(1 for x in rem if x >= t) / SESSIONS_TOTAL) for t in (1000, 2000, 5000, 10000)},
        'repeat_count_distribution': {b: r4(sum(1 for x in qev if lo <= x <= hi) / max(1, len(qev))) for b, (lo, hi) in {'1': (1, 1), '2-3': (2, 3), '4-7': (4, 7), '8+': (8, 10 ** 9)}.items()},
        'removable_ratio_median': r4(med(ratios)),
        'removable_ratio_p90': r4(pctl(ratios, 0.90)),
    }
    return out

# union cross-shape overlaps (session-level)
s2 = set(s['session'] for s in sess_ledger if s['E2']['qualifying_events'] > 0)
s3 = set(s['session'] for s in sess_ledger if s['E3']['qualifying_events'] > 0)
s14 = set(s['session'] for s in sess_ledger if s['E14']['qualifying_events'] > 0)
overlaps = {
    'E2_and_E3': len(s2 & s3) / SESSIONS_TOTAL, 'E2_and_E14': len(s2 & s14) / SESSIONS_TOTAL,
    'E3_and_E14': len(s3 & s14) / SESSIONS_TOTAL, 'E2_E3_E14': len(s2 & s3 & s14) / SESSIONS_TOTAL,
}

# concentration on union removable
rem_by_sess = sorted(((s['union']['conservative_removable_chars'], s) for s in sess_ledger), key=lambda x: -x[0])
total_rem = sum(x[0] for x in rem_by_sess)
conc = {}
cum = 0
for rank, (v, s) in enumerate(rem_by_sess, 1):
    cum += v
    if rank in (1, int(0.01 * len(rem_by_sess)) or 1, int(0.05 * len(rem_by_sess)) or 1, int(0.10 * len(rem_by_sess)) or 1):
        conc[f'top{round(rank / len(rem_by_sess) * 100)}_cumulative_share'] = r4(cum / max(1, total_rem))
# length buckets + top5% removal
by_len = sorted(sess_ledger, key=lambda s: s['n_events'])
buckets = {'<=20': by_len[:int(0.25 * len(by_len))], '21-40': by_len[int(0.25 * len(by_len)):int(0.5 * len(by_len))], '41-60': by_len[int(0.5 * len(by_len)):int(0.75 * len(by_len))], '>60': by_len[int(0.75 * len(by_len)):]}
bucket_out = {k: {'sessions': len(v), 'union_removable_median': med([s['union']['conservative_removable_chars'] for s in v]), 'union_removable_p75': pctl([s['union']['conservative_removable_chars'] for s in v], 0.75)} for k, v in buckets.items()}
top5_cutoff = max(1, int(0.05 * len(by_len)))
trimmed = by_len[:len(by_len) - top5_cutoff]
trim_out = {
    'removed_top5pct_sessions': top5_cutoff,
    'remaining_union_removable_median': med([s['union']['conservative_removable_chars'] for s in trimmed]),
    'remaining_union_removable_p75': pctl([s['union']['conservative_removable_chars'] for s in trimmed], 0.75),
    'remaining_ge1K_incidence': r4(sum(1 for s in trimmed if s['union']['conservative_removable_chars'] >= 1000) / len(trimmed)),
    'remaining_ge2K_incidence': r4(sum(1 for s in trimmed if s['union']['conservative_removable_chars'] >= 2000) / len(trimmed)),
    'remaining_ge5K_incidence': r4(sum(1 for s in trimmed if s['union']['conservative_removable_chars'] >= 5000) / len(trimmed)),
}
resolved_stats = {}
for label, flt in (('resolved_true', lambda s: s['resolved'] is True), ('resolved_false_or_unknown', lambda s: s['resolved'] is not True)):
    sel = [s['union']['conservative_removable_chars'] for s in sess_ledger if flt(s)]
    resolved_stats[label] = {'sessions': len(sel), 'union_removable_median': med(sel), 'union_removable_p75': pctl(sel, 0.75)}

out = {
    'schema_version': 1,
    'stage': 'V0.11-D3-E3 repetition-class task-level savings census (prereg 0b16c0c6 FROZEN before first aggregate)',
    'date': '2026-09-23',
    'dataset': {'pin': 'D:/tasco-temp/d3_hf_data/sessions.parquet', 'sessions': SESSIONS_TOTAL},
    'definitions_reused_unchanged': True,
    'session_ledger_stats': {
        'E2_repeated_similar_command': shape_stats('E2'),
        'E3_same_file_reread': shape_stats('E3'),
        'E14_output_followed_by_reread': shape_stats('E14'),
        'deduplicated_union': shape_stats(None),
    },
    'cross_shape_overlaps_session_incidence': overlaps,
    'dual_denominators_note': 'removable_ratio uses observation-only denominator; observation+assistant totals: ' + json.dumps(CTX),
    'context_totals': CTX,
    'concentration': {'top_shares': conc, 'length_buckets': bucket_out, 'after_removing_top5pct_longest': trim_out, 'resolved_strata': resolved_stats},
    'naming_discipline': 'estimated removable chars per frozen mechanical oracle; NOT token savings',
    'verdict': 'CENSUS_COMPLETE',
}
out['aggregates_sha256'] = hashlib.sha256(json.dumps({k: v for k, v in out.items()}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print('sessions:', SESSIONS_TOTAL)
for k, v in out['session_ledger_stats'].items():
    print(f"{k:32s} inc={v['session_incidence']:<7} qevMed={v['qualifying_events_median']} remMed={v['conservative_removable_chars']['median']} remP75={v['conservative_removable_chars']['p75']} >=1K={v['cumulative_removable_thresholds']['>= 1000 chars']} >=5K={v['cumulative_removable_thresholds']['>= 5000 chars']} ratioMed={v['removable_ratio_median']}")
print('overlaps:', overlaps)
print('top shares:', conc)
print('after top5% removal:', trim_out)
print('hash:', out['aggregates_sha256'][:16], '...')
