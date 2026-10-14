# paper-a-final-correction-report — PAPER-A-FINAL-CORRECTION-AND-FREEZE-R1

日期：2026-10-12。
判定：**TECHNICAL_FREEZE_READY = YES（全部修正已完成并通过验证）**。

---

## 修正清单

| # | 问题 | 修正 | 状态 |
|---|---|---|---|
| 1 | §3.5 "314/360" → "317/360" | MD + Tex 同步更新 | **FIXED** |
| 2 | 340-item "heterogeneous LLM evaluators" → 准确描述 | MD + Tex 中改为 "rule-based annotation script + GPT-5.6-sol LLM evaluator"；κ 解释加注 "not inter-LLM agreement" | **FIXED** |
| 3 | RQ5 旧 COC → event-payload proxy | Abstract/RQ5/Finding 5/Discussion/Conclusion 全部替换 | **FIXED**（前轮） |
| 4 | E14 51.7% 覆盖缺口 | Limitations Coverage boundary 已添加 | **FIXED**（前轮） |
| 5 | E13 Q2a 主观性 | §3.5 "fair, reflecting inherent subjectivity" | **FIXED**（前轮） |

## 权威数字（冻结）

| 指标 | 值 |
|---|---|
| 计划单元 | 360 |
| VALID | **317** |
| INFRA_BLOCKED | **43** |
| all-three-VALID | **98/120** |
| Q1 三方一致率 | **85.71%**（Fleiss κ = 0.8049） |
| Q2a 三方一致率 | **80.61%**（Fleiss κ = 0.3835） |
| Q2b 三方一致率 | **94.90%**（Fleiss κ = 0.7961） |
| Detector replication | **9/14**（7R + 2P + 5DS，E8 NOT_MEASURABLE） |
| Event-payload COC (OSW) | shipped **0.018%** / candidate **95.96%** / gap **99.98%** |
| Event-payload COC (Qwen) | shipped **0.27%** / candidate **97.67%** / gap **99.72%** |

## PDF 验证

- **9 pages** ≤ 10 ✓
- **0 errors / 0 undefined / 0 overfull** ✓
- 317 PRESENT / 314 clean ✓
- rule-based PRESENT ✓
- 全部新指标 PRESENT ✓
- Anonymous ✓

## 冻结版本

| 文件 | 说明 |
|---|---|
| paper-a-candidate-r1.md | 最终 Markdown 候选稿 |
| paper-a-candidate-r1.tex | 最终 LaTeX 候选稿 |
| paper-a-candidate-r1.pdf | 最终 PDF（9 pages） |
| paper-a-final-authoritative-metrics.json | 权威指标冻结 |
| paper-a-final-freeze-manifest.json | 冻结清单 |

**STOP**——技术冻结完成；VENUE_FORMAT_VERIFIED = UNVERIFIED。
