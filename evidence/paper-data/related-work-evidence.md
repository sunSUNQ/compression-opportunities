# Related Work Evidence (D4-P4)

检索日期：2026-09-24/28。检索源：arXiv API（两轮查询：agent+context compression；coding agent+trajectory+empirical）+ 已知系统/benchmark 家族。
检索结果：第一轮 49 条命中（取前 15 评审），第二轮 16 条命中（取前 12 评审）；合计评审 27 条，入选 nearest works 13 篇 + 系统/benchmark 基础设施 4 篇。

## 定位检查结论

**未发现 novelty collision。** 没有任何已发表工作同时做到：natural opportunity taxonomy + 跨 corpus 复现 + 跨 model 稳定性 + 跨 scaffold 对照 + capability-gap 测量。

最接近的两篇 empirical 工作（2609.22114 cost attribution；2608.16370 reacquisition cost）分别在 compression-cost 分解与 reacquisition 行为上与我们部分重叠，但均无 opportunity taxonomy、无跨 corpus/scaffold/model 的机会结构验证、无 capability coverage 映射。两篇 2026 mechanism 工作（AttnCompress、Paritok-4B）为 compressor 设计，不做 opportunity surface 测量。

**无需收紧主 claim**；新增一处对比义务：Related Work 必须明确区分"cost-lever decomposition"（2609.22114）与"opportunity-surface characterization"（本文），并引用其 F1 同族发现（reacquisition/trajectory-amplification）作为独立佐证。

## Nearest-work matrix

| # | Work (arXiv) | Compression mechanism | Natural trajectory characterization | Taxonomy | Cross-corpus | Cross-model | Cross-scaffold | Capability coverage | Main difference from ours |
|---|---|---|---|---|---|---|---|---|---|
| 1 | AttnCompress (2609.08318, ISSTA 2026) | ✓ attention-guided trajectory compression | ✗ (own compression runs only) | ✗ | ✗ | ✗ | ✗ | ✗ | mechanism paper; no opportunity-surface measurement |
| 2 | Paritok-4B (2608.24188) | ✓ extractive intent-conditioned compressor | partial (67,074 OpenHands trajectories as training data) | ✗ | ✗ | ✗ | ✗ | ✗ | trains a compressor; does not characterize opportunity structure |
| 3 | Cost Attribution of Compression Gateways (2609.22114) | ✓ (gateway levers measured) | partial (gateway-level cost decomposition) | ✗ | ✗ | ✗ | ✗ | partial (lever-level savings) | closest empirical work: decomposes cost levers, but no shape taxonomy, no cross-corpus/model/scaffold validation, no capability mapping |
| 4 | What Does Compression Cost an Agent? (2608.16370) | ✗ (measures others' compression) | partial (reacquisition-cost protocol) | ✗ | ✗ | ✓ (3 models) | ✗ | ✗ | measures reacquisition cost of compression; no opportunity taxonomy or coverage mapping |
| 5 | ICLR long-horizon compression (2609.29875) | ✓ (reasoning-block elision) | partial (trajectory amplification analysis) | ✗ | ✗ | ✗ | ✗ | ✗ | mechanism + behavior-drift analysis, not opportunity characterization |
| 6 | ACM agentic context management (2607.23809) | ✓ (lossless offload + on-demand retrieval) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | mechanism/system paper |
| 7 | Harness Design empirical study (2609.20804) | partial (5 context-management strategies compared) | partial (trajectory-level analysis) | ✗ | partial (4 models, SWE-bench+Terminal-Bench) | ✓ | partial (1 harness family) | ✗ | component-level harness ablation; no opportunity taxonomy or capability gap |
| 8 | Failure as a Process (2607.09510) | ✗ | ✓ (3,843 trajectories, process-oriented failure anatomy) | ✓ (failure taxonomy) | ✓ (7 models, 3 scaffolds) | ✓ | ✓ | ✗ | closest methodological relative: large-scale trajectory characterization — but of failures, not compression opportunities |
| 9 | Issue-resolution difficulty (2608.18280, ESEM 2026) | ✗ | ✓ (CoderForge-Preview trajectories, difficulty prediction) | ✓ (difficulty factors) | ✓ (largest open trajectory dataset) | ✗ | ✗ | ✗ | characterizes task difficulty, not compression opportunity |
| 10 | Context rot white-box study (2607.17937) | ✗ | partial (context-length case study) | ✗ | ✗ | ✗ | ✗ | ✗ | bounded failure classification for code auditing |
| 11 | HasMem (2609.30797) | ✓ (softened memory) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | memory-system paper (chat domain) |
| 12 | TRACE (2608.06503) | ✓ (verifier-guided compaction) | partial (behavioral effects) | ✗ | ✗ | ✗ | ✗ | ✗ | mechanism + preliminary behavioral study |
| 13 | Summaries Distort Decisions (2606.29251, EMNLP 2026) | ✓ (LLM compression fidelity) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | information-fidelity framing (finance domain); motivates our preservation-gate requirement |

## Infrastructure / benchmark family (cited as systems, not compared as studies)

| Work | Role in our paper |
|---|---|
| SWE-bench (2310.06770) / SWE-bench Verified | task benchmark family (correctness-oriented; contrast with trajectory benchmark) |
| SWE-agent (2405.15793) | scaffold under study |
| OpenHands (2407.16741) | scaffold under study |
| Multi-SWE-Bench (2504.02605) | multi-language benchmark family |
| SWE-Gym (2412.21139) | executable task environment family |
| Thoughtworks agentic-coding-trajectories | discovery corpus |
| NVIDIA Open-SWE-Traces v1.0 | external validation corpus |

## Claim adjustments forced by literature (recorded)

1. "First large-scale characterization of compression opportunities in coding-agent trajectories" must be softened: 2609.22114 (cost attribution) and 2607.09510 (failure anatomy) are prior large-scale trajectory characterizations in adjacent problem spaces. Accepted wording: *first systematic characterization of the natural compression-opportunity surface with a frozen taxonomy, external replication, and capability-gap quantification*.
2. F1 (offline→online gap) gains independent support: 2609.22114 independently reports that single-shot compression benchmarks "must not be cited as a cost-saving argument" for multi-turn agents — convergent finding, cited as corroboration.
