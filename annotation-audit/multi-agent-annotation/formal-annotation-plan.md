# formal-annotation-plan — PAPER-A-MULTI-AGENT-FORMAL-ANNOTATION-V1（冻结执行计划）

日期：2026-10-12。本文件在正式执行前冻结；执行期间不得修改。

## 冻结参数

- manifest：`multi-agent-pilot-manifest.json`（sha256-16 `5d54eb69461cd14c`，120 items）
- packets：120 个（`D:\tasco-temp\longrun_annotation\packets\`，SHA 见 `packet_hashes.json` sha `8ecd87483ae81b7f`）
- runner：`longrun_runner.py`（sha256-16 `bfedf5ecd16b37e9`，含全部修复）
- prompt 模板：`longrun_frozen_config.json`（sha `68d0f94db08163c4`）
- 三通道绑定：`three-channel-binding.json`（EVAL-1 Codex+GPT gpt-5.6-sol / EVAL-2 OpenCode+GLM-5.3 / EVAL-3 Claude Code+DeepSeek v4 flash）
- 输出目录：`results/formal/{channel}/{item_id}.json`（与 pilot `results/pilot/` 完全隔离）
- 评分：3 类 nominal {YES, NO, INSUFFICIENT_EVIDENCE}；标准 unweighted Cohen κ；Krippendorff α

## 质量门槛（冻结于本文件；正式阶段完成后审计）

- F1 completeness = 360/360 单元有结果文件
- F2 schema = 有结果文件中 100% 三键合规
- F3 citation = 有结果文件中 100% 引用可定位
- F4 零跨通道 canary 泄漏
- F5 零配置/输入漂移
- F6 成本 ≤ 900K completion tokens
- 判定：F1–F6 全 PASS → FORMAL_COMPLETE = YES

## Pilot 样本重跑规则（冻结）

Pilot 的 14 个样本在正式阶段照常执行，Pilot 结果不并入正式统计。正式结果独立生成于 formal 目录。

## 重试策略（冻结）

瞬时错误（timeout/空 content/5xx/连接）重试 ≤2 次（退避 30s/60s）。usage-limit/身份不一致 → STOP 保留进度。
