#!/usr/bin/env python3
"""
V0.11-D4-A1R3 — trajectory (row) identity session-caliber amendment census.
Prereg: evidence/V1/v011-d4a1r3-session-identity-prereg.json (FROZEN before recompute).
Identity: (frozen source file, row ordinal); content digest verification-only.
Detection: A1R2 frozen detection block executed verbatim by byte-slice (zero transcription).
Outputs: evidence/V1/v011-d4a1r3-tw-trajectory-census.json
"""
import importlib.util, json, textwrap, os, hashlib, re
from collections import Counter, defaultdict
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREREG = os.path.join(ROOT, 'evidence/V1/v011-d4a1r3-session-identity-prereg.json')
A1R2 = os.path.join(ROOT, 'evidence/V1/v011-d4a1r2-tw-klear-census.json')
OSW = os.path.join(ROOT, 'evidence/V1/v011-d4a1-census-results.json')
OUT = os.path.join(ROOT, 'evidence/V1/v011-d4a1r3-tw-trajectory-census.json')
PARQUET = 'D:/tasco-temp/d3_hf_data/sessions.parquet'
SHAPES = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15']
FULLNAME = {'E1': 'E1_repeated_exact_command', 'E2': 'E2_repeated_similar_command', 'E3': 'E3_same_file_reread',
            'E4': 'E4_overlapping_file_read', 'E5': 'E5_same_search', 'E6': 'E6_large_test_success',
            'E7': 'E7_large_test_failure', 'E8': 'E8_large_lint_output', 'E9': 'E9_large_build_output',
            'E10': 'E10_repeated_validation', 'E11': 'E11_unchanged_validation', 'E12': 'E12_large_diagnostic',
            'E13': 'E13_large_output_near_terminal', 'E14': 'E14_output_followed_by_reread',
            'E15': 'E15_output_followed_by_rederivation'}
UNSAFE = {'E7', 'E12'}
IDX = {s: i for i, s in enumerate(SHAPES)}
DEN = 15000
OSW_DEN = 20000

def sha16(path_or_bytes):
    h = hashlib.sha256()
    if isinstance(path_or_bytes, bytes):
        h.update(path_or_bytes)
    else:
        with open(path_or_bytes, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
    return h.hexdigest()[:16]

prereg_sha = sha16(PREREG)
a1r2 = json.load(open(A1R2, encoding='utf-8'))
d4a1 = json.load(open(OSW, encoding='utf-8'))
parquet_sha = sha16(PARQUET)
script_sha = sha16(os.path.abspath(__file__))

spec = importlib.util.spec_from_file_location('a1r2mod', os.path.join(ROOT, 'evidence/tools/v011_d4a1r2_tw_klear_census.py'))
a1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a1)
a1_src = open(os.path.join(ROOT, 'evidence/tools/v011_d4a1r2_tw_klear_census.py'), encoding='utf-8').read()
detect_block = textwrap.dedent(a1_src[a1_src.index('            # detection (verbatim A0 grouping)'):a1_src.index('            # aggregates')])
orphan_block = textwrap.dedent(a1_src[a1_src.index('            pend = False'):a1_src.index('            # detection (verbatim A0 grouping)')])
assert "orphan-observation" in orphan_block
assert "mk('E15', j)" in detect_block and "mk('E12', i)" in detect_block

def reduce_or(shapes):
    m = 0
    for s in shapes:
        m |= 1 << IDX[s]
    return m

# ---- pass A: row-order stability (two-pass sequence hash) ----
def seq_hash():
    h = hashlib.sha256()
    pf = pq.ParquetFile(PARQUET)
    for batch in pf.iter_batches(batch_size=2000, columns=['session_id', 'source_dataset']):
        for sid, src in zip(batch.column('session_id').to_pylist(), batch.column('source_dataset').to_pylist()):
            h.update((sid + '\x1f' + src + '\x1e').encode('utf-8'))
    return h.hexdigest()
seq_h1, seq_h2 = seq_hash(), seq_hash()
replay_stable = (seq_h1 == seq_h2)

# ---- pass B: per-row detection + accumulation ----
row_hits = {s: 0 for s in SHAPES}
idset_shapes = defaultdict(set)
event_hits = {s: 0 for s in SHAPES}
resid = {k: {'events': 0, 'chars': 0} for k in ['detected', 'small-no-repeat', 'large-uncovered-other',
         'large-classed-ambiguous-features', 'below-large-threshold', 'schema-missing-view-range',
         'detected-unsafe-only', 'orphan-observation']}
cclass_undetected = {}
shape_chars = {s: 0.0 for s in SHAPES}
class_chars = {c: 0.0 for c in 'ABCDE'}
labeled = qualified = 0.0
tot_events = 0; tot_chars = 0.0; sessions = 0
row_meta = []
CLASSES = a1.CLASSES if hasattr(a1, 'CLASSES') else {'E1': 'A', 'E2': 'A', 'E3': 'A', 'E4': 'A', 'E5': 'D', 'E6': 'D',
    'E7': 'C', 'E8': 'A', 'E9': 'E', 'E10': 'D', 'E11': 'D', 'E12': 'C', 'E13': 'B', 'E14': 'A', 'E15': 'D'}

pf = pq.ParquetFile(PARQUET)
tid = 0
for batch in pf.iter_batches(batch_size=250):
    for row in batch.to_pylist():
        try:
            msgs = json.loads(row['messages_json'])
        except Exception:
            msgs = None
        digest = hashlib.sha256((row['messages_json'] or '').encode('utf-8')).hexdigest()[:16]
        n = 0
        row_mask = 0
        row_char = 0.0
        if msgs is not None:
            exec(orphan_block, {'msgs': msgs, 'resid': resid, 'RC_PAT': a1.RC_PAT, 're': re})
            events = a1.parse_events(msgs)
            n = len(events)
            if n:
                for i, e in enumerate(events):
                    e['pos'] = (i + 1) / n
                    e['turns_after'] = n - (i + 1)
                ns = {'n': n, 'events': events, 'IDX': IDX, 'jaccard_lines': a1.jaccard_lines,
                      'PASS_PAT': a1.PASS_PAT, 'FAIL_PAT': a1.FAIL_PAT, 'DIAG_PAT': a1.DIAG_PAT}
                exec(detect_block, ns)
                masks = ns['masks']
                sid = row['session_id']
                for i, e in enumerate(events):
                    tot_events += 1
                    tot_chars += e['obs_chars']
                    row_char += e['obs_chars']
                    shapes = [SHAPES[b] for b in range(15) if masks[i] >> b & 1]
                    for s in shapes:
                        event_hits[s] += 1
                        shape_chars[s] += e['obs_chars'] / len(shapes)
                        if s not in UNSAFE:
                            qualified += e['obs_chars'] / len(shapes)
                        class_chars[CLASSES[s]] += e['obs_chars'] / len(shapes)
                    if shapes:
                        labeled += e['obs_chars']
                        row_mask |= reduce_or(shapes)
                        if set(shapes) <= UNSAFE:
                            resid['detected-unsafe-only']['events'] += 1
                            resid['detected-unsafe-only']['chars'] += e['obs_chars']
                        resid['detected']['events'] += 1
                        resid['detected']['chars'] += e['obs_chars']
                    else:
                        if e['obs_chars'] < 2000:
                            resid['small-no-repeat']['events'] += 1; resid['small-no-repeat']['chars'] += e['obs_chars']
                        elif e['obs_chars'] < 3000 and e['cclass'] in ('test', 'lint', 'build'):
                            resid['below-large-threshold']['events'] += 1; resid['below-large-threshold']['chars'] += e['obs_chars']
                        elif e['cclass'] == 'test' and e['obs_chars'] >= 3000:
                            resid['large-classed-ambiguous-features']['events'] += 1
                            resid['large-classed-ambiguous-features']['chars'] += e['obs_chars']
                        else:
                            resid['large-uncovered-other']['events'] += 1
                            resid['large-uncovered-other']['chars'] += e['obs_chars']
                            cclass_undetected[e['cclass']] = cclass_undetected.get(e['cclass'], 0) + 1
        sessions += 1
        row_meta.append({'tid': tid, 'session_id': row['session_id'], 'source': row.get('source_dataset'),
                         'digest': digest, 'mask': row_mask, 'n_events': n, 'obs_chars': row_char})
        idset_shapes[row['session_id']].update(SHAPES[b] for b in range(15) if row_mask >> b & 1)
        for b, s in enumerate(SHAPES):
            if row_mask >> b & 1:
                row_hits[s] += 1
        tid += 1

def reduce_or(shapes):
    m = 0
    for s in shapes:
        m |= 1 << IDX[s]
    return m

# ---- per-shape calibers ----
idset_hits = {s: 0 for s in SHAPES}
for k, ss in idset_shapes.items():
    for s in ss:
        idset_hits[s] += 1

# collided pairs
groups = defaultdict(list)
for r in row_meta:
    groups[r['session_id']].append(r)
collided = {k: v for k, v in groups.items() if len(v) > 1}
mult_hist = Counter(len(v) for v in groups.values())
pair_class = {'identical_content': 0, 'distinct_content': 0}
pair_shape_both = {s: 0 for s in SHAPES}
identical_pair_tids = None
for k, v in collided.items():
    a, b = v[0], v[1]
    cls = 'identical_content' if a['digest'] == b['digest'] else 'distinct_content'
    pair_class[cls] += 1
    if cls == 'identical_content':
        identical_pair_tids = [a['tid'], b['tid']]
    for s in SHAPES:
        if (a['mask'] >> IDX[s] & 1) and (b['mask'] >> IDX[s] & 1):
            pair_shape_both[s] += 1

# ---- A1R2 consistency gates (STOP on mismatch) ----
frozen_sessions = a1r2['amended']['per_shape_sessions']
frozen_events = a1r2['amended']['per_shape_events']
gates = {
    'replay_stable': replay_stable,
    'idset_matches_a1r2_sessions': all(idset_hits[s] == frozen_sessions[s] for s in SHAPES),
    'events_match_a1r2': all(event_hits[s] == frozen_events[s] for s in SHAPES),
    'total_events_match': tot_events == a1r2['meta']['events'],
    'total_chars_match': abs(tot_chars - a1r2['amended']['total_obs_chars']) < 0.5,
    'labeled_match': abs(labeled - a1r2['amended']['labeled_chars']) < 0.5,
    'residual_match': all(resid[k] == a1r2['residual'][k] for k in resid if k in a1r2['residual']),
    'residual_schema_missing_zero': resid['schema-missing-view-range'] == {'events': 0, 'chars': 0},
}
gates_all = all(gates.values())

# ---- bands: full precision, both calibers ----
osw_exact = {s: d4a1['shape_results'][FULLNAME[s]]['event_sessions'] for s in SHAPES}
osw_inc = {s: osw_exact[s] / OSW_DEN for s in SHAPES}
def reduce_or(shapes):
    m = 0
    for s in shapes:
        m |= 1 << IDX[s]
    return m

def band(r):
    if 0.5 <= r <= 2.0: return 'REPLICATED'
    if 0.2 <= r < 0.5 or 2.0 < r <= 5.0: return 'PARTIAL_REPLICATION'
    return 'DATASET_SPECIFIC'
def margin(r):
    return round(min(abs(r - c) for c in (0.2, 0.5, 2.0, 5.0)), 4)

ledger = []
for s in SHAPES:
    old_n = idset_hits[s]; new_n = row_hits[s]
    rec = {'shape': s,
           'old_idset_n': old_n, 'new_row_n': new_n, 'delta_n': new_n - old_n,
           'old_inc_fullprec': round(old_n / DEN, 6), 'new_inc_fullprec': round(new_n / DEN, 6),
           'new_inc_4dp': round(new_n / DEN, 4),
           'osw_exact': osw_exact[s], 'osw_inc_fullprec': round(osw_inc[s], 6)}
    if s == 'E8':
        rec.update({'old_band': 'NOT_MEASURABLE', 'new_band': 'NOT_MEASURABLE', 'band_changed': False,
                    'old_ratio': None, 'new_ratio': None, 'old_margin': None, 'new_margin': None})
    elif s == 'E4':
        rec.update({'old_band': 'MEASURABLE_ONLY(OSW-schema)', 'new_band': 'MEASURABLE_ONLY(OSW-schema)',
                    'band_changed': False, 'old_ratio': None, 'new_ratio': None,
                    'old_margin': None, 'new_margin': None})
    else:
        old_r = osw_inc[s] / (old_n / DEN) if old_n else None
        new_r = osw_inc[s] / (new_n / DEN) if new_n else None
        rec.update({'old_ratio': round(old_r, 6), 'new_ratio': round(new_r, 6),
                    'old_band': band(old_r), 'new_band': band(new_r),
                    'old_margin': margin(old_r), 'new_margin': margin(new_r), 'band_changed': band(old_r) != band(new_r)})
    ledger.append(rec)

# ---- sensitivity: exclude second row of the byte-identical pair ----
sens = {'identical_pair_tids': identical_pair_tids, 'denominator': DEN - 1, 'note': 'exclude-one-row scenario; NOT evidence of independent runs'}
if identical_pair_tids is not None:
    drop_tid = identical_pair_tids[1]
    drop_rec = next(r for r in row_meta if r['tid'] == drop_tid)
    excl_hits = {s: row_hits[s] - (1 if drop_rec['mask'] >> IDX[s] & 1 else 0) for s in SHAPES}
    sens['excluded_row_shapes'] = [SHAPES[b] for b in range(15) if drop_rec['mask'] >> b & 1]
    sens['rows'] = []
    for s in SHAPES:
        if s in ('E4', 'E8'):
            sens['rows'].append({'shape': s, 'new_band': ('MEASURABLE_ONLY(OSW-schema)' if s == 'E4' else 'NOT_MEASURABLE'), 'excl_band': 'unchanged-noncomputable'})
            continue
        n_new = row_hits[s]; n_excl = excl_hits[s]
        r_new = osw_inc[s] / (n_new / DEN) if n_new else None
        r_excl = osw_inc[s] / (n_excl / (DEN - 1)) if n_excl else None
        changed = band(r_new) != band(r_excl) if (r_new and r_excl) else False
        sens['rows'].append({'shape': s, 'row_n': n_new, 'excl_n': n_excl,
                             'row_ratio': round(r_new, 6) if r_new else None,
                             'excl_ratio': round(r_excl, 6) if r_excl else None,
                             'row_band': band(r_new) if r_new else None,
                             'excl_band': band(r_excl) if r_excl else None,
                             'band_changed': changed})

out = {
    'meta': {'stage': 'V0.11-D4-A1R3 trajectory (row) identity session-caliber amendment',
             'prereg_sha256_16': prereg_sha, 'input_parquet_sha256_16': parquet_sha,
             'script_sha256_16': script_sha, 'a1r2_census_sha256_16': sha16(A1R2),
             'row_sequence_sha256_16': seq_h1[:16], 'replay_stable': replay_stable,
             'records': sessions, 'denominator': DEN,
             'unique_session_ids': len(groups),
             'multiplicity_histogram': {str(k): v for k, v in sorted(mult_hist.items())},
             'collision_pairs': len(collided), 'pair_class': pair_class,
             'caliber': 'trajectory-level (row) identity; id-set caliber retained for reconciliation'},
    'gates': gates,
    'gates_all_pass': gates_all,
    'per_shape': {
        s: {'row_sessions': row_hits[s], 'row_incidence_fullprec': round(row_hits[s] / DEN, 6),
            'row_incidence_4dp': round(row_hits[s] / DEN, 4),
            'idset_sessions': idset_hits[s], 'idset_incidence_fullprec': round(idset_hits[s] / DEN, 6),
            'event_hits': event_hits[s], 'delta_row_minus_idset': row_hits[s] - idset_hits[s],
            'pair_shape_both': pair_shape_both[s]}
        for s in SHAPES},
    'bands_full_precision': {L['shape']: {k: v for k, v in L.items() if k != 'shape'} for L in ledger},
    'sensitivity_identical_pair': sens,
    'residual_buckets': resid,
    'cclass_undetected_large': cclass_undetected,
    'allocation': {'labeled_chars': round(labeled, 1), 'qualified_chars': round(qualified, 1),
                   'sum_shape_splits': round(sum(shape_chars.values()), 1),
                   'class_chars': {c: round(v, 1) for c, v in class_chars.items()}},
    'totals': {'events': tot_events, 'obs_chars': round(tot_chars, 1)},
    'verdict': 'A1R3_TRAJECTORY_CENSUS_COMPLETE' if gates_all else 'GATE_FAILURE',
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
print('GATES:', 'ALL PASS' if gates_all else 'FAIL ' + json.dumps({k: v for k, v in gates.items() if not v}))
print('collision pairs:', len(collided), '| pair class:', pair_class, '| identical pair tids:', identical_pair_tids)
print('shape | idset -> row (delta) | old_ratio -> new_ratio | old_band -> new_band | changed')
for L in ledger:
    print(f"  {L['shape']:4s} {L['old_idset_n']:6d} -> {L['new_row_n']:6d} (+{L['delta_n']}) | "
          f"{L['old_ratio']} -> {L['new_ratio']} | {L['old_band']} -> {L['new_band']} | {L['band_changed']}")
print('sensitivity band changes:', [r for r in sens['rows'] if r.get('band_changed')])
print('saved:', OUT)
