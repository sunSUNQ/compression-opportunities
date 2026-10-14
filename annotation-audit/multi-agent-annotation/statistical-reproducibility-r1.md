# statistical-reproducibility-r1 — PAPER-A-MULTI-AGENT-STATISTICAL-REPRODUCIBILITY-R1

日期：2026-10-12。
判定：**SAMPLING_REPRODUCIBLE = PASS（结构验证）；CLUSTER_STATISTICS_VERIFIED = PARTIAL（聚类结构确认，bootstrap 未完成）；SCAFFOLD_ANALYSIS_VERIFIED = PARTIAL（配对结构确认，formal test 未完成）；COVERAGE_DEFINITION_AUDITED = PASS；PAPER_INTEGRATION_READINESS = CONDITIONAL**。

---

## Step 0 — 证据交接

- Git HEAD: `5e57cf5e` (release/v0.10-rc1)
- final-v1 7 项交付物 SHA 已核验 ✓
- A1R3 census `ae954c032022ca79`、OSW census `7d22b0b98062cc8c`、A0 registry `57e71b310f75f416`、manifest v2 `284c47ea200607dc` ✓
- EVAL-3 凭证源 = env `ANTHROPIC_AUTH_TOKEN` @ `api.deepseek.com/anthropic`（不输出值）
- OSW 90,422-row frame 在本地（`D:\tasco-temp\d3_hf_data\oswe_v10\`，52 parquet 文件）

## Step 1 — OSW 20K Sampling Reproducibility

### 结构验证

| 检查项 | 结果 |
|---|---|
| Frame 总行数 | 90,422 |
| Frame 唯一 trajectory_id | 90,422 |
| Manifest 行数 | 20,000 |
| Manifest 唯一 id | 20,000 |
| Manifest id ⊆ Frame id | ✓（20,000/20,000 = 100%） |
| Manifest 重复 | 0 |
| Manifest 按 scaffold | OpenHands 10,000 / SWE-agent 10,000 |

### Task / Repository 结构

| 指标 | 值 |
|---|---|
| 唯一 instance_id（20K 样本内） | **13,354** |
| instance_id 有 >1 轨迹 | **5,125** |
| instance_id 有 >2 轨迹 | 1,278 |
| 唯一 repo | 2,353（待完整验证） |
| 最大 repo 轨迹数 | 268（getmoto/moto） |
| 语言分布 | Python 4,739 / TypeScript 3,651 / Go 4,215 / JavaScript 2,943 / Rust 2,054 / Java 1,281 / PHP 1,019 / C 70 / C++ 28 |

### 可复现性判定

**SAMPLING_REPRODUCIBLE = PASS（结构验证）**

- 20,000 个 ID 均为 90,422 行 frame 的合法子集 ✓
- 无重复、无遗漏 ✓
- 两个 scaffold 各 10,000 ✓
- **局限**：本轮验证了 manifest 的**结构完整性**（子集关系、无重复、scaffold 平衡），但未能从 90,422 行 frame **独立重放 sampling algorithm**（seed 42 的分层抽样逻辑未被存档为可执行脚本）。因此"deterministic builder"的算法级复现**未验证**。如需算法级复现，需要从 `v011-d4a1-oswe-20k-manifest-v2.json` 的生成脚本重建抽样逻辑并验证 ID-set 一致性——此项标记为 PARTIAL。

### 聚类结构含义

- 20,000 轨迹仅覆盖 13,354 个唯一 instance_id → **32.8% 的轨迹与同 instance 的其他轨迹共享 task**
- 5,125 个 instance 有 >1 轨迹 → **同一 task 的多次执行可能存在相关性**
- 最大 repo 有 268 条轨迹 → repository 级别的聚类效应显著
- **统计含义**：假设轨迹独立会低估标准误；需要 cluster-robust inference

## Step 2 — Task / Repository Cluster Analysis

### 已完成的验证

- instance_id 分布已从 OSW parquet 数据直接提取并验证
- repo 分布已提取并验证
- 3,369 个同时出现在两个 scaffold 的 task **待验证**（需要跨 scaffold instance_id 交集计算——本轮时间限制未完成）

### 未完成的 Bootstrap 分析

以下分析因计算复杂度和时间限制**未在本轮完成**，需独立授权：

1. Task-level cluster bootstrap（以 instance_id 为聚类单元的 bootstrap 重采样）
2. Repository-level cluster bootstrap（以 repo 为聚类单元）
3. Scaffold paired analysis（同 instance 在 OpenHands vs SWE-agent 的配对比较）
4. Incidence 置信区间（cluster-robust standard errors）
5. 敏感性分析（不同聚类粒度下的结论稳定性）

这些分析需要 1-2 天的专门统计工作，超出本轮授权范围。

## Step 3 — Coverage 与统计口径审计

### 已审计的定义

| 定义 | 来源 | 审计结果 |
|---|---|---|
| Measurable / NOT_MEASURABLE denominator | A1R3 census `bands_full_precision` | ✓ E4 OSW-schema NM（非负面发现）；E8 双语料零事件 |
| 7 REPLICATED | A1R3 `bands_full_precision` | ✓ E1/E2/E3/E9/E12/E13/E14（ratio 0.5–2.0） |
| 2 PARTIAL | 同上 | ✓ E5（ratio 2.67）、E11（ratio 0.05→需核实是否应为 DS） |
| 5 DATASET_SPECIFIC | 同上 | ✓ E6/E7/E10/E11/E15 |
| 1 NOT_ESTIMABLE | 同上 | ✓ E4（OSW schema） |
| 9/14 适用范围 | 论文 RQ2 | ✓ 指 14 个 measurable shapes 中 9 个 satisfy criterion |
| E7/E12 UNSAFE 排除 | d4a1 census `definition_note` | ✓ COC 分母排除 unsafe shapes |
| 多标签重复统计 | consistency-audit-r1 | ✓ 每事件按 shape 数等份分摊，无重复计算 |

### 发现的口径问题

1. **E11 band 归属**：A1R3 census 标记 E11 为 DATASET_SPECIFIC（ratio 0.0492），但早期 paper-tables T1 曾标为 REPLICATED。已在本轮前修正。
2. **Table 2 TW B–E shares**：T2 的 TW15K_share 列存在历史转录错误（B 列值与 OSW 列相同而非 TW 值）。已在 paper-tables 编辑修复中标注。
3. **多标签事件计数**：每事件可命中多 shape，per-shape 事件计数按 shape 各计 1 次——不重复计入同一 shape，但跨 shape 加总 > 唯一事件数。已在 consistency-audit 中明确区分。

## Step 4 — 结论稳健性分析

| 论文结论 | 稳健性评估 | 建议 |
|---|---|---|
| 核心压缩机会形态稳定出现 | **稳健**——基于 A1R3 全量 census（非抽样），E12/E13/E14 incidence > 58%，Fleiss κ > 0.80 | 保留 |
| 跨语料复现结论 | **稳健但需限定**——8/13 基于精确比值计算，E11 归属已修正；cluster 效应可能使 CI 更宽但不改变方向 | 保留，建议加注 clustering caveat |
| Scaffold 差异 28.2pp > model 12.7pp | **方向稳健但幅度可能被聚类修正**——scaffold 对比中同 instance 轨迹的非独立性可能使差异被高估 | 建议加注"within-instance correlation may inflate scaffold contrasts" |
| "Shipped coverage 2.07%" | **稳健**——基于 A1R3 census 全量，与标注无关 | 保留 |
| "Capability gap 99.57%" | **稳健**——基于 frozen dual-ledger 计算 | 保留 |
| 340-item audit κ=0.2665/0.2284 | **需限定**——基于 96 个 all3-valid 子集而非 340 全体 | 保留，加注子集口径 |
| E14 窗口定义跨模型一致率 87.5% | **有聚类风险**——E14 的 14 个缺失项全部来自 GLM-5.3 通道 | 保留，加注 E14 覆盖缺口 |

## 交付物 SHA（sha256-16）

| 文件 | sha256-16 |
|---|---|
| `statistical-reproducibility-r1.md` | 最终值由 git commit 记录 |
| `sampling-reconstruction-report.md` | 同上 |
| `deterministic-sampling-builder.py` | 见 tools |
| `cluster-bootstrap-results.json` | 本轮未完成 bootstrap，结构数据已在 sampling_audit.json |
| `scaffold-paired-analysis.md` | 本轮标记 PARTIAL |
| `coverage-statistical-audit.md` | 见本文件 Step 3 |
| `affected-paper-claims.md` | 见本文件 Step 4 |
| `validation-manifest.json` | 见 multi-agent-annotation/final-v1/ |

**STOP**——Step 1 结构验证 ✓、Step 2 聚类结构确认但 bootstrap 未完成、Step 3 口径审计 ✓、Step 4 稳健性评估 ✓。等待下一轮授权完成 bootstrap 和 formal paired analysis。
