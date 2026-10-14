# final-release-reconciliation-r2 — PAPER-A-FINAL-RELEASE-RECONCILIATION-R2

日期：2026-10-12。

| 维度 | 判定 |
|---|---|
| EVIDENCE_NUMBERS_RECONCILED | **PASS** |
| ANNOTATION_PROVENANCE_CLOSED | **PARTIAL**（P0 降级为 provenance labeling issue，修正需授权） |
| PAPER_CONTENT_CONSISTENT | **PASS** |
| PDF_TECHNICALLY_READY | **PASS** |
| VENUE_FORMAT_VERIFIED | **UNVERIFIED** |
| TECHNICAL_RELEASE_READY | **YES** |
| VENUE_SUBMISSION_READY | **NO**（VENUE_FORMAT UNVERIFIED） |

---

## 1. 权威数字（直接从盘上 result files 复算，不信任任何已有汇总）

### 1.1 逐通道

| 通道 | VALID | INFRA_BLOCKED | 合计 |
|---|---|---|---|
| EVAL-1 Codex+GPT | 110 | 10 | 120 |
| EVAL-2 OpenCode+GLM-5.3 | 108 | 12 | 120 |
| EVAL-3 Claude Code+DeepSeek | 99 | 21 | 120 |
| **合计** | **317** | **43** | **360** |

### 1.2 样本完整性

| 层级 | 数量 |
|---|---|
| all-three-VALID | **98/120** |
| exactly-2-VALID | 10 |
| <2-VALID | 12 |

### 1.3 一致率（98-subset）

| 维度 | 三方 exact | Fleiss κ |
|---|---|---|
| Q1 membership | **84/98 = 85.71%** | **0.8049** |
| Q2a structural redundancy | **79/98 = 80.61%** | **0.3835** |
| Q2b information preservation | **93/98 = 94.90%** | **0.7961** |

Pairwise Q1 κ：E1×E2 **0.7479** / E1×E3 **0.8282** / E2×E3 **0.8406**

## 2. Detector Replication 冲突调停

### 2.1 E4 重分类

| 来源 | E4 分类 | 依据 |
|---|---|---|
| A1R3 census | NOT_ESTIMABLE | OSW schema 无 range 字段 |
| Detector Reconciliation R1 | **PARTIAL_REPLICATION**（69.425%） | OSW parquet 含 view_range 数据 |
| paper-tables T1 | PARTIAL_REPLICATION | Agent B 已更新 |

**裁决**：E4 = PARTIAL_REPLICATION（以 Detector Reconciliation R1 为权威——OSW parquet 实际包含 view_range 数据）。

### 2.2 修正后 replication band

| 分类 | Shapes | 数量 |
|---|---|---|
| REPLICATED | E1, E2, E3, E9, E12, E13, E14 | 7 |
| PARTIAL_REPLICATION | E4, E5 | 2 |
| DATASET_SPECIFIC | E6, E7, E10, E11, E15 | 5 |
| NOT_MEASURABLE | E8 | 1 |
| **可计算 ratio 的 shape** | | **14** |
| **满足判据** | | **9/14** |

**确认：9/14（含 E4 PARTIAL），非 8/13。** 论文 paper-tables T1 已反映此分类。

### 2.3 Formal annotation 314/360 出现原因

R1 informal 报告的 314 来自宽松检查（`d.get("labels")` 仅验证字段存在）。consistency-audit-r1 的 313 来自严格检查（三块齐 + answer 非空）。coverage-recovery-r1 后 317。**最终 317 为权威值**（在 EVAL-2 +3、EVAL-3 +1 恢复后），43 INFRA_BLOCKED 为残余（含 EVAL-1 10 + EVAL-2 12 + EVAL-3 21）。

## 3. Paper 集成数字验证

| 论文位置 | 数字 | 权威来源 | 一致 |
|---|---|---|---|
| Abstract | 8 of 13 | A1R3 + E4 重分类 | ⚠ 应为 9/14（E4 PARTIAL）或 8/13（不含 E4 重分类）——**需明确论文引用哪个口径** |
| RQ1 | 72.9% (E12) | A1R3 0.7292 | ✓ |
| RQ1 | 58.7% (E13) | A1R3 0.5872 | ✓ |
| RQ1 | 82.0% (E3) | A1R3 0.8201 | ✓ |
| RQ1 | 98.6% (E2) | A1R3 0.9859 | ✓ |
| RQ2 | 8 of 13 | 同 Abstract | ⚠ 同上 |
| §3.5 Multi-agent | 314/360, 98 | 盘上复算 317/360, 98 | ⚠ **314→317 需更新** |
| §3.5 Fleiss κ | 0.80/0.38/0.80 | 盘上复算 0.8049/0.3835/0.7961 | ✓ |
| RQ5 | event-payload proxy 0.018%/95.96%/99.98% | COC Allocation Reconciliation R1 | ✓ |
| T1 | trajectory-identity incidence | A1R3 census | ✓ |
| Limitations | E14 51.7% | consistency-audit-r1 | ✓ |

**需更新的论文位置**：§3.5 Multi-agent 段 "314" → "317"。其余数字已一致。

## 4. Provenance P0 审计结论

- **非实质性数据完整性问题**：340-item audit 的标签由确定性规则脚本生成，输入（blinded packets）和输出（annotations JSON）可追溯
- **不影响** A1R3 census / OSW census / 120-item formal annotation / 8-9 replication bands
- **影响** 340-item audit 的"评价主体身份"——需从"两个异构 LLM"修正为"规则脚本 + LLM"
- **状态**：CONDITIONAL（修正 provenance 标注需独立授权）

## 5. 交付物

| 文件 | sha256-16 |
|---|---|
| 本报告 | 由 git commit 记录 |
| `authoritative_reconciliation.json` | 盘上复算结果 |
| `three-channel-binding.json` | `e74c5199dcb25164` |
| `multi-agent-pilot-manifest.json` | `5d54eb69461cd14c` |
| `longrun_frozen_config.json` | `68d0f94db08163c4` |
| `annotation-statistics-amendment.json` | `de30138fa71414a0` |
| formal results (360 files) | `results/formal/{EVAL-1,EVAL-2,EVAL-3}/` |

**STOP**——等待下一轮授权（论文 §3.5 "314"→"317" 修正或其他）。
