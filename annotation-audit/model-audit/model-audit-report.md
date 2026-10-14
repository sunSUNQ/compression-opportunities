# D4-P3R4 — Model Annotation Audit Report（SUPERSEDED）

> **Authority status: SUPERSEDED / AUDIT HISTORY ONLY.** This report was computed
> from 292 paired-valid items before 48 GLM retrieval failures were recovered. It
> must not be used as the manuscript, claim-trace, or Supplement authority.
> Final authority: `model-audit-reconciled.json` (340/340 paired valid; overall
> Q1 raw agreement 52.65%, kappa 0.1531; overall Q2 raw agreement 49.41%, kappa
> 0.0003; E13 Q1/Q2 raw agreement 96.4%/78.6%). Historical values below are
> preserved verbatim for audit provenance.

## 1. Arm integrity

```text
GLM (OpenCode + GLM-5.3)   340/340 items, 0 schema violations, 48 data-retrieval errors
GPT (Codex + GPT)          340/340 items, 0 schema violations, 0 errors
item identity              GLM == GPT == manifest (340/340) ✓
blinding leak              'detector_negative' in packet A sample_type field
                           (structural, not answer-key leakage)
observable cross-arm leak  NONE
```

## 2. Inter-model agreement

```text
Q1 shape membership
  raw agreement         54.45% (159/292)
  Cohen's κ             0.2385 (poor)
  distribution          YES/YES 34 | NO/NO 42 | UNC/UNC 83 | disagree 133

Q2 compression opportunity
  raw agreement         57.53% (168/292)
  Cohen's κ             -0.1886 (worse than chance — systematic disagreement)
  distribution          NO/NO 100 | YES/YES 68 | GLM-NO/GPT-YES 124
```

Q2 负 κ 表示两个模型**系统性分歧**而非随机不一致——GLM 系统性判 NO，
GPT 系统性判 YES（或 vice versa），这不是噪声而是对 Q2 定义的根本性
理解差异。

## 3. Per-shape agreement（核心发现）

| Shape | n | Q1 agree | Q2 agree | 解读 |
|---|---:|---:|---:|---|
| E1 exact repeat | 28 | 57% | 39% | 假重复（view 无 path 导致） |
| E2 similar repeat | 28 | 54% | 50% | 同上 |
| E3 file reread | 1 | 0% | 0% | DESCRIPTIVE_ONLY_SMALL_N |
| E12 large diagnostic | 7 | 100% | 71% | 小样本 |
| **E13 late large output** | **28** | **96%** | **79%** | **shape membership 高一致；opportunity 判定分歧** |
| E14 output→reread | 28 | 39% | 18% | 最低 agreement——definition 歧义 |
| E5 same search | 28 | 64% | 75% | |
| E6 test pass | 28 | 25% | 68% | |
| E7 test fail | 28 | 25% | 64% | |
| E8 lint | 8 | 88% | 63% | 小样本 |
| E9 build | 9 | 78% | 67% | 小样本 |
| E10 repeated validation | 28 | 64% | 64% | |
| E11 unchanged validation | 19 | 58% | 63% | |
| E15 rederivation | 16 | 50% | 44% | |

**E13 Q1 agreement 96.4% = 全表最高**——两个模型对"这是否是 late-trajectory
大输出"高度一致，说明 E13 的**形状定义是清晰的**。但 Q2 agreement 79%
说明对"它是否构成 compression opportunity"有分歧——这正对应 D3-E2
的发现（机械去重 3.5%，语义价值不确定）。

E14 Q2 agreement 18% = 全表最低——"output→reread" 的 definition
歧义最大，需要在 future work 中收紧定义。

## 4. Detector ↔ Model unblind

```text
detector-positive → GLM agrees: 84/180 (46.7%)
detector-positive → GPT agrees: 50/180 (27.8%)
both-model-reject (det pos, both NO): 0
both-model-accept (det neg, both YES): 34
```

detector 标记为 positive 的 180 items 中：
- GLM 认可 84 个（46.7%）
- GPT 认可 50 个（27.8%）
- 两模型均认可的比例更低

detector false-positive rate 很高——detector 判为 positive 的
事件中，超过半数被模型标注者拒绝。

## 5. Bucket 分布

```text
Bucket A (detector=GLM=GPT, all positive)     34 (10.0%)
Bucket B (GLM=GPT≠detector)                    74 (21.8%)
Bucket C (GLM≠GPT)                            133 (39.1%)  ← 最大
Bucket D (any UNCERTAIN)                        9 (2.6%)
Bucket E (det pos, both reject)                 0 (0.0%)
Bucket F (det neg, both accept)                 0 (0.0%)
```

Bucket C 最大（39.1%）= 两个 AI 模型对同一 observation 的 shape
membership 判断就有 39% 分歧——说明 shape 定义边界模糊是核心问题，
而非某一个模型的错误。

## 6. E13 专项

```text
E13 shape membership (Q1): GLM 96.4% agree with GPT（高一致）
E13 opportunity (Q2): GLM/GPT agreement 79%（低于 Q1）
E13 detector positive → GLM accepts 20/28, GPT accepts 20/28
E13 "large but semantically important" cases: 需人工复核
```

## 7. MODEL AUDIT VERDICT

```text
MODEL_AUDIT_CONCERN
```

理由：
- Q1 κ = 0.2385（远低于 0.60 ACCEPTABLE 线）
- Q2 κ = -0.1886（负值 = 系统性分歧）
- Bucket C（模型间不一致）= 39.1%（最大 bucket）
- 核心 shapes 中 E14 Q2 agreement 仅 18%

但以下方面表现良好：
- E13 shape membership 一致性 96.4%（定义清晰）
- E12 small-n 内 100% shape agreement
- A/B correctness 24/24 无退化

## 8. 对 Paper A 的含义

1. **compression-opportunity construct 本身具有主观性**——两个 AI
   模型对同一 observation 是否构成 opportunity 有 39% 分歧，说明
   "compression opportunity" 不是一个客观存在的实体，而是依赖于
   评估框架和定义口径的构念。
2. **detector precision 需人工验证**——模型标注 ≠ 人类判断；
   48 ERR + 弱 footer 检查 + path-aware normalization 差异都
   可能导致系统性偏差。
3. **F1 的 trajectory variance finding 被强化**——如果 AI 模型
   之间就有 39% 分歧，那么模型与人类之间、甚至同一模型两次运行
   之间的方差只会更大。这证实了 online task-token qualification
   在当前条件下不可行。
4. **E13 shape membership 定义清晰**——可以作为 taxonomy 中
   定义最明确的 shape 保留，但需要单独验证其作为 compression
   target 的实际价值（E13 semantic primitive = Paper B future work）。
