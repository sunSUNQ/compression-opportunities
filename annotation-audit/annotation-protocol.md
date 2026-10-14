# D4-P3R2 — Detector Construct-Validity Annotation Protocol（FROZEN）

状态：**PROTOCOL FROZEN**（2026-09-24）。本 protocol 在生成任何
annotation packet 之前冻结。此后 sampling、packet generation、
annotation、adjudication 均按本 protocol 执行，不可修改。

**当前状态：ANNOTATION_PACK_READY — 等待两名独立人类标注者。**
当前 Agent 不伪造双人标注结果。

---

## 1. 目标

验证 OSW 20K census 使用的 E1–E15 frozen detectors 是否确实
检测到了其声称测量的 compression-opportunity construct。

三个验证问题：
1. Detector 判定为某 shape 时，人类是否认同？
2. Detector 未判定时，是否存在明显漏检？
3. 两名独立 annotator 的一致性如何？

## 2. Sampling design（冻结）

```text
来源     OSW 20K census（v2 manifest，sample-id-set 601318a7）
总量     300 instances（15 shapes × 20/shape 目标；不足则全取正例
         并补 matched negatives）
分层
  A 高频核心（E1/E2/E3/E12/E13/E14）：每 shape 15–20 positive
    + 5–10 negative/near-miss
  B 中低频（E5–E11/E15）：≥10 positive（不足则全取）+ matched
    negatives
  C 边界：threshold 附近 / near-duplicate command / path
    normalization 边界 / late-vs-not-late / large-output threshold
    附近 / test-build-lint 分类边界——每个边界类 ≥3 items
seed     42
抽取逻辑 seed=42 随机抽样，按 shape 分层，正/负例比例按
  detector 实际命中分布
```

## 3. Annotation unit（冻结）

每个 item 包含：

```text
- anonymous_session_id（脱敏后 UUID）
- trajectory_position（第 N / 共 M 个事件）
- relevant_tool_command（仅命令行，无 model/scaffold 信息）
- relevant_observation（工具输出，截取前 2000 chars + 后 500 chars）
- previous_events（前 3 个事件的 cmd + obs 截断至 200 chars）
- detector_predicted_shape（此字段在 packet 中隐藏）
```

Annotator 不应知道：
- detector 预测的 shape
- TASCO capability support
- Paper A 结论
- production/research coverage

## 4. Annotation questions（冻结）

```text
Q1  Does this instance satisfy the formal definition of shape Ex?
    YES / NO / UNCERTAIN
    （Ex 在 packet 中标明——标注者评估的是"是否属于该类"）

Q2  Does this instance contain a genuine context-compression
    opportunity under the paper's definition?
    YES / NO / UNCERTAIN
    注意：不问"can it be safely deleted?"

Q3  If Q1 = NO, error category:
    detector_false_positive / taxonomy_definition_ambiguity /
    insufficient_context / schema_ambiguity / other

Q4  Confidence: 1 (low) – 5 (high)
```

## 5. Annotators（冻结）

两名独立人类标注者。第一轮完全独立（不得边标边讨论），完成后再做
disagreement adjudication。

必须保存：raw annotator A / raw annotator B / adjudicated label。

**当前状态：Agent 无法模拟两名独立人类标注者。本轮不伪造标注
结果。等待真实第二位标注者。**

## 6. Metrics（冻结）

```text
Detector precision  TP / (TP + FP)
  分 shape precision / macro precision / pooled precision
Sampled false-negative estimate  FN / sampled negatives
  仅称 sampled FN estimate，不宣称全 corpus recall
Inter-rater agreement  Cohen's κ
  shape-membership agreement + opportunity-presence agreement
  如 imbalance 导致 κ 异常，同时报告 raw agreement + positive
  agreement / prevalence
Uncertain rate
```

## 7. Validation gate（解释性，不触发 detector tuning）

```text
STRONG                   pooled precision ≥0.90; core shapes ≥0.90;
                         κ ≥0.80
ACCEPTABLE_WITH_LIMITATION  precision ≥0.80; κ ≥0.60; defects in
                         identified boundary cases
VALIDITY_CONCERN         precision <0.80; κ <0.60; systematic FP
                         in core shapes
```

## 8. E13 专项（冻结）

E13 是 Paper A 最重要的 scaffold result，必须单独报告：
- late-position 判定是否符合 formal definition（后 25% 位置）；
- large-output 判定是否合理（≥2000 chars）；
- annotator 是否认同它确实构成 compression opportunity；
- 是否存在"large but semantically indispensable"导致含糊。

E13 validation 目标 = 证明 detector 正确识别了论文定义的
opportunity construct，**不是**证明它能安全压缩。

## 9. 如果 annotation 暴露 detector 问题

如发现某核心 detector precision 明显不足 / taxonomy definition
歧义 / false-negative 系统性严重：
本轮记 CONSTRUCT_VALIDITY_CONCERN → STOP。
不自动修改 detector（修改 = census 重跑 = 新 amendment）。
