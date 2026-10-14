#!/usr/bin/env python3
"""
PAPER-A-ANNOTATION-STATISTICS-AMENDMENT — locked recomputation of the 340-item
heterogeneous-LLM annotation-audit statistics (A1R3-adjacent; read-only over frozen raw evaluations).

Labels: Q1_shape_membership / Q2_compression_opportunity in {YES, NO, UNCERTAIN}
(exact strings; no recoding). Missing values: none in the paired-valid 340 set
(GLM 48 recovered items are first-class rows). Categories are treated nominally;
Cohen's kappa is the standard unweighted form kappa = (po - pe) / (1 - pe) with
pe = sum_c p_GLM(c) * p_GPT(c).

Outputs evidence/V1/paper/construct-validity/model-audit/annotation-statistics-amendment.json
and asserts consistency with taxonomy-annotation-validity-v1-report.md
(Q1 raw 0.5265 kappa 0.2665; Q2 raw 0.4941 kappa 0.2284) — mismatch exits non-zero.
"""
import json, os, hashlib, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CV = os.path.join(ROOT, 'evidence/V1/paper/construct-validity')
OUT = os.path.join(CV, 'model-audit/annotation-statistics-amendment.json')
CATS = ['YES', 'NO', 'UNCERTAIN']
AUDIT = {'Q1': {'raw': 0.5265, 'kappa': 0.2665}, 'Q2': {'raw': 0.4941, 'kappa': 0.2284}}

def sha16(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]

man = json.load(open(os.path.join(CV, 'sample-manifest.json'), encoding='utf-8'))
glm = json.load(open(os.path.join(CV, 'model-audit/glm53-annotations.json'), encoding='utf-8'))
gpt = json.load(open(os.path.join(CV, 'model-audit/gpt-annotations.json'), encoding='utf-8'))
manifest = {i['item_id']: i for i in man['items']}
gann = {a['item_id']: a for a in glm['annotations']}
pann = {a['item_id']: a for a in gpt['annotations'] if isinstance(gpt, list) or True} if isinstance(gpt, dict) else {a['item_id']: a for a in gpt}
ids = sorted(manifest)
assert set(gann) == set(ids) and set(pann) == set(ids), 'PAIRED-SET MISMATCH'

def kappa(pairs):
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum(ca.get(c, 0) * cb.get(c, 0) for c in CATS) / (n * n)
    return po, pe, ((po - pe) / (1 - pe) if pe < 1 else float('nan'))

def posneg(Q):
    both = [(gann[i][Q], pann[i][Q]) for i in ids]
    ys = [(a, b) for a, b in both if a == 'YES' or b == 'YES']
    ns = [(a, b) for a, b in both if a == 'NO' or b == 'NO']
    pa = sum(1 for a, b in ys if a == b == 'YES')
    na = sum(1 for a, b in ns if a == b == 'NO')
    return {'positive_agreement': {'both_yes': pa, 'denom_either_yes': len(ys), 'value': round(pa / len(ys), 4)} if ys else 'N/A',
            'negative_agreement': {'both_no': na, 'denom_either_no': len(ns), 'value': round(na / len(ns), 4)} if ns else 'N/A'}

stats = {'Q1_shape_membership': {}, 'Q2_compression_opportunity': {}}
for Q in stats:
    pairs = [(gann[i][Q], pann[i][Q]) for i in ids]
    po, pe, k = kappa(pairs)
    cm = Counter(pairs)
    stats[Q] = {
        'n': len(pairs),
        'categories': CATS,
        'observed_agreement': round(po, 6),
        'expected_agreement': round(pe, 6),
        'cohens_kappa_unweighted': round(k, 6),
        'marginals_glm': {c: sum(1 for i in ids if gann[i][Q] == c) for c in CATS},
        'marginals_gpt': {c: sum(1 for i in ids if pann[i][Q] == c) for c in CATS},
        'contingency_3x3': {f'{a}|{b}': cm[(a, b)] for a in CATS for b in CATS if cm[(a, b)]},
        'posneg': posneg(Q),
    }

# ---- detector-unblind (current caliber, full 340) ----
det_pos = [i for i in ids if manifest[i]['sample_type'] == 'detector_positive']
det_neg = [i for i in ids if manifest[i]['sample_type'] == 'detector_negative']
glm_acc = sum(1 for i in det_pos if gann[i]['Q1_shape_membership'] == 'YES')
gpt_acc = sum(1 for i in det_pos if pann[i]['Q1_shape_membership'] == 'YES')
both_reject = sum(1 for i in det_pos if gann[i]['Q1_shape_membership'] != 'YES' and pann[i]['Q1_shape_membership'] != 'YES')
both_accept_neg = sum(1 for i in det_neg if gann[i]['Q1_shape_membership'] == 'YES' and pann[i]['Q1_shape_membership'] == 'YES')
stats['detector_unblind'] = {
    'det_positive': len(det_pos), 'det_negative': len(det_neg),
    'glm_accepts_det_positive': {'n': glm_acc, 'denom': len(det_pos), 'value': round(glm_acc / len(det_pos), 4)},
    'gpt_accepts_det_positive': {'n': gpt_acc, 'denom': len(det_pos), 'value': round(gpt_acc / len(det_pos), 4)},
    'both_reject_det_positive_q1_not_yes': both_reject,
    'both_accept_det_negative_q1_yes': both_accept_neg,
}

# ---- per-shape ----
per_shape = {}
by_shape = defaultdict(list)
for i in ids:
    by_shape[manifest[i]['target_shape']].append(i)
for sh, items in sorted(by_shape.items()):
    rec = {'n': len(items)}
    for Q in ('Q1_shape_membership', 'Q2_compression_opportunity'):
        pairs = [(gann[i][Q], pann[i][Q]) for i in items]
        po, pe, k = kappa(pairs)
        degenerate = (len(set(a for a, _ in pairs)) < 2) or (len(set(b for _, b in pairs)) < 2) or len(items) < 8
        rec[Q] = {'agree': sum(1 for a, b in pairs if a == b), 'raw': round(po, 4),
                  'kappa': 'N/A(degenerate)' if degenerate else round(k, 4)}
    per_shape[sh] = rec

out = {
    'schema_version': 1,
    'stage': 'PAPER-A-ANNOTATION-STATISTICS-AMENDMENT — locked recomputation of the 340-item heterogeneous-LLM annotation audit',
    'date': '2026-10-10',
    'label_semantics': {'categories': CATS, 'treatment': 'nominal; standard unweighted Cohen kappa; no recoding; UNCERTAIN is a first-class category'},
    'missing_values': 'none in the paired-valid 340 set (GLM 48 recovered items are first-class rows)',
    'superseded_values': {'q1_kappa_published': 0.1531, 'q2_kappa_published': 0.0003,
                          'status': 'UNREPRODUCIBLE under standard conventions (see taxonomy-annotation-validity-v1-report.md section 2.2); computation convention not archived; superseded-for-publication by this file'},
    'inputs': {'manifest_sha256_16': sha16(os.path.join(CV, 'sample-manifest.json')),
               'glm_sha256_16': sha16(os.path.join(CV, 'model-audit/glm53-annotations.json')),
               'gpt_sha256_16': sha16(os.path.join(CV, 'model-audit/gpt-annotations.json')),
               'reconciled_sha256_16': sha16(os.path.join(CV, 'model-audit/model-audit-reconciled.json'))},
    'statistics': stats,
    'per_shape': per_shape,
}
# ---- V1-audit consistency assertions (STOP on mismatch) ----
ok = (abs(stats['Q1_shape_membership']['observed_agreement'] - AUDIT['Q1']['raw']) < 5e-5 and
      abs(stats['Q1_shape_membership']['cohens_kappa_unweighted'] - AUDIT['Q1']['kappa']) < 5e-5 and
      abs(stats['Q2_compression_opportunity']['observed_agreement'] - AUDIT['Q2']['raw']) < 5e-5 and
      abs(stats['Q2_compression_opportunity']['cohens_kappa_unweighted'] - AUDIT['Q2']['kappa']) < 5e-5 and
      stats['detector_unblind']['glm_accepts_det_positive']['n'] == 84 and
      stats['detector_unblind']['gpt_accepts_det_positive']['n'] == 53 and
      stats['detector_unblind']['both_reject_det_positive_q1_not_yes'] == 117 and
      stats['detector_unblind']['both_accept_det_negative_q1_yes'] == 0)
out['v1_audit_consistency'] = {'expected': AUDIT, 'pass': ok}
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
if not ok:
    print('STOP: recomputation does not match the V1 audit expectations')
    sys.exit(2)
print('LOCKED:', OUT)
print('Q1: raw', stats['Q1_shape_membership']['observed_agreement'], 'kappa', stats['Q1_shape_membership']['cohens_kappa_unweighted'])
print('Q2: raw', stats['Q2_compression_opportunity']['observed_agreement'], 'kappa', stats['Q2_compression_opportunity']['cohens_kappa_unweighted'])
print('detector-unblind:', json.dumps(stats['detector_unblind']))
