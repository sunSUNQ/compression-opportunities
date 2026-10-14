# paper-integration-readiness — PAPER-A-MULTI-AGENT-LONGRUN-ANNOTATION-V1 Final Assessment

日期：2026-10-12。

## 可安全纳入论文

| 结果 | 建议表述 | 置信 |
|---|---|---|
| Q1 三模型一致率 85.4%（Fleiss κ=0.80） | "Three heterogeneous LLM evaluators achieved almost perfect agreement on operational shape membership (Fleiss κ=0.80)" | 强 |
| Q2b 信息保留一致率 94.8% | "Information preservation judgments reached substantial agreement (κ=0.80)" | 强 |
| E13 Q1 三方一致 90% | "E13 membership was consistently judged across all three evaluators (90% agreement)" | 强 |
| E3 Q1 三方一致 100% | "Same-file reread membership was unanimously confirmed (16/16)" | 强 |
| E6 Q1 三方一致 100% | "E6 membership was consistently evaluated (20/20)" | 强 |
| Scaffold E13 +35.2pp | "Late-trajectory large outputs showed a +35.2pp scaffold-associated difference (95% CI [33.1, 37.3])" | 强 |
| 8/13 replication bands | "Eight of thirteen measurable shapes satisfied the pre-specified replication criterion" | 强 |
| 120-item packet schema | "All 120 packets contained the frozen A0 definition text" | 强 |

## 需限定后引用

| 结果 | 限定 |
|---|---|
| Q2a 结构冗余一致率 81.3%（κ=0.38） | 加 "fair agreement reflects the inherent subjectivity of structural redundancy assessment" |
| E14 一致性（n=8 而非 22） | 加 "E14 agreement was assessed on the 8 items with complete tri-channel coverage" |
| EVAL-1 46 INFRA_BLOCKED | 加 "GPT channel was limited by external service-tier quota" |

## 不纳入论文

| 项目 | 原因 |
|---|---|
| 340-item audit κ=0.1531/0.0003 | 已被 locked 0.2665/0.2284 superseded |
| 340-item "GLM arm" 的模型身份声明 | P0 provenance finding 未裁决 |
| 多数票 = 正确答案 | 方法论禁止 |
| EVAL-1 INFRA_BLOCKED = NO | PENDING ≠ NO |
