# Limitations（D4-P0 冻结）

以下 limitation 与正文 claim 同时冻结；论文/汇报使用对应结论时必须
一并披露。

## L1 — 评价框架边界（RQ4）

E13 2×2 证明的是**本次 evaluation frame 内的 association /
controlled contrast**（两个 corpus、两个 scaffold、两个 model 的
特定组合），不证明对所有 agent architecture 的普遍因果关系。
scaffold 效应方向跨模型一致，但 interaction 16.5pp 表明模型会调制
scaffold 效应幅度。

## L2 — 低 incidence shapes 的判定噪声（RQ3）

E5/E6/E7/E10/E11 的 MODEL_SENSITIVE 判定基于低 incidence（0.03%-2%）
下的比值，受小样本波动影响大；这些判定的置信度低于核心六 shapes
（E1/E2/E3/E12/E13/E14 比值 0.68-1.013）。

## L3 — E4 NOT_MEASURABLE ≠ negative result（RQ2）

Open-SWE-Traces 的 tool_calls 不含 view_range 字段，E4
（overlapping-file-read）detector 无法机械应用。这是 schema 限制，
不是"重叠读取不存在"的证据。Thoughtworks 侧 E4 incidence 27.7%
（基于 args path，无 range）同样低估了 range 级重叠。

## L4 — RDS 状态边界（RQ5）

RDS = CAPABILITY_CANDIDATE / DEFAULT_OFF（D3-E8）。research coverage
（+candidate SOC 100%/COC 90.13%）**不得**与 production coverage
（shipped-only SOC 2.07%/COC 0.39%）混写。D5 aggregate +7.38% 为
NON-QUALIFYING OBSERVATION（permutation p=0.1185、nonneg 54%、
first-divergence 先于 marker、机制暴露 0.011%），禁止进入任何
release benefit claim。

## L5 — 领域外推边界（RQ1/RQ2）

taxonomy 的发现（Thoughtworks）与验证（Open-SWE）均来自
**coding-agent trajectories**（SWE 任务、PR 修复类）。外推到非
coding-agent workload（如通用 chat、数据分析、写作任务）需另行
census，本文数据不支持该外推。

## L6 — detector 规范化口径差异（RQ2）

Open-SWE 侧 E1/E2/E3/E14 使用 path-aware cmd 规范化（bug fix 后）；
Thoughtworks 侧为原始 detector 口径（view 类命令未含 path）。两侧
对比方向性成立，但 E1/E2 的 TW 值可能被规范化差异抬高——精确对比
需以同口径重算 TW（列为 future work，不在 P0 中解决）。

## L7 — 在线功效结论的适用范围（RQ5）

E7 power 结论（28% within-task 噪声、0.011% 机制暴露、power<0.80）
来自 deepseek-v4-flash + claude-code + SWE-rebench 工作负载。
其他 model/agent/工作负载的噪声与暴露量不同，需重新执行 E7 方法
（方法可复用，结论不直接迁移）。
