# Paper Evidence Reconciliation Pass — Authority Closure

状态：**RECONCILIATION_REPORT_COMPLETE / SOURCE_EDITS_APPLIED**（2026-10-08）。

本 pass 只解决 evidence authority、supersession、编号、BibTeX 与 preflight 漂移。
不修改 manuscript，不重跑 detector/experiment，不新增统计量，不改变 frozen numbers，
也不生成 Supplement A–G。本文档取代此前 D4-P5R1 reconciliation report，作为下一轮
正文修订与 Supplement 生成前的唯一 reconciliation authority。

---

## 1. Scope and non-goals

本次核对范围：

- TW/OSW normalization 口径；
- heterogeneous-LLM annotation audit 的最终 authority；
- Qwen acquisition inventory、cross-model 中间结果与 full-factorial 终态的 authority；
- paper figure number 与 frozen figure-data key 的映射；
- `refs.bib` 与 manuscript reference placeholder 的闭合状态；
- submission preflight 的当前真实性；
- 文件地图中 C0/C1 artifact 的可定位性。

明确不做：

- 不执行 same-caliber recalculation、clustered bootstrap、human annotation 或其他新实验；
- 不改变 `PAPER_EVIDENCE_FROZEN` 的数值集合；
- 不把 descriptive criteria 升格为 statistical equivalence；
- 不将 model audit 表述为 human construct-validity validation；
- 不直接修改 `.md`/`.tex` manuscript 或生成 A–G。

---

## 2. Authority decisions

### A1 — TW/OSW normalization caliber

**Authoritative statement：**

> Open-SWE 的 E1/E2/E3/E14 使用 path-aware command normalization；
> Thoughtworks 仍使用 original detector caliber。两侧方向性比较保留，但精确
> incidence ratio 不是 same-caliber comparison；统一重算属于 future work。

Authority：

1. `evidence/V1/paper/limitations.md` L6；
2. `evidence/V1/paper/paper-tables.json` T1 note；
3. `evidence/V1/paper/rq-claim-evidence-matrix.json` 各 claim 的 limitation 字段。

Resolved drift：`rq-claim-evidence-matrix.json` 顶层 `detector_version` 与
`paper-tables.json` T1 note 已按上述 authority 修正。冻结 detector commit `1865a160` 不变。

正文锁定措辞：**descriptive cross-corpus replication under the documented
caliber difference**。不得写 statistical equivalence 或 same-caliber replication。

### A2 — Annotation-audit authority

**Final authority：**

`evidence/V1/paper/construct-validity/model-audit/model-audit-reconciled.json`

终态样本为 340/340 paired valid：

- overall Q1 raw agreement = **52.65%**, Cohen's kappa = **0.1531**；
- overall Q2 raw agreement = **49.41%**, Cohen's kappa = **0.0003**；
- E13 Q1 agreement = **96.4%**；
- E13 Q2 agreement = **78.6%**。

`model-audit-report.md` 是 292-pair、48 GLM items 尚未恢复时的旧报告，
其 Q1 kappa 0.2385 / Q2 kappa -0.1886 **已被 superseded**。该文件只能用于审计历史，
不得再作为 manuscript、claim trace 或 Supplement B 的数值来源。

解释边界：这是 heterogeneous-model interpretation-sensitivity diagnostic，
不是 human ground truth，也不验证 detector precision。正文必须同时报告总体 audit 与
E13-specific 结果，不能只报告 96.4%。

### A3 — Qwen / full-factorial authority

结果 authority 顺序：

1. `v011-d4a2r1-full-factorial.json` — **终态 authority**；SA x Qwen 9/9 shards，
   20,334 trajectories，2x2 四 cell 完整；
2. `v011-d4a2-cross-model.json` — OH x Qwen 15K 与 pre-closure 中间结果；
3. `v011-d4a2-qwen-frame-inventory.json` — acquisition-time snapshot，仅用于记录恢复前状态。

`v011-d4a2-qwen-frame-inventory.json` 已显式标记为 superseded acquisition snapshot；
`v011-d4a2-cross-model.json` 已标记为 pre-closure intermediate。Supplement G 必须基于
`v011-d4a2r1-full-factorial.json` 的最终 manifest/closure 生成。

### A4 — Figure numbering authority

Paper 中实际编号以 `.tex` 引用与 `figures/` 文件名为 authority：

| Paper 编号 | 文件 | frozen figure-data key / 类型 |
|---|---|---|
| Fig. 1 | `fig1_trajectory.*` | conceptual trajectory diagram；`figures.json` 无对应 key |
| Fig. 2 | `fig2_design.*` | conceptual study-design diagram；`figures.json` 无对应 key |
| Fig. 3 | `fig3_incidence.*` | `fig1_taxonomy_incidence_tw_vs_osw` |
| Fig. 4 | `fig4_e13_interaction.*` | `fig3_e13_full_factorial_2x2` |
| Fig. 5 | `fig5_coverage.*` | `fig4_coverage_dual_ledger` |
| Supp. Fig. 6 | `fig6_power_curve.*` | `fig5_power_curve` |

`figures.json` 已增加显式 paper-label → file-stem → semantic-data-key 映射。
`fig2_ae_class_distribution_osw` 与 `fig6_rds_replay_capture` 明确标记为仅有 frozen data、
未映射到已渲染主文 figure；JSON 内部序号不再被解释为 paper 编号。

### A5 — Bibliography authority

Reconciled source state：

- `refs.bib` 已覆盖当前 manuscript 实际点名/编号的 **29 works**，另含 2 个 corpus records；
- manuscript 的 `[1]`–`[29]` 仍是手写编号；
- `.tex` 中 `\\bibliography{refs}` 被注释；
- 当前 PDF 无 References section。

因此 BibTeX inventory 为 **CLOSED**，但 manuscript integration 仍为 **OPEN / NOT
SUBMISSION-READY**。旧 preflight 中“19 entries ready”“unresolved citations = 0”均不成立。
下一轮 manuscript pass 必须：

1. 全部正文引用改为 citation keys；
2. 启用 `\\bibliography{refs}` 并执行 BibTeX/Biber 对应编译链；
3. 确认零 undefined citation 与零手写编号漂移。

本 pass 不补造缺失 bibliographic metadata。

### A6 — Preflight authority

旧 `submission-preflight-status.md` 与旧 reconciliation report 已过期，原因包括：

- MiKTeX 已安装，`xelatex`/`pdflatex` 可执行；
- 当前 PDF 为 6 页，但没有 References section；
- `findingbox` 环境未定义；
- `sec:f1` reference 未定义；
- bibliography 被注释；
- Table 2 右列溢出，figure descriptions/keywords/CCS metadata 未闭合；
- conference metadata 仍为 `Conference '17` placeholder。

当前真实状态：

```text
Evidence numbers          FROZEN（未在本 pass 改动）
Evidence authority        RECONCILED（以本文档决议为准）
Source drift cleanup      COMPLETE
BibTeX inventory          CLOSED
Manuscript citation integration OPEN
LaTeX clean compile       FAIL / NOT ESTABLISHED
PDF visual audit          FAIL / issues identified
Supplement A-G            NOT MATERIALIZED
Submission readiness      NOT READY
```

旧 preflight 的 “sole blocker = TeX environment installation”、
“syntax verified, zero compile errors”、“placeholders = 0”和“PDF audit blocked only by TeX”
全部 superseded。

### A7 — C0/C1 artifact location

文件地图中的 `v011-*` 路径是错误别名；当前 worktree 中的 canonical artifacts 为：

- `evidence/V1/v010-c0-stable-task-line-audit.json` — introduced at commit `1084893da938362a66f37ef8724ebd06af448d97`；
- `evidence/V1/v010-c1-task-level-net-benefit.json` — introduced at commit `6da14a7cf516286f667a4dc35b02d26716f8a620`。

D5、D4 frame reports、D3/D4 frozen artifacts 与上述 C0/C1 均可定位。后续引用不得使用
不存在的 `v011-c0-*` / `v011-c1-*` 别名。

---

## 3. Locked wording for the frozen-evidence path

在不重开 evidence tree 的前提下，后续正文统一采用：

| 避免 | 锁定表述 |
|---|---|
| compressible content（作为已证事实） | detector-defined compression opportunity |
| replicated（未限定） | satisfies our descriptive replication criterion |
| scaffold effect | scaffold-associated difference / variation within the evaluation frame |
| safe-compressible bytes | registry-qualified opportunity bytes |
| validated taxonomy（指 model audit） | mechanically reproducible taxonomy with heterogeneous-model interpretation audit |

标题可以保留为研究问题式的 “What Is Actually Compressible?”，但 abstract、methods、
results 与 conclusion 必须遵守上述测量边界。

---

## 4. Source-cleanup acceptance closure

以下 source-cleanup 已完成；自动 citation pipeline 属于下一轮 manuscript edit，未在本 pass
越界修改：

1. 修正 RQ matrix 顶层 normalization 冲突；
2. 为旧 model audit 与 Qwen inventory 增加明确 superseded 标记或归档说明；
3. 建立稳定的 figure-data key -> paper figure number 映射；
4. refs.bib 与实际引用全集闭合；自动 citation pipeline 留给 manuscript pass；
5. 更新 preflight，使其反映真实 compile/PDF/Supplement 状态；
6. 定位或正式标记 C0/C1 artifacts 为 unavailable；
7. `git diff` 仅包含上述 reconciliation/source-cleanup 范围，无 frozen-number 变化。

下一阶段可执行：

- 主文四块短补充：RQ1 magnitude、E13 decomposition、完整 model audit、
  registry-qualified COC definition；
- 将 replication 统一表述为 descriptive criterion；
- 生成真实 Supplement A–G。

---

## 5. Final verdict

```text
PAPER_EVIDENCE_RECONCILIATION = COMPLETE
FROZEN_NUMBERS_CHANGED         = NO
NEW_EXPERIMENTS                = NO
MANUSCRIPT_CHANGED             = NO
AUTHORITY_CHAIN                = RESOLVED
SOURCE_ARTIFACT_CLEANUP         = COMPLETE
READY_FOR_MANUSCRIPT_AND_SUPPLEMENTS = YES
SUBMISSION_READY               = NO
```

本报告与 `source-artifact-cleanup-report.md` 构成当前 authority contract；旧 D4-P5R1
report 不再代表当前状态。当前 submission state 以更新后的
`submission-preflight-status.md` 为准。
