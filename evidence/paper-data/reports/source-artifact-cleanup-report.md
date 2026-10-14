# Paper Source Artifact Cleanup Report

Date: 2026-10-08
Scope: authority, supersession, figure mapping, BibTeX inventory, preflight, artifact location,
and normalization wording only. No manuscript prose, experiment, detector, census, factorial result,
frozen number, or Supplement A–G was changed or generated.

## Closure ledger

| Requirement | Resolution |
|---|---|
| Model-audit authority | `construct-validity/model-audit/model-audit-report.md`, `model-audit-results.json`, and `full-aggregation.json` are marked superseded/history-only; the sole final authority is `model-audit-reconciled.json` (340 paired-valid items). |
| Qwen authority | `v011-d4a2-qwen-frame-inventory.json` is marked a superseded acquisition snapshot and `v011-d4a2-cross-model.json` an intermediate artifact; both point to `v011-d4a2r1-full-factorial.json`. |
| Figure mapping | `paper-figures-data/figures.json` now has one explicit mapping from manuscript Fig.1–5 and Supp. Fig.6 to file stems and semantic data keys. The two data-only keys are explicitly unmapped. Both PDF and PNG variants exist for all mapped figures. |
| BibTeX | `refs.bib` covers every work currently named or numbered in the manuscript (29 works) plus two corpus records. AgentDiet, Multi-SWE-bench, and SWE-Gym placeholder metadata were repaired. Manuscript hand-number-to-key conversion is intentionally deferred to the manuscript pass. |
| Preflight | `submission-preflight-status.md` no longer treats TeX installation as the sole blocker and lists the current manuscript, metadata, and compile blockers. |
| C0/C1 | Canonical paths are `evidence/V1/v010-c0-stable-task-line-audit.json` at introduction commit `1084893da938362a66f37ef8724ebd06af448d97`, and `evidence/V1/v010-c1-task-level-net-benefit.json` at `6da14a7cf516286f667a4dc35b02d26716f8a620`. The reported `v011-*` names are non-authoritative aliases that do not exist. |
| Normalization | `rq-claim-evidence-matrix.json` now states that Open-SWE E1/E2/E3/E14 use path-aware normalization while Thoughtworks retains original detector caliber; cross-corpus results are descriptive under this difference. |
| Claim trace | C38–C40 now point to the reconciled 340-item model audit and distinguish raw agreement from Cohen's kappa. |
| Historical/outline sources | `paper-draft-v1.md` is explicitly marked superseded; the v2 outline now routes Supplement B/G to reconciled/final authorities. No manuscript prose was rewritten. |

## Canonical figure map

| Paper label | File stem | Frozen data key |
|---|---|---|
| Fig.1 | `fig1_trajectory` | conceptual / none |
| Fig.2 | `fig2_design` | conceptual / none |
| Fig.3 | `fig3_incidence` | `fig1_taxonomy_incidence_tw_vs_osw` |
| Fig.4 | `fig4_e13_interaction` | `fig3_e13_full_factorial_2x2` |
| Fig.5 | `fig5_coverage` | `fig4_coverage_dual_ledger` |
| Supp. Fig.6 | `fig6_power_curve` | `fig5_power_curve` |

Data-only, currently unrendered: `fig2_ae_class_distribution_osw`,
`fig6_rds_replay_capture`.

## Validation gates

- All edited JSON parses successfully.
- Full-repository paper-artifact scan found no conflicting active authority for the six cleanup
  topics; remaining old values occur only inside artifacts now explicitly marked superseded/history-only.
- BibTeX 0.99e parses all 31 unique entries successfully (`BIBTEX_EXIT=0`).
- `git diff --check` passes.
- Frozen experimental result artifacts and frozen numerical values were not edited; changes to Qwen
  inventory/cross-model JSON are additive authority metadata only.
- Current manuscript `paper-draft-v1-icse.{tex,md}`, detector code, census/factorial outputs,
  and Supplements A–G are untouched; changes to the superseded draft and v2 outline are authority-only.

```text
SOURCE_ARTIFACT_CLEANUP = COMPLETE
READY_FOR_MANUSCRIPT_AND_SUPPLEMENTS = YES
```
