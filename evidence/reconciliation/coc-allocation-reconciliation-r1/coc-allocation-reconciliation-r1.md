# Paper A COC allocation reconciliation R1

## Decision

**Status: PARTIAL.** The historical results are reproducible, and R1 provides deterministic event-level allocation ledgers for the frozen OSW 20K and Qwen 35,334 frames. However, the raw data and frozen detectors do not identify exact byte spans. R1 therefore supports a verifiable event-payload allocation proxy, not exact byte-span allocation, safe deletion, online token savings, or realized task-cost reduction.

## Isolation and scope

- Branch: `codex/paper-a-coc-allocation-reconciliation-r1`
- Base commit: `5e57cf5e62a688cfd43b5762d83b1906e637283c`
- Worktree: `D:\tasco-temp\paper-a-coc-allocation-reconciliation-r1\worktree`
- Unique variable: COC allocation/accounting.
- Frozen inputs preserved: A0 taxonomy, OSW/Qwen raw shards, census artifacts, historical detector implementations, and formal annotation files.
- Excluded: paper edits, detector changes, taxonomy changes, human/LLM annotation, mechanism-level A/B, and formal annotation outputs.

## Historical implementation audit

The paper's event-level wording did not match the historical programs.

| Frame | Historical implementation | Reproduced shipped COC | Reproduced candidate COC | Frozen display |
|---|---|---:|---:|---:|
| OSW Minimax 20K | Whole-trajectory observation characters divided across session-level detected shapes; unsafe shares omitted | 0.391218% | 90.123552% | 0.39% / 90.12% |
| Qwen OpenHands 15K | Each qualifying session has unit mass divided across its session-level shapes; no bytes are read | 1.142333% | 91.272000% | 1.14% / 91.27% |

Thus, 0.39% and 90.12% remain valid only as reproductions of the historical OSW whole-trajectory proxy. The Qwen 1.14%/91.27% values are not byte coverage and were computed only on 15,000 OpenHands trajectories, not the full 35,334 Qwen frame.

## R1 event-level results

The preregistered R1 primary rule uses UTF-8 re-encoded observation payload bytes, splits each event equally across every fired frozen-detector shape, then applies the A0 eligibility and full-fit capability mapping. Exact rational arithmetic is used for corpus aggregates.

| Corpus | Sessions | Parsed events | Labeled events | Qualified allocated bytes | Shipped COC | Shipped + candidate COC | Relative full-fit gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| OSW Minimax manifest v2 | 20,000 | 1,296,519 | 695,780 | 1,393,926,798.1167 | 0.018496% | 95.957692% | 99.980725% |
| Qwen, both scaffolds | 35,334 | 3,936,803 | 1,643,280 | 2,817,958,834.6667 | 0.273375% | 97.673127% | 99.720112% |

For the same Qwen OpenHands 15K frame used historically, event-level COC is 0.053476% shipped and 96.829525% shipped-plus-candidate. The Qwen full-frame value above additionally includes 20,334 SWE-agent trajectories; it must not be presented as a direct replacement without disclosing that scope expansion.

The historical-to-R1 same-frame differences are:

- OSW shipped: −0.372723 percentage points (−95.27% relative); candidate: +5.834140 points (+6.47%).
- Qwen OpenHands 15K shipped: −1.088857 points (−95.32% relative); candidate: +5.557525 points (+6.09%).

The direction is explained by unit and overlap semantics, not altered detectors: sparse shipped shapes receive far less mass when only their actual labeled events are counted, while dominant repeated-delivery shapes receive more candidate mass than under whole-session dilution.

## Overlap control and bounds

- OSW contains 606,397 multi-label events among 695,780 labeled events (87.16%).
- Qwen contains 1,364,876 multi-label events among 1,643,280 labeled events (83.06%).
- Each event's total per-shape allocation equals its payload; ineligible shares are excluded, not reassigned.
- Every event passes `supported allocation ≤ qualified allocation ≤ event payload`.
- Repeated payloads in separate events remain separate opportunity observations.

Exact span union remains `NOT_MEASURABLE`: the detectors return event membership but no byte offsets. Consequently, an event firing E1 and E12 cannot reveal which payload bytes belong to repetition versus diagnostic content. Equal split is a deterministic allocation rule, not a recovered ground-truth span.

## Sensitivity

Across eligible-renormalized, optimistic any-supported, conservative all-supported, code-point-character, and legacy-mapping strategies:

- OSW candidate COC ranges from 94.4684% to 96.4171%; shipped COC ranges from 0% to 0.0465%.
- Qwen full-frame candidate COC ranges from 97.1432% to 97.8008%; shipped COC ranges from 0.0004% to 0.5999%.

The qualitative finding of a large full-fit capability gap is stable, but the exact COC percentages are method-dependent. They should be reported as allocation-proxy estimates with the rule stated.

## Validation

- Unit / Component Regression: **PASS**, 5/5 focused fixtures.
- Historical proxy regression: **PASS** at the frozen four-decimal display precision for all four OSW/Qwen values.
- Input identity closure: **PASS**, OSW 20,000 manifest identities and Qwen 35,334 rows.
- Ledger invariant validation: **PASS**, zero allocation-bound violations.
- Independent ledger aggregation: **PASS**, ledger sums reproduce corpus summaries.
- Determinism replay: **PASS**, all three Parquet outputs plus the main JSON and CSV are byte-identical across two complete runs.

This is not an A/B Evaluation, Stability Validation of model behavior, Canary, or Release qualification.

## Required paper action

The current paper's COC method description and the historical implementation cannot both remain authoritative. For method/implementation consistency, use the R1 event-level proxy values and explicitly label the historical values as superseded provenance. The paper must retain the opportunity-versus-safety boundary and must not convert these percentages into deletable bytes or token savings.

See `affected-paper-claims.md` for exact locations and `summaries/historical-vs-recomputed-diff.json` for machine-readable differences.

## Evidence index

- Frozen method: `coc-method-definition.md`, `method-definition.json`
- Event ledgers: `ledger/osw-event-allocation-ledger.parquet`, `ledger/qwen-event-allocation-ledger.parquet`
- Session ledger: `ledger/session-allocation-summary.parquet`
- Primary summary: `summaries/coc-recalculation-summary.json`
- Shape allocations: `summaries/shape-allocation-summary.csv`
- Same-frame diff: `summaries/historical-vs-recomputed-diff.json`
- Validation gates: `summaries/replay-validation.json`
- Reproduction code and tests: `tools/`, `tests/`
- Provenance and SHA: `validation-execution-manifest.json`
