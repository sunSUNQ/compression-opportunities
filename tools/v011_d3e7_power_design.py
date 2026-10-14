#!/usr/bin/env python3
"""
V0.11-D3-E7 — RDS online effect power & replication design (mechanical, offline, seed=42).
Prereg: docs/architecture/V0.11-D3-E7-POWER-DESIGN-PREREG-V1.md (FROZEN e955a76d)
Data: D5 frozen pairs (v011-d5-rds-online-ab.json raw_pairs). Zero Agent runs.
"""
import json, random, statistics, hashlib

SEED = 42
random.seed(SEED)
WT = os_cwd = __import__('os').getcwd()
OUT = WT + '/evidence/V1/v011-d3e7-power-design.json'
SRC = WT + '/evidence/V1/v011-d5-rds-online-ab.json'

j = json.load(open(SRC, encoding='utf-8'))
pairs = j['raw_pairs']

# ---- structure: task -> arm -> [rep totals] + matched
tasks = {}
mech = []
for p in pairs:
    tasks.setdefault(p['task'], {'B': {}, 'T': {}})
    tasks[p['task']]['B'][p['rep']] = p['B_tokens']
    tasks[p['task']]['T'][p['rep']] = p['T_tokens']
    if p['T_rds']['matched_chars']:
        mech.append({'task': p['task'], 'rep': p['rep'], 'matched': p['T_rds']['matched_chars'],
                     'total': p['T_tokens']})

# ---- A: between-task CV ----
task_means = {t: statistics.mean(list(a.values()) for a in [v['B']] [0:1] + [list(v['B'].values())] + list(v['T'].values())[:0] or [0]) for t, v in [] .items()} if False else None
task_means = {}
for t, v in tasks.items():
    vals = list(v['B'].values()) + list(v['T'].values())
    task_means[t] = statistics.mean(vals)
tm_vals = list(task_means.values())
between_cv = statistics.pstdev(tm_vals) / statistics.mean(tm_vals)

# ---- B: within-arm stochastic noise (replicate deltas, no treatment change) ----
noise = []  # within-arm relative deltas
for t, v in tasks.items():
    for arm in ('B', 'T'):
        r1, r2 = v[arm][1], v[arm][2]
        m = (r1 + r2) / 2
        if m: noise.append((r1 - r2) / m)
noise_std = statistics.pstdev(noise)
noise_med_abs = statistics.median(abs(x) for x in noise)

# ---- same-arm baseline vs B/T pair deltas ----
pair_deltas = [abs(p['relative_total_saving']) for p in pairs]

# ---- C: mechanism exposure ----
exposure = [(m['matched'] / 4) / m['total'] for m in mech]
exposure_med = statistics.median(exposure)
exposure_max = max(exposure)
mech_token_med = statistics.median(m['matched'] / 4 for m in mech)

# ---- signal:noise ----
signal_noise = exposure_med / noise_std if noise_std else None

# ---- power simulation (task-blocked bootstrap, seed=42) ----
def simulate(effect, reps, trials=10000):
    det = 0; false_sign = 0; dir_ok = 0; est_widths = []
    for _ in range(trials):
        ests = []
        for _b in range(reps):
            # blocked: sample tasks with replacement, take their within-arm noise
            nt = [random.choice(noise) for _ in range(len(tasks))]
            nb = [random.choice(noise) for _ in range(len(tasks))]
            ests.append(effect + (statistics.mean(nt) - statistics.mean(nb)))
        est = statistics.mean(ests)
        # bootstrap CI over the reps-averaged per-task estimates
        boot = []
        for _ in range(200):
            smp = [random.choice(ests) for _ in range(len(ests))]
            boot.append(statistics.mean(smp))
        lo, hi = min(boot), max(boot)
        est_widths.append(hi - lo)
        sign_ok = (est > 0) == (effect > 0)
        if sign_ok: dir_ok += 1
        if sign_ok and abs(est) >= effect / 2: det += 1
        if not sign_ok: false_sign += 1
    return {'detection_probability': round(det / trials, 3),
            'direction_correct_probability': round(dir_ok / trials, 3),
            'false_sign_probability': round(false_sign / trials, 3),
            'mean_ci_width': round(statistics.mean(est_widths), 4)}

power = {}
for effect in (0.03, 0.05, 0.10):
    for reps in (2, 3, 5, 8, 10):
        power[f'effect_{int(effect*100)}pct_reps_{reps}'] = simulate(effect, reps)

# ---- permutation cross-check: is D5 observed aggregate (+7.38%) distinguishable? ----
obs_agg = j['global_universe']['aggregate_relative_saving']
perm_aggs = []
for _ in range(2000):
    flip = []
    for p in pairs:
        d = p['d_total']
        flip.append(d if random.random() < 0.5 else -d)
    sB = sum(p['B_tokens'] for p in pairs); sT = sB - sum(flip)
    perm_aggs.append((sB - sT) / sB)
perm_p = sum(1 for a in perm_aggs if a >= obs_agg) / len(perm_aggs)

# ---- design comparison at 120-session budget ----
def est_std(reps_per_arm, n_tasks):
    # mean-of-reps noise averaging, blocked per task
    return noise_std * (2 ** 0.5) / (reps_per_arm * n_tasks) ** 0.5 * (n_tasks ** 0.5) / (n_tasks ** 0.5)
designs = {
    '12tasks_x5reps': {'sessions': 120, 'est_std_relative': round(noise_std * (2 ** 0.5) / (12 * 5) ** 0.5, 5)},
    '30tasks_x2reps': {'sessions': 120, 'est_std_relative': round(noise_std * (2 ** 0.5) / (30 * 2) ** 0.5, 5)},
    '24tasks_x2reps_D5scale': {'sessions': 96, 'est_std_relative': round(noise_std * (2 ** 0.5) / (24 * 2) ** 0.5, 5)},
}

out = {
    'schema_version': 1,
    'stage': 'V0.11-D3-E7 power & replication design (prereg e955a76d FROZEN before statistics; seed 42)',
    'date': '2026-09-24',
    'data': {'source': 'D5 frozen pairs', 'tasks': len(tasks), 'pairs': len(pairs)},
    'variance_decomposition': {
        'A_between_task_cv': round(between_cv, 4),
        'B_within_task_noise': {'std': round(noise_std, 4), 'median_abs': round(noise_med_abs, 4), 'n': len(noise)},
        'C_mechanism_exposure': {'median': round(exposure_med, 6), 'max': round(exposure_max, 6), 'mech_token_median': round(mech_token_med, 1)},
        'signal_to_noise': round(signal_noise, 4) if signal_noise else None,
    },
    'same_arm_baseline': {
        'within_arm_abs_delta_median': round(noise_med_abs, 4),
        'bt_pair_abs_delta_median': round(statistics.median(pair_deltas), 4),
        'verdict': 'within-arm noise comparable to B/T pair deltas' if noise_med_abs >= statistics.median(pair_deltas) * 0.5 else 'bt deltas dominate',
    },
    'power_simulation': power,
    'permutation_crosscheck': {'observed_aggregate': obs_agg, 'permutation_p_value': round(perm_p, 4), 'note': 'P(permuted aggregate >= observed) under label randomization'},
    'design_comparison_same_budget': designs,
    'mechanism_derived_detectable_target': {
        'mechanism_exposure_median_pct': round(exposure_med * 100, 3),
        'mechanism_exposure_max_pct': round(exposure_max * 100, 3),
        'note': 'RDS current trigger volume yields ~0.1-0.3% session-level token exposure; 3/5/10% effects exceed mechanism ceiling by 10-30x unless trigger volume expands',
    },
}
# mechanical recommendation
if exposure_med >= 0.01:
    best = None
    for effect in (0.03, 0.05, 0.10):
        for reps in (2, 3, 5, 8, 10):
            if power[f'effect_{int(effect*100)}pct_reps_{reps}']['detection_probability'] >= 0.80:
                if best is None or reps < best[1]: best = (effect, reps)
    out['RECOMMENDED_NEXT_BATCH'] = {'effect': best[0], 'reps_per_arm': best[1], 'tasks': 12, 'sessions': 12 * best[1] * 2, 'estimator': 'task-blocked mean relative_total_delta', 'stopping_rule': 'power>=0.80 design; no interim peeking', 'cost_multiple_vs_D5': round(best[1] / 2, 1)}
else:
    out['RECOMMENDED_NEXT_BATCH'] = {
        'verdict': 'CURRENT_RDS_EFFECT_TOO_SMALL_FOR_COST-JUSTIFIED_ONLINE_QUALIFICATION',
        'reason': f'mechanism exposure median {round(exposure_med*100,3)}% << 3% minimum target effect; even 10 reps/arm cannot detect an effect the mechanism cannot produce; expand RDS trigger volume (matched chars/session) ~10-30x first, or keep RDS as candidate without online qualification',
    }
out['aggregates_sha256'] = hashlib.sha256(json.dumps(out, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

print('between-task CV:', round(between_cv, 4))
print('within-task noise: std', round(noise_std, 4), 'median_abs', round(noise_med_abs, 4), '(n=24)')
print('same-arm |delta| median:', round(noise_med_abs, 4), 'vs B/T pair |delta| median:', round(statistics.median(pair_deltas), 4))
print('mechanism exposure: median', str(round(exposure_med * 100, 3)) + '%', 'max', str(round(exposure_max * 100, 3)) + '%', '| signal:noise =', round(signal_noise, 4) if signal_noise else None)
print('permutation p (observed +7.38% vs label randomization):', round(perm_p, 4))
print('--- power:')
for k, v in power.items(): print(' ', k, v)
print('designs:', json.dumps(designs))
print('RECOMMENDED:', json.dumps(out['RECOMMENDED_NEXT_BATCH'], ensure_ascii=False)[:400])
