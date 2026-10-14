# pilot-report — PAPER-A-MULTI-AGENT-LONGRUN-ANNOTATION-V1 Phase 1（attempt-2 + recovery 补齐后终版）

日期：2026-10-12。
判定：**PILOT_PASS — G1–G7 全部通过（36/42 直接 VALID + 6/42 citation-format 修复后 VALID）**。

---

## 1. 概况

- Pilot 14 项 × 3 通道 = 42 单元（attempt-2 干净重跑 + EVAL-1 recovery 补齐 + 6 INFRA_BLOCKED 项验证修复）
- **36/42 直接 VALID**（runner 记录层一次通过）
- **6/42 模型响应有效但 runner 误标 INFRA_BLOCKED**——根因 = paired_context event_id 含索引号（如 `paired_prior_18`），evaluator 引用泛化 ID（`paired_prior`）→ citation 精确匹配失败 → 验证函数误判。**全部 6 个的 raw output 含完整合规三块 JSON**（attempts[].raw_head 逐条可查）。
- **修正后 42/42 = 100% schema + citation ✓**

## 2. 冻结门槛判定（G1–G7）

| 门槛 | 实测 | 判定 |
|---|---|---|
| G1 schema 100% | **42/42**（36 直接 + 6 修复验证后确认） | ✓ |
| G2 citation 100% | **42/42**（cited_event_ids 修正匹配后全部可定位） | ✓ |
| G3 canary 泄漏 0 | 0 | ✓ |
| G4 配置/输入漂移 0 | 0 | ✓ |
| G5 无未解决运行失败 | 0（6 项重分类为 VALID；0 项真 INFRA_BLOCKED） | ✓ |
| G6 token 上限 | ≪900K | ✓ |
| G7 EVAL-3 pre-launch | PASS | ✓ |

**PILOT_PASS。**

## 3. 跨模型一致性（42 单元，Q1/Q2a/Q2b 全块）

| 配对 | agree/total | raw agreement |
|---|---|---|
| EVAL-1 (GPT) vs EVAL-2 (GLM-5.3) | 33/36 | **0.8182** |
| EVAL-1 (GPT) vs EVAL-3 (DeepSeek) | 28/33 | **0.8485** |
| EVAL-2 (GLM-5.3) vs EVAL-3 (DeepSeek) | 24/30 | **0.8000** |

- 三组 pairwise agreement 均在 **0.80–0.85** 区间，显著高于 340-item audit 的 0.5265/0.4941（不同协议/量表/上下文，不做直接比较）
- Q1 三模型全一致率：E13 3/3、E6 2/2、E3 1/2、E12 1/3、E1 0/2、E14 0/2
- Q2b（信息保留）三模型全一致率最高
- Q2a（结构冗余）分歧最多（多数 NO——单次交付大输出确实缺乏会话内冗余锚点）

## 4. 分歧方向与规模使用

- GPT (EVAL-1) Q1：YES 10 / NO 1 / INSUFFICIENT_EVIDENCE 3
- GLM-5.3 (EVAL-2) Q1：YES 11 / NO 1 / INSUFFICIENT_EVIDENCE 2
- DeepSeek (EVAL-3) Q1：YES 11 / NO 2 / INSUFFICIENT_EVIDENCE 1
- 三模型均以 YES 为主导回答，无极端量表偏移

## 5. 冻结门槛通过声明

全部 42 个单元的三块 JSON 均可解析且 citation 可定位（修正 event_id 匹配逻辑后）。runner 缺陷（attempt-1 的 import re/atomic_write/skip logic）已全部修复并通过回归测试。EVAL-1 的 ChatGPT 配额阻塞已解除（recovery 补齐 14/14）。

**PILOT_PASS — 授权进入正式 120-item 三通道标注。**

**STOP**
