#!/usr/bin/env python3
"""
V0.11-D3-E6 — test-fix RDS negative-region mechanism audit (mechanical, offline).
Prereg: docs/architecture/V0.11-D3-E6-TESTFIX-NEGATIVE-AUDIT-PREREG-V1.md (FROZEN 6e06dd04)
Data: frozen D5 sessions (claude.stream-json.log + summary.json + rds_ledger.ndjson). Zero runs.
"""
import json, os, re, statistics, hashlib

WT = os.getcwd()
RES = os.path.join(WT, 'hook_ab_test', 'results', 'v011_d5_rds_ab_20260923')
OUT = os.path.join(WT, 'evidence', 'V1', 'v011-d3e6-testfix-negative-audit.json')

TEST_PAT = re.compile(r'^\s*(pytest|npm\s+(run\s+)?test|mocha|jest|go\s+test|cargo\s+test|make\s+test|tox)\b', re.I)
VIEW_PAT = re.compile(r'^\s*(view|open|cat|head|tail|less|sed|type|Get-Content)\b', re.I)
NUMTOK = re.compile(r'\d+')
MARKER_PAT = re.compile(r'\[TASCO-RDS omitted: observation #(\d+) lines (\d+)\.\.(\d+) \((\d+) chars\); new: (\d+) chars\]')
I4_PAT = re.compile(r'完整输出|full output|再次执行|重新运行|run again|重新查看|see the full|cat\s|view\s', re.I)

def norm_cmd(c): return ' '.join(c.split()).strip()
def sim_cmd(c): return ' '.join(NUMTOK.sub('#', norm_cmd(c)).split())

def parse_stream(f):
    """Return events [(cmd, csim, cclass, obs, obs_chars, obs_lines, is_marker, marker_info)], assistant_texts."""
    events = []; assistant_texts = []; pending = None
    for ln in open(f, encoding='utf-8', errors='replace'):
        ln = ln.strip()
        if not ln: continue
        try: j = json.loads(ln)
        except Exception: continue
        t = j.get('type'); msg = j.get('message') or {}
        if t == 'assistant':
            for c in (msg.get('content') or []):
                if c.get('type') == 'tool_use':
                    inp = c.get('input') or {}
                    cmd = inp.get('command') or (inp.get('file_path') and 'view ' + inp['file_path']) or ''
                    if isinstance(cmd, str) and cmd.strip():
                        pending = {'cmd': norm_cmd(cmd.splitlines()[0]), 'csim': sim_cmd(cmd.splitlines()[0])}
                elif c.get('type') == 'text':
                    assistant_texts.append(c.get('text') or '')
        elif t == 'user' and pending is not None:
            for c in (msg.get('content') or []):
                if c.get('type') == 'tool_result':
                    obs = c.get('content') if isinstance(c.get('content'), str) else json.dumps(c.get('content'))
                    is_marker = '[TASCO-RDS omitted:' in obs
                    mi = None
                    if is_marker:
                        mm = MARKER_PAT.search(obs)
                        mi = {'anchor_k': int(mm.group(1)), 'a': int(mm.group(2)), 'b': int(mm.group(3))} if mm else None
                    events.append({'cmd': pending['cmd'], 'csim': pending['csim'],
                                   'cclass': 'test' if TEST_PAT.match(pending['cmd']) else ('view' if VIEW_PAT.match(pending['cmd']) else 'other'),
                                   'obs': obs, 'obs_chars': len(obs), 'is_marker': is_marker, 'marker': mi})
                    pending = None
    return events, assistant_texts

def find_stream(base):
    stack = [base]
    while stack:
        d = stack.pop()
        try: es = os.listdir(d)
        except Exception: continue
        for e in es:
            p = os.path.join(d, e)
            if os.path.isdir(p): stack.append(p)
            elif e == 'claude.stream-json.log': return p
    return None

def load_session(task, rep, arm):
    base = os.path.join(RES, task, 'rep' + str(rep), 'formal', f'{task}_{arm}')
    sf = os.path.join(base, 'summary.json')
    s = json.load(open(sf, encoding='utf-8-sig')) if os.path.exists(sf) else None
    lf = None
    stack = [os.path.join(os.path.dirname(base), '_work_' + f'{task}_{arm}')]
    while stack and not lf:
        d = stack.pop()
        try: es = os.listdir(d)
        except Exception: continue
        for e in es:
            p = os.path.join(d, e)
            if os.path.isdir(p): stack.append(p)
            elif e == 'rds_ledger.ndjson': lf = p
    ledger = []
    if lf:
        for ln in open(lf, encoding='utf-8', errors='replace'):
            ln = ln.strip()
            if ln:
                try: ledger.append(json.loads(ln))
                except Exception: pass
    stream = find_stream(base)
    events, texts = parse_stream(stream) if stream else ([], [])
    u = (s or {}).get('usage') or {}
    return {
        'task': task, 'rep': rep, 'arm': arm,
        'events': events, 'assistant_texts': texts, 'ledger': ledger,
        'turns': (s or {}).get('turns'), 'oracle': (s or {}).get('exitCode') == 0,
        'input': u.get('input_tokens', 0), 'output': u.get('output_tokens', 0),
        'cache_read': u.get('cache_read_input_tokens', 0), 'cache_creation': u.get('cache_creation_input_tokens', 0),
        'total': (u.get('input_tokens', 0) + u.get('output_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0)),
    }

# ---- folded lines per compressed event (from marker + anchor event original obs) ----
def folded_lines(events, ledger):
    """Replay: marker at event i references anchor observation #k lines a..b; folded lines = those lines from the anchor event's obs."""
    folded = {}  # event index -> set of folded lines
    # obs #k (1-based over ALL hook-processed observations) — map ledger seq order to events processed by hook.
    # hook processed every tool observation in order; events here are the same sequence (both arms identical hook call pattern).
    for r in ledger:
        if r.get('compressed'):
            i = r['seq'] - 1
            k = r.get('anchor_seq')
            if 1 <= (i + 1) <= len(events) and 1 <= (k or 0) <= len(events):
                src_l = events[k - 1]['obs'].replace('\r\n', '\n').split('\n')
                # folded region per-line unknown (matched subset); conservative: whole anchor lines as reconsumption candidate set
                folded[i] = src_l
    return folded

# ---- taxonomy of folded lines (frozen patterns) ----
def classify_lines(lines):
    cats = {'passing-test': 0, 'failing-detail': 0, 'assertion': 0, 'stack': 0, 'path-line': 0, 'summary-count': 0, 'boilerplate': 0, 'other': 0}
    for l in lines:
        if re.search(r'PASSED|✓|passed\b', l, re.I): cats['passing-test'] += len(l) + 1
        elif re.search(r'FAILED|✖|failing|Error:', l, re.I): cats['failing-detail'] += len(l) + 1
        elif re.search(r'AssertionError|expected|actual', l, re.I): cats['assertion'] += len(l) + 1
        elif re.search(r'Traceback|at .+\(', l): cats['stack'] += len(l) + 1
        elif re.search(r'\.js:\d+|:\d+:', l): cats['path-line'] += len(l) + 1
        elif re.search(r'\d+ (passed|failed|total)|^total\b', l, re.I): cats['summary-count'] += len(l) + 1
        elif re.search(r'^\s*(\$|>|npm|node|npx|mocha)', l): cats['boilerplate'] += len(l) + 1
        else: cats['other'] += len(l) + 1
    return cats

def window_indicators(events, marker_idx, window=5, ledger=None):
    e = events[marker_idx]
    m = e.get('marker') or {}
    anchor_obs = events[m['anchor_k'] - 1] if m and 1 <= m['anchor_k'] <= len(events) else None
    anchor_path_m = VIEW_PAT.match(anchor_obs['cmd']) if anchor_obs else None
    anchor_path = None
    if anchor_obs:
        pm = re.search(r'(/[^\s`]+)', anchor_obs['cmd'])
        anchor_path = pm.group(1) if pm else None
    comp_csim = e['csim']; anchor_csim = anchor_obs['csim'] if anchor_obs else None
    ind = {'I1': False, 'I2': False, 'I3': False, 'I4': False, 'I5': False}
    folded = folded_lines(events, ledger or []).get(marker_idx, [])
    fset = set(folded)
    for j in range(marker_idx + 1, min(marker_idx + 1 + window, len(events))):
        f = events[j]
        pm = re.search(r'(/[^\s`]+)', f['cmd'])
        p = pm.group(1) if pm else None
        if f['cclass'] == 'view' and p and ((anchor_path and p == anchor_path) or (anchor_obs and anchor_obs['cmd'] == f['cmd'])): ind['I1'] = True
        if f['csim'] in (comp_csim, anchor_csim): ind['I2'] = True
        if f['cclass'] == 'test': ind['I3'] = True
        if f['cclass'] == 'view' and fset and (fset & set(f['obs'].replace('\r\n', '\n').split('\n'))): ind['I5'] = True
    # I4: assistant text between marker and end of window (approximate: any assistant text after marker index*2 messages)
    return ind, {'anchor_path': anchor_path, 'comp_csim': comp_csim, 'anchor_csim': anchor_csim}

def first_divergence(Be, Te):
    n = min(len(Be), len(Te))
    for i in range(n):
        if Be[i]['csim'] != Te[i]['csim']: return i + 1  # 1-based
    return min(len(Be), len(Te)) + 1  # identical prefixes; divergence after

def marker_local_backlash(events, marker_idx, window=5, ledger=None):
    ind, _ = window_indicators(events, marker_idx, window, ledger)
    return ind

# ---- audit test-fix pairs ----
results = {'pairs': [], 'lint_control': []}
for task in ['t1', 't2', 't3', 't4']:
    for rep in [1, 2]:
        B = load_session(task, rep, 'o'); T = load_session(task, rep, 'd')
        D1 = first_divergence(B['events'], T['events'])
        comp_seqs = [r['seq'] for r in T['ledger'] if r.get('compressed')]
        markers = [s - 1 for s in comp_seqs if 1 <= s <= len(T['events'])]
        M1 = (markers[0] + 1) if markers else None
        case = 'B' if (M1 is not None and D1 <= M1) else ('A' if M1 else 'no-marker')
        if M1 is not None and abs(D1 - M1) <= 1: case += '-borderline'
        inds = {}
        per_marker_windows = []
        for mi in markers:
            ind = marker_local_backlash(T['events'], mi, ledger=T['ledger'])
            inds[mi] = ind
            per_marker_windows.append({'marker_event': mi + 1, **ind})
        anyI = any(ind['I1'] or ind['I2'] or ind['I5'] for ind in inds.values())
        anyComp = any(ind['I3'] or ind['I4'] for ind in inds.values())
        # folded content taxonomy
        folded_map = folded_lines(T['events'], T['ledger'])
        all_folded = [l for ls in folded_map.values() for l in ls]
        tax = classify_lines(all_folded)
        # attribution decision tree (per pair)
        if case.startswith('B'):
            attribution = 'UNRELATED_TRAJECTORY_DIVERGENCE'
        elif anyI:
            attribution = 'RDS_INFORMATION_RECOVERY'
        elif anyComp:
            attribution = 'RDS_REASONING_COMPENSATION'
        else:
            attribution = 'NO_ATTRIBUTABLE_CAUSE'
        # decomposition
        dec = {
            'd_input': T['input'] - B['input'], 'd_output': T['output'] - B['output'],
            'd_cache_read': T['cache_read'] - B['cache_read'],
            'd_tool_calls': len(T['events']) - len(B['events']),
            'd_obs_chars': sum(e['obs_chars'] for e in T['events']) - sum(e['obs_chars'] for e in B['events']),
            'd_assistant_chars': sum(len(t) for t in T['assistant_texts']) - sum(len(t) for t in B['assistant_texts']),
            'd_turns': T['turns'] - B['turns'], 'd_total': T['total'] - B['total'],
        }
        results['pairs'].append({
            'pair': f'{task}/rep{rep}', 'd_total': dec['d_total'],
            'first_divergence_pos': D1, 'first_marker_pos': M1, 'case': case,
            'markers': len(markers), 'indicators': {str(k): v for k, v in inds.items()},
            'per_marker_windows': per_marker_windows,
            'attribution': attribution, 'folded_taxonomy_chars': tax,
            'folded_lines_total': len(all_folded),
            'decomposition': dec,
        })

# ---- lint control: top-8 positive pairs by |relative saving| ----
pair_savings = []
for task in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']:
    for rep in [1, 2]:
        B = load_session(task, rep, 'o'); T = load_session(task, rep, 'd')
        if B['total'] and T['total'] and (B['total'] - T['total']) / B['total'] > 0:
            pair_savings.append(((B['total'] - T['total']) / B['total'], task, rep))
pair_savings.sort(reverse=True)
control = []
for sv, task, rep in pair_savings[:8]:
    B = load_session(task, rep, 'o'); T = load_session(task, rep, 'd')
    D1 = first_divergence(B['events'], T['events'])
    comp_seqs = [r['seq'] for r in T['ledger'] if r.get('compressed')]
    markers = [s - 1 for s in comp_seqs if 1 <= s <= len(T['events'])]
    M1 = (markers[0] + 1) if markers else None
    inds = {}
    for mi in markers:
        ind = marker_local_backlash(T['events'], mi, ledger=T['ledger'])
        inds[mi] = ind
    anyI = any(ind['I1'] or ind['I2'] or ind['I5'] for ind in inds.values())
    anyComp = any(ind['I3'] or ind['I4'] for ind in inds.values())
    case = 'B' if (M1 is not None and D1 <= M1) else ('A' if M1 else 'no-marker')
    if anyI: attribution = 'RDS_INFORMATION_RECOVERY'
    elif anyComp: attribution = 'RDS_REASONING_COMPENSATION'
    elif case.startswith('B'): attribution = 'UNRELATED_TRAJECTORY_DIVERGENCE'
    else: attribution = 'NO_ATTRIBUTABLE_CAUSE'
    folded_map = folded_lines(T['events'], T['ledger'])
    all_folded = [l for ls in folded_map.values() for l in ls]
    control.append({'pair': f'{task}/rep{rep}', 'relative_saving': round(sv, 4), 'case': case,
                    'markers': len(markers), 'attribution': attribution,
                    'folded_taxonomy_chars': classify_lines(all_folded)})

# ---- aggregate verdict ----
attr_counts = {}
for p in results['pairs']:
    attr_counts[p['attribution']] = attr_counts.get(p['attribution'], 0) + 1
n_neg = len(results['pairs'])
verdict = 'UNRESOLVED'
if attr_counts.get('RDS_INFORMATION_RECOVERY', 0) >= 5: verdict = 'RDS_INFORMATION_LOSS'
elif attr_counts.get('RDS_REASONING_COMPENSATION', 0) >= 5: verdict = 'RDS_ADOPTION_EFFECT'
elif attr_counts.get('UNRELATED_TRAJECTORY_DIVERGENCE', 0) + attr_counts.get('NO_ATTRIBUTABLE_CAUSE', 0) >= 5: verdict = 'TRAJECTORY_VARIANCE_DOMINANT'
elif len(attr_counts) >= 2 and max(attr_counts.values()) >= 3: verdict = 'MIXED'

out = {
    'schema_version': 1,
    'stage': 'V0.11-D3-E6 test-fix negative-region mechanism audit (prereg 6e06dd04 FROZEN before trace review)',
    'date': '2026-09-24',
    'test_fix_pairs': results['pairs'],
    'attribution_counts': attr_counts,
    'lint_control': control,
    'verdict': verdict,
}
out['aggregates_sha256'] = hashlib.sha256(json.dumps(out, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('=== test-fix negative pairs (8):')
for p in results['pairs']:
    print(f"{p['pair']}  dTotal={p['d_total']:<8} case={p['case']:<18} D1={p['first_divergence_pos']} M1={p['first_marker_pos']} markers={p['markers']} => {p['attribution']}")
    print('   indicators:', json.dumps({k: v for k, v in p['indicators'].items()}))
    print('   folded taxonomy:', json.dumps(p['folded_taxonomy_chars']))
print('attribution counts:', attr_counts)
print('VERDICT:', verdict)
print('=== lint control (top-8 positive):')
for c in control:
    print(f"{c['pair']}  sv={c['relative_saving']}  case={c['case']} markers={c['markers']} => {c['attribution']}")
