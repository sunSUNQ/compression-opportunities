# PAPER-A-TAXONOMY-CONSTRUCTION-AMENDMENT — 修订报告

日期：2026-10-10。依据：`taxonomy-construction-v2-report.md`（§1–§6）及其引用的原始 prereg/commit/census 记录（本轮对全部一手文档已于 V2 任务中逐字复核，未发现分歧）。
范围纪律：**仅修改 §3.1 Construction（tex + md 孪生）与 claim-trace C02 同步**；detector、阈值、shape ID、census、8/13 replication、Figures、frozen artifacts 零改动。

---

## 1. 修改文件

| 文件 | 修改前 sha256-16 | 修改后 sha256-16 | 变更 |
|---|---|---|---|
| `paper-draft-v1-icse.tex` | `d042198429d67c29` | `29dc6ea436c66327` | §3.1 Construction 重写为两段；保留 thoughtworks2026 引用（移入 discovery corpus 句） |
| `paper-draft-v1-icse.md` | `d06c1427bae888d2` | `e1a5d157af36ebdf` | 同步 markdown 孪生 |
| `paper-claim-trace.md` | `ed0333adf0afaa53` | `42157751200d2e08` | C02 artifact 扩展至两份 prereg（49482bbf / 55494bce）+ amendment 注记 |
| `paper-draft-v1-icse.pdf` + aux/out/bbl/blg/log | `1ca34801572fbb19`（pdf） | `5e416228f6419faf`（pdf） | clean rebuild，8 pages |

未改动：rq-claim-evidence-matrix.json、paper-tables.json、figures.json、全部图、supplements、全部冻结证据、registry。

## 2. Claim-to-Evidence Ledger（新文本逐句 → 证据）

| 新文本主张 | 证据 | 强度 |
|---|---|---|
| "constructed in two preregistered stages" | 内部 prereg `49482bbf`（FROZEN before any aggregation）→ D3-E1 prereg amendment `55494bce`（commit 明文 "BEFORE aggregation"）→ `fde05652`（TW 15K 首次应用） | EVIDENCED |
| "158 sessions with session telemetry from seven real work batches (a planned universe of approximately 256 sessions; the 158 with telemetry form the realized denominator)" | 内部 prereg §1 "≈256 sessions"（计划值）；census 报告 §1 "158 sessions with telemetry（7 批…）"；incidence 分母=158（S1 153/158=0.968 交叉验证） | EVIDENCED |
| S1–S8+S7b 形态清单、"by form rather than by capability name" | 内部 prereg §3（"按输出形态，非能力名"）逐字定义；census JSON `shapes` 键名逐一对应 | EVIDENCED |
| 内部 gate（≥20% ∧ ≥1000）"frozen before any aggregation" | 内部 prereg §5 + commit `49482bbf` | EVIDENCED |
| "only the generic large-tool-output shape passed the gate" | census JSON `candidate_pool = [S1_large_tool_output]`（S1 0.968 / median 3,119） | EVIDENCED |
| "command repeats proved small-payload (median 311 chars)" | census JSON S2 median_raw_chars=311（inc 1.0） | EVIDENCED |
| "multi-rerun validation was rare (1.3%)" | census JSON S3 session_incidence=0.013 | EVIDENCED |
| "test-output family produced no internal events under the available telemetry fields (recorded as-is)" | census 报告 §2 "S7/S7b 0（test_executed 字段覆盖不足，如实记录）"；JSON S7/S7b 无记录键 | EVIDENCED |
| "large search outputs were already covered by a shipped capability" | census 报告 §3 S8 existing overlap=1.0（quick_grep） | EVIDENCED |
| 第二份 prereg "isomorphically … + dataset-specific shapes (overlapping-range reads, lint and build outputs, short-window rederivation)" | D3-E1 prereg §3 标题逐字（"与 D3 内部 census 同构 + 数据集特有扩展"）+ E4/E8/E9/E15 定义无内部前身；commit `55494bce` | EVIDENCED |
| 三组细分：S2→E1/E2（归一化层级）；S3→E10/E11（line-set Jaccard ≥0.8）；S1→E12（诊断特征化）与 E13（位置定义） | 两份 prereg 定义逐字对比；E11 定义含 "Jaccard ≥0.8"；fde05652 "D0 terminal intuition broadened beyond terminal_state classifier which only matched 15% per D2 Q1=0"；D3-E3 分账 + 不变量 E1⊆E2、E11⊆E10、E14⊆E3（V1 验证零违反） | EVIDENCED（S1→E13 尺寸成分为定义级对应，V2 报告定级"中"，故正文用 "refined into … alongside" 而非声称审议记录） |
| "deliberately unconstrained by the internal terminal-summary classifier, which had matched only 15% of sessions" | 内部 census S6 inc=0.152；fde05652 原文；D3-E1 prereg 三重点 "不受现有 terminal_state classifier 约束" | EVIDENCED |
| "The frozen record contains no candidate merges and no rejected-candidate list" | V2 报告 §2/§6（记录核查结论）；两份 prereg 只含入选清单 | EVIDENCED（对记录的否定性陈述，不推测审议过程） |
| "verbatim-comparable across the two released pre-registrations" | 两份 prereg 均入库且逐字冻结 | EVIDENCED |
| "E-numbers follow that pre-registration's enumeration order and do not rank importance" | D3-E1 prereg §3 枚举序（主题分组）；V2 报告 §4-#6 判定 | EVIDENCED |
| "no model in the detection loop" | 两份 prereg "零模型调用"；census 脚本；V1 锚点复现 | EVIDENCED |
| "After the first full census … and a series of mechanism and risk probes" | `fde05652` → D3-E2..E8（cf604d54/0b16c0c6/7d9b343e/35c10393/6e06dd04/e955a76d） | EVIDENCED |
| "six shapes pass the pre-registered gate and form the capability candidate pool; the remaining shapes are measured and reported regardless" | fde05652（pool 6/15：E3/E2/E14/E12/E13/E4；15 类全量普查 + 三重点负发现入档） | EVIDENCED |
| disposition "at a registry freeze that preceded any external use" | `1865a160`（D4-A0：A–E classes + contract，先于 d229a6a4/168b7a86 外部验证） | EVIDENCED |
| A–E 五类定义句、AgentDiet 对照句、dataset-independence contract 句、class C 句 | 原句保留（registry `abcde_classes`/`reason`；`dataset_independence_contract` 原文；nearest-work-matrix） | EVIDENCED（未改动） |
| 删除/纠正的四处旧措辞 | 见 §4 扫描结果 | — |

**未引入的禁止主张核查**：新文本无 "merge/converged/consensus/human coding/excluded candidates were …" 类表述；"no candidate merges and no rejected-candidate list" 为对记录缺失的如实披露。S1→E13 映射以 "refined into … alongside"（定义级对应）表述，未声称审议过程（对应 V2 报告"中"级置信的限定措辞）。

## 3. 中文对应版本（完整翻译，供内部核对；论文本身为英文）

**Construction（§3.1 重写版）**

第一段：本分类体系的构建分为两个预注册阶段。我们首先在一个探索性形态普查中考察了内部自然工作负载 Agent 会话中天然出现的输出形态——来自七个真实工作批次的 158 个带会话遥测的 session（计划宇宙约 256 个 session；有遥测的 158 个构成实际分母）——按形态而非能力名标注：大工具输出（S1）、命令重跑（S2）、多轮重跑验证（S3）、重复读取（S4）、即时重读（S5）、终端摘要形态（S6）、大失败/成功测试输出（S7/S7b）、搜索扇出（S8）；候选门（incidence ≥20% 且中位载荷 ≥1,000 chars）先于任何聚合冻结。该阶段是探索性的：只有通用大工具输出形态通过门；普遍存在的命令重复被证明载荷很小（中位 311 chars），多轮重跑验证很稀少（1.3%），测试输出族在可用遥测字段下未产生内部事件（如实记录），大搜索输出已被已有已交付能力覆盖。第二份预注册——先于对公开 discovery 语料的任何聚合而冻结——随后将该形态集合按数据集 schema 允许的范围同构扩展，并加入少量数据集特有形态（重叠区间读取、lint 与 build 输出、短窗重推导）。冻结文本中记录了三处定义级细分：命令重复按归一化层级拆分（精确 E1 / 去数字 E2）、重复验证按输出稳定性拆分（行集合 Jaccard ≥0.8：E10/E11）、通用大输出形态细化为带诊断标记的变体（E12）与基于位置的轨迹末端大输出形态（E13，刻意不受内部终端摘要 classifier 约束——后者仅命中 15% 的 session）。冻结记录中不存在候选合并，也不存在被否决候选清单；内部到外部的形态对应关系可在两份公开预注册之间逐字比对。最终定义集包含 15 个形态；E 编号遵循该预注册的枚举顺序，不表示重要性排序。

第二段：每个形态都是*机械可检测*的：作用于可观察轨迹结构的确定性规则——精确与去数字命令重复、共享文件路径、输出大小阈值、轨迹位置、文本 pass/fail 与诊断标记——检测回路中无模型，因此相同输入总是产生相同判定。在对 15,000-session discovery 语料完成首次全量普查（六个形态通过预注册门并构成能力候选池；其余形态无论入池与否均被测量并报告）以及一系列机制与风险探查之后，每个形态在一个先于任何外部使用的注册表冻结点被赋予*显式能力处置*：可由已交付或冻结候选原语压缩（A 类）、仅可由未来语义原语压缩（B）、因下游轮次依赖内容而不安全（C）、按体量低价值（D）、无实质机会（E）。因此，本分类并非先前判断式轨迹分类（如 AgentDiet）那种自由格式的"浪费"清单：每个形态既是可复现的测量目标，又是可行动的——或显式不可行动的——压缩目标，这正是 RQ4 能力覆盖分析得以机械化计算的原因。分类及其检测器在数据集独立性契约下**先于外部验证冻结**（形态定义必须原封应用于任何外部数据集；此后发现的形态标记为 post-hoc-discovered 并仅在下一个数据集上验证），此后未被修改。检测器只作用于可观察轨迹结构；不推断模型内部状态；检测不意味着可安全删除——C 类形态恰恰因为不安全才被测量。完整检测规则、逐形态注册表字段与支持级别见 Supplement A。

## 4. Provenance 用语扫描（旧措辞零残留）

扫描模式：`iteratively consolidating` / `discovery order` / `recorded at freeze time` / `converged on 15` / `derived the taxonomy` / `by scanning tool observations`。

- **活文件（参与论文与证据链）**：tex、md、rq-claim-evidence-matrix.json、paper-tables.json、figures.json、supplements/* → **全部 0 命中**。
- `paper-claim-trace.md` 唯一命中为 amendment 注记中对已纠正措辞的引述（有意保留的文档记录）。
- **历史记录（不修改，仅列示）**：`final-submission-preflight-report.md`（上一轮版式会话的过程记录，正是旧措辞的引入点，留作 provenance）、`taxonomy-origin-audit.md`、`taxonomy-validity-audit.md`、`taxonomy-paper-expansion.md`、`taxonomy-construction-v2-report.md`（审计/报告文档本身引用旧措辞作分析对象）。
- PDF 提取文本（8/8 页）：新措辞全 PRESENT（含空白归一化复核 "registry freeze that preceded any external use"）；六条旧措辞全 clean。

## 5. 编译与一致性检查日志

- clean rebuild：删除 aux/out/bbl/blg/log/pdf → `pdflatex → bibtex → pdflatex ×2`（MiKTeX）。
- 结果：**8 pages / 533,499 bytes**（≤10 页预算；bibtex 0 error，页码类 warning 与上一轮同源）。
- log：**0 errors / 0 undefined references / 0 overfull boxes**。
- thoughtworks2026 引用保留核查：原 Construction 段是该条目唯一 `\cite` 点；重写后移入 "public discovery corpus (Thoughtworks …~\cite{thoughtworks2026})" 句，bbl 正常渲染。
- PDF 文本审计（pypdf）：15 条新表述全 PRESENT、6 条旧表述全 clean（含 whitespace 归一化二次核对）。
- 定量主张零变化核查：claim-trace C01–C40 数值主张全部未动；本任务仅 C02 artifact 引用扩展 + 方法叙述重写。

## 6. 判定

通过标准逐项核对：所有改写具有可核对证据（§2 ledger）✓；未扩大研究方法主张（明确 158 实现值、无合并/共识/排除清单主张、S1→E13 用限定措辞）✓；编译通过（8 页 / 0-0-0）✓；旧错误表述零残留（§4）✓。frozen artifacts 零改动 ✓。无法回溯的主张（S→E 审议细节、被否候选）保持不宣称 ✓。
**判定：PASS。** 按任务要求，commit 后 STOP，不继续类别关系分析或其它论文改写。
