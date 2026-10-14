# postfreeze-evidence-augmentation-report — PAPER-A-POSTFREEZE-EVIDENCE-AUGMENTATION-R1

日期：2026-10-13
授权：作者授权，在**不引入任何新实验、只使用冻结工件**前提下增强 Paper A 可解释性与说服力；
正文 10 页预算不含 references；supplement/appendix 可扩展 representative cases。

## 1. 新增内容清单与放置理由

| # | 内容 | 位置 | 理由 |
|---|---|---|---|
| 1 | **Annotation unit case 卡片图**（`fig_case_annotation_unit`，packet `M-TW-E13-detector_positive-0`） | 主文 §3.5，multi-agent 段落之后 | 把 §3.5 的 κ 数字落到一个真实冻结样本：冻结 E13 定义 + 真实 target 事件（sphinx-gallery 复现长输出）+ 三通道盲评（一致 YES/NO/YES）。直接回答"标注到底怎么做的" |
| 2 | **RDS replay capture 图**（`fig_rds_replay_capture`，3 横条） | 主文 §8 第一段后 | §8 引用 218M chars / oracle capture 0.8098 但无图；图中 69.4M/85.7M 的比值 0.8098 由断言锁定，即正文 oracle-capture 数值的来源分解 |
| 3 | **T6 紧凑表**（`tab:qualification`，3 行） | 主文 §8，simulation 段落后 | §8 三个资格验证尝试（D3-E7/D3-E5/D2）原为散文，表格化后可核对；同时挂接 Supplement~D |
| 4 | **Supplement B：3 张补充 case 卡**（S1 `M-OSW-E3-detector_positive-82`、S2 `M-TW-E12-detector_positive-54`、S3 `M-OSW-E13-negative_or_nearmiss-66`）+ T7 agreement 表 | supplements/supplement-B-model-audit.md 末尾新节 | S1 展示 Q2a 分歧、S2 展示 Q2a 全体 NO（检测阳性但三通道均判非冗余）、S3 near-miss 展示 Q2a/Q2b 真实分歧——与 κ=0.38 "construct ambiguity" 叙事互相印证 |
| 5 | **Supplement C：A–E class distribution 汇总表** | supplements/supplement-C-census-factorial.md 末尾新节 | 未渲染冻结数据键 `fig2_ae_class_distribution_osw`（OSW 侧）；TW C/D 格如实标 UNRESOLVED（T2 冻结状态），不做推断 |
| 6 | **Supplement D（新文件）：T6 资格验证明细账** | supplements/supplement-D-qualification-feasibility.md | 主文紧凑表的逐字段版本；同时如实记录"主文引用 Supplement F 但该文件不存在"的预存缺口 |

主文 prose 变更（最小化，仅为挂接新图表）：
- §3.5 加 1 句 "Figure~\ref{fig:case-annotation} walks through one frozen annotation unit end to end..."
- §8 加 2 句（RDS 图引导句 + T6/Supplement~D 引导句）；caption 与 \Description 全部新写，数值均来自冻结工件

## 2. 数据一致性核查（全部 PASS）

**20/20 表格数值断言 PASS**（tools/postfreeze_augment_figures.py 中对 paper-tables.json T6/T7 与
figures.json A–E 的逐值断言，TeX 中手写表格数字与冻结 JSON 一致）。

**Case 卡溯源**（4 单元）：
| Packet | 账本 sha16（packet_hashes.json）= 磁盘实测 | 三通道运行时快照 sha（一致） | 判定 EVAL-1/2/3 |
|---|---|---|---|
| M-TW-E13-detector_positive-0 | `920c4be9def6aa4d` ✓ | `8d0dc28872f3f0e2` | YES/NO/YES ×3 |
| M-OSW-E3-detector_positive-82 | `51b0db5cc88b11ca` ✓ | `871978b9ca046824` | Y/Y/Y · Y/N/Y · Y/Y/Y |
| M-TW-E12-detector_positive-54 | `2663a4990209c708` ✓ | `4043c9bcfbd356b6` | YES/NO/YES ×3 |
| M-OSW-E13-negative_or_nearmiss-66 | `d98a7dad25ca940e` ✓ | `6d027c3791c0fcc9` | N/Y/Y · N/Y/N · N/N/N |

**披露**：三通道结果文件记录的运行时 packet 快照 sha 与账本 sha 不同（各 case 内三通道完全一致），
与"运行后 packet 文件被重新序列化"一致；卡片渲染的实质字段（冻结定义、target 事件）取自账本
packet，与运行时判定 rationale 引用的轨迹位置/观察内容一致。已在 Supplement B 中如实披露。

**RDS 断言**：85,724,720 / 69,417,330 / 218,043,264 字节逐一断言；比值 round(69417330/85724720,4)=0.8098 断言通过（即 §8 的 oracle capture）。

## 3. 编译结果与页数核查

验证构建（jobname `-augmented`，因正式 PDF 被阅读器锁定）：

| 构建 | 总页数 | 正文边界 | errors | overfull | undefined cites | 图 |
|---|---|---|---|---|---|---|
| paper-a-candidate-r1-augmented.pdf (`0dce2b87b5b977e5`) | 11 | **Conclusion 止于 p10**，References p10–11 | 0 | 0 | 0 | 7 张全部装入 |
| paper-a-clarity-revised-en-augmented.pdf (`223546f9ff9b9bae`) | 11 | Conclusion 止于 p10，References p10–11 | 0 | 0 | 0 | 7 张全部装入 |

**页数核查：正文（不含 references）≤ 10 页，恰好卡线满足 venue 要求**；references 溢出至第 11 页不计入预算。
7 张图（5 旧 + 2 新）在两份编译 PDF 中缩放矩阵实测均为 **1.0000**（WYSIWYG 链路保持）。

修复记录：T6 表初次编译 2 处 overfull（判定列过窄 + 列宽总和超限），改列宽配比 0.21/0.44/0.25 后清零。

## 4. 交付物

- 新图 10 件（5× PDF+PNG，`figures/`）：sha 见 `figure-inventory.csv`（已追加）
- 主文 tex 双版本更新（candidate + clarity-revised-en，同步编辑）
- Supplement B/C 追加、Supplement D 新建
- 生成脚本 `tools/postfreeze_augment_figures.py`（含全部断言）+ 审计输出 `figures/postfreeze_augmentation_audit.json`
- 验证构建件 `paper-a-*-augmented.pdf/.log/.aux/.bbl`（正式件写回待解锁）

## 5. 待办与边界

- ~~正式 PDF 写回被阻塞~~ **已完成**：作者关闭阅读器后以正式 jobname 重编译，11 页 / 0 errors /
  0 overfull / 0 undefined，逐页文本与验证构建比对**完全一致**（SHA 差异仅为内嵌时间戳）：
  - `paper-a-candidate-r1.pdf` sha16 `4ca5449e98efbe29`
  - `paper-a-clarity-revised-en.pdf` sha16 `b20c4a712a3874d7`
- 无新实验、无新数据、无结论变化；仅使用冻结工件；不提交 commit。
- 预存缺口记录：主文引用的 Supplement F（resampling procedure）无对应文件——已在 Supplement D 中披露，未擅自代写。

**STOP** —— 正文（不含 references）10 页达标，正式 PDF 已写回；等待作者审阅与提交授权。
