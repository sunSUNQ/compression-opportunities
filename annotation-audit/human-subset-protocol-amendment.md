# D4-P3R5 — Human Construct-Validity Subset Protocol Amendment（FROZEN）

状态：**AMENDMENT FROZEN**（2026-09-24，早于 subset packet 生成）。

## 1. 与原始 340-item protocol 的关系

```text
原始 protocol           construct-validity/annotation-protocol.md（FROZEN，不变）
原始 340-item pack      保留不删除（blinded packets A/B 不覆盖）
本 amendment            从 340 items 中选一个 information-enriched subset
                        用于 human construct-validity validation
model audit 角色        仅用于选样（identify disagreement/boundary cases）；
                        model labels 不向 human annotators 展示；
                        不用于 adjudication；不作为 ground truth
```

## 2. Primary construct-validity metric（重要调整）

```text
Q1（shape membership）= PRIMARY construct-validity metric
  验证的是：detector 判定的 operational shape membership 是否
  与人类判断一致

Q2（compression opportunity）= SECONDARY semantic judgment
  验证的是：检测到的结构是否构成有意义的压缩机会（更高层的
  semantic judgment，预期 agreement 低于 Q1）

Q1 与 Q2 的差异本身就是一个有价值的 finding（如果出现）：
  structural opportunity detection can be operationalized reliably,
  while the semantic value of compression remains a separate and
  more judgment-dependent question.
```

## 3. Subset composition（冻结规则）

```text
目标总量 ~150 items（不强行凑整）

Priority 1（全部纳入）：
  ① GLM Q1 ≠ GPT Q1 的 disagreement cases
  ② 任一模型 Q1 或 Q2 = UNCERTAIN 的 cases
  ③ GLM = GPT 但 ≠ detector prediction 的 cases
     （models agree, detector differs = construct-validity risk）
  ④ E13 的 boundary/disagreement cases

Priority 2（补充至 ~150）：
  ⑤ detector = GLM = GPT positive 的 random sample
     （六核心 shape 均须有 control）
  ⑥ detector = GLM = GPT negative 的 random sample

分 shape 配额：不机械均分；按 disagreement 密度自然分布；
  但六核心 shapes（E1/E2/E3/E12/E13/E14）至少各 5 items。
```

## 4. Blinding（冻结）

human packets 中不得出现：
- GLM/GPT label 或 model 身份
- detector prediction
- disagreement bucket 分类
- selection reason
- TASCO capability status
- 论文结论

每 item 仅包含：anonymous session ID / trajectory position / tool
command / observation excerpt / previous events / target shape name。

## 5. 预期产出

```text
construct-validity/human-subset/human-manifest.json
construct-validity/human-subset/human-A.json
construct-validity/human-subset/human-B.json
```

完成后等待两名独立人类标注者。Agent 不伪造标注结果。
