# final-review-fix-r1 — PAPER-A-FINAL-REVIEW-FIX-R1

日期：2026-10-12。基于 independent-final-audit-r1 的 P1 修复 + P2 处理 + 最终验证。

判定：**PASS — SUBMISSION_READY = YES**（P0=0；P1 全部 FIXED；P2 已合理处理；PDF 9 pages 0-0-0）。

---

## 审稿问题关闭矩阵

| 审稿 ID | 问题 | 修复 | 状态 | 证据 |
|---|---|---|---|---|
| P1-1 | 残留旧 COC 90.12%/99.57% | 全文替换为 95.96%/99.98% event-payload proxy | **FIXED** | PDF text scan: 90.12=clean, 99.57=clean |
| P1-2 | P0 340-item GLM arm = 规则脚本 | provenance-p0-audit.md 独立审计 + 论文 §3.5 降级描述 | **FIXED** | 论文不再引用 340-item 为"异构 LLM 一致性"；已由 120-item × 3 通道替代 |
| P1-3 | E14 51.7% 覆盖缺口 | Limitations Coverage boundary 段已添加 E14 集中缺失说明 | **FIXED** | PDF text: "51.7" PRESENT |

## P2 处理

| P2 ID | 处理 | 状态 |
|---|---|---|
| P2-1 E13/Q2a 主观性 | §3.5 Q2a 段 "fair, reflecting inherent subjectivity" 已在位 | **DONE** |
| P2-2 E14 缺失技术说明 | Limitations E14 coverage gap 已在位 | **DONE** |
| P2-3 E1 跨模型分歧 | E1 Q1 一致率 64.3% 在 final-agreement-report.md 中有数据支撑 | **ACCEPTED_LIMITATION** |

## Step 1 — 历史 COC 清理

全文扫描并替换：
- `0.39%` → `0.018%` (event-payload COC)
- `90.12%` → `95.96%` (event-payload COC)
- `99.57%` → `99.98%` (relative gap)
- `91.27%` → `97.67%` (Qwen cross-check)
- `1.14%` → `0.27%` (Qwen shipped)

替换位置：Abstract、RQ5 dual ledger、Finding 5、Figure 5 caption+Description、Discussion、Conclusion。
**保留**：SOC 2.07%/100%（独立 session-level 指标）；90.1%（F1 offline replay 90.1% ≠ COC 90.12%）。

## Step 2 — 340-item Provenance 修正

论文 §3.5 新增 Multi-agent formal annotation 段：
- 明确区分 340-item 历史 audit（保留为背景）与 120-item formal annotation（当前权威）
- 340-item audit 的 provenance 问题记录在 provenance-p0-audit.md
- 论文不再引用 340-item κ 作为"异构 LLM 一致性"证据

## Step 3 — E14 Coverage Limitations

Limitations 新增：GLM-5.3 通道对 E14 项的 51.7% cell-level 覆盖缺口说明。

## 4. PDF 最终验证

| 检查 | 结果 |
|---|---|
| 页数 | 9 ≤ 10 ✓ |
| Errors | 0 ✓ |
| Undefined | 0 ✓ |
| Overfull | 0 ✓ |
| 新数字 (0.018/95.96/99.98) | PRESENT ✓ |
| 旧数字 (0.39/90.12/99.57) | clean ✓ |
| Fleiss κ (0.80/0.38/0.80) | PRESENT ✓ |
| E14 gap (51.7%) | PRESENT ✓ |
| Anonymous | ✓ |
| Stale '0.0003' | F1 signal:noise（合法无关） |

## 5. 判定

全部 P0（0 个）/ P1（3 个）关闭，P2（3 个）已合理处理。
PDF 9 pages 0-0-0。
所有新旧数字一致性验证通过。

**SUBMISSION_READY = YES**

**STOP**——等待最终提交授权。
