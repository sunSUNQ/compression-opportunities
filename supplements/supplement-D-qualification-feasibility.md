# Supplement D — Online qualification feasibility ledger (frozen)

(PAPER-A-POSTFREEZE-EVIDENCE-AUGMENTATION-R1, 2026-10-13)

Source: `data/paper-tables.json`, key `T6_online_qualification_feasibility` (D4-P0 paper evidence freeze; all numbers from frozen artifacts, no recomputation). The main text (§ "Secondary Finding: Offline-to-Online Gap", Table `tab:qualification`) condenses this ledger.

## Detailed rows (verbatim from the frozen ledger)

### D3-E7 simulation detection design

- within-arm noise median |Δ| relative: 0.2796
- B/T pair delta median |Δ|: 0.2379
- mechanism exposure median: 0.00011
- signal-to-noise: 0.0003
- simulation-based detection probability (best per effect size): +3% → 0.622; +5% → 0.699; +10% → 0.856
- permutation p of the observed +7.38% A/B aggregate: 0.1185

### D3-E5 RDS A/B

- pairs: 24
- oracle pass: 24/24
- aggregate relative saving: 0.0738
- non-negative pairs: 13/24
- G2 gate: FAIL

### V0.11-D2 terminal-state

- pairs: 18
- opportunity incidence: 0.0
- aggregate: −0.0805
- verdict: NOT_QUALIFIED

## Reading (frozen)

Within-task stochastic trajectory variance (median 27.96%) exceeds both B/T pair deltas (23.79%) and any hundred-token-scale mechanism exposure (0.011%) — online task-token qualification of such mechanisms is not cost-justifiable at practical sample sizes.

## Boundary

The simulation counts a trial as detected when its estimate has the target direction and an absolute magnitude at least half the injected effect; the frozen resampling pools within-arm noise and is not a significance-test rejection probability.

Note: the main text previously attributed the exact resampling procedure to "Supplement F"; no Supplement F file existed in this supplement set (A: detectors, B: model audit, C: census-factorial, D: this file). Resolved 2026-10-13 (PAPER-A-ARXIV-PREFLIGHT-R1): the main-text pointer now reads "Supplement D", and the exact procedure is recorded below from the frozen fields.

## Exact simulation procedure (frozen fields)

All items below are verbatim frozen fields of `data/figures.json`, key `fig5_power_curve` (D4-P0 paper evidence freeze; no recomputation):

- Measured quantity (frozen `caption` field): "Simulation-based detection probability under our decision criterion (not significance-test rejection probability)".
- Detection rule (main text, § Secondary Finding: Offline-to-Online Gap): a trial counts as detected when its estimate has the target direction and an absolute magnitude at least half the injected effect.
- Target line (frozen `hline_power_target` = 0.8; frozen `threshold_note` field): "0.8 is a descriptive decision-criterion target; legacy hline_power_target is only a frozen field identifier".
- Design: repetitions per arm x ∈ {2, 3, 5, 8, 10}; series = true effect +3%, +5%, +10% (15 frozen points).
- Context (frozen `annotation` field): "within-task stochastic noise median 27.96% relative token swing; mechanism exposure median 0.011%".
- Reading (§8 / T6): under this noise, no replication count ≤10/arm reaches 0.80 detection probability for +3%/+5% effects; +10% reaches 0.856 at 10 repetitions per arm.
