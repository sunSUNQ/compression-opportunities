# PAPER-A-SESSION-IDENTITY-AMENDMENT — Reconciliation Report (V0.11-D4-A1R3 trajectory-identity caliber)

日期：2026-10-10。依据：`taxonomy-session-identity-v1-report.md`（PASS）+ `taxonomy-residual-v1-report.md`（PASS，id 碰撞发现源）。
判定：**PASS**（gates ALL PASS；无 STOP 触发）。commit SHA 见 git log（本轮）。

---

## 1. 预注册与权威工件（sha256-16）

| 工件 | sha256-16 | 说明 |
|---|---|---|
| `evidence/V1/v011-d4a1r3-session-identity-prereg.json` | （FROZEN before recompute；预注册先于任何重算写入） | 身份定义 = (frozen source file, row ordinal)；digest 仅校验；15,000 records vs 13,053 original IDs；1,947 碰撞对事实；明确 row uniqueness ≠ run independence |
| `evidence/V1/v011-d4a1r3-tw-trajectory-census.json` | `ae954c032022ca79` | A1R3 官方 trajectory census（GATES ALL PASS） |
| `evidence/tools/v011_d4a1r3_tw_trajectory_census.py` | （见 git） | 冻结检测块/残差块字节切片 exec（零转写） |
| `evidence/V1/paper/paper-tables.pre-a1r3.json` | `63328233664c217f` | A1R3 前 T1 的 byte-identical superseded 快照 |
| 冻结输入 | TW parquet `3dd8ec3546cf771c`；A1R2 census `630dcfaae0bca521`；OSW `7d22b0b98062cc8c`；manifest v2 `284c47ea200607dc` | 未改动 |

## 2. 口径修订决策（本 amendment 采纳）

**TW 会话级统计采用 trajectory (row) identity**：分子 = 含该 shape 的记录轨迹行数（每条独立记录轨迹计 1），分母 = 15,000 行（两种口径分母相同）。依据：(1) 1,946/1,947 碰撞对内容不同（不同记录轨迹），1 对同内容按行序区分；(2) id-set 口径混合语义（id 折叠分子 × 行分母）且系统性低估 klear 覆盖；(3) 身份重放稳定（两遍序列 SHA256 `8a74f744b1f79930`）；(4) 全部 15 个复制带在两种口径下不变、R 带比值向 1 收紧（保守方向）；(5) OSW 1:1:1 干净，行口径使两语料语义对齐。**行唯一性 ≠ 运行独立性**：碰撞对的两条轨迹是否独立执行不由本口径断言。

## 3. 守恒与对账（Step 4；census 内置 gates ALL PASS）

- id-set 重算 = A1R2 `per_shape_sessions` 逐 shape 精确相等 ✓
- 事件命中 = A1R2 `per_shape_events` 逐 shape 精确相等 ✓；总事件 578,283 ✓
- 总观测字符 1,239,474,486 ✓；labeled 920,214,271 ✓；allocation Σ分摊 = labeled ✓；qualified 703,167,334.5 ✓
- 残差七桶（含 orphan 15,011 / 70,819,544）= A1R2 逐桶精确相等 ✓
- 会话级 delta（新−旧）= 碰撞对双成员共现数：E1 +1,746、E2 +1,844、E3 +710、E5 +3、E6 +40、E7 +23、E10 +45、E11 +8、E12 +621、E13 +120、E14 +550、E15 +10、E4/E8/E9 +0

## 4. 复制判据复算（Step 5；精确分数）

15 个 shape 逐项 status/ratio/margin 见 A1R3 census `bands_full_precision` 与 Supplement C 新表。**全部带不变**：R7（E1 1.0285、E2 1.0140、E3 1.2191、E9 0.75、E12 1.0902、E13 0.7942、E14 1.2847）+ P1（E5 2.6652）= 8/13；DS5 比值全部远离 0.2 边界（最近 E11 0.0492，距 0.1508）；R 带最近边界距离 E13 0.2942（距 0.5）。旧比值与 A1R2 冻结全精度值内置断言一致（含 E9 舍入陷阱修复：OSW 精确分母 1/20,000 → 0.75，非 4 位舍入 0.0001 → 1.5）。

## 5. 同内容对敏感性（Step 6）

字节级相同对 = tids 317/318（klear，E1∧E2∧E3）。排除其中一行（分母 14,999）：E1 14,577、E2 14,788、E3 12,301，比值 1.0286/1.0141/1.2193——**零带变化**；E9 excl ratio 0.74995 → R。该敏感性不作为独立运行的证据，仅记录边界稳健性。

## 6. 受影响数字账本与修改位置（Step 7；仅更新有权威来源的数字）

| 位置 | 旧（id-set/A1R2） | 新（trajectory/A1R3） |
|---|---|---|
| 摘要 | ratios 0.81–1.35；68.8%/79.5%；57.9%/46.6% | **0.79–1.28；72.9%/79.5%；58.7%/46.6%** |
| Contributions (2) | 0.81–1.35 | 0.79–1.28 |
| §3.1 | "15,000-session discovery corpus" | "15,000-recorded-trajectory discovery corpus" |
| RQ1 | 68.8/79.5；57.9/46.6；77.3/~100；86.3/~100；0.77% | **72.9/79.5；58.7/46.6；82.0/~100；98.6/~100；0.81%**（0.77% 系 A1R2 文本对 E11 的舍入错置，本次顺带修正） |
| RQ2 | E12 68.8→79.5；E13 57.9→46.6；ratios 1.17/1.16/1.29/1.35；E6 293 (1.95%) | **E12 72.9→79.5；E13 58.7→46.6；ratios 1.03/1.01/1.22/1.28；E6 333 (2.22%)** |
| Fig.3 caption | A1R2；0.81–1.35 | A1R2 + trajectory identity (A1R3)；0.79–1.28 |
| §4 Metrics/Frames | "fraction of sessions" | "fraction of recorded trajectories" + **Recorded trajectories and session identifiers 披露段**（13,053 唯一 id；1,947 对；非 run-independence 证据；id-set 下带全不变） |
| Limitations | — | **新增 Session identity 条**；Detector caliber 段补 A1R3 |
| Conclusion | 0.81–1.35 | 0.79–1.28 |
| figures.json series[0] | A1R2 id-set 14 值 | **A1R3 row 口径 14 值**（E1 0.9719/E2 0.9859/E3 0.8201/E5 0.0075/E6 0.0222/E7 0.0155/E10 0.0228/E11 0.0081/E12 0.7292/E13 0.5872/E14 0.7382/E15 0.0084；E4 0.2771 不变；E8 缺席） |
| paper-tables T1 | 同上旧值 | 同上新值 + amendment(A1R3) 块 + previous_amendments[A1R2] + sources 增 A1R3 |
| Supplement C | A1R2 会话级数字 | **A1R3 小节**（15-shape 对照表 + identity 披露）；A1R2 会话级标注 superseded-for-session-semantics |
| Supplement A | relations 例样节 | 口径注记（V1 scan id-set vs 论文行口径；格与蕴含与口径无关） |
| rq-claim-evidence-matrix | A1R2 authority；RQ1 values | **A1R3 authority**（含 A1R2 prior）；RQ1 values E12 [0.7292,0.795]、E13 [0.5872,0.4663]、E2 [0.9859,0.9998]、E3 [0.8201,0.9999]；RQ2 claim 0.79-1.28 |
| claim trace | C03-C05/C13-C17/C19（A1R2） | 更新至 A1R3 + amendment 注记；C41 及其余行不变 |

不变项：OSW 全部数字；事件命中；观测字符；allocation；残差桶；median/p75（pre-amendment frozen ledger）；T2–T6；RQ3–RQ5；Fig.1/2/4/5/6。

## 7. 构建、审计与验证（Step 9）

- Fig.3 经 `generate_figures.py::fig3()` 从更新后 figures.json 重建；14 值与 A1R3 census `row_incidence_4dp` 精确互证（E8 缺席、E4 不变 ✓）。
- clean rebuild：pdflatex + bibtex + pdflatex ×2 → **9 pages / 537,788 bytes**（≤10 页预算）；log **0 errors / 0 undefined / 0 overfull**；bibtex 0 error。
- PDF 文本审计（pypdf，9/9 页）：新数字全 PRESENT（72.9/58.7/82.0/98.6/0.81/0.79–1.28/1.03-1.01-1.22-1.28/13,053/1,947/333 trajectories (2.22%)/58.72/披露段标题）；旧数字全 clean（68.8/57.9/77.3/86.3/0.81–1.35/1.17-1.16-1.29-1.35/57.92/293 sessions (1.95%)/0.77）；匿名/泄漏检查 clean。
- 跨文件口径一致性：figures.json、paper-tables.json、rq-claim-evidence-matrix.json、Supplement A/C、tex/md 全部声明 trajectory (row) identity（A1R3）；T1/figures 与 A1R3 census 精确互证（ALL match）。
- JSON 有效性：三个 JSON 解析通过。

## 8. Claim-to-Evidence Ledger（核心行）

| 主张 | 证据 |
|---|---|
| 15,000 records / 13,053 unique ids / 1,947 对（1,946+1） | 两遍序列哈希 + 全列 Counter + 逐对 digest（V1 报告 + A1R3 census gates） |
| trajectory identity 重放稳定 | 两遍 (session_id, source) 序列 SHA256 相等 |
| id-set = A1R2 / events = A1R2 / chars = A1R2 / residual = A1R2 | census 内置 gates 全 PASS（逐 shape 精确断言） |
| 新 incidence（14 值） | A1R3 census `per_shape`（行命中/15,000） |
| bands 全不变 + margins | A1R3 `bands_full_precision`（精确分数；新旧 status/ratio/margin 逐 shape） |
| 同内容对敏感性零带变化 | census `sensitivity_identical_pair`（tids 317/318；excl shapes E1∧E2∧E3） |
| OSW 1:1:1 | osw_identity_out.json（manifest 唯一、无跨文件复用、digest 零重复） |
| 行唯一性 ≠ 运行独立性 | prereg 声明 + 报告 §2/§3 措辞（碰撞对 = 标签属性） |

## 9. 判定

STOP 条件核对：身份重放稳定 ✓；旧口径回归一致（idset/events 与 A1R2 全等）✓；事件/字符零漂移 ✓；复制状态变化 = 0（无未解释变化）✓；分母一致（两种口径均 15,000）✓；PDF 审计通过 ✓。
**判定：PASS。** 修订清单/关键 SHA/证据路径见 §1/§6/§7。**STOP**——等待下一轮独立授权任务。
