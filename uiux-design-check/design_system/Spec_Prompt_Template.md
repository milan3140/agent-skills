# Vibe Coding Spec Prompt Template (60-min sprint, simplified v2)

此 template 只需填寫 6 + 1 個欄位（5-8 分鐘）。其他工作（Data Schema、三狀態、AC 細化、OOUX 物件分析、design tokens 等）全部由 AI agent 在 build phase 按以下檔案執行：

- `UIUX_Design_Check-list_v2.md` — Phase 0-6 完整工作清單
- `Tailwind_Design_Token_Setup.md` — Design token 直接 copy

---

## 使用流程

```
[Step 1] 填本 spec (5-8 min)
[Step 2] 餵 agent 三份檔案 + 啟動指令（見文末）
[Step 3] Agent 跑 Phase 0 (研究/JTBD/比對 happy path) → 可能問你問題
[Step 4] 你回答 → Agent 跑 Phase 1-5 全部設計（不寫 code）
[Step 5] Phase 5.5 → Agent 產出 Design Spec MD → STOP 等你 approve
[Step 6] 你 review MD → "approved" 或 "change A, B, C"
         - 若 approve → 進 Step 7
         - 若 change → Agent loop 回對應 Phase 修，再 emit MD
[Step 7] Agent 跑 Phase 6 build implementation (15-20 min)
         你同時準備簡報，每幾分鐘看 TodoWrite 進度
[Step 8] Agent 跑 Phase 7 verification (3-5 min)
[Step 9] Demo rehearsal
```

**關鍵紀律**：Step 5-6 的 Design Spec approval gate **不能省**。沒看過設計稿就讓 Agent 直接寫 code = 高機率走偏，60 min sprint 沒空 retrofit。

---

## 1. One-liner 產品定義

```
為 <user persona> 提供 <product shape> 來解決 <specific job-to-be-done>。
成功的衡量是 <single success metric>。
```

**範例**：
> 為籌碼K線重度用戶提供「取消挽留 (save-flow) 介面」，在使用者點擊「取消訂閱」後 30 秒內呈現個人化挽留方案。成功衡量是 save-rate 從 8% 提升到 ≥ 15%。

> ⬇ 你寫的版本：
>
> _________________________________________________

---

## 2. Tech Stack（預設直接用，需偏離時才覆寫）

```
✅ DEFAULT (適用 90% 的 60-min sprint case)

Framework:         React 18 + Vite + TypeScript
Styling:           Tailwind CSS (Tailwind_Design_Token_Setup.md 直接 copy)
Components:        Hybrid — Agent 依 UIUX checklist Phase 4.0 框架自主判斷
                   * 預設 shadcn/ui 處理: Dialog / Select / Form / Tabs / Toast /
                     Tooltip / Sheet / Button (a11y + focus trap 自寫風險高)
                   * 預設自寫 (純 Tailwind): Table / Layout / Header /
                     Card-like containers / 任何 BP-1 敏感的容器
                   * 預設 Recharts / lightweight-charts: 圖表
                   * 任何不確定的 component, Agent 必須在 Design Spec MD
                     §7 列出 sourcing 決策 + 理由
Icons:             Lucide React
Charts (if needed): Recharts (一般) 或 lightweight-charts (K 線/股票)
Forms (if needed):  React Hook Form + Zod
State:             useState / useReducer (不上 Zustand 除非真需要)
Data persistence:  in-memory / localStorage
Testing:           Vitest (核心邏輯) — 不寫 Playwright/Cypress
Deployment:        localhost (現場面 demo)
```

**禁止 AI 自由發揮**：
- 嚴禁未列出的 dependency
- 嚴禁切換 framework
- 嚴禁加入 Sentry / GA / Mixpanel 等分析工具

> ⬇ 偏離預設的覆寫（沒有就留空）：
>
> _________________________________________________

---

> ❌ User Stories 已移除：one-liner + happy path 已涵蓋使用者敘事；功能 toggle / domain 標配由 `UIUX_Design_Check-list_v2.md` Phase 1.2.0 (Domain feature taxonomy) 自動帶出，不需要在 spec 列舉。

---

## 3. Out-of-scope（預設 + 自訂）

```
✅ DEFAULT 不做（known limitations）

[ ] Responsive 手機 layout（只做 desktop 1280px+）
[ ] 多語系 i18n（只做繁中 / 英文擇一）
[ ] Accessibility WCAG AAA（基本 keyboard nav OK，screen reader 不在範圍）
[ ] 完整 auth flow（mock 一個 logged-in user 即可）
[ ] 真實 API 串接（mock data + setTimeout 模擬 latency）
[ ] E2E 自動化測試（Playwright / Cypress）
[ ] 真實 payment integration（按鈕點完顯示 toast 即可）
[ ] Analytics / observability
[ ] SEO / meta tags
[ ] Print stylesheets
```

> ⬇ 額外要 skip 的項目：
>
> _________________________________________________

---

## 4. Demo Happy Path（4-6 步；AI 在 Phase 0.7 會跟它推導的版本對齊）

```
Step 1: 落地 <哪個頁面>，看到 <什麼>
Step 2: 點擊 <什麼>，觸發 <什麼>
Step 3: <關鍵 interaction>，顯示 <關鍵 output>
Step 4: 看到 <success state / final result>
Step 5 (optional): 展示 <1 個 error path 處理>
```

**範例**：
> Step 1: 落地「我的訂閱」頁面，看到目前 pro plan + 訂閱資訊
> Step 2: 點擊「取消訂閱」按鈕
> Step 3: Save-flow modal 出現，呈現「30% 季度折扣 + 1 個月免費 chip K-line Pro」
> Step 4: 點擊「接受方案」，看到 success toast「優惠已套用」
> Step 5: 點擊「我不接受任何方案」，看到 confirm modal「確定取消嗎？將失去 X / Y / Z」

> ⬇ 你的 demo path：
>
> _________________________________________________

---

## 5. Boundaries（永遠 / 先問 / 絕不做）

```
✅ DEFAULT 全套規則（皆已寫進 UIUX checklist v2 + Tailwind setup，此處再強化一次）

永遠做:
- [ ] 每個 user-facing button 必須有 hover / active / disabled state（Phase 5.1.1）
- [ ] 每個 API call 必須 try-catch + error UI（Phase 6.2.3）
- [ ] 任何 mutation 必須有成功 / 失敗 feedback (toast)
- [ ] 所有資料數字必須 tabular-nums 對齊

先問我（不要假設）:
- [ ] 任何 UI 大幅偏離 mockup 的決定
- [ ] 任何 data model 欄位增減
- [ ] 任何 navigation 結構改動
- [ ] 任何 dependency 新增
- [ ] Phase 0.7 happy path 差異 ≥ 2 步時

絕不做:
- [ ] 加入 emoji（用 Lucide icon 代替）
- [ ] 用卡片式設計（BP-1 詳列）
- [ ] 用純灰色 (#888 / #555)（必須帶品牌 hue）
- [ ] 自由發揮新增功能（按 happy path + Phase 1.2.0 domain taxonomy 跑，不要加料）
- [ ] 切換 framework / 重大 refactor
- [ ] Arbitrary value (p-[7px], text-[#123456])
```

> ⬇ 額外的 case-specific boundaries：
>
> _________________________________________________

---

## 6. Execution Mode

```
模式: Hybrid (預設) — Agent 依下方框架自主判斷每個 phase 用 single 或 multi-agent

✅ Multi-Agent 自動觸發框架

Default: single-agent (sequential, safest)

升級到 multi-agent 當且僅當 ALL 條件成立:
1. 工作有清楚獨立的 sub-task (無 shared mutable state, 無依賴鏈)
2. 平行節省 > 子 agent overhead (每個 sub-task ≥ 90 sec 工作量)
3. Failure isolation 合理 (單一 sub-agent 失敗不阻塞其他)
4. 主 agent 能在 sub-agent 啟動前明確界定: 各自只 touch 哪些 file / 範圍

Phase-level guidance:

- Phase 0 研究: 通常用 multi (2-3 個平行 research stream)
  例: a) 設計語言對標 (Apple HIG / Linear / Vercel)
      b) 同業競爭者 happy-path 解構
      c) Reddit / PTT / Dcard 使用者痛點
  條件: 三條都有 ≥ 90 sec 工作量

- Phase 1-5 設計: 一律 single (有依賴鏈)
  Phase 1 UI type → Phase 2 OOUX/Schema → Phase 4 component → 都是順序

- Phase 5.5 approval gate: 一律 single (是 sync point)

- Phase 6 build: 視 user stories 結構決定
  觸發條件: ≥ 2 個視覺獨立區塊 (e.g., 主頁面 + Modal / Page A + Page B)
            且 visually independent, 不共享 component
  範例: stories 涵蓋「訂閱頁面」+「取消挽留 Modal」+「成功 toast」
        → 可切 2 sub-agent: agent A 做主頁面, agent B 做 Modal
  反例: 單一 view 一條流程 → single 即可

- Phase 7 verification: 一律 single (整體 review)

✅ Single-Agent 規則 (大多數情況)

- Agent 用 TodoWrite 維護階段進度，每 phase 結束更新狀態
- 每個 phase break 暫停 30 秒等使用者審計 (不審 = 默認通過繼續)
- 不主動做 self-critique 或 summary，由使用者手動觸發
- 階段性漸進產出，不要一口氣 think 完才輸出
- 若卡住超過 3 min 必須立即停下來向使用者提問，禁止亂猜
- TodoWrite 每 5 min 一個 progress entry

⚠ Multi-Agent 啟動時的紀律

- 主 agent 必須先在 TodoWrite 標記「parallel: <sub-task 1>, <sub-task 2>, ...」讓使用者看見
- 子 agent 透過 Claude Code Agent tool 派發 (不用 claude -p subprocess)
- 衝突解決: 主 agent 規定每個子 agent 只能 touch 哪些 file / 哪些 component
- 進度可視化: 主 agent 在 TodoWrite 標每個子 agent 的狀態 (running / done / blocked)
- 整合: 主 agent 在 sub-agent 全部完成後負責 integration step
- 若任一子 agent 卡住 > 2 min, 主 agent 立即收回任務改 single 重做

階段終止點:
- 每個 phase 結束都是 hard stop point，使用者可叫停
- 超時應急按 UIUX checklist v2「終止與回退策略」順序砍
```

> ⬇ 偏離預設的 execution overrides（沒有就留空）：
>
> _________________________________________________

---

## 啟動 Agent 的 Prompt（filled spec 完成後 copy-paste）

```
請開始 50 min vibe coding sprint。

我的 Spec 寫在: vibe-coding/Spec_Prompt_Template.md (已填妥)
請依 vibe-coding/UIUX_Design_Check-list_v2.md 從 Phase 0 開始執行。
Design tokens 直接 copy vibe-coding/Tailwind_Design_Token_Setup.md。

執行規則:
1. 用 TodoWrite 維護 phase 進度，每 phase 結束更新並 1 句 status summary
2. Phase 0.7 (happy path 對齊) 若發現差異 ≥ 2 步，立即停下來向我報告
3. 每個 phase 結束等我 30 秒（我不審 = 你繼續）
4. 若卡住超過 3 min，立即提問不要猜
5. 不主動 self-critique，等我手動觸發
6. 超時應急按 UIUX checklist「終止與回退策略」砍

現在開始 Phase 0。
```

---

## Known Limitations

- 適合 60-90 min 的 single-flow vibe coding sprint
- 不適合 multi-page web app（>3 頁需更完整 routing + nav spec）
- 不適合 backend-heavy 題目（預設前端 mock；接真 API 需另寫 API contract）
- 不適合純 algorithm 題目（leetcode-style 不需要此 template）
