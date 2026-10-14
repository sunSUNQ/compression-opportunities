# What Is Actually Compressible? — Artifact Repository

Artifact repository for the paper **"What Is Actually Compressible? An Empirical Study of Context Compression Opportunities in Coding-Agent Trajectories"** (Qing Sun, 2026).

This repository publishes the frozen measurement instrument, deterministic detectors, census tools, evidence pack, annotation-audit data, figures, and the paper itself, so that every number in the paper can be traced to a mechanical artifact.

## Paper

Coding agents accumulate repeated and structurally redundant context: tool outputs, file contents, diagnostics, and command results re-enter the conversation as the agent iterates. This work asks a measurement question that precedes mechanism design: **what does the workload actually contain?** We derive a 15-shape compression-opportunity taxonomy with deterministic, frozen detectors and apply it across two independent public corpora (35,000 trajectories), across two backbone models, and across two agent scaffolds.

- **Paper PDF**: [`paper/Paper_A.pdf`](paper/Paper_A.pdf) (LaTeX source in [`paper/`](paper/))

### Findings at a glance

| RQ | Question | Result |
|---|---|---|
| RQ1 | Prevalence | Opportunities are common: large diagnostics in 72.9% (TW) / 79.5% (OSW) of sessions; late-trajectory large outputs 58.7% / 46.6%; same-file rereads 82.0% / ~100% |
| RQ2 | Cross-corpus replication | 8 of 13 measurable shapes satisfy the pre-specified descriptive replication criterion (REPLICATED or PARTIAL) — all six core shapes with incidence ratios 0.79–1.28; the five sparse shapes are DATASET_SPECIFIC |
| RQ3 | Cross-model stability | All six core shapes persist across Minimax-M2.5 and Qwen3.5-122B within both scaffolds (ratios 0.68–1.013) |
| RQ4 | Scaffold modulation | E13 incidence is strongly scaffold-modulated: mean scaffold-associated variation 28.2 pp vs. model-associated 12.7 pp; difference-in-differences interaction 16.5 pp |
| RQ5 | Capability coverage | In the evaluated system, shipped mechanisms cover SOC 2.07% / event-payload COC 0.018%; a reversible research candidate reaches SOC 100% / COC 95.96% — a 99.98% relative allocation gap |
| F1 | Offline vs. online | A 24-pair online A/B was correctness-clean but its aggregate effect is indistinguishable from trajectory noise (within-task median swing 27.96% vs. mechanism exposure median 0.011%) |

## Datasets

Both corpora are public on Hugging Face; this repository does not redistribute them.

| Corpus | Trajectories | Role | Link |
|---|---:|---|---|
| Thoughtworks agentic-coding-trajectories | 15,000 | discovery | [thoughtworks/agentic-coding-trajectories](https://huggingface.co/datasets/thoughtworks/agentic-coding-trajectories) |
| NVIDIA Open-SWE-Traces v1.0 (OpenHands/SWE-agent × Minimax-M2.5) | 20,000 | external validation + scaffold contrast | [nvidia/Open-SWE-Traces](https://huggingface.co/datasets/nvidia/Open-SWE-Traces) |
| NVIDIA Open-SWE-Traces v1.0 (OpenHands/SWE-agent × Qwen3.5-122B) | 35,334 | model contrast + 2×2 factorial | [nvidia/Open-SWE-Traces](https://huggingface.co/datasets/nvidia/Open-SWE-Traces) |

Each census pins the exact sample it used (see `evidence/census/*manifest*.json` and `*frame-report*.json`).

## Taxonomy

Fifteen mechanically detectable opportunity shapes (E1–E15), frozen before any external use under a dataset-independence contract. Full registry with definitions, detector rules, capability mapping, and A–E classes:

- [`taxonomy/taxonomy-registry.json`](taxonomy/taxonomy-registry.json)
- Human-readable detector specifications: [`supplements/supplement-A-detectors.md`](supplements/supplement-A-detectors.md)

| ID | Shape | ID | Shape |
|---|---|---|---|
| E1 | repeated exact command | E9 | large build output |
| E2 | repeated similar command | E10 | repeated validation |
| E3 | same-file reread | E11 | unchanged validation |
| E4 | overlapping file read | E12 | large diagnostic |
| E5 | same search | E13 | late-trajectory large output |
| E6 | large test success | E14 | output followed by reread |
| E7 | large test failure | E15 | output followed by rederivation |
| E8 | large lint output | | |

## Repository map

```
paper/            Paper PDF, LaTeX source, bibliography, arXiv figure set
taxonomy/         Frozen E1-E15 taxonomy & capability-mapping registry
tools/            Frozen census / replay / audit scripts (detectors unmodified)
prereg/           Pre-registrations frozen before each campaign
evidence/
  census/         Discovery, external-validation, cross-model, factorial census results + manifests
  rds/            RDS candidate: offline replay, online A/B, variance audit, power design, freeze
  reconciliation/ Post-census reconciliations (detector cross-corpus; COC allocation)
  campaign-reports/  Per-campaign evidence reports (D3/D4 lines)
  paper-data/     Paper tables, figure data, claim trace, RQ-evidence matrix, limitations
annotation-audit/ 340-item two-arm audit + 120-item x 3-evaluator formal annotation
supplements/      Supplements A-D (self-contained; sources/ holds referenced artifacts)
figures/          Final figure set (PDF + PNG)
docs/             Reproduction guide and data-source notes
```

## Reproducing

The censuses are offline, deterministic analyses of recorded trajectories — no agent or model is invoked anywhere in the measurement pipeline. See [`docs/REPRODUCING.md`](docs/REPRODUCING.md) for setup, data layout, and per-script commands.

## Annotation audits

Two audits diagnose interpretation sensitivity of the frozen definitions (neither is human ground truth nor a detector-precision estimate; the frozen detectors define the census instrument):

- **340-item two-arm audit** (blinded, stratified): Q1 raw agreement 52.65% (κ=0.2665), Q2 49.41% (κ=0.2284); E13 Q1 96.4% (κ=0.9146). Data in [`annotation-audit/`](annotation-audit/), narrative in [Supplement B](supplements/supplement-B-model-audit.md).
- **120-item × 3-evaluator formal annotation** (three isolated Agent CLI evaluators): 317/360 valid cells; on the 98 tri-channel-complete samples, Q1 three-way exact agreement 85.71% (Fleiss κ=0.80), Q2b information preservation 94.90% (κ=0.80), Q2a structural redundancy 80.61% (κ=0.38). Data in [`annotation-audit/multi-agent-annotation/`](annotation-audit/multi-agent-annotation/).

## Provenance and integrity

- All JSON evidence files are verbatim frozen artifacts (no post-hoc edits). Where a number was superseded by a later reconciliation, both the superseded and reconciled artifacts are included (e.g., `evidence/paper-data/paper-tables.pre-a1r*.json`, `evidence/reconciliation/`).
- The paper's authoritative evidence chain is indexed in [`evidence/paper-data/authoritative-evidence-index.json`](evidence/paper-data/authoritative-evidence-index.json) with SHA-256 hashes of the source artifacts.
- Tool scripts in `tools/` and `evidence/reconciliation/*/tools/` contain hardcoded local data paths from the original runs; detector logic is frozen and unmodified — see [`docs/REPRODUCING.md`](docs/REPRODUCING.md) before running them elsewhere.

## License

To be decided. Dataset content is governed by the upstream datasets' licenses (see [`docs/DATA-SOURCES.md`](docs/DATA-SOURCES.md)).

## Citation

```bibtex
@misc{sun2026compressible,
  title  = {What Is Actually Compressible? An Empirical Study of Context Compression Opportunities in Coding-Agent Trajectories},
  author = {Qing Sun},
  year   = {2026},
  note   = {Preprint. Artifact repository: \url{https://github.com/sunSUNQ/compression-opportunities}}
}
```

If you use the upstream corpora, please also cite the original dataset publications.
