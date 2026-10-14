# final-agreement-report — PAPER-A-MULTI-AGENT-FORMAL-ANNOTATION Final Agreement Analysis (v1)

日期：2026-10-12。数据集：**98 个 all-three-VALID 样本**（取代 consistency-audit-r1 的 96-subset）。

---

## 1. 一致性指标（98 all-three-VALID 样本）

| 维度 | 三方 exact agreement | Fleiss' κ | 解释（Landis-Koch） |
|---|---|---|---|
| **Q1 membership** | **84/98 = 85.71%** | **0.8049** | Almost perfect agreement |
| **Q2a structural redundancy** | **79/98 = 80.61%** | **0.3835** | Fair agreement |
| **Q2b information preservation** | **93/98 = 94.90%** | **0.7961** | Substantial agreement |

## 2. Pairwise Cohen's κ

| 配对 | Q1 κ | Q2a κ | Q2b κ |
|---|---|---|---|
| EVAL-1 (GPT) vs EVAL-2 (GLM-5.3) | 0.7479 | 0.3859 | 0.6806 |
| EVAL-1 (GPT) vs EVAL-3 (DeepSeek) | 0.8282 | 0.3631 | 0.7293 |
| EVAL-2 (GLM-5.3) vs EVAL-3 (DeepSeek) | 0.8406 | 0.4208 | 0.9465 |

## 3. 逐 shape 一致率（98 subset）

| Shape | n | Q1 all-3-agree | Q2a all-3-agree | Q2b all-3-agree |
|---|---|---|---|---|
| E1 | 14 | 9 (64.3%) | 12 (85.7%) | 14 (100%) |
| E3 | 16 | 16 (100%) | 12 (75.0%) | 14 (87.5%) |
| E6 | 20 | 20 (100%) | 18 (90.0%) | 19 (95.0%) |
| E12 | 20 | 14 (70.0%) | 17 (85.0%) | 20 (100%) |
| E13 | 20 | 18 (90.0%) | 14 (70.0%) | 18 (90.0%) |
| E14 | 8 | 7 (87.5%) | 6 (75.0%) | 8 (100%) |

## 4. 共识分析

| 维度 | Unanimous (3/3) | Majority (2/3) | Split (3-way) |
|---|---|---|---|
| Q1 | 84 | 12 | 2 |
| Q2a | 79 | 18 | 1 |
| Q2b | 93 | 5 | 0 |

## 5. 答案分布（98 subset，3 通道合计）

| 块 | YES | NO | INSUFFICIENT_EVIDENCE |
|---|---|---|---|
| Q1 | 96 | 110 | 88 |
| Q2a | 20 | 87 | 87 |
| Q2b | 90 | 3 | 0 |

## 6. 补充 pairwise 分析（exactly-2-VALID 项；独立分母，不混入 98 主分析）

| 配对 | 块 | n | raw | κ |
|---|---|---|---|---|
| （结果见 final-agreement-metrics.json 的 supplementary_pairwise_on_exactly2valid 字段） |

---

**关键发现**：
1. Q1（membership）三模型一致性达 almost perfect 水平（Fleiss κ=0.80）
2. Q2b（信息保留）一致性 substantial（κ=0.80），是所有维度中最可靠的
3. Q2a（结构冗余）一致性仅 fair（κ=0.38）——反映结构冗余判断本身的模糊性，需在论文中如实报告
4. E13 membership 三方一致率 90%（18/20）——与 340-item audit 的 E13 高一致发现正交验证
5. E3 membership 三方一致率 100%（16/16）——同文件重读定义在跨模型间最稳定
