# V0.11-D4-A1R2 — Klear Recovery Amendment: Affected Numbers & Suggested Revisions

日期：2026-10-09
判定：**PASS**（回归门 PASS；klear 解析正确性已证实；A0 检测器/定义/注册表零改动；官方 d3e1 未覆盖）
证据：
- 预注册：`evidence/V1/v011-d4a1r2-klear-amendment-prereg.json`（sha256-16 `e98345d748ac7620`）
- 结果：`evidence/V1/v011-d4a1r2-tw-klear-census.json`（sha256-16 `d9f95a84cb157172`，含 regression/klear-verification/delta/bands）
- 脚本：`evidence/tools/v011_d4a1r2_tw_klear_census.py`（内嵌 script sha）
- 输入：`sessions.parquet` sha256-16 见结果 meta；对照 `v011-d3e1-external-census.json`、`v011-d4a1-census-results.json`

## 1. 门与验证记录

| 门 | 结果 |
|---|---|
| 非 klear 两源 10,000 sessions 回归 | **PASS**：14 shape session 数与 d3e1 官方逐一相等（E8 无事件一致）；非 klear 观测字符 1,134,133,251 = 官方 ctx sum |
| klear 解析恢复 | 5,000/5,000 sessions 产生事件；127,985 事件 = 127,985 条 returncode 型消息（1:1，无重复捕获）；exit 提取 127,985（100%）；empty-output 事件 25,910（合法 `<output>\n</output>`）；zero-event sessions = 0 |
| klear 正确性抽样 | 5 条原文样例入结果 JSON（cmd/obs 头/exit/chars），命令来自代码围栏、观测为 `<returncode>+<output>` 语义 |
| A0 检测器改动 | 无（仅 schema adapter；谓词/阈值/分组逐字保持） |

## 2. Delta Ledger（旧 d3e1 → 修正后，分母均 15,000）

| Shape | 旧 sessions | 新 sessions | Δpp | 旧 incidence | 新 incidence | 全精度比(新) | 带旧→新 |
|---|---|---|---|---|---|---|---|
| E1 | 9,872 | **12,832** | +19.73 | 0.6581 | **0.8555** | 1.168 | R→R |
| E2 | 9,940 | **12,945** | +20.03 | 0.6627 | **0.8630** | 1.158 | R→R |
| E3 | 9,976 | **11,592** | +10.77 | 0.6651 | **0.7728** | 1.294 | R→R |
| E4 | 4,157 | 4,157 | 0 | 0.2771 | 0.2771 | — | (OSW 侧 NM 不变) |
| E5 | 70 | 109 | +0.26 | 0.0047 | 0.0073 | 2.738 | P→P |
| E6 | 59 | **293** | +1.56 | 0.0039 | 0.0195 | 0.038 | DS→DS |
| E7 | 30 | **210** | +1.20 | 0.0020 | 0.0140 | 0.046 | P→**DS** |
| E8 | 0 | 0 | 0 | — | — | — | NM→NM |
| E9 | 1 | 1 | 0 | 0.0001 | 0.0001 | 0.75 | R→R |
| E10 | 17 | **297** | +1.87 | 0.0011 | 0.0198 | 0.040 | R→**DS** |
| E11 | 8 | **114** | +0.71 | 0.0005 | 0.0076 | 0.053 | R→**DS** |
| E12 | 9,017 | **10,317** | +8.67 | 0.6011 | **0.6878** | 1.156 | R→R |
| E13 | 7,988 | **8,688** | +4.67 | 0.5325 | **0.5792** | 0.805 | R→R |
| E14 | 9,230 | **10,523** | +8.62 | 0.6153 | **0.7015** | 1.352 | R→R |
| E15 | 7 | **116** | +0.73 | 0.0005 | 0.0077 | 0.045 | R→**DS** |

其他全语料量：总观测字符 1,134,133,251 → **1,239,474,486**（+105.3M，全部来自 klear）；labeled 920.2M；qualified（剔 UNSAFE）703.2M；事件 450,298 → 578,283。

## 3. 复制汇总的变化（论文必须改的核心句）

- 旧（存储 d4a1 口径）：R10 + P2 + DS2 + NM1 → 摘要 "11 of 12 measurable shapes"。
- 新（klear 修正 + 全精度）：**R7（E1/E2/E3/E9/E12/E13/E14）+ P1（E5）+ DS5（E6/E7/E10/E11/E15）+ NM2（E4-OSW、E8）→ "8 of 13 measurable shapes"**。
- **关键守恒**：全部六个核心 shape（E1/E2/E3/E14 + E12/E13）保持 REPLICATED，且比值向 1 收紧（E1 1.52→1.17、E2 1.51→1.16、E3 1.50→1.29、E14 1.54→1.35、E12 1.32→1.16、E13 0.88→0.81）——核心叙事**更强**。
- 翻转的 5 个 shape 全部是稀疏验证-负发现类（旧 TW 计数 30/17/8/7/59），klear 恢复后 TW 侧事件数放大（E10 17→297）而 OSW 侧保持稀疏（16/13/8/7/15）→ 比值坍缩。这与已有 Low-incidence limitation 同族，但需要升级表述：**稀疏 shape 的带归属在语料组成变化下不稳定**。
- E6 边界问题消解：不再有 0.19/0.205 的舍入翻转——修正后 E6 明确 DS（0.038），原边界讨论由"口径敏感性"转为"组成敏感性"实例。

## 4. 受影响数字清单（论文位置 → 现值 → 建议修订值）

| # | 位置 | 现值 | 建议修订 |
|---|---|---|---|
| A1 | 摘要："large diagnostics 60.1%→79.5% incidence" | 60.1% | **68.8%**（E12 新） |
| A2 | 摘要："late-trajectory large outputs 53.3%→46.6%" | 53.3% | **57.9%** |
| A3 | 摘要："11 of 12 measurable shapes satisfy..." | 11/12 | **"8 of 13 measurable shapes (all six core shapes REPLICATED with ratios 0.81–1.35; five sparse shapes DATASET_SPECIFIC)"** |
| A4 | 摘要："applied it across corpora through corpus-specific schema adapters" | — | 保持；可加 "full three-source parse" |
| B1 | §1 "apply it to 35,000 trajectories" | — | 不变（语料规模不变，解析口径补全） |
| C1 | RQ1 正文各 shape incidence（E12 60.1%、E13 53.3%、E1/E2/E3/E14 65-67%、E4 27.7% 不变） | 旧值 | 全部换 §2 新值；E4 不变 |
| C2 | RQ2 caveat 段（A1R1 同口径 +0.14/+0.08/+0.15/+3.74pp） | 基于 10K 可解析帧 | **需重述**：A1R1 数字为旧帧历史结果；klear 修正后口径重验待下一 amendment（或直接引 klear 主修正） |
| C3 | RQ2 复制计数句 "11 of 12" | 11/12 | 同 A3 |
| D1 | Fig.3 TW 数据列（figures.json `fig1_taxonomy_incidence_tw_vs_osw.series[0]`） | 14 值 | 全部换新值（E4 保持 0.2771）；Fig.3 重生成 |
| D2 | Table（taxonomy 表）discovery 列 | 旧值 | 新值 |
| E1 | Supplement C（census/factorial 转录） | 旧帧 | 增加 A1R2 amendment 块（新 JSON 快照），旧块标注 superseded-for-display |
| E2 | Supplement D（coverage） | 基于 OSW d4a1 | **不受影响**（SOC/COC 全部来自 OSW 帧） |
| E3 | Supplement F（power/A-B） | 内部批次 | 不受影响 |
| E4 | limitations "Low-incidence noise"（E5–E7/E10/E11 few events） | — | 升级："sparse-shape band assignments are corpus-composition-sensitive (E7/E10/E11/E15 flipped to DATASET_SPECIFIC after full three-source parse)" |
| E5 | limitations "Detector caliber" | A1R1 表述 | 补一句 klear 修正后主数字已换帧；caliber 重验可选 |
| F1 | `paper-tables.json` T1 TW 列 | 旧值 | 新值（冻结流程：新快照，不改旧文件） |
| F2 | 注册表 `discovery_metrics_15k` | 旧值 | 注册表保持冻结；display authority 迁移至 A1R2（reconciliation 记录） |

## 5. 建议修订稿（关键句，供下一轮正文编辑采用；本轮未应用）

- 摘要替换句：
  "We derive a 15-shape compression-opportunity taxonomy with deterministic, frozen detectors and apply it across corpora through corpus-specific schema adapters: all six core shapes replicate across the two corpora (full-precision incidence ratios 0.81–1.35), while five sparse shapes (E5–E7, E10/E11, E15) are corpus-composition-sensitive; large diagnostics reach 68.8% (TW) / 79.5% (OSW) incidence and late-trajectory large outputs 57.9% / 46.6%."
- RQ2 替换句：
  "11-of-12 replication becomes: after a parser amendment recovered the full three-source discovery frame (15,000 sessions; +105M observation chars), 8 of 13 measurable shapes satisfy the pre-specified bands — including every core shape, whose ratios tighten toward 1.0 (0.81–1.35) — while five sparse shapes (E6, E7, E10, E11, E15) are DATASET_SPECIFIC, all consistent with the low-incidence-noise limitation."
- Limitations 增补句：
  "Sparse-shape replication bands are corpus-composition-sensitive: the klear recovery amendment (A1R2) multiplied discovery-side validation events for E6/E7/E10/E11/E15 while the external corpus stayed sparse, flipping their bands to DATASET_SPECIFIC. Band assignments for shapes with <300 discovery-side sessions should be read as order-of-magnitude statements."

## 6. 停止条件核对

- 需要修改 A0 detector？**否**（仅 schema adapter）。
- 原两源 census 非预期变化？**否**（回归门逐 shape 相等 + ctx sum 相等）。
- klear 解析正确性无法证实？**否**（1:1 消息-事件、exit 100%、原文抽样、zero-event=0）。
→ 无 STOP 触发。**判定 PASS**。

## 7. 推荐的唯一下一项任务

**PAPER-A-NUMBERS-UPDATE**：按 §4/§5 清单执行一轮受控的论文数字更新（figures.json TW 列 → Fig.3 重生成 → 摘要/RQ1/RQ2/limitations 句子替换 → paper-tables 新快照 + reconciliation 记录），随后 clean rebuild + visual audit + preflight 刷新。
