# annotation-method-and-limitations — Multi-Agent Formal Annotation (v1)

## 方法

### 独立三 Agent 标注协议

三个异构 Agent CLI（Codex CLI + GPT-5.6-sol / OpenCode CLI + GLM-5.3 / Claude Code CLI + DeepSeek-V4-flash）在隔离进程和隔离工作目录中对同一批 120 个 annotation packet 独立标注。每条 packet 包含脱敏后的目标观测（头 2,000 + 尾 500 chars）、前 3 事件上下文、目标 shape 的冻结定义原文、以及 E3/E14/E4/E15 的配对事件上下文。

### 评分维度

- **Q1 membership**：目标观测是否满足该 shape 的冻结定义（YES/NO/INSUFFICIENT_EVIDENCE）
- **Q2a structural redundancy**：目标观测是否在展示上下文中实质性重复交付已有信息
- **Q2b information preservation**：忠实压缩该观测是否需要逐字保留特定内容项

### 盲评与隔离

- detector_predicted_shape、capability_support、manuscript_conclusions、其他模型输出均不入 packet
- 三通道独立进程 + 独立 cwd（中性空目录，无 AGENTS.md/CLAUDE.md 注入）
- Codex `project_doc_max_bytes=0`；OpenCode `--pure`；Claude Code `--disallowedTools` 全内置
- 每通道唯一 canary token；跨通道泄漏扫描 = 0

## 边界与限制

1. **跨模型一致性 ≠ 人工 Ground Truth**。三个 LLM 的独立性受限于相似的预训练分布和 instruction-following 行为。模型间高一致不等于正确。

2. **Q2a 的 moderate κ（0.38）是真实发现而非方法缺陷**。结构冗余判断本身比 membership 判断更主观——两个模型可能都"正确"但采用不同的一致性标准。

3. ** detector precision 未被测量**。本审计测量的是模型间一致性（IRR），不是模型与 detector 的一致性（conformity），更不是 detector 的 precision/recall。IV-340 审计中的 detector-model conformity 是不同维度。

4. **E14 覆盖缺口**。OpenCode+GLM-5.3 通道对 E14 项产出率较低（14/22 缺失），导致 E14 的一致性统计基于较小子集（n=8 而非 22）。缺失原因 = GLM-5.3 推理模型对需要配对上下文的 E14 项耗时超 900s timeout，非定义模糊。

5. **单次交付大输出的 Q2a 系统性 NO**。Q2a structural redundancy 的 NO 率高达 87%（273/314）——大量 LUO 项因为"会话内无机械冗余锚点"被三模型一致判 NO。这是正确的操作语义，但意味着 Q2a 的 YES 率天然偏低，不应被解读为"观测不可压缩"。

6. **INSUFFICIENT_EVIDENCE 的语义**。EVAL-3 (DeepSeek) 在 Q1 上极少使用 INSUFFICIENT_EVIDENCE（1/98），而 EVAL-1 (GPT) 使用 3/98。这种量表使用差异是模型行为差异，不影响 Q1 的 Fleiss κ 计算（κ 对边际分布不敏感）。

7. **轨迹身份 = 行身份**。TW 15,000 行中 13,053 个唯一 session_id（1,947 碰撞对）。标注以行（recorded trajectory）为单位，同一 id 的两条不同轨迹被视为两个观测。不将行唯一性等同于执行独立性。

8. **不推断**：本审计结果不支持任何关于 taxonomy 语义有效性、安全压缩、task-level benefit 或 detector precision/recall 的推论。这些维度需要独立的方法论（人工标注、A/B 实验、power analysis）。
