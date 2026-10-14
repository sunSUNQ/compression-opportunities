# D4-P0 — Paper Evidence Freeze（FROZEN，终态）

> **SUPERSEDED-FOR-DISPLAY (2026-10-10, PAPER-A-NUMBERS-UPDATE):** the RQ1/RQ2
> discovery-side numbers below are the D4-P0 freeze-frame values (pre-klear-recovery
> two-source parse). Display authority for TW discovery incidence and cross-corpus
> replication bands migrated to **V0.11-D4-A1R2** (`v011-d4a1r2-tw-klear-census.json`,
> sha256-16 `630dcfaae0bca521`; prereg `e98345d748ac7620`; regression gate PASS; A0
> detectors zero changes): 8 of 13 measurable shapes satisfy the pre-specified bands;
> all six core shapes REPLICATED (full-precision ratios 0.81-1.35); five sparse shapes
> E6/E7/E10/E11/E15 DATASET_SPECIFIC (corpus-composition-sensitive). OSW-side, model,
> scaffold, factorial, and coverage values unchanged. The frozen content below is
> retained verbatim as superseded provenance.

状态：**D4-P0 = PAPER_EVIDENCE_FROZEN**（2026-09-24）。零新增实验、
零 detector/capability 修改；全部数字自 frozen artifact 引用。

## 1. 冻结证据包清单

```text
evidence/V1/paper/paper-evidence-freeze.md          本文档
evidence/V1/paper/rq-claim-evidence-matrix.json     RQ→claim→metric→artifact 全链
evidence/V1/paper/paper-tables.json                 T1-T6 论文表格数据
evidence/V1/paper/paper-figures-data/figures.json   fig1-fig6 图表数据
evidence/V1/paper/limitations.md                    L1-L7 冻结 limitation
```

## 2. RQ → 答案摘要（P0R1 aligned；每条可追溯至 matrix）

**RQ1（Natural opportunity prevalence）— YES**：核心大 payload 形态 E12
（60.1%/79.5%）、E13（53.3%/46.6%）与高频重复形态 E2/E3/E14
（62-100%）在两个独立公开 corpus 上均高 incidence；
E1-E15 taxonomy 11/12 measurable shapes REPLICATED/PARTIAL。

**RQ2（Cross-corpus reproducibility）— 主要高频机会形态在两个独立
Coding-Agent trajectory corpus 中得到复现**：11/12 shapes
REPLICATED/PARTIAL；E6 DATASET_SPECIFIC；E4 NOT_MEASURABLE（schema
字段缺失，非 negative result）。

**RQ3（Cross-model stability）— 核心形态不依赖 model**：六核心 shapes
（E1/E2/E3/E12/E13/E14）在两个 scaffold 内均为 MODEL_STABLE
（比值 0.68-1.013）；稀疏 shapes 的 MODEL_SENSITIVE 判定受小样本
比值噪声影响（L2）。

**RQ4（Scaffold modulation）— 显著调制**：E13 的 scaffold-associated
variation（mean 28.2pp）> model-associated variation（mean
12.7pp），interaction 16.5pp；仅在本次 evaluation frame 内成立（L1）。

**RQ5（Existing capability coverage）— shipped 覆盖接近零，gap
集中在重复交付形态**：production shipped-only **SOC 2.07% / COC
0.39%**；research +RDS candidate **SOC 100% / COC 90.13%**；
**Capability Gap Rate 99.57%**——RDS = CAPABILITY_CANDIDATE /
DEFAULT_OFF，production 与 research coverage 禁止混写（L4）。

**F1（Secondary finding）— Offline→online observability /
variance limitation**：within-task 随机轨迹方差（median 27.96%）≫
机制暴露（median 0.011%，signal:noise 0.0003）；3%/5% 效应在 ≤10
reps 内 power < 0.80；RDS 在线 A/B correctness 干净但 token benefit
NOT_ESTABLISHED；+7.38% = NON-QUALIFYING（L4/L7）。

## 3. 系统（TASCO）定位

- implementation/system：V0.10 GA payload（10 shipped capabilities）
  + RDS candidate（env-gated default OFF，工程基线 289,822 events /
  0 重构失败 / capture 0.8098）
- coverage 结论（Minimax 20K）：production shipped-only SOC 2.07% /
  COC 0.39%；research +candidate SOC 100% / COC 90.13%；Gap Rate
  99.57%——**shipped 能力对自然重复交付机会近乎零覆盖**是核心 gap
  发现（跨模型稳定）。

## 4. Provenance

```text
detector freeze   1865a160（A0 registry）
D3 链             a741673/43f4afea（E1 内部）→ 55494bce/fde05652（E1
                  external）→ cf604d54/b8dfc2d9（E2）→ 0b16c0c6/
                  b8a41cdf（E3）→ 7d9b343e/fe0706b9（E4）→ 35c10393/
                  21735560/3d593b06（E5）→ 6e06dd04/53a4a820（E6）→
                  e955a76d/6ac31a3f（E7）→ 42073396（E8 freeze）
D4 链             1865a160（A0）→ d229a6a4/126159c4（A1 manifest）→
                  675294e6（Am2 HOLD）→ 3c6c14ed（R1 closure）→
                  168b7a86（A1 census）→ 2c174416/6802ca14（A2）→
                  74b3b6a7/d15c3272（A2R1）
manifests         TW sessions.parquet 325,563,194 B；OSW v1.0 37/37
                  shards footer-ok（90,422 traj）；v2 20K manifest
                  895a96c0（sample-id-set 601318a7）
本 freeze commit  见 git log（P0 evidence commit）
```

## 5. 停点

STOP。P0 冻结后允许进入**论文正文/汇报成稿**（引用本包，不产生新
数字）；E13 semantic primitive 与 RDS 触发量扩展均为独立 future
work（需新授权 + 新 prereg）。
