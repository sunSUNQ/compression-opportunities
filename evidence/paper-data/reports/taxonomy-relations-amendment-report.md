# PAPER-A-TAXONOMY-RELATIONS-AMENDMENT — 修订报告

日期：2026-10-10。依据：`taxonomy-relations-v1-report.md`（PASS）、`v1-taxonomy-scan-{tw,osw}.json` 不变量、`taxonomy-v1-overlap-matrix.csv`、A0 冻结检测器、D3-E3 multi-label union ledger / anti-inflation 设计记录（commit `0b16c0c6`）。
边界核查：detectors、thresholds、shape IDs、census、RQ1–RQ5、figures、历史证据 **零改动**；未追加新的研究结论（全部关系陈述来自 relations-v1 报告的既有分级）。
判定：**PASS**（§5）。独立 commit 后 STOP。

---

## 1. 修改文件（sha256-16 前/后）

| 文件 | 前 | 后 | 变更 |
|---|---|---|---|
| `paper-draft-v1-icse.tex` | `29dc6ea436c66327` | `834bec7f927daf1f` | §3 新增 `\subsection{Non-Exclusive Shape Semantics and Overlap Accounting}`（Taxonomy Overview 与 LLM Audit 之间） |
| `paper-draft-v1-icse.md` | `e1a5d157af36ebdf` | `0ffc657437016ad4` | 同步 markdown 段落 |
| `supplements/supplement-A-detectors.md` | （前值见 git） | `47603d1e49e8ea21` | 新增 "Shape relations and multi-label semantics" 子节 |
| `paper-claim-trace.md` | `42157751200d2e08` | `d15fa927192b720e` | 新增 C41 行 + amendment 注记 |
| `paper-draft-v1-icse.pdf` + aux/out/bbl/blg/log | `5e416228f6419faf`（pdf） | `af5090742878904b`（pdf） | clean rebuild |

## 2. Claim-to-Evidence Ledger（分级标注；正文仅保留构造性蕴含与定性交叉，观察性数字全部留在 Supplement A）

| 正文/补充主张 | 分级 | 证据 |
|---|---|---|
| "Shapes are concurrent morphology labels, not a strict tree"（非互斥、非树） | 操作性陈述 | D3-E3 prereg/commit `0b16c0c6`："shape multi-label in union ledger"、"cross-shape overlaps reported"（设计记录）；A0 检测器掩码语义（多 bit） |
| E1 ⊆ E2（by construction） | **LOGICAL_IMPLIES** | 键嵌套（norm ⇒ digit-norm）；全量反例搜索 0 违反（TW 233,334 / OSW 600,181 E1 事件；`v1_taxonomy_validation.py` L306-308，扫描件 sha `407db29b24447c7b`/`447c684196acf4b5`）；会话 containment 1.0 |
| E14 ⊆ E3、E4 ⊆ E3（by construction） | **LOGICAL_IMPLIES** | 后件/区间重叠 ⇒ path 组 ≥2；0 违反（66,081 / 154,643 E14 事件；E4 TW 29,088/29,088=1.0；OSW E4 结构不可测） |
| E11 ⊆ E10（by construction） | **LOGICAL_IMPLIES** | E11 仅在 E10 组内标记；0 违反（22 / 11 事件） |
| "exhaustive counterexample search … zero violations" | EVIDENCED | 扫描器全事件掩码检查，两语料全量；谓词实现 = 冻结 verbatim（锚点 TW 14/14、OSW 15/15） |
| "a late-trajectory output can itself be a large diagnostic (E12∩E13)"、"repeated failing command produces both" | **INTERSECTION**（观察性，正文定性不给数字） | overlap CSV：TW 3,930 事件/7,249 会话、OSW 1,648/7,531；E12∧E1/E2 OSW 28,381–29,995 事件（数字仅在 Supplement A） |
| "four distinct denominators"（session incidence / event hits / character allocation / session-level COC） | 操作性陈述（代码直证） | 各自实现：census 会话计数、per-shape 掩码位、split 分摊（conventions_note 明文不与 COC 混用）、`v011_d4a1_census.py coverage()` |
| "allocation … splits each event's observation length equally … sum exactly to the measured characters" | **EVIDENCED（守恒）** | 三帧两语料 Σsplit = labeled 精确成立：TW 859,174,937.9≈859,174,938、OSW 1,782,349,136.0、A1R2 920,214,270.8≈920,214,271；detected+4 桶 = total（1,239,474,486） |
| "unsafe shapes excluded from qualified denominators" | EVIDENCED | `coverage()` verbatim（q_shapes 排除 E7/E12）+ d4a1 `definition_note` |
| "not safe-compression rates, not deletable-character volumes, not token savings" | 措辞纪律 | d4a1 `definition_note`（"coverage accounting proxy, not an exact byte-offset union or directly measured safely deletable bytes"）；论文 Metrics 段既有表述 |
| Supplement A 多标签统计：≥2 标签事件 319,843/578,283 = **55.31%**；含多标签会话 14,825/15,000 = **98.83%**；assignments 883,658 | **A1R2 权威帧只读重算**（任务步骤 6 要求） | 冻结 A1R2 检测块字节切片 exec（零转写）+ pinned parquet `3dd8ec3546cf771c`；与冻结 census 精确互证（unique events 578,283 ✓、per-shape events 逐 shape 相等 ✓、census sha `630dcfaae0bca521`）；分母显式记录（事件级 = 全部解析事件；会话级 = 全部 15,000 session） |
| 未引用旧帧多标签占比 | 合规 | relations-v1 报告 §7 的 42% 草稿数字**未进入任何文件**；正文与新 Supplement A 均使用 A1R2 帧数字 |
| 14 行真实例样表 | EVIDENCED | V1 例样池（5 条，seed 冻结）+ relations 审计只读挖掘（9 行，冻结块 exec；全部带语料/session/event 出处；E8 合成例明确排除在外） |

**禁止项核查**：无 "merged/converged/consensus/excluded candidates" 主张；未把观察重叠表述为逻辑证明（INTERSECTION 数字只出现在 Supplement A 且标注 observed, not logical）；无新研究结论（全部内容为 relations-v1 报告已分级事实的转写）；统计数字与 frozen artifacts 零变化。

## 3. 中文对应段落（§3.2 新增小节）

**非互斥形态语义与重叠计量。** 形态是并发的形态学标签，而非严格树：一条观测可以同时满足多个冻结谓词，且逐形态计数绝不可跨形态相加。三个包含关系由构造保证而非观察得出：每个精确重复（E1）必然是去数字重复（E2）；每个同文件重读后件（E14）与每个区间重叠读取（E4）必然是同文件重读（E3）；未变验证（E11）只在重复验证组（E10）内部标记。对两语料全部解析事件的穷举反例搜索零违反。形态亦跨维度交叉：轨迹末端大输出本身可以是大诊断（E12∩E13——任务收尾时的失败报告），重复的失败命令同时产生重复与诊断。计量在构造上抑制多标签重复计算：会话 incidence、事件命中、字符分摊与能力覆盖是四个不同分母，allocation-based byte accounting with overlap control 将每条观测长度在其命中的形态间等份分摊、不安全形态排除在资格分母之外——因此逐形态字符份额恰好加总等于实测字符。这些是覆盖计量份额，不是安全压缩率、可删除字符量或 token 节省；Supplement A 给出完整关系格、adapter 前提与真实事件例样。

## 4. 构建与交叉引用审计

- clean rebuild：`pdflatex → bibtex → pdflatex ×2`：**8 pages / 535,544 bytes**（≤10 页预算）；log **0 errors / 0 undefined references / 0 overfull boxes**；bibtex 0 error。
- 新增 `\label{sec:overlap}` 无悬空引用（未被引用，预留给后续编辑）；全部既有 `\ref`/`\cite` 不变（log 零 undefined）。
- PDF 文本审计（pypdf 8/8 页）：9 条新表述全 PRESENT；正文**无**多标签百分比（42%/55.31%/98.83%/319,843 全 clean——数字仅存于 Supplement A 文档）；无 "mutually exclusive" 类排他性表述。
- 计数夸大扫描：正文逐句核对——三处蕴含均为 "by construction"、一处交叉为定性 "can itself be / produces both"、守恒句为精确等式表述、结尾三连否定（not safe-compression / deletable / token savings）在位。
- 定量主张零变化：C01–C40 未动；新增 C41（方法论/计量语义主张，无新统计数字入正文）。

## 5. 判定

通过标准逐项核对：证据映射完整（§2，含分级标签）✓；无计数夸大（正文无百分比、观察性数字仅入 Supplement A 并标注 observed）✓；clean rebuild 通过（8 页 0-0-0）✓；frozen artifacts 零改动 ✓；未追加研究结论 ✓。
**判定：PASS。** 独立 commit 后 STOP——不继续其它论文改写。
