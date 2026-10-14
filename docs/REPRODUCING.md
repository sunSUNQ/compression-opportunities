# Reproducing the censuses

## Overview

Every census in the paper is an **offline, deterministic replay** over recorded
trajectories: a Python/Node script reads parquet shards, applies the frozen
E1–E15 detectors, and writes a JSON result. No LLM, no agent, and no network
access is involved. The same input always yields the same output.

## Requirements

- Python 3.10+ with `pyarrow` (`pip install pyarrow`) — for the `.py` tools
- Node.js 18+ — for the `.js` tools
- The two public datasets (see [`DATA-SOURCES.md`](DATA-SOURCES.md)) on local disk

## Important: frozen tools, local paths

The scripts in `tools/` are the **verbatim frozen implementations** that
produced the published numbers (detector freeze `1865a160`; dataset-independence
contract in `taxonomy/taxonomy-registry.json`). Two consequences:

1. **Do not modify detector logic.** The dataset-independence contract requires
   the rules to be applied unchanged. If you need different I/O behavior, write
   a wrapper, not a patch.
2. **The scripts contain hardcoded absolute paths** from the original machine
   (e.g. `D:/tasco-temp/d3_hf_data/...`). Before running, adjust only the
   path constants at the top of each script (`PARQUET`, `DST`, `MF`, `OUT`,
   etc.) to your local data locations. Detector rules live below those
   constants and must stay untouched.

## Data layout expected by the tools

```
<somewhere>/
  agentic-coding-trajectories/   # TW discovery corpus
    sessions.parquet             # 15,000 sessions
  oswe_v10/                      # NVIDIA Open-SWE-Traces v1.0
    data/openhands/minimax_m25/  # parquet shards
    data/sweagent/minimax_m25/
    data/openhands/qwen35_122b/
    data/sweagent/qwen35_122b/
```

## Pipeline (order matters)

| Step | Tool | Consumes | Produces |
|---|---|---|---|
| 0. Candidate discovery (TW 15K) | `tools/opportunity_census.py` | TW `sessions.parquet` | `evidence/census/v011-d3e1-external-census.json` |
| 0b. Natural-opportunity census | `tools/v011_d3_natural_opportunity_census.js` | TW corpus | `evidence/census/v011-d3-natural-opportunity-census.json` |
| 1. E13 decomposition | `tools/v011_d3e2_e13_shape_analysis.py` | TW corpus | `evidence/census/v011-d3e2-e13-shape-analysis.json` |
| 2. Repeat-class census | `tools/v011_d3e3_repeat_class_census.py` | TW corpus | `evidence/census/v011-d3e3-repeat-class-census.json` |
| 3. RDS offline replay | `tools/v011_d3e4_rds_prototype.py` | TW corpus | `evidence/rds/v011-d3e4-rds-prototype-replay.json` |
| 3b. RDS self-test | `tools/v011_d5_rds_js_selftest.js` | — | console |
| 4. External validation (OSW 20K) | `tools/v011_d4a1_census.py` | OSW Minimax strata + `evidence/census/v011-d4a1-oswe-20k-manifest-v2.json` | `evidence/census/v011-d4a1-census-results.json` |
| 4b. TW klear recovery (A1R2) | `tools/v011_d4a1r2_tw_klear_census.py` | TW corpus | `evidence/census/v011-d4a1r2-tw-klear-census.json` |
| 4c. TW trajectory identity (A1R3) | `tools/v011_d4a1r3_tw_trajectory_census.py` | TW corpus | `evidence/census/v011-d4a1r3-tw-trajectory-census.json` |
| 5. Cross-model census | `tools/v011_d4a2_cross_model.py` | OSW Qwen strata | `evidence/census/v011-d4a2-cross-model.json` |
| 6. Full 2×2 factorial | `tools/v011_d4a2r1_full_factorial.py` | OSW Qwen + Minimax strata | `evidence/census/v011-d4a2r1-full-factorial.json` |
| 7. Test-fix negative audit | `tools/v011_d3e6_testfix_negative_audit.py` | frozen A/B pair data | `evidence/rds/v011-d3e6-testfix-negative-audit.json` |
| 8. Power design / simulation | `tools/v011_d3e7_power_design.py` | frozen A/B pair data | `evidence/rds/v011-d3e7-power-design.json` |
| 9. Online A/B analysis | `tools/v011_d5_rds_online_ab_analyzer.js` | session JSONL pairs | `evidence/rds/v011-d5-rds-online-ab.json` |
| 10. Annotation statistics | `tools/annotation_audit_statistics.py` | `annotation-audit/model-audit/*.json` | agreement/κ metrics |
| 11. COC recompute (RQ5) | `evidence/reconciliation/coc-allocation-reconciliation-r1/tools/recalculate_coc.py` | OSW parquet + frozen detector | COC allocation summaries |

Steps 4–6 depend on the OSW parquet shards referenced by the manifest; steps
7–9 replay the frozen online A/B session data (the 24-pair raw table ships in
`evidence/rds/v011-d5-rds-online-ab.json`).

## COC allocation ledgers

The COC allocation reconciliation (`evidence/reconciliation/coc-allocation-reconciliation-r1/`)
ships its method, tools, tests, and summaries. The per-event parquet ledgers
(~125 MB) are not committed; regenerate them with
`tools/build_manifest.py` + `tools/recalculate_coc.py` against the public
datasets, then verify byte identity against
`summaries/replay-artifact-sha.json`.

## Determinism notes

- All census scripts are deterministic: no sampling at runtime, no model calls.
- Sample manifests pin trajectory IDs and SHA-256 hash prefixes
  (e.g. manifest v2 hash `895a96c02eb49434`; TW trajectory census
  `ae954c032022ca79`). Re-running a census against the pinned samples must
  reproduce the stored result byte-for-byte.
- The preregistration documents in `prereg/` were frozen *before* each
  campaign; treat them as the protocol of record for each step above.
