# Frozen measurement tools

Verbatim copies of the scripts that produced the published census numbers.
Detector logic is **frozen** (dataset-independence contract; A0 freeze commit
`1865a160`) — see [`../docs/REPRODUCING.md`](../docs/REPRODUCING.md) for data
layout and the path-constant adjustment you need before running.

| Script | Stage | Output artifact |
|---|---|---|
| `opportunity_census.py` | D3-E1 candidate discovery on TW 15K | `v011-d3e1-external-census.json` |
| `v011_d3_natural_opportunity_census.js` | D3 natural-opportunity census | `v011-d3-natural-opportunity-census.json` |
| `v011_d3e2_e13_shape_analysis.py` | E13 structural decomposition | `v011-d3e2-e13-shape-analysis.json` |
| `v011_d3e3_repeat_class_census.py` | Repeat-family task-level ledger | `v011-d3e3-repeat-class-census.json` |
| `v011_d3e4_rds_prototype.py` | RDS offline replay (15K) | `v011-d3e4-rds-prototype-replay.json` |
| `v011_d3e6_testfix_negative_audit.py` | Test-fix negative pair attribution | `v011-d3e6-testfix-negative-audit.json` |
| `v011_d3e7_power_design.py` | Variance / power simulation (F1) | `v011-d3e7-power-design.json` |
| `v011_d4a1_census.py` | D4-A1 external validation on OSW 20K | `v011-d4a1-census-results.json` |
| `v011_d4a1r2_tw_klear_census.py` | A1R2 klear recovery re-census (TW) | `v011-d4a1r2-tw-klear-census.json` |
| `v011_d4a1r3_tw_trajectory_census.py` | A1R3 trajectory-identity census (TW) | `v011-d4a1r3-tw-trajectory-census.json` |
| `v011_d4a2_cross_model.py` | D4-A2 cross-model census (Qwen) | `v011-d4a2-cross-model.json` |
| `v011_d4a2r1_full_factorial.py` | D4-A2R1 full 2×2 factorial | `v011-d4a2r1-full-factorial.json` |
| `v011_d5_rds_js_selftest.js` | RDS JS self-test (17 checks) | console |
| `v011_d5_rds_online_ab_analyzer.js` | Online A/B analyzer (24 pairs) | `v011-d5-rds-online-ab.json` |
| `annotation_audit_statistics.py` | Annotation-audit agreement / κ | audit statistics |
