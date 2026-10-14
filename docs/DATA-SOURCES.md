# Data sources and licensing

## Upstream corpora

### 1. Thoughtworks agentic-coding-trajectories (discovery corpus)

- Link: <https://huggingface.co/datasets/thoughtworks/agentic-coding-trajectories>
- Used as: 15,000 recorded trajectories / 13,053 unique session identifiers (discovery + all TW-side censuses)
- Content: multi-turn agentic-coding sessions drawn from three public upstream
  datasets (Nebius SWE-rebench OpenHands, SWE-bench SWE-smith trajectories,
  Kwaipilot Klear-SWE-Smith-Mini), normalized and tokenized
- License: derivative dataset — each row governed by its `source_dataset`
  license; see the dataset card

### 2. NVIDIA Open-SWE-Traces v1.0 (external validation, model contrast, factorial)

- Link: <https://huggingface.co/datasets/nvidia/Open-SWE-Traces>
- Used as:
  - OpenHands × Minimax-M2.5: 10,000 trajectories
  - SWE-agent × Minimax-M2.5: 10,000 trajectories
  - OpenHands × Qwen3.5-122B: 15,000 trajectories (6/17 shards, ordinal selection fixed before analysis)
  - SWE-agent × Qwen3.5-122B: 20,334 trajectories (9/9 shards)
- License: CC BY 4.0 per the dataset card
- Task sources: Scale-SWE, SWE-rebench-V2 (permissively licensed upstreams)

## Scaffolds and models referenced

- [OpenHands](https://github.com/All-Hands-AI/OpenHands) — agent scaffold
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) — agent scaffold
- Backbone models as recorded by the dataset authors: Minimax-M2.5, Qwen3.5-122B

## What this repository contains vs. redistributes

This repository contains **derived, aggregate artifacts only**:

- census results (per-shape incidence, payload statistics, coverage ledgers)
- annotation-audit records (detector-classified observation snippets drawn from
  the public corpora, plus blinded annotations)
- figures and figure data

It does **not** redistribute trajectory content at corpus scale. To reconstruct
the full analysis, download the two public corpora and follow
[`REPRODUCING.md`](REPRODUCING.md).

## Annotation-audit data

The annotation records in `annotation-audit/` quote short observation snippets
from the Open-SWE-Traces corpus (public, CC BY 4.0) for annotation purposes;
upstream terms apply.
