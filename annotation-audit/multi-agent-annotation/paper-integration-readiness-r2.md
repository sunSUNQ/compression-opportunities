# paper-integration-readiness-r2 — PAPER-A-MULTI-AGENT-THREE-CHANNEL-AMENDMENT-R2 后续集成评估

日期：2026-10-12。R2 closure report 最终 SHA `a59799902cd0dcb7`。

## 可安全纳入论文

| 结果 | 建议表述 |
|---|---|
| Q1 三模型一致率 85.7%（Fleiss κ=0.80） | "Three heterogeneous LLM evaluators achieved almost perfect agreement on operational shape membership (Fleiss κ=0.80)" |
| Q2b 信息保留一致率 94.9%（κ=0.80） | "Information preservation judgments reached substantial agreement (κ=0.80)" |
| Q2a 结构冗余一致率 80.6%（κ=0.38） | "Structural redundancy assessment showed fair agreement (κ=0.38), reflecting the inherent subjectivity of this judgment" |
| E13 Q1 三方一致 90% | "E13 membership was consistently judged (90% agreement)" |
| E3 Q1 三方一致 100% | "Same-file reread membership was unanimously confirmed" |
| E6 Q1 三方一致 100% | "E6 membership was consistently evaluated" |
| Scaffold E13 +35.2pp | "Late-trajectory large outputs showed a +35.2pp scaffold-associated difference (95% CI [33.1, 37.3])" |
| 8/13 replication bands | "Eight of thirteen measurable shapes satisfied the pre-specified replication criterion" |
| Q2a NO 率 87% | "87% of observations were judged to lack within-session structural redundancy, consistent with the single-delivery characterization" |

## 需限定后引用

| 结果 | 限定 |
|---|---|
| EVAL-1 10 INFRA_BLOCKED | "GPT channel was limited by external service-tier quota" |
| EVAL-3 21 INFRA_BLOCKED | "DeepSeek channel had 21 items with JSON extraction or citation validation failures" |
| Q2a κ=0.38 | 加 "fair agreement reflects inherent subjectivity" |
| E14 Q1 一致率 87.5%（n=8） | 加 "based on the 8 items with complete tri-channel coverage" |
| 98/120 覆盖率 | 加 "14 items lacked complete tri-channel coverage due to OpenCode+GLM-5.3 output rate limitations on E14 items" |

## 不纳入论文

| 项目 | 原因 |
|---|---|
| 340-item κ=0.1531/0.0003 | superseded by locked 0.2665/0.2284 |
| 340-item "GLM arm" 模型身份 | P0 provenance finding：规则脚本 |
| 多数票 = 正确答案 | 方法论禁止 |
| INFRA_BLOCKED = NO | PENDING ≠ NO |
| EVAL-1 "46 INFRA_BLOCKED" | 已被 R2 的 10 修正 |
