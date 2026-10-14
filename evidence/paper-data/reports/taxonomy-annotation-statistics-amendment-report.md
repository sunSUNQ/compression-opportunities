# PAPER-A-ANNOTATION-STATISTICS-AMENDMENT — Reconciliation Report

日期：2026-10-10。依据：`taxonomy-annotation-validity-v1-report.md`（PARTIAL；κ 复现性发现）。
判定：**PASS**（独立复算与 V1 审计一致；无 STOP 触发）。commit SHA 见 git log（本轮）。

---

## 1. 权威输入（sha256-16）

| 输入 | sha256-16 |
|---|---|
| `taxonomy-annotation-validity-v1-report.md` | `71d67ee570b94251` |
| `construct-validity/sample-manifest.json` | `187439f0141102fd` |
| `construct-validity/model-audit/glm53-annotations.json` | `0f2d6e33a2815f6b` |
| `construct-validity/model-audit/gpt-annotations.json` | `4f59464f0b709300` |
| `construct-validity/model-audit/model-audit-reconciled.json` | `e5409620439dc7d9` |
| 本轮统计脚本 `evidence/tools/annotation_audit_statistics.py` | `515737a30e128321` |
| 本轮锁定统计工件 `construct-validity/model-audit/annotation-statistics-amendment.json` | `de30138fa71414a0` |

## 2. 标准 κ 复算与锁定（Step 2）

标签语义：Q1/Q2 ∈ {YES, NO, UNCERTAIN}（名义变量，不做重编码）；缺失值：paired-valid 340 集内为零（GLM 48 条恢复项为一等行）；κ = 标准未加权 Cohen κ = (po−pe)/(1−pe)，pe = Σ_c p_GLM(c)·p_GPT(c)。

锁定统计（工件含 3×3 列联表、边际分布、observed/expected agreement、pos/neg agreement、逐 shape κ 及 N/A 标记、detector-unblind）：

| 统计 | 值 |
|---|---|
| Q1 observed agreement | 0.526471（179/340） |
| Q1 expected agreement | 0.354392 |
| **Q1 Cohen κ（unweighted）** | **0.266534** |
| Q1 marginals GLM YES/NO/UNC | 100/42/198；GPT 54/135/151 |
| Q2 observed agreement | 0.494118（168/340） |
| Q2 expected agreement | 0.344394 |
| **Q2 Cohen κ（unweighted）** | **0.228374** |
| Q2 marginals GLM YES/NO/UNC | 68/224/48；GPT 233/107/0（GPT 从不使用 UNCERTAIN） |
| Q1 pos/neg agreement | 0.2833（34/120）/ 0.3111（42/135） |
| Q2 pos/neg agreement | 0.2918（68/233）/ 0.4329（100/231） |
| E13 Q1 κ（局部，唯一可解释高值） | 0.9146 |

历史 0.1531/0.0003 → **superseded（UNREPRODUCIBLE）**：标准约定穷尽（3 类 unweighted/linear/quadratic、PABAK、36 组二元映射、listwise、340/292/48 子集）均不匹配；其计算约定未存档。本轮**不猜测**其产生算法。与 V1 审计期望值（0.2665/0.2284）的等值性由脚本内置断言强制（不一致即非零退出）。

## 3. detector-unblind 修正（Step 3）

| 统计 | 旧（superseded vintage） | 新（全 340 口径） |
|---|---|---|
| GLM 接受 detector-positive | 84/180（46.7%） | **84/220 = 38.18%**（分子一致；分母为恢复前 vintage） |
| GPT 接受 detector-positive | 50/180（27.8%） | **53/220 = 24.09%** |
| both reject det-positive | 0 | **117**（Q1≠YES 定义） |
| both accept det-negative | 34 | **0**（34 为全样本 YES\|YES 桶计数误植） |

全文扫描：旧 κ（0.1531/0.0003）、旧分母（84/180、46.7%、27.8%）、"chance-level" 解释在论文/Supplement B/claim trace 中已全部替换或标注 superseded；`0.0003` 的剩余命中 = F1 signal:noise（合法无关）。det-unblind 块所在的 `model-audit-results.json` 本身已标 SUPERSEDED（本轮在其 Supplement B 转录处补 vintage 混装警告）。

## 4. 正文与 Supplement B 修订（Step 4）

| 位置 | 旧 → 新 |
|---|---|
| tex §3.3 | κ=0.1531 → **0.2665**；κ≈0.0003 → **0.2284**（"standard unweighted three-category κ, locked recomputation in the released statistics artifact"）；E13 补 κ=0.9146（"the only shape whose κ is high and interpretable"）；新增量表使用句（"a large share of the Q2 disagreement reflects differing scale usage between the evaluators (one evaluator never used the UNCERTAIN option on Q2)—an observable response-style difference, not evidence about the underlying content"） |
| tex Threats（Construct validity） | 同步两处 κ + E13 κ |
| md | 两处孪生同步 |
| Supplement B | 新增 "Statistics amendment" 小节：superseded κ 声明 + 锁定脚本/工件引用 + 3×3 两表 + pos/neg agreement + E13 局部高一致（不推广）+ detector-unblind 现行值 + vintage 混装警告 + 协议差异披露（原 300-item 人工计划 vs 实际 340-item LLM audit）原样保留 |
| claim trace | C38/C39 更新（新 κ + superseded 说明 + 工件 SHA）；"chance-level" 措辞移除 |

有效性边界（Step 5）维持：A detector reproducibility（强，A0+重放）；B operational interpretation（E13 局部清晰）；C evaluator agreement（raw/κ 如上）；D/E/F 不支持（无 semantic validation、无 human ground truth、无 detector precision、无 safe compression/在线收益表述——全文扫描确认）。

## 5. 零变化验证（Step 6）

- RQ1–RQ5 结论与数字：零变化（本轮仅触及 §3.3/Threats/Supplement B/claim trace）。
- A1R3 census、8/13 replication、core six 0.79–1.28、Fig.1–6、T1–T6：`git status` 确认 figures.json/paper-tables.json/census 工件**零修改**。
- 历史冻结原始评价（glm53-annotations.json、gpt-annotations.json、reconciled.json、manifest）：零修改（SHA 见 §1——reconciled `e5409620439dc7d9` 与 V1 审计记录一致）。

## 6. 构建审计

- clean rebuild：pdflatex + bibtex + pdflatex ×2 → **9 pages / 539,542 bytes**（≤10 页预算）；log **0 errors / 0 undefined / 0 overfull**；bibtex 0 error。
- PDF 文本审计：新值全 PRESENT（0.2665/0.2284/0.9146/differing scale usage/locked recomputation/52.65/49.41/96.4/78.6）；旧值全 clean（0.1531/chance-level/84/180）；`0.0003` 唯一残留 = F1 signal:noise（合法无关）。
- 匿名/泄漏：clean。

## 7. 中文对应段落（§3.3 修订）

> 调和后的审计包含 340 对有效观测。Q1（shape 归属）raw agreement 52.65%（Cohen κ=0.2665），Q2（压缩机会）raw agreement 49.41%（κ=0.2284；标准未加权三分类 κ，锁定复算见随文发布的统计工件）。E13 的 raw agreement 显著更高：Q1 96.4%、Q2 78.6%（E13 Q1 κ=0.9146，为唯一 κ 高且可解释的 shape）。因此 E13 的一致性不能代表整个 taxonomy：跨 shape 的自然语言解释不一致，且 Q2 分歧的很大一部分反映两个评估器的量表使用方式不同（一个评估器在 Q2 上从未使用 UNCERTAIN 选项）——这是可观察的作答风格差异，不是关于底层内容的证据。该分类因冻结确定性规则而机械可复现；此性质不建立语义有效性。该审计不是人类金标、不是 detector 精度估计、也不是安全压缩的验证；它诊断异构模型评估器之间的解释敏感性。

## 8. 判定

STOP 条件核对：独立 κ 复算与 V1 审计一致（内置断言通过）✓；类别定义/分母无冲突（3 类名义、n=340、无缺失）✓；未修改任何原始评价 ✓；RQ/A1R3/Fig.3/冻结件零变化 ✓；构建与 PDF 审计通过 ✓。
**判定：PASS。** **STOP**——不开展人工验证；等待下一轮独立授权任务。
