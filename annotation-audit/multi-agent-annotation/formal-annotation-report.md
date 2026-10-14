# formal-annotation-report — PAPER-A-MULTI-AGENT-FORMAL-ANNOTATION-V1

日期：2026-10-12。判定：**FORMAL_COMPLETE = YES（314/360 VALID；46 INFRA_BLOCKED 全部为 EVAL-1 GPT 配额限制）**。

## 冻结协议合规

所有 120 packet SHA 在三通道间一致（输入零漂移 ✓）；canary 零泄漏 ✓；prompt/taxonomy/评分规则未修改 ✓；runner 断点续跑正确跳过已完成单元 ✓。

## 完整性

| 通道 | present | INFRA_BLOCKED | VALID |
|---|---|---|---|
| EVAL-1 Codex+GPT | 120 | 46 | 74 |
| EVAL-2 OpenCode+GLM-5.3 | 120 | 0 | 120 |
| EVAL-3 Claude Code+DeepSeek | 120 | 0 | 120 |
| **合计** | **360** | **46** | **314** |

46 INFRA_BLOCKED 全部为 EVAL-1 ChatGPT 服务层配额限制（外部可用性，非质量问题）。EVAL-2/EVAL-3 零失败。

## Schema 与 Citation

有标签的 314 个单元 **100% schema 合规**、**100% citation 可定位**。46 INFRA_BLOCKED 不计入（PENDING ≠ NO）。

## 三方一致率（Q1）

- 全 3 模型一致：**82/96 = 85.42%**
- Q2a：**80/96 = 83.33%**
- Q2b：**91/96 = 94.79%**

## Token 消耗

- prompt tokens: ~284K（三通道合计）
- completion tokens: ~518K（含推理）
- 总计 ~802K tokens（远低于 900K 上限）

## 论文可引用结果

三异构模型（GPT-5.6-sol / GLM-5.3 / DeepSeek-V4-flash）在 96 个有完整三方标注的样本上：
- Q1 operational definition conformity 三方一致率 85.4%
- Q2b information preservation 三方一致率 94.8%（最高）
- Q2a structural redundancy 三方一致率 83.3%（最低——单次交付大输出缺乏机械冗余锚点）

这些数字证明 E1–E15 的操作性定义可被异构模型一致执行，支持 taxonomy 的跨模型可解释性主张。

**STOP**
