# longrun-annotation-plan.md — PAPER-A-MULTI-AGENT-LONGRUN-ANNOTATION-V1（冻结执行计划）

日期：2026-10-12。授权：用户明确授权在隔离工作目录内连续执行 Pilot 与正式 120-item 三通道标注；禁止越界扩大权限/范围/预算。

## 0. 冻结输入（sha256-16）

| 输入 | sha256-16 |
|---|---|
| multi-agent-validation-protocol-v1.md | `09c1243740e03b45` |
| multi-agent-packet-schema-v1.json | `29f25a6d347b8602` |
| multi-agent-pilot-manifest.json（120 items） | `5d54eb69461cd14c`（冻结抽样 sha `3c559d3c1eb61bb8`，三次独立重生成一致） |
| three-channel-binding.json | `e74c5199dcb25164` |
| A1R3 census | `ae954c032022ca79` |
| OSW census / A0 registry | `7d22b0b98062cc8c` / `57e71b310f75f416` |
| annotation-validity-v1-report / statistics amendment | `71d67ee570b94251` / 统计工件 `de30138fa71414a0` |
| three-channel R1/R2 报告 | R1 `56adab67f7dfd994`（前值）/ R2（本轮前最新） |

## 1. 三通道绑定（冻结，不得变更）

| 通道 | Agent CLI | 后端模型 | 调用方式（冻结） |
|---|---|---|---|
| EVAL-1 | Codex CLI 0.162.0-alpha.2（`...\Codex\bin\979a96ce184041d1\codex.exe`） | gpt-5.6-sol（provider openai） | `codex exec --skip-git-repo-check --sandbox read-only -c project_doc_max_bytes=0 -o <last_message> <prompt>`；cwd=中性目录；stdin=DEVNULL；timeout 900s |
| EVAL-2 | OpenCode CLI 1.18.35（真实 exe） | glm-5.3（Volcano 网关，served glm-5-3-260814） | `opencode.exe run --pure -m 火山AI网关/glm-5.3 <prompt>`；timeout 900s |
| EVAL-3 | Claude Code CLI 2.1.280（claude.cmd） | deepseek-v4-flash（api.deepseek.com/anthropic；transport-confirmed） | `claude.cmd -p --model deepseek-v4-flash --max-turns 3 --disallowedTools <全部内置> `；**prompt 经 stdin**（.cmd 8K argv 截断规避）；timeout 900s |

binding 证据：R1 报告 + R2 closure（EVAL-1 binding 三元组 + 2/2 smoke；EVAL-3 transport response.model=deepseek-v4-flash；EVAL-2 2/2 smoke）。

## 2. Prompt 模板（冻结；逐字符使用，不得修改）

System prompt = `PROMPT_TEMPLATE`（见 `longrun_frozen_config.json` 的 `prompt_template` 字段；与 three-channel smoke 相同文本：定义 + 三问 + 严格 JSON 三键输出 + 禁工具 + canary 句）。User 内容 = packet JSON（`target_shape` + `events`）。每通道 canary 唯一（`CANARY-EVAL{n}-<run hex>`）。

## 3. Packet 生成（冻结）

- 120 个 manifest item 各生成 1 个 packet：从冻结帧（TW parquet 行 / OSW manifest 行）解析事件，取 `items[].event_idx` 目标观测（头 2,000 + 尾 500 chars）+ previous_events（≤3 × 200 chars）+ paired_context（E3/E14/E4/E15：配对事件全文头 300 + gap + 窗口事实）+ target shape 冻结定义。
- packet 写入 `packets/{item_id}.json`（schema 按 multi-agent-packet-schema-v1.json 的 packet_item），SHA 全部入档（`packet_hashes.json`）。
- 生成器：`evidence/tools/longrun_generate_packets.py`；对 manifest 逐项确定性生成；不调用模型。

## 4. Pilot 选样规则（冻结；12–18 项，E12/E13 必含）

从 120-item manifest 按 target_shape 分组、seed 20261012 确定：

| 组 | 规则 | 数量 |
|---|---|---|
| E12 | 每 stratum kind（detector_positive/negative_or_nearmiss/luo_or_crossing）各 1（如缺则顺延其他 kind） | 3 |
| E13 | 同上 | 3 |
| E1 | 2（RNG 抽取） | 2 |
| E3 | 2 | 2 |
| E14 | 2 | 2 |
| E6 或 E7 | E6 优先，不足取 E7 | 2 |
| E5/E10/E11/E15 中 RNG 选一 shape | 2 | 2 |
| E4 | 1（OSW matched negative；如 manifest 无则不计） | 0–1 |

合计 16–17 项（12–18 授权区间内）；两语料均须出现（同一 shape 组内 TW/OSW 混合抽取）。

## 5. Pilot 质量门槛（冻结于本文件；不得事后修改）

- G1 schema 有效性 = 100%（Pilot 全部 51 单元 = 17 × 3 通道，每个单元产出可解析三键 JSON）。
- G2 citation 有效性 = 100%（cited_event_ids ⊆ packet 事件集；cited_fields ⊆ 白名单）。
- G3 跨通道 canary 泄漏 = 0。
- G4 配置/输入漂移 = 0（同 item 三通道 packet SHA 一致；manifest SHA 不变）。
- G5 无未解决运行失败：每单元每通道最多 1 原始 + 2 重试（瞬时错误：timeout/5xx/连接；退避 30s/60s）；重试后仍失败 → 该单元 INFRA_BLOCKED → G5 FAIL。
- G6 成本上限：全阶段累计 completion tokens ≤ 900,000；单调用 ≤ 16,384 completion tokens；超限 → STOP 保留进度。
- G7 EVAL-3 pre-launch 一致性核查 PASS（§6）。
- 判读：G1–G7 全 PASS → Pilot PASS → 进入正式阶段；任一 FAIL → 诊断报告 + STOP（不进入正式阶段，不修改门槛）。

## 6. EVAL-3 pre-launch 一致性核查（G7，只读）

- claude.cmd 实际请求路由 = env `ANTHROPIC_BASE_URL`（api.deepseek.com/anthropic）✓（R2 transport 探测复现：response.model = deepseek-v4-flash）。
- 凭证来源 = env `ANTHROPIC_AUTH_TOKEN`（仅记录来源，不输出值）。
- `--model deepseek-v4-flash` 与直连 request model 一致 ✓。
- 结论：Claude Code 运行时与 DeepSeek 直连证据一致（transport 层）；模型自报 "Claude" 为 framework identity confound（沿用 R2 处置）。

## 7. 正式阶段规则（冻结）

- 顺序：manifest items 数组固定顺序 × 3 通道 = 360 计划单元。
- **Pilot 样本独立重跑**：Pilot 所用 17 个 manifest 项在正式阶段照常执行，Pilot 结果不并入正式统计（预冻结规则）。
- 隔离：每通道独立 cwd（`{run}/EVAL-{n}/`）+ 独立会话（每单元独立调用）；禁止读取其他通道输出。
- 断点续跑：单元结果文件 `results/{phase}/{channel}/{unit_id}.json` 原子写入（tmp+rename）；存在且校验通过 → 跳过；重复/不一致记录 → fail-closed（STOP）。
- 重试策略（冻结）：瞬时错误（timeout/5xx/连接拒绝/空 content）重试 ≤2 次（退避 30s/60s）；usage-limit/身份不一致/证据损坏 → 立即 STOP 保留进度。
- 记录字段：packet SHA、model/provider/session、raw trace（stdout/stderr 全文）、parsed 标签、reason_code、citations、tokens、时延、attempt 次数。
- 单元状态枚举：VALID / INVALID / INFRA_BLOCKED / PENDING（未完成不算 NO）。

## 8. Phase 3 审计与分析（冻结）

- 审计：360 单元 completeness/schema/citation/input-hash/binding/isolation/retry/cost 全量核查；状态计数（VALID/INVALID/INFRA_BLOCKED/PENDING）。
- 统计：标签分布、三方 exact agreement、pairwise raw agreement + Cohen κ（3 类 nominal）、Fleiss κ（3 rater）、INSUFFICIENT_EVIDENCE 率、reason_code 分歧矩阵、E12/E13 细分、语料间差异、聚类（轨迹）说明。
- 纪律：结论仅限跨模型一致性；多数投票 ≠ ground truth；不宣称人工标注准确率/安全压缩。

## 9. 成本与运行上限（冻结）

- completion tokens 硬上限 900,000（全阶段累计）；单调用 16,384。
- 单调用墙钟 ≤900s；每通道预期总时延 3–8 h（GLM-5.3 推理为长尾）——三通道并行 + 每通道 2 worker 执行。
- 超限 → STOP 保留进度。

## 10. 交付物

`evidence/V1/paper/multi-agent-annotation/` 下：longrun-annotation-plan.md（本文件）、pilot-report.md、formal-annotation-report.md、annotation-results.jsonl、disagreement-analysis.md、evidence-index.json、final-readiness-verdict.md。运行原始迹在隔离目录 `D:\tasco-temp\longrun_annotation\`（SHA 全部入 evidence-index）。
