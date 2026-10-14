# Submission Preflight Status 鈥?Current Authority

Status date: 2026-10-08
SUPERSEDED 2026-10-09 by final-submission-preflight-report.md (PAPER-LAYOUT-PREFLIGHT pass; all six active blockers below were resolved). Retained for provenance only.

Authority: supersedes the D4-P5R2 鈥淭eX is the sole blocker鈥?ledger.

## Evidence and source-artifact state

| Item | State |
|---|---|
| Frozen evidence numbers | FROZEN; unchanged by source cleanup |
| Evidence authority | RECONCILED |
| Source artifact cleanup | COMPLETE |
| TW/OSW normalization | Different calibers documented; descriptive cross-corpus comparison only |
| Model audit | `model-audit-reconciled.json` is the sole numerical authority |
| Qwen frame | `v011-d4a2r1-full-factorial.json` is final authority |
| Figure mapping | Explicit and unique in `paper-figures-data/figures.json` |
| C0/C1 | Canonical `v010-*` artifacts and introduction commits recorded |
| BibTeX inventory | Closed for the 29 works cited/named in the current manuscript, plus 2 corpus records |

## Compilation state

MiKTeX is installed and `pdflatex`/`xelatex` are available. A PDF exists and is six pages,
but compilation availability is no longer evidence of submission readiness.

## Active blockers before submission

1. Manuscript still uses hand-written citation numbers and has `\\bibliography{refs}` commented;
   the current PDF therefore has no References section.
2. `findingbox` is undefined and `sec:f1` is an undefined reference.
3. Table 2 overflows its column.
4. Figure descriptions, keywords, and CCS metadata are incomplete.
5. ACM conference metadata still contains the `Conference '17` placeholder.
6. The revised manuscript and eventual Supplement A鈥揋 require a fresh compile and visual audit.

```text
SOURCE_ARTIFACT_CLEANUP          COMPLETE
READY_FOR_MANUSCRIPT_WORK       YES
SUBMISSION_PREFLIGHT            PENDING
SOLE_BLOCKER_TEX_INSTALLATION   FALSE
```

No claim of submission readiness is made by this ledger.
