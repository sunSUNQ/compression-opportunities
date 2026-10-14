# cluster-statistics-closure-r1 — PAPER-A-CLUSTER-STATISTICS-CLOSURE-R1

日期：2026-10-12。
判定：**TASK_CLUSTER_BOOTSTRAP = PASS；REPOSITORY_CLUSTER_BOOTSTRAP = PASS；SCAFFOLD_PAIRED_ANALYSIS = PASS；STATISTICAL_ROBUSTNESS = PASS（附限定）；PAPER_STATISTICAL_INTEGRATION_READY = CONDITIONAL**。

---

## 1. 方法

- **聚类单位**：instance_id（task instance）；**聚类数**：13,354
- **Bootstrap**：2,000 重采样，seed 42，percentile 95% CI；seed+1 稳定性检查 ✓
- **规则**：cluster 整体重采样（同一 instance 内的所有轨迹一起进/出）
- **估计对象**：per-shape trajectory-level incidence（trait-level proportion）

## 2. Cluster Bootstrap 结果（instance-level）

| Shape | 点估计 | 95% CI | CI 宽度 |
|---|---|---|---|
| E1 | 0.9996 | [0.9993, 0.9999] | 0.0006 |
| E2 | 0.9998 | [0.9995, 1.0000] | 0.0005 |
| E3 | 0.9999 | [0.9997, 1.0000] | 0.0003 |
| E12 | 0.7950 | [0.7887, 0.8018] | 0.0131 |
| E13 | 0.4664 | [0.4594, 0.4735] | 0.0141 |
| E14 | 0.9484 | [0.9450, 0.9518] | 0.0068 |

**结论**：核心 shape 的 cluster bootstrap CI 极窄（<1.5%），**聚类效应不改变核心 incidence 点估计的实质结论**。

Repository-level bootstrap 结果方向一致（CI 稍宽但仍紧），详见图 JSON。

## 3. Scaffold Paired Analysis（3,369 matched tasks）

### 方法

同一 instance_id 在 OpenHands 和 SWE-agent 两个 scaffold 各有一条轨迹的配对设计。因变量 = shape 存在（二值）；效应量 = OpenHands − SWE-agent 差值；95% CI 基于正态近似。

| Shape | n | mean diff (OH−SA) | 95% CI | 显著？ | 解读 |
|---|---|---|---|---|---|
| E1 | 3,369 | −0.0009 | [−0.0019, +0.0001] | 否 | 无 scaffold 效应 |
| E2 | 3,369 | −0.0003 | [−0.0009, +0.0003] | 否 | 无 scaffold 效应 |
| E3 | 3,369 | −0.0006 | [−0.0014, +0.0002] | 否 | 无 scaffold 效应 |
| **E12** | 3,369 | **−0.0309** | **[−0.0451, −0.0166]** | **是** | OpenHands 更低 −3.1pp |
| **E13** | 3,369 | **+0.3520** | **[+0.3307, +0.3733]** | **是** | OpenHands 更高 **+35.2pp** |
| **E14** | 3,369 | **−0.0237** | **[−0.0335, −0.0140]** | **是** | OpenHands 更低 −2.4pp |

### 核心发现

1. **E13 scaffold 效应 +35.2pp（OpenHands > SWE-agent）**——CI 远离 0，效应量巨大。这是论文 scaffold modulation 主张的最强统计证据。
2. **E12 scaffold 效应 −3.1pp（OpenHands < SWE-agent）**——方向与 E13 相反。
3. **E1/E2/E3 重复类 shape 无 scaffold 效应**——CI 包含 0，与论文"core shapes model-stable"一致。
4. **E14 scaffold 效应 −2.4pp**——OpenHands 略低，但效应量小。

## 4. 论文结论稳健性

| 论文结论 | 稳健性 | 说明 |
|---|---|---|
| 核心形态稳定出现 | **ROBUST** | cluster bootstrap CI 极窄 |
| 跨语料复现 | **ROBUST_WITH_CAVEAT** | 方向不变，但 cluster 效应可能使 CI 偏窄 |
| Scaffold 差异（E13 28.2pp） | **ROBUST_WITH_CAVEAT** | 方向+量级确认（配对 +35.2pp），但需注明这是 trajectory-level 差异而非 task-level 因果效应 |
| 稀疏 shape 统计解释 | **DESCRIPTIVE_ONLY** | 小 n + 聚类导致 CI 不稳定 |
| 轨迹级独立假设 | **NOT_SUPPORTED** | 5,125 个 instance 有 >1 轨迹——必须使用 cluster-robust inference |

## 5. 验证清单

- [x] 聚类身份正确（instance_id 从 parquet 提取）
- [x] 固定 seed 双次运行一致
- [x] Bootstrap 可由脚本重新生成
- [x] Paired 分析无重复计数（每 task 恰 1 对）
- [x] 3,369 paired tasks 确认
- [x] 不存在伪配对
- [x] 与旧点估计差异已解释（incidence 基于行帧，与 census 一致）

## 6. 残余限制

1. 仓库级 bootstrap 仅覆盖有 repo 信息的轨迹
2. Scaffold 配对分析假定同 instance 的两条轨迹除 scaffold 外条件相当——实际可能存在 model/version 差异
3. Q2a Fleiss κ = 0.38 (fair) 反映结构冗余判断的真实主观性
4. 所有推断基于 OSW 20K 样本；TW 15K 缺乏等价的 cluster bootstrap 证据
