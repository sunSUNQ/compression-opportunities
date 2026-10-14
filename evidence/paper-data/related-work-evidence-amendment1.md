# Related Work Evidence — Amendment 1 (D4-P4R1, 2026-09-24)

外部检索轮（用户提供的 2024–2026 检索，重点：coding-agent context compression、trajectory reduction、scaffold/harness study、evaluation variance）。本 amendment 新增 14 篇近邻工作；**AgentDiet (FSE/PACMSE 2026) 为最高风险近邻**，触发 positioning 重写。

## 新增近邻工作

| # | Work | Venue | 已做 | 与本文重叠 | 本文区别 | 风险 |
|---|---|---|---|---|---|---|
| N1 | **AgentDiet — Reducing Cost of LLM Agents with Trajectory Reduction** | FSE/PACMSE 2026 | 人工分析 100 条 Trae Agent trajectory；归纳 useless/redundant/expired 三类 waste；AgentDiet 系统 2 LLM × 2 benchmark 验证 | **直接研究 trajectory 中可删/可压缩 waste**；示例与本文 taxonomy 接近（str_replace_editor redundancy、verbose test output、过期 file/search info） | 3 个高层定性 waste 类 vs 本文 15-shape deterministic frozen detector taxonomy + 跨 corpus 复现 + 2×2 scaffold/model 分析 + capability coverage ledger；AgentDiet 单 agent/100 trajectories 且仅实现于 Trae Agent | **最高** |
| N2 | The Complexity Trap | NeurIPS 2025 workshop (DL4Code) | SWE-agent + SWE-bench Verified 上比较 masking 与 LLM summarization；5 model configs；OpenHands generality probe；发现 summarization 拉长 trajectory | context management 策略效果比较、多模型 | 比较 compression strategies 的效果，非枚举自然 opportunity；OpenHands 为 generality probe 非完整 2×2 | 高 |
| N3 | Process-Centric Analysis of Agentic Software Systems | OOPSLA 2026 | Graphectory；4,000 trajectories；SWE-agent + OpenHands；4 backbone LLM；重复/backtracking/复杂度/成功失败过程分析 | trajectory characterization、双 scaffold、多 model、重复/低效行为 | 研究 agent process quality/behavior，非 compression opportunity taxonomy，无 opportunity coverage | 高（互补） |
| N4 | Harness Design empirical study | arXiv 2609.20804 | 4 models；SWE-Bench Verified + Terminal-Bench 2.1；176 matched settings；planning/action-space/context-management 变量 | harness/scaffold 改变行为与 context management（与 RQ4 近） | 研究 harness 组件对性能/效率；本文研究 frozen opportunity incidence 的 controlled factorial contrast | 高（必须引用） |
| N5 | Understanding Software Engineering Agents | ASE 2025 | 3 agents、120 trajectories、2,822 interactions；action patterns、token usage、behavioral motifs/anti-patterns | empirical trajectory study、recurring action sequences | 规模较小、目标为 reasoning/behavior 理解，非 compressibility | 中高 |
| N6 | Dissecting Model Behavior through Agent Trajectories | 2026 | SSA 上 138K trajectories、多 model families；code state-space 行为差异分析 | trajectory 数量更大、cross-model behavior analysis | 单一 harness、非 compression-specific、无 cross-scaffold opportunity replication | 中高 |
| N7 | Agent Trajectories as Programs | 2026 | 10 agents、程序化 representation/fingerprint | trajectory structural patterns 可比较表示 | 目标为 agent fingerprinting，非 context waste/compression | 中 |
| N8 | SWE-Pruner | 2026 | task-aware code context pruning；4 benchmarks；23–54% token 减少 | coding-agent compression | relevance-selected code/context pruning（how to prune）；无自然 opportunity characterization | Paper B 强邻居 / Paper A 中 |
| N9 | TACO | 2026 | 自演化 terminal-observation compression rules；跨 benchmark/scaffold | 根据 trajectory/observation 特征动态压缩 | self-evolving compression mechanism；非 frozen opportunity measurement | Paper B 高 |
| N10 | CORVUS | 2026 | 改变 trajectory 架构：file reads 指向同步 registry，避免 stale snapshot 与重复 reread | 本文 E3/E14 repeated read/reread 机会直接相关 | 专解 file-state synchronization；无完整 opportunity space characterization | Paper B 高 / Paper A 要引用 |
| N11 | Squeez | 2026 | 11,477 tool-output pruning examples + 618 人工 test set；tool output 最小 verbatim evidence | E12/E13 邻近 | 单个 tool output 内 evidence 保留；不刻画自然 trajectory opportunity 分布 | E13 后续强邻居 |
| N12 | ACON | ICML 2026 | observations + interaction history 压缩；26–54% peak-token 减少 | general agent context compression | 非 coding-agent trajectory measurement | 中 |
| N13 | ReSum / AgentFold | 2025 | Web agents periodic summarization / proactive folding | context history compression 背景 | Web search agent | 背景 |
| N14 | On Randomness in Agentic Evals | 2026 | 60K SWE-Bench trajectories、3 models × 2 scaffolds；证明 repeated runs 显著 variance；建议 multiple runs + power analysis | 与本文 F1（trajectory variance / power）直接呼应 | 研究 benchmark stochasticity，非 compression | **必须引用（F1 外部佐证）** |

## Positioning 修正（由 N1 触发）

**禁用 claims**（会被 N1/N3/N4/N6 反驳）：
1. ~~"We are the first to identify waste in coding-agent trajectories"~~
2. ~~"We are the first to study coding-agent trajectories across models and scaffolds"~~
3. ~~"Prior work only studies how to compress and does not study what is compressible"~~

**Novelty 锁定句**（正文采用）：
> We provide a systematic and reproducible measurement of naturally occurring context-compression opportunities in coding-agent trajectories, moving beyond prior qualitative waste analyses and compression-mechanism evaluations through a fine-grained detector-backed taxonomy, cross-corpus replication, controlled model×scaffold validation, and opportunity-to-capability coverage analysis.

**RQ4 收窄**：
- 禁用：~~"We disentangle model and scaffold effects on coding-agent behavior"~~（N3/N4/N6 已在 general behavior 层面做过）
- 采用：*"We disentangle model- and scaffold-associated variation specifically in the incidence of empirically defined compression-opportunity shapes."*
- RQ4 不写 "首次发现 agent scaffold matters"（SWE-agent 的 ACI 设计已证明 interface 影响 agent 行为）；采用 "quantifying scaffold-associated modulation of specific compression-opportunity incidence under a controlled model×scaffold design"

**RQ4 补充引用义务**：SWE-agent 的 ACI 设计论文（interface design 影响 agent 行为）+ N3 Process-Centric + N4 Harness Design。

## F1 外部佐证（N14）

On Randomness in Agentic Evals（60K SWE-Bench trajectories、3 models × 2 scaffolds）独立证明 single-run agent evaluation 存在显著 stochastic variance 并推荐 multiple runs + power analysis——与本文 F1 的 within-task 27.96% 波动及 power-design 方法**收敛**。F1 据此升级为 methodological finding（compression-mechanism evaluation 在稀疏激活机制下对 trajectory variance 特别脆弱；offline opportunity incidence 与 online effect size 需分开测量）。

## Taxonomy 命名纪律

正文必须使用完整名称：**Compression Opportunity Taxonomy** 或 **Fine-grained Taxonomy of Naturally Occurring Context-Compression Opportunities**——不得简写为 "trajectory taxonomy"。
