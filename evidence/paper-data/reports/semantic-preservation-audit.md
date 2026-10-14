# semantic-preservation-audit — PAPER-A-BILINGUAL-ACADEMIC-CLARITY-REVISION-R1

审计目的：确认语言修订未改变技术含义、数字、结论或限定条件。

## 逐项核对

| 项 | 原稿 | 修订稿 | 一致？ |
|---|---|---|---|
| RQ1–RQ5 研究目标 | ✓ | ✓ | ✓ |
| RQ1–RQ5 主要结论 | ✓ | ✓ | ✓ |
| 8/13 replication band | ✓ | ✓ | ✓ |
| E12 72.9%/79.5% | ✓ | ✓ | ✓ |
| E13 58.7%/46.6% | ✓ | ✓ | ✓ |
| E1 0.9719 | ✓ | ✓ | ✓ |
| E2 0.9859 | ✓ | ✓ | ✓ |
| E3 0.8201 | ✓ | ✓ | ✓ |
| E14 0.7382 | ✓ | ✓ | ✓ |
| E4 PARTIAL_REPLICATION | ✓ | ✓ | ✓ |
| 9/14 detector replication | ✓ | ✓ | ✓ |
| E7/E12 UNSAFE exclusion | ✓ | ✓ | ✓ |
| COC proxy 0.018%/95.96%/99.98% | ✓ | ✓ | ✓ |
| COC proxy ≠ byte-span disclaimer | ✓ | ✓ | ✓ |
| SOC ≠ COC distinction | ✓ | ✓ | ✓ |
| Fleiss κ Q1 0.8049 | ✓ | ✓ | ✓ |
| Fleiss κ Q2a 0.3835 | ✓ | ✓ | ✓ |
| Fleiss κ Q2b 0.7961 | ✓ | ✓ | ✓ |
| 317/360 VALID | ✓ | ✓ | ✓ |
| 43/360 INFRA_BLOCKED | ✓ | ✓ | ✓ |
| 98/120 all-three-VALID | ✓ | ✓ | ✓ |
| E14 51.7% coverage gap | ✓ | ✓ | ✓ |
| 340-item provenance correction | ✓ | ✓ | ✓ |
| "not human ground truth" disclaimer | ✓ | ✓ | ✓ |
| "not detector precision" disclaimer | ✓ | ✓ | ✓ |
| "not safe compression" disclaimer | ✓ | ✓ | ✓ |
| "allocation proxy ≠ byte-span" disclaimer | ✓ | ✓ | ✓ |
| "scaffold association ≠ causation" disclaimer | ✓ | ✓ | ✓ |
| E1⊆E2, E11⊆E10, E4⊆E3 inclusions | ✓ | ✓ | ✓ |
| 0 counterexample violations | ✓ | ✓ | ✓ |
| 70.0% LUO share (TW) | ✓ | ✓ | ✓ |
| 73.8% LUO share (OSW) | ✓ | ✓ | ✓ |
| P0 GLM arm = rule-based script | ✓ | ✓ | ✓ |
| P0 = provenance labeling issue | ✓ | ✓ | ✓ |
| Session identity = trajectory (row) | ✓ | ✓ | ✓ |
| 13,053 unique session IDs | ✓ | ✓ | ✓ |
| 1,947 collided identifiers | ✓ | ✓ | ✓ |

**结果：37/37 项语义保持一致 ✓**

## 数字变化审计

| 数字 | 旧值 | 新值 | 变化原因 |
|---|---|---|---|
| （无数字变化——本轮为语言编辑） | | | |

## 结论

全部 37 项语义保持审计项均一致。语言修订未改变任何技术含义、数字、结论或限定条件。

## 附录：§3.5 结构调整复核（2026-10-13）

经作者授权的 §3.5 子节移动与标题简化（"Annotation Agreement Analysis"）为纯结构/标题变更：
全部 37 项审计项复核后仍然 37/37 一致；数字变化审计仍为空（无任何数字变化）。
chinese-review-version.md 同步时将滞留的修订前数字（314/87.2%）校正为冻结权威值（317/88.1%），
属于向冻结版本的数字对齐，不是实验结果变更。
