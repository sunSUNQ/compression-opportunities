# final-evidence-closure-r2 — PAPER-A-FORMAL-ANNOTATION-FINAL-EVIDENCE-CLOSURE-CORRECTION-R2

日期：2026-10-12。

| 维度 | 判定 |
|---|---|
| DETECTOR_ANNOTATION_COMPATIBILITY | **PASS** |
| STATISTICAL_QUALIFICATION | **PASS** |
| SAMPLING_REPRODUCIBILITY | **PARTIAL** |
| CLAIM_EVIDENCE_CLOSURE | **CONDITIONAL** |
| PAPER_EVIDENCE_READY | **CONDITIONAL** |

---

## 1. 权威数字（单一来源 = 直接从盘上 result files 复算）

| 指标 | 权威值 |
|---|---|
| 计划单元 | 360（120 items × 3 通道） |
| **VALID（三键齐 + answer 非空）** | **317** |
| **INFRA_BLOCKED** | **43**（EVAL-1: 10 / EVAL-2: 12 / EVAL-3: 21） |
| **all-three-VALID samples** | **98/120** |
| exactly-2-VALID | 10 |
| <2-VALID | 12 |
| Q1 三方 exact agreement | **84/98 = 85.71%** |
| Q1 Fleiss κ | **0.8049** |
| Q2a 三方 exact agreement | **79/98 = 80.61%** |
| Q2a Fleiss κ | **0.3835** |
| Q2b 三方 exact agreement | **93/98 = 94.90%** |
| Q2b Fleiss κ | **0.7961** |

## 2. 版本冲突调停（Step 1）

| 版本 | VALID | INFRA | all-3 | 来源 | 状态 |
|---|---|---|---|---|---|
| R1 informal（formal-annotation-report.md） | 314 | 46 | — | `d.get("labels")` 仅检查存在 | **SUPERSEDED** |
| consistency-audit-r1 | 313 | 47 | 96 | `all(b in labels for b in BLKS)` | **SUPERSEDED** |
| coverage-recovery-r1 | 317 | 43 | 98 | 恢复后独立重算 | **SUPERSEDED** |
| **R2（本报告）** | **317** | **43** | **98** | 直接从盘上 result files 重算（bulletproof get_answer） | **AUTHORITATIVE** |

R1 的 85.4%/94.8%/83.3% 来自 96-subset（consistency-audit-r1），后被 coverage-recovery-r1 的 98-subset 取代。R1 的 EVAL-1 "46 INFRA_BLOCKED" 来自宽松检查（`d.get("labels")` 仅验证字段存在，不验证三块齐全）。R2 使用 bulletproof `get_answer`（try/except）从盘上 .json 直接复算，与 coverage-recovery-r1 和 consistency-audit-r1 的高严格口径一致。

**旧口径 96-subset、313/360、314/360 均不再作为最终数字。**

## 3. 遗漏验收项补查（Step 2）

| 验收项 | 状态 | 证据 |
|---|---|---|
| 120-item Detector × Annotation compatibility | ✓ PASS | 120/120 schema_def match; 120/120 sample_id match; 360/360 shape_target match |
| Repo-level cluster bootstrap | ✓ PASS | 2000× seed 42，CI 与 instance-level 方向一致 |
| E13 +35.2pp paired analysis | ✓ VERIFIED | CI [0.331, 0.373] 排除 0；Bonferroni ×9 仍显著 |
| E12/E14 多重比较 | ✓ E13/E12/E14 CI 均 survive Bonferroni | |
| E14 缺失集中 51.7% | ✓ 精确定义 = 31/60 cells（E14 × 3 通道 = 60 cells，31 INFRA_BLOCKED） | |
| 20K manifest integrity | ✓ PASS（20,000/20,000 唯一 ID ⊆ 90,422 frame） | |
| 20K sampling algorithm reproducibility | **PARTIAL**（结构验证 ✓；算法级重放未完成） | |

## 4. P0 Provenance Finding 独立审计（Step 3）

### 4.1 发现

`glm_annotate.py`（8,822 chars）为纯 Python 启发式脚本，**零网络/LLM 调用**（requests/urllib/http/openai/anthropic 全文扫描 = NONE）。其 OUT 路径直接指向 `glm53-annotations.json`。该脚本被记录为产出 340 条 "GLM-5.3-flash" 标签。

### 4.2 逐项影响评估

| 影响面 | 是否受影响 | 依据 |
|---|---|---|
| 原始数据身份 | **否** | TW/OSW parquet 与 manifest SHA 独立于该脚本 |
| detector replay | **否** | A1R3/A0 冻结 census 基于独立检测器代码（`opportunity_census.py` 等），SHA 可追溯 |
| 正式标注来源 | **否** | 360-cell 标注使用三个 Agent CLI（Codex/OpenCode/Claude Code），独立于 glm_annotate.py |
| 统计和论文主张 | **部分** | 340-item audit 的 κ/一致性数字基于脚本生成的标签而非真实 LLM 评价——这些数字不可作为"异构 LLM 审计"引用 |
| 冻结证据追溯 | **无混用** | 340-item audit 结果不进入 A1R3/OSW census 或正式标注结果 |

### 4.3 影响定级

**P0 finding 限于 340-item audit 的 provenance 标注**。不影响：
- A1R3 census（TW 15K trajectory-level incidence）
- OSW 20K census
- 三通道正式标注（120 × 3 = 360 cells）
- 8/13 replication bands
- Cluster bootstrap / scaffold paired analysis
- Coverage 定义审计

**结论**：P0 = 元数据/标签来源问题，非实质性数据完整性问题。可通过修改 340-item audit 的 provenance 描述（从"GLM-5.3-flash LLM evaluation"改为"rule-based heuristic annotation script"）关闭，无需重跑实验。但该项修改需独立授权。

## 5. 统一验证清单

| 验证 | SHA/路径 |
|---|---|
| 120-item manifest | `multi-agent-pilot-manifest.json` sha `5d54eb69461cd14c` |
| 冻结 prompt/config | `longrun_frozen_config.json` sha `68d0f94db08163c4` |
| Runner（全部修复） | `longrun_runner.py` sha `bfedf5ecd16b37e9` |
| 统计锁定工件 | `annotation-statistics-amendment.json` sha `de30138fa71414a0` |
| Formal results (314 VALID) | `formal-annotation-results.jsonl` sha `dff84bbcce6ab5bb` |
| Shared sample manifest | `shared-sample-manifest.json` sha `e1eb50282188dedc` |
| 360 result files | `results/formal/{EVAL-1,EVAL-2,EVAL-3}/*.json` |

**STOP**——等待下一轮独立授权。
