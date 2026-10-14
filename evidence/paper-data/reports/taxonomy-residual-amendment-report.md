# PAPER-A-TAXONOMY-RESIDUAL-AMENDMENT — Reconciliation Report

日期：2026-10-10。依据：`taxonomy-residual-v1-report.md`（PASS）+ A1R3 权威口径（`v011-d4a1r3-tw-trajectory-census.json` sha256-16 `ae954c032022ca79`；`taxonomy-session-identity-amendment-report.md` sha256-16 `6b6ab4dcf77563bc`）。
判定：**PASS**。commit SHA 见 git log（本轮）。

---

## 1. 证据预检（Step 1）

- A1R3 gates ALL PASS；残差七桶 **A1R3 = A1R2 逐桶精确相等**（census gates 内置断言 + 本轮独立复核）——按任务要求，正文与 Supplement A 一律引用 **A1R3 行帧**为当前权威。
- 分母确认：TW 事件宇宙 578,283 / 字符 1,239,474,486（轨迹行帧；15,000 recorded trajectories / 13,053 unique ids）；OSW 1,296,519 / 2,757,167,294。
- 输入 SHA：residual 报告 `4f8600828cb8ff0f`；session-identity amendment 报告 `6b6ab4dcf77563bc`；A1R3 census `ae954c032022ca79`；A1R3 prereg `4561f8297aa3512d`；A1R2 census `630dcfaae0bca521`；本任务前 tex `d594200daab0cf70`、Supplement A `49ce9b59dd5e1ffa`。

## 2. 修改位置与内容（Step 2–4）

| 位置 | 变更 |
|---|---|
| `paper-draft-v1-icse.tex` §3.2 末尾 | 新增 `\paragraph{Residual coverage and boundary.}`（约 150 词）：LUO 占未命中字符 70.0%（TW）/ 73.8%（OSW）（A1R3 residual accounting）；构造性刻画（无会话内精确/相似命令重复、无同 path 组）+ "predominantly single-delivery large outputs" + **桶是混合体、不主张同构**；未命中 ≠ 不可压缩；检测 ≠ 安全压缩；指向 Supplement A |
| `paper-draft-v1-icse.tex` Limitations | 新增 `\textbf{Coverage boundary.}` 条（15 shapes 非穷尽；detectors 对部分单次结构化输出与跨轨迹重复不敏感；残差池 = post-hoc hypotheses，非已验证扩展） |
| `paper-draft-v1-icse.md` | 以上两处 markdown 孪生同步 |
| `supplements/supplement-A-detectors.md` | 新增 "Residual accounting and coverage boundary" 小节：七桶 TW/OSW 全量表（含 uncovered 合计与 totals）、守恒句、LUO 构成分解（cclass/长度带/位置/来源/scaffold 两语料）、结构性刻画、五条 detector 边界表、11 条真实例样（corpus/session/event + 判读）、boundary vs speculative 区分（post-hoc hypotheses；无 E16；未命中≠安全可压缩≠不可压缩） |

不变项：E1–E15 定义/detectors/阈值；A1R3 census；OSW；RQ1–RQ5 结论与数字；Fig.1–6；T1–T6；8/13 复制判据；core six 结论；rq-claim-evidence-matrix；claim trace（本轮无新 claim 行——残差段为边界陈述而非定量主张，其数字全部可溯源至 residual-v1 报告与 A1R3 census）。

## 3. 中文对应段落（§3.2 新增）

**残差覆盖与边界。** 该分类体系是十五个冻结 shape 上的测量工具，而非观测内容的穷尽划分。未被任何谓词命中的事件记入固定残差桶；主导桶 *large-uncovered-other*（≥2,000 字符且无 shape 命中）占 discovery 语料未命中观测字符的 70.0%、Open-SWE 的 73.8%（A1R3 残差计量；Supplement A）。由重复谓词的构造可知，这些事件在会话内没有精确或相似命令重复、也没有同 path 组；它们以"单次交付的大型输出"为主——目录树、文件内容、搜索结果集、依赖与工具日志——但该桶是残差混合体，不主张其成员共享同一结构。未命中不等于不可压缩：它只说明冻结谓词未找到会话内机械锚点，而语义结构或跨轨迹规律仍可能提供机会；反之，被检测也不意味着可安全压缩。Supplement A 给出七桶全量账本、检测器边界分析与真实事件例样。

**Limitations 新增（中文对应）**：**覆盖边界。** 十五个 shape 不穷尽观测内容：大型未命中输出作为残差记账（Supplement A），而非不可压缩内容。当前检测器按构造对部分单次交付的结构化输出与跨轨迹重复不敏感；残差池激发的是待未来数据集验证的 post-hoc 假设，而非已验证的分类扩展。

## 4. Claim-to-Evidence Ledger

| 主张 | 分级 | 证据 |
|---|---|---|
| LUO 占未命中字符 70.0%（TW）/ 73.8%（OSW） | EVIDENCED | A1R3 census residual_buckets（29,925/223,431,268；110,359/719,563,215）；未命中合计 319,260,215 / 974,818,158；residual-v1 报告 §2 |
| LUO 事件"构造性无会话内重复锚点" | EVIDENCED（构造性推论） | E2/E3 冻结谓词无条件覆盖任意 csim ≥2 组与 path 组 ≥2 → 未命中 ⇒ csim 唯一 ∧ 无 path 组 |
| "predominantly single-delivery large outputs (directory dumps, file contents, search result sets, dependency and tool logs)" | EVIDENCED（hedged） | cclass 构成（other/view/search）+ 11 条分层抽样真实例样（residual 报告 §4） |
| "the bucket is a residual mixture … not asserted to share one structure" | 边界声明 | 例样异质性（树 dump vs 文件 dump vs 搜索集 vs heredoc 回显 vs 下载日志） |
| 未命中 ≠ 不可压缩；检测 ≠ 安全压缩 | 操作性纪律 | 与 §3.2 既有 coverage-shares 纪律一致；C 类"因不安全才被测量"对称 |
| 五条 detector 边界（命令分类/阈值/窗口/重复谓词/schema） | EVIDENCED | residual 报告 §5（mvn 2,669、compound 命令、klear nl|sed 族、E4/E8） |
| 残差池 = post-hoc hypotheses（非 E16、非已验证扩展） | 边界声明 | dataset-independence contract；任务边界 |
| 七桶数字表 + 例样表 | EVIDENCED | A1R3 census（residual_buckets 与 A1R2 相等断言）+ residual 报告 §2/§4 |

## 5. 一致性审计（Step 5）

- 全局不当主张扫描：`exhaustive taxonomy of` / `uncovered … incompressible`（肯定式）/ `safely compressible residual` / `E16` → 全部 clean。
- A1R3 权威口径引用：§3 残差段标注 "(A1R3 residual accounting; Supplement A)"；Supplement A 节头声明 A1R3 authority + 与 A1R2 相等断言。
- 无变化验证：8/13（3 处）、core six ratios 0.79–1.28、Fig.3（本任务未触碰 figures.json/fig3 文件）、RQ3–RQ5、T2–T6、coverage 数字全部未动。
- JSON/markdown 编码核查：Supplement A 追加段非 ASCII 字符 = em-dash×15、→×1、§×1（全部合法 UTF-8，无 mojibake）。

## 6. 构建与版面（Step 6）

- clean rebuild：pdflatex + bibtex + pdflatex ×2 → **9 pages / 539,190 bytes**（≤10 页预算 ✓）；log **0 errors / 0 undefined / 0 overfull**；bibtex 0 error。
- PDF 文本审计：新表述 10 条全 PRESENT；不当主张 4 条全 clean；匿名/泄漏 clean。
- 版面余量：新增 ~150 词 + Limitations 条后仍 9 页，无需压缩；未删任何证据、未缩小字号。

## 7. 文件 SHA（修改前 → 修改后，sha256-16）

| 文件 | 前 | 后 |
|---|---|---|
| paper-draft-v1-icse.tex | `d594200daab0cf70` | （见 commit diff） |
| paper-draft-v1-icse.md | （见 git） | （见 commit diff） |
| supplements/supplement-A-detectors.md | `49ce9b59dd5e1ffa` | （见 commit diff） |
| paper-draft-v1-icse.pdf | （前值 git） | （见 commit diff） |

## 8. 判定

STOP 条件核对：输入 provenance 一致 ✓；数据守恒一致（A1R3=A1R2 残差逐桶精确）✓；正文主张全部有证据且限定措辞到位（混合体声明、非穷尽声明、双向不可推定）✓；关键数字零漂移（8/13、core six、Fig.3、RQ1–RQ5 未动）✓；版面满足（9 页 ≤10）✓。
**判定：PASS。** **STOP**——不继续 Annotation Audit；等待下一轮独立授权任务。
