# PAPER-A-NUMBERS-UPDATE — Reconciliation Report (V0.11-D4-A1R2 klear recovery amendment)

日期：2026-10-10。上游：PAPER-A-TAXONOMY-P0 → `v011-d4a1r2-affected-numbers.md`（判定 **PASS**，2026-10-09）。
终态判定：**PASS**。Submission readiness：**NOT submission-ready-by-this-task** — 本任务完成受控数字同步与 clean rebuild；投稿前仍需既有 preflight 流程的最终刷新（见 §7）。

---

## 1. 权威输入与 hash 校验

| 产物 | sha256-16 | 校验结果 |
|---|---|---|
| 预注册 `evidence/V1/v011-d4a1r2-klear-amendment-prereg.json` | `e98345d748ac7620` | 与 affected-numbers.md 记录一致 ✓ |
| 结果 `evidence/V1/v011-d4a1r2-tw-klear-census.json` | **`630dcfaae0bca521`** | 见下方勘误说明 |
| 脚本 `evidence/tools/v011_d4a1r2_tw_klear_census.py` | `9d599d820038311d` | 与 census `meta.script_sha256_16` 一致 ✓ |
| 输入 parquet `D:/tasco-temp/d3_hf_data/sessions.parquet`（325,563,194 bytes） | `3dd8ec3546cf771c` | 与 census `meta.input_parquet_sha256_16` 一致 ✓ |
| 上游 d3e1 官方 `v011-d3e1-external-census.json`、d4a1 `v011-d4a1-census-results.json` | （未改动） | 仅读取对照 ✓ |

**Hash 勘误（非 STOP 项）**：`v011-d4a1r2-affected-numbers.md` 为 census JSON 记录的 sha256-16 为 `d9f95a84cb157172`，与磁盘文件（`630dcfaae0bca521`）不符。处置：以冻结 prereg + pinned parquet + 冻结脚本做**确定性重放**（仅重定向输出路径，未触碰任何冻结文件），重放输出与冻结 census JSON **byte-for-byte 一致**（LF 归一化后 `True`；replay sha16 = `630dcfaae0bca521`）。结论：冻结 census 为该（prereg, parquet, script）三元组的真实确定性产物，`d9f95a84cb157172` 为 affected-numbers.md 中的**陈旧 provenance 注记（erratum）**，权威 hash = `630dcfaae0bca521`。重放中 regression gate PASS、klear 验证（127,985 事件 1:1、exit 100%、zero-event=0）逐项复现。**无权威统计冲突、无分母异常（两帧分母均 15,000）、无冻结证据覆盖 → 无 STOP 触发。**

上游 PASS 链：prereg（FROZEN before recompute）→ census（regression_gate.pass=true）→ affected-numbers.md（判定 PASS，"本轮未应用"）→ 本任务（应用）。

## 2. Source-of-truth 数字映射（A1R2 census，分母 15,000）

| Shape | 旧 TW sessions | 新 TW sessions | 旧 TW inc | 新 TW inc | 全精度比（新） | 带旧→新 |
|---|---|---|---|---|---|---|
| E1 | 9,872 | 12,832 | 0.6581 | 0.8555 | 1.1685 | R→R |
| E2 | 9,940 | 12,945 | 0.6627 | 0.8630 | 1.1585 | R→R |
| E3 | 9,976 | 11,592 | 0.6651 | 0.7728 | 1.2938 | R→R |
| E4 | 4,157 | 4,157 | 0.2771 | 0.2771 | — | MEASURABLE_ONLY（不变） |
| E5 | 70 | 109 | 0.0047 | 0.0073 | 2.7385 | P→P |
| E6 | 59 | 293 | 0.0039 | 0.0195 | **0.0384** | DS→DS |
| E7 | 30 | 210 | 0.0020 | 0.0140 | 0.0464 | P→**DS** |
| E8 | 0 | 0 | — | — | — | NM→NM |
| E9 | 1 | 1 | 0.0001 | 0.0001 | 0.75 | R→R |
| E10 | 17 | 297 | 0.0011 | 0.0198 | 0.0404 | R→**DS** |
| E11 | 8 | 114 | 0.0005 | 0.0076 | 0.0526 | R→**DS** |
| E12 | 9,017 | 10,317 | 0.6011 | 0.6878 | 1.1559 | R→R |
| E13 | 7,988 | 8,688 | 0.5325 | 0.5792 | 0.8052 | R→R |
| E14 | 9,230 | 10,523 | 0.6153 | 0.7015 | 1.3518 | R→R |
| E15 | 7 | 116 | 0.0005 | 0.0077 | 0.0453 | R→**DS** |

- 复制汇总：**R7（E1/E2/E3/E9/E12/E13/E14）+ P1（E5）= 8 of 13 measurable**；DS5（E6/E7/E10/E11/E15）= DATASET_SPECIFIC；NM2（E4 OSW-schema、E8）。
- **六个核心 shape 全部保持 REPLICATED**，比值向 1 收紧（0.81–1.35）；摘要/RQ2/结论明确"六个核心复现"，**未**声称 taxonomy universally replicates；五个稀疏 shape 明确标注 corpus-composition-sensitive（DATASET_SPECIFIC）。
- **E6 全精度判定**：0.0384（未取整），明确 DS；旧 0.19/0.205 舍入边界讨论消解，显示值仅用于出版格式。
- OSW 侧全部不变（79.5%/46.6% 等，d4a1 authority）。

对 amendment 建议句的一处修正：affected-numbers.md §5 摘要建议句将稀疏 DS 集误写为 "E5–E7, E10/E11, E15"（会把 PARTIAL 的 E5 错误划入 DS）；本任务采用正确集合 **E6, E7, E10, E11, E15**（与 §3/§5-RQ2 句一致）。

## 3. 修改位置（文件 → 变更）

| 文件 | 变更 |
|---|---|
| `paper-draft-v1-icse.tex` | 摘要（8/13、六核心 0.81–1.35、五稀疏 DS、68.8/79.5、57.9/46.6、same-caliber 句标注 pre-amendment frame）；Contributions (2)；Intro same-caliber 限定；Fig.3 caption+Description；RQ1 E13 分解句（57.92% + pre-amendment ledger 归属）；RQ1 prevalence 段（68.8/57.9/77.3/86.3/0.77%）；RQ2 答案段重写（8/13、核心复现、klear recovery、E10 17→297 例证）；边界段（E6/E9 稀疏性重述）；caliber caveat 段（A1R1 数字标注历史、A1R2 比值、13-shape）；Finding 2；Limitations Low-incidence（corpus-composition 升级 + <300 sessions 序数表述）；Limitations Detector caliber（klear 换帧 + 重验可选）；Conclusion（core structures 限定 + 0.81–1.35） |
| `paper-draft-v1-icse.md` | 同步以上全部（markdown 孪生）+ 头部 A1R2 amendment 注记 |
| `paper-figures-data/figures.json` | `fig1_taxonomy_incidence_tw_vs_osw.series[0]`（TW 列）→ A1R2 权威 14 值（E4 不变、E8 缺席）；新增 `amendment_authority` 字段；note 更新 |
| `figures/fig3_incidence.pdf/.png` | 仅经 `generate_figures.py::fig3()`（无硬编码数字）从上述 figures.json 重建 |
| `paper-tables.json` | T1 TW15K_incidence 列 14 值 + replication_band 列（E7/E10/E11/E15→DS）+ note（A1R2 authority、median 为 pre-amendment ledger、E6 全精度 0.0384）+ sources；文件级 `amendment` 块。**T2–T6 零改动** |
| `paper-tables.pre-a1r2.json` | **新增**：更新前 paper-tables.json 的 byte-identical 快照（sha256-16 `ccf174ebc8fa591e`），superseded provenance |
| `supplements/supplement-C-census-factorial.md` | 顶部 AMENDMENT 总注记；Discovery census 块标 SUPERSEDED-FOR-DISPLAY（原文保留）；A1R1 节 display-authority 迁移注记；**新增 A1R2 amendment census 节**（prereg/census 链接、gates、关键 JSON 快照、band 读数、E6 边界消解、registry 冻结说明） |
| `supplements/source-inventory.json` | 追加 2 条（A1R2 prereg + census）；bundled 副本与源 byte-identical（`e98345d748ac7620` / `630dcfaae0bca521`） |
| `paper-claim-trace.md` | C03/C04/C05/C13/C14/C15/C16/C17/C19 更新至 A1R2 authority；PAPER-A-NUMBERS-UPDATE amendment 行 |
| `rq-claim-evidence-matrix.json` | RQ1 values（E12 0.6878、E13 0.5792、E2 0.863、E3 0.7728）+ artifact；RQ2 claim（8/13、R7+P1、DS5、composition-sensitive）；`amendment_authority` 字段；detector_version 限定补注。RQ3/RQ4/RQ5 零改动 |
| `paper-evidence-freeze.md` | 顶部 SUPERSEDED-FOR-DISPLAY banner（D4-P0 冻结原文逐字保留） |
| `paper-draft-v1-icse.pdf` + `.aux/.log/.out/.bbl/.blg` | clean rebuild（见 §5） |
| `refs.bib`、`submission-preflight-status.md` | 上一轮 preflight 会话的未提交一行修正（SWE-bench 作者勘误 / superseded banner），因 bbl 一致性随本 commit 收编；本任务零内容改动 |
| 注册表 `v011-d4a0-taxonomy-registry.json`（`discovery_metrics_15k`） | **零改动**（F2：display authority 迁移至 A1R2，以此报告为证） |
| limitations.md（D4-P0 冻结） | **零改动**；正文 Limitations 为 paper-facing authority（banner 模式一致） |

## 4. 文件 SHA（修改前 → 修改后，sha256-16）

| 文件 | 前 | 后 |
|---|---|---|
| paper-draft-v1-icse.tex | `86155f247e33ecf6` | `d042198429d67c29` |
| paper-draft-v1-icse.md | `becb66845b75c795` | `d06c1427bae888d2` |
| paper-figures-data/figures.json | `1dde08b168039ec4` | `7bcb29826bc584a9` |
| paper-tables.json | `ccf174ebc8fa591e` | `63328233664c217f` |
| figures/fig3_incidence.pdf | `8efc484bded7618d` | `723f6f66861fc878` |
| figures/fig3_incidence.png | `5d6c0c456fe43aee` | `4457e7eed3bfdd07` |
| supplements/supplement-C-census-factorial.md | `d108b7592a614b0e` | `708d38d8c5727269` |
| paper-claim-trace.md | `b996defa03fba870` | `ed0333adf0afaa53` |
| rq-claim-evidence-matrix.json | `d11532cfd9f892b4` | `ce454f0a62970a18` |
| paper-evidence-freeze.md | `48278659b544183c` | `6788b36db0141788` |

## 5. 验证命令与结果

1. **Hash 校验**：`Get-FileHash`（prereg ✓、script ✓、parquet ✓；census 勘误见 §1）。
2. **确定性重放**：wrapper 导入冻结脚本、仅重定向 OUT → 重放输出与冻结 census byte-identical（sha16 `630dcfaae0bca521`）；`REGRESSION GATE: PASS`，klear 统计逐项一致。
3. **数据绑定校验**：figures.json TW 列 14 值 vs census `session_incidence` → 全部一致（E4 不变、E8 缺席）；paper-tables T1 14 值 + bands vs census（含 E4 0.2771 不变检查）→ 一致（仅 `REPLICATED*` 口径星标差异，属预期）。
4. **Fig.3 重建**：`generate_figures.py::fig3()`（仅此图），无硬编码数字；PNG 非空白（dark-pixel 0.185）；build log 含 fig3_incidence 引用。注：本环境无图像查看能力，Fig.3 审计为数据级+构建级（脚本确定性 + 输入值 14/14 绑定校验）。
5. **Clean rebuild**：删除 `.aux/.out/.bbl/.blg/.log` 后 `pdflatex → bibtex → pdflatex ×2`（MiKTeX）：**8 pages / 531,882 bytes**（≤10 页预算）；log：**0 errors、0 undefined references、0 overfull boxes**；bibtex：0 errors（63 条 page-number 类 warning，与上一轮同源）。
6. **PDF 文本提取审计**（pypdf，8/8 页）：新数字全 PRESENT（8 of 13、68.8、57.9、77.3、86.3、0.81–1.35、1.17/1.16/1.29、corpus-composition-sensitive、klear recovery amendment、full three-source parse、0.77%、293 sessions、13-shape）；旧数字全 clean（11 of 12、11/12、60.1、53.3、53.25、66.5、66.3、0.39% TW、12th measurable、12-shape、0.05%）。
7. **泄漏/匿名审计**：TODO/TBD/PLACEHOLDER/FIXME/内部路径（`D:\tasco`、`C:\Users` 等）0 命中；作者匿名 ✓；citations 渲染 ✓（ACM-Reference-Format 编号出现）；Supplement A/B/F 交叉引用 ✓。

## 6. 停止条件核对

- A0 taxonomy/detector 修改？**否**（A1R2 本身亦为零 detector 改动；本轮仅消费）。
- 重新跑 Agent？**否**（唯一重执行为离线确定性 census 重放，输出至 temp，冻结文件未触碰）。
- 权威统计冲突？**否**（唯一差异为 affected-numbers.md 的 hash 注记 erratum，已由确定性重放裁决）。
- 分母变化？**否**（两帧均 15,000；分母显式写入 supplement C 与报告）。
- 原冻结证据被覆盖？**否**（superseded 模式：pre-a1r2 快照 + banner + verbatim 保留；git 历史完整）。
- preflight 失败？**否**（build/引用/文本/版式审计全过；遗留一项环境注意：构建期间 PDF 被用户 WPS 查看器锁定，经用户关闭后重建成功——非证据问题）。
- 未经验证的新研究主张？**否**（全部数字/表述可溯源至 A1R2 census 或既有冻结 artifact；amendment 建议句的 E5 归类笔误已修正）。
→ **无 STOP 触发，终态 PASS。**

## 7. Submission readiness（如实标注）

- 本任务后：正文/表格/图/补充材料与 A1R2 权威口径一致；PDF clean build 8 页、零 error/undefined/overfull。
- **尚未**重新签署 final submission preflight（上一轮 `final-submission-preflight-report.md` 的检查面需按新 PDF 刷新：figure 视觉复核、版式细节、supplement 链接全量走查）。故本任务**不宣布 SUBMISSION_READY**；建议下一轮 = PAPER-A-PREFLIGHT-REFRESH（对 8 页新 PDF 执行既有 preflight 清单）。

## 8. 范围外观察（不在本任务内，留档）

- `paper-tables.json` T2 行 `B semantic gap (E13)` 的 TW15K_share 列值 0.4663 与 OSW 列相同，而 note 声明 TW class union 未计算（应疑似填入 OSW 值的转录错误，D4-P0 起即存在）。与本 amendment 无关（A1R2 未计算 class union），未改动；需独立授权核实修正。
