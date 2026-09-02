# UIUX & Functional Design Check-list (vibe-coding integrated v2)

給 AI agent 在使用者填完 Spec 後，照此檔逐 phase 執行。

設計原則：
- 遵循 Apple HIG + Material Design + Minimalist style，以 Linear / Stripe / Notion / Vercel 為美學標竿
- 清晰直觀、降低使用負擔為最高原則
- Symbol / Icon 一律用 SVG 或 Lucide（備用 Heroicon / Phosphor / Material），嚴禁 emoji
- 嚴禁卡片式設計（含圓角填色背景容器、陰影浮起容器等）— 詳見 BP-1
- 不要「修補」，要「建立統一設計美學邏輯系統」

**Debug 鐵則** (Phase 6/7 嚴格遵守，詳見 6.0.1 / 6.0.2 / 7.0)：
- **改前先 impact analysis**：function caller / type usage / state shape / prop chain / HMR state stale → 一次改齊所有受影響的檔
- **typecheck pass / HMR ok ≠ fix 對** (S0/S1 訊號零證據)
- **第一次 fix 走 normal path**（一次到位 + 請 user 驗 S4），**第二次起若 user 回報失敗 → 強制升級 instrument-driven**（加 console.log 拿實際訊號）
- user 說「一樣」 = 第一次 fix 失敗 → **停手 + 加 instrument**，不再憑空換解法
- 同一 bug 換 ≥ 2 解法 = 在 hypothesis space 隨機跳 → **鎖死 instrument-first**

---

## 50 min Sprint 時間預算

| Phase | 時長 | 性質 | 內容 |
|---|---|---|---|
| Phase 0 — 研究與目標分析 | 3-4 min | 設計 + dialog | 多 agent 平行對標 (見 §7 multi-agent 框架) |
| Phase 1 — UI 種類 + 功能清單 | 2-3 min | **設計（不寫 code）** | |
| Phase 2 — IA + 資料層 | 3-5 min | **設計** | OOUX / Schema / API / Edge Case Surface Map |
| Phase 3 — Design Tokens | < 1 min | **設計** | 直接 copy `Tailwind_Design_Token_Setup.md` |
| Phase 4 — 元件與佈局 **設計** | 3-4 min | **設計** | 規格產出，**不寫 code** |
| Phase 5 — 互動 + Guards **設計** | 2-3 min | **設計** | 規格產出，**不寫 code** |
| **Phase 5.5 — Design Spec 審核 gate** | 3 emit + 3 review | **審核** | Agent 彙整 Phase 0-5 為設計稿 MD + Wireframes → 使用者 approve 才能進 Phase 6 |
| **Phase 6 — Build Implementation** | 18-22 min | **實作** | 依已 approved 的設計稿寫 code（可多 agent 平行） |
| Phase 7 — 最終驗證與自檢 | 2-3 min | **驗證** | 對照設計稿勾選實作完整性 |
| **總計** | **~50 min** | | 留 10 min 給 demo rehearsal + 簡報製作 |

**重要工作流規則**：
- Phase 1-5 全部產出「設計規格」進 Phase 5.5 的 Design Spec MD
- 使用者 approve Design Spec 後才開始 Phase 6 寫 code
- **設計階段（Phase 1-5）不允許動 code**
- 實作階段（Phase 6）以已 approved 的設計稿為唯一來源，任何 drift 必須立即向使用者報告

**超時應急**：見文末「終止與回退策略」。

---

## 📍 Phase 0: 研究與目標分析 

從 Spec 出發，AI 自行做使用者研究與情境推導，產出後與使用者寫的 Demo Happy Path 對齊。

[ ] **0.1 網路 / 論壇調研** ─ 為了支撐 0.2-0.5（使用者畫像 / 起始狀態 / JTBD / 常見錯誤）所做的資料蒐集。從論壇 / 評論 / 文章 / Reddit / Dcard / PTT / 競品案例去找使用者真實聲音、行為、痛點、常見誤解。**不是找產品 reference / 競品 UI，那是 Phase 1.1 業界對標的工作**。若使用者已提供足夠 context 就跳過。

[ ] **0.2 使用者畫像**：列至少 1 個主要 persona + 1 個次要 persona，每個 persona 包含：
   - 環境（哪裡用、什麼裝置）
   - 時間（什麼時段、有多少時間）
   - 資訊認知與行動順序（先看到什麼、先想什麼、先點什麼）
   - 情緒狀態（猶豫 / 焦慮 / 信心 / 急迫 / 好奇）
   - 心智認知狀態與習慣（領域熟悉度、過去類似產品使用經驗）

[ ] **0.3 起始狀態**：使用者進入此 flow 時：
   - 已擁有的資訊（已知什麼）
   - 所處使用情境（剛做完什麼、預期接下來要做什麼）

[ ] **0.4 JTBD (Job To Be Done)**：使用者要完成什麼任務、需要什麼最終資訊 / 行動。

[ ] **0.5 常見錯誤**：使用者最容易犯什麼錯（點錯、看錯、誤解、放棄），設計系統時最常犯的誤區或盲點，可網路調研。

[ ] **0.6 推導使用流程**：從 0.3 + 0.4 + 0.5 推導理想使用步驟序列。

[ ] **0.7 比對使用者 Demo Happy Path**：
   - 差異小（< 2 步不同）→ 以 Demo Happy Path 為骨架，把 0.6 的細節補上
   - 差異大（≥ 2 步不同或方向不同）→ **STOP**：向使用者報告差異 + 洞察依據，等使用者裁決
   - 對齊後產出最終 Demo Happy Path（含 error path 變體）

[ ] **0.8 細化 AC (Acceptance Criteria)**：對每個 User Story 補 3-5 個 AC，每個 AC 明確、可驗證。不要超過 5 個。

---

## 📍 Phase 1: UI 種類與功能清單

### 1.1 判斷 UI 介面種類（基於 Phase 0 結論）

[ ] **1.1.1 B2B / Enterprise / Industrial UI**：資訊密度極高、操作效率與精準度優先。設計重點：「防呆」與「易讀性」。（例：ERP, HMI, 數位製造平台）

[ ] **1.1.2 Productivity / Utility UI**：完成特定任務、強調沉浸感。設計重點：最大化畫布、靈活工具列、拖曳操作、右鍵選單。（例：Figma, Notion）

[ ] **1.1.3 Content-heavy / Reading-oriented UI**：長時間舒適吸收資訊。設計重點：大量留白、講究排版、弱化介面干擾。

[ ] **1.1.4 B2C / E-commerce UI**：吸引注意力、最大化轉化率。設計重點：吸睛 CTA、高畫質圖片。

[ ] **1.1.5 Dashboard / Data Analytics UI**：數據概覽、決策支援優先。設計重點：圖表、資料層級清晰、模組化區塊（注意 BP-1：避免卡片化）。

### 1.2 完整功能清單樹

[ ] **1.2.0 領域配方比對 (Domain Feature Taxonomy) — 必跑在 1.2.1 之前**

從 Phase 1.1 的 UI 類型判斷 + Phase 0.1 競品 union table，**先列出該領域的 well-known feature checklist**，再把產品需求對映進去。對映輸出格式：

```
| Feature 類別 | 標配選項 | in / out / TBD-by-user |
|---|---|---|
```

各領域 starter taxonomy（agent 可自擴）：

- **Chart / 圖表工具**：input methods（paste / CSV / manual）/ chart-type switch（含搜尋）/ color picker / gradient & opacity / **axis controls (visible / format / tick density)** / **label toggles (data labels / category labels / axis values / legend)** / sort / **format (raw / % / currency / unit)** / title (editable inline) / per-element override / export (format / size / bg / scale / aspect ratio)
- **Dashboard / 數據總覽**：filter bar / date range / refresh / drill-down / pin / share / annotation / export
- **Form builder / 表單**：field types / validation rules / conditional logic / multi-step / save draft / submit confirm
- **B2B 工作流 / 列表**：list view + detail / bulk actions / sort+filter+search / column resize / saved views / pagination
- **B2C / E-commerce**：search / filter facets / sort / wishlist / quick view / add-to-cart / variant picker / reviews
- **Content / 編輯器**：toolbar / format menu / shortcuts / auto-save / version history / collaboration cursors

紀律：
- 屬於該領域**表 stake (3 個對標競品都有)** 的 feature → 預設 in-scope，**不需 user 在 spec 顯式提**
- 屬於**差異化 (1-2 個有)** → TBD，STOP 問 user
- 屬於**out-of-scope by spec §3** → 標 out

⚠ 漏列領域標配 = 在 Phase 6 build 階段 user 必須一個個指出來補 → 嚴重耗 sprint 預算。

[ ] **1.2.1 資訊元素**：列出畫面需要顯示的所有資料項目（user name、訂閱 tier、價格、CTA 文字等）。遺漏 = 重做。

[ ] **1.2.2 操作元素**：列出使用者可執行的所有動作（click / submit / cancel / hover-reveal / drag / keyboard shortcut）。

[ ] **1.2.3 系統狀態元素**：抽象狀態列表（登入 / 未登入、編輯中 / 檢視中、subscribed / unsubscribed、admin / user 等）。

[ ] **1.2.4 畫面三狀態 (loading / empty / error)**：對 1.2.1 與 1.2.2 的每一項展開：
   - **Loading**：skeleton / spinner / progress bar 三選一；超時 > X 秒顯示什麼
   - **Empty**：兩種變體必須分別處理：
     - First-time（從沒用過）→ 引導 CTA + 圖示
     - Filtered-no-result（用過但這次無結果）→ 「清除篩選」CTA
   - **Error**：訊息三要素必須完整 — (a) 發生什麼 (b) 為什麼 (c) 使用者能做什麼 + retry CTA

---

## 📍 Phase 2: 資訊架構與資料層

### 2.1 資訊架構 (Information Architecture)

[ ] **2.1.1 OOUX 物件導向分析**：自然語言列出系統核心 entity，圍繞 entity 而非系統技術結構分類：
   - 列每個 entity（例：User, Subscription, CancellationReason, SaveOffer, SaveAction）
   - 列 entity 之間關係（1:1 / 1:N / N:N）
   - 列每個 entity 的關鍵屬性（自然語言，不寫型別）

[ ] **2.1.2 導覽層級控制**：
   - 主導覽項目 ≤ 7 項（Miller's Law）
   - 從首頁到任何功能最大點擊次數 ≤ 3
   - 60 min sprint 通常只有 1-2 頁，多半此條退化

[ ] **2.1.3 漸進式揭露**：
   - 核心資訊直接可見
   - 次要資訊用 hover / 摺疊隱藏
   - 進階設定放二級頁面或 modal

### 2.2 資料層 (Data Layer)

[ ] **2.2.1 Data Schema**：把 2.1.1 翻譯成 TypeScript types（純資料型別設計，不含實例資料）：
   - 每個 entity 寫 `type` 或 `interface`
   - 每個 field 宣告：型別、必填 / optional、預設值、validation 規則
   - **每個 field 同時宣告 null / empty / edge 行為**（例：`email?: string` vs `email: string \| null` vs `email: string`，並備註「empty 時顯示什麼」）
   - **不寫實例資料**（mock data 在 2.2.3）

[ ] **2.2.2 API Function Contracts**：mock 介面層的 function signatures：
   ```typescript
   async function getUser(id: string): Promise<User | null>;
   async function cancelSubscription(userId: string, reason: CancellationReason):
     Promise<{ success: boolean; saveOffer?: SaveOffer; error?: string }>;
   async function acceptSaveOffer(offerId: string):
     Promise<{ success: boolean; newSubscription?: User['subscriptionTier']; error?: string }>;
   ```
   - 每個 function 寫死 input / output / error 三種 shape
   - 標註是否 idempotent（重複呼叫安全嗎）
   - 標註 latency 模擬範圍（例：300-800ms 隨機）

[ ] **2.2.3 Mock Data Seeds**（僅在 build 需要實例資料時做，可省略）：
   - 每個 entity 3-5 筆 realistic 範例（不要 "Test 1" / "Lorem ipsum"）
   - 中文場景用真實中文名 / 真實價格 / 真實日期
   - 邊界資料各一筆：n=0 (空)、n=1 (單筆)、極端值（最長字串、最大數字）

[ ] **2.2.4 Edge Case Surface Map (在此 phase 設計，build phase 實作，Phase 6 驗證)**：
   逐項標記哪些 edge case 適用哪個 entity / interaction。**只列清單，不實作**。實作分發到 Phase 4-5。

   - **Data 層**（會在 build 時影響 component 寫法）:
     - `null` / `undefined` / `empty string` / `空陣列` / `巨型字串` 各 entity field 哪些要防護
     - 數字邊界（負、0、Infinity、NaN）哪些 field 要 guard
     - n = 0 / 1 / many / 10000 哪些 list 要分別處理（empty state / pagination / virtualization）

   - **Interaction 層**（會在 Phase 5.2.3 實作）:
     - 雙擊送出哪些按鈕要 debounce / idempotency key
     - 慢網路 race condition 哪些 mutation 要 lock
     - Optimistic UI 哪些 action 要 rollback 機制

   - **Boundary 層**（會在 Phase 5.4 實作）:
     - Auth / token 過期哪些頁面要重導
     - 越權（看別人資料 / 改別人資料）哪些 API call 要擋
     - Input 上限 / 基本 XSS 防護哪些欄位要 sanitize

   產出：一張清單 mapping「entity / interaction × edge category × 實作 phase」，供 Phase 4-5 inline 實作 + Phase 6.2 最終驗證。

---

## 📍 Phase 3: 視覺基礎規範設定 (Design Tokens — 決定品質的 80%)

⚠ **若使用 Tailwind CSS，直接 copy [Tailwind_Design_Token_Setup.md](./Tailwind_Design_Token_Setup.md) 內的 config + CSS variables。此 phase 各條目仍須逐項檢查 token 是否符合規範。**

嚴格禁止隨意使用數值，必須建立並嚴格遵守以下 Token 系統。

### 3.1 色彩系統 — 告別純灰與純色

[ ] **3.1.1 品牌色 (Brand)**：提取主 Hue（如 Purple 260°），建立 Brand / Brand-hover / Brand-subtle / Brand-wash 四級。

[ ] **3.1.2 品牌灰階 (Tinted Grays)**：**嚴禁純灰** (#888, #555)。所有灰色必須帶品牌 Hue（Saturation 8-15%）。建立 50 (近白) → 950 (近黑) 共 10-12 級灰階。

[ ] **3.1.3 語義色 (Semantic)**：**嚴禁純 RGB** (#FF0000, #00FF00)。用調和過的 Green (Success) / Red (Error) / Amber (Warning) / Blue (Info) — 各建基調色(500) + 極淺底色(50)。

[ ] **3.1.4 背景圖層**：建立三層空間 — Level 0 (基底, #FAFAFA) / Level 1 (內容面板, #FFFFFF) / Level 2 (浮層, #FFFFFF)。層間色差微小但可感知。

### 3.2 間距與尺寸系統 — 嚴格 4px Grid

[ ] **3.2.1 基礎網格**：絕對禁止 5px, 6px, 10px, 15px。所有 margin / padding / gap 必須 4px 倍數（4, 8, 12, 16, 20, 24, 32, 40, 48px）。**Tailwind 預設已是 4px grid，直接用 `p-1 ~ p-12` 即可，不需自訂 token。**

[ ] **3.2.2 視覺群組 (Gestalt Proximity)**：外間距必須大於內間距。相關元素靠攏（4-8px），不相關元素拉開（24-32px）。

### 3.3 形狀與陰影

[ ] **3.3.1 圓角系統 (Border Radius)**：嚴格 3 級。Small (4-6px: 按鈕 / badge), Medium (8px: modal), Large (12-16px: 大容器)。嚴禁同一介面混用超過 3 種圓角。

[ ] **3.3.2 陰影系統 (Shadows)**：嚴格 5 級。陰影顏色必須是「帶品牌色的近黑 rgba(...)」而非純黑。強度標準：xs (微凸) / sm (卡片) / md (浮動工具列) / lg (toast) / xl (modal)。
除非必要或使用者明確提及需求，否則盡可能少使用陰影，要使用僅限於互動動態效果出現。

### 3.4 排版系統 — 數學比例與微調

[ ] **3.4.1 字型選擇**：優先 Inter / SF Pro / Roboto 等高品質字型。

[ ] **3.4.2 字級限制 (Type Scale)**：控制 5 級內（11, 12, 13, 14, 16 / 18px）。相鄰字級必須差 ≥ 2px 以建立對比。

[ ] **3.4.3 行高與字距**：內文行高 1.5-1.6，標題 1.1-1.3。全大寫標籤增加 letter-spacing (0.05em)。數值必須 `font-variant-numeric: tabular-nums` 對齊。

[ ] **3.4.4 Font Smoothing**：統一加 `-webkit-font-smoothing: antialiased;`。

---

## 📍 Phase 4: 介面元件與佈局設計

⚠ **此 phase 產出「設計規格」，不寫 code**。所有條目以「設計決策」形式寫入 Phase 5.5 的 Design Spec MD，使用者 approve 後在 Phase 6 才實作。

### 4.0 Component Sourcing Decision (NEW — Agent 自主判斷)

對每個 component，Agent 依下方框架判斷 source，並在 Design Spec MD 列出表格供使用者 review。

**Decision tree**：

```
1. 這 component 有 shadcn primitive 嗎？
   ├── 沒有 → 自寫
   └── 有
       2. 設計需求偏離 shadcn 預設 > 50% 嗎？
          ├── 是 → 自寫 (用 shadcn 反而要 fight Radix 內部)
          └── 否
             3. 是純 layout container (header / sidebar / grid / page) 嗎？
                ├── 是 → 純 Tailwind 自寫 (shadcn 不擅長 layout)
                └── 否
                   4. 涉及 a11y / focus trap / portal / keyboard nav 嗎？
                      ├── 是 → **強烈推薦 shadcn** (自寫 60 min 內難寫好)
                      └── 否 → 視時間決定，兩者皆可
```

**Default decisions (Agent 不確定時的 fallback)**：

| Component | 預設來源 | 理由 |
|---|---|---|
| Button | shadcn | 易客製，className override 即可 |
| Dialog / Modal | **shadcn** | Focus trap + portal + a11y 自寫風險高 |
| Select / Dropdown | **shadcn** | Keyboard nav + ARIA + portal 複雜 |
| Form (input + validation) | shadcn + react-hook-form + Zod | Form state 自寫繁瑣 |
| Tabs | shadcn | Keyboard nav + ARIA |
| Tooltip / Popover | shadcn | Positioning + portal |
| Toast / Snackbar | shadcn (`sonner`) | Queue / stacking 機制 |
| Sheet / Drawer | shadcn | Slide-in + portal |
| Table | **自寫** (Tailwind) | shadcn-table 需 tanstack-table，60 min 過頭 |
| Card-like container | **自寫** (Tailwind) | 須遵守 BP-1，shadcn `<Card>` 違反 BP-1 |
| Header / Footer / Sidebar | **自寫** | 純 layout，shadcn 不擅長 |
| Chart / 圖表 | Recharts / lightweight-charts | 非 shadcn 範圍 |
| Skeleton (loading) | shadcn | 簡單但 className API 方便 |
| Badge / Pill | 視情況 | shadcn 有但簡單到可自寫 |

**判斷產出格式**（寫進 Design Spec MD 的元件清單）：

| 元件名稱 | 來源 | 客製內容 | 理由 |
|---|---|---|---|
| SaveOfferModal | shadcn `<Dialog>` + 自寫內容 | 內部 layout / 字級 / 按鈕排列依 Phase 3 token | a11y 留給 shadcn，內容自寫 |
| CancellationReasonRadio | shadcn `<RadioGroup>` | 增加 description 區塊 | keyboard nav 留給 shadcn |
| AccountHeader | 純自寫 (Tailwind flexbox) | n/a | 純 layout |
| SubscriptionTable | 純自寫 (Tailwind table) | n/a | shadcn-table 過頭 |

使用者在 Phase 5.5 review 此表，可指定「這個我想自寫」/「這個改用 shadcn」並 trigger Agent 修改。

### 4.1 現代化元件設計法則（視覺減法）

[ ] **4.1.1 邊框減量 (Borderless)**：優先用「留白 (Gap)」+「微底色 (Wash)」區分區域，極度克制使用 border（限 1px solid gray-100/200）。嚴禁滿版格狀邊框。

[ ] **4.1.2 動作按鈕隱藏 (Hover-reveal)**：列表中次要操作（刪除、編輯）預設 `opacity: 0`，hover 時才出現。大幅降低靜態視覺密度。

[ ] **4.1.3 輕量化標題 (Lightweight Headers)**：面板標題不用厚重深色背景 Bar。改用透明背景 + `11-12px font-weight:600 uppercase color:gray-500` 小標籤 + 下方 1px 淺色底線。

[ ] **4.1.4 狀態點示 (Dot Indicators)**：側欄 / 列表狀態提示，優先用 6px 色點（綠 / 紅 / 黃），避免大型 Icon（除非需明確區分錯誤類型）。

[ ] **4.1.5 透明化按鈕**：放在品牌深色 Header 上的按鈕，用 `rgba(255,255,255, 0.15)` 半透明樣式，融入感更好。

[ ] **4.1.6 Optical Padding**：按鈕底部 padding 比頂部多 1-2px，抵銷文字基線視覺下沉。

### 4.2 佈局與動線

[ ] **4.2.1 評估並套用適合佈局**：Dashboard (數據總覽) / Split Screen (一側列表一側預覽) / F-Pattern (大量表單)。

[ ] **4.2.2 垂直對齊軸線**：所有元素左邊界對齊 2-3 條剛性隱形垂線，創造專業對齊感。

---

## 📍 Phase 5: 互動設計與狀態管理

⚠ **此 phase 產出「互動規格 + Guards 規格」，不寫 code**。所有條目（含 5.2.3 Interaction Guards、5.4 Boundary Guards）以「設計決策」形式寫入 Phase 5.5 的 Design Spec MD，使用者 approve 後在 Phase 6 才實作。

### 5.1 元件狀態完整性 (Component State Coverage)

[ ] **5.1.1 每個可點擊元件必須包含 4 個基礎狀態**：
   - Default
   - Hover（背景變色或不透明度改變）
   - Active / Pressed（微縮放或加深）
   - Disabled（降不透明度 + 禁止游標）

⚠ **注意**：此處 4 狀態是「元件互動狀態」，與 Phase 1.2.4 的「畫面三狀態 (loading/empty/error)」不同層次，兩者都要做。

### 5.2 核心互動實作

[ ] **5.2.0 Pattern Stress Test (NEW — 必跑在 5.2.1-5.2.3 之前)**

對每個「非自明」的互動（編輯 / 刪除 / 確認 / 拖曳 / 點擊選取 / 範圍編輯 / 上傳 / context switch / undo），agent 必須先填這張表再寫實作 spec：

| 欄位 | 必填內容 |
|---|---|
| Interaction | 一句話描述 user action |
| Industry default | SO / shadcn / Apple HIG / Material 對這類動作的 80% 答案（modal 編輯 / inline edit / drawer / popover…）|
| Lib-specific default | 若用第三方 lib（Recharts / dnd-kit / TanStack Table…）, 召回該 lib 最穩定的 API 路徑（chart-level state vs leaf-element onClick…）|
| Why deviate? | 留空 = 走 default；填了 = 必須是 「技術 / a11y / scope」級理由；「我覺得更輕量 / 更酷」**不算**理由 |
| Sprint pivot path | 若選定模式在 Phase 6 ≥30 秒沒搞定，30 秒內能 fallback 回 default 嗎？fallback 路徑明寫 |
| Final choice | default / deviation |

紀律：
- **Default wins ties**：沒明確偏離理由就用 industry default
- **Yellow flag = ≥2 deviations / 同一 cell 內**：STOP 問 user
- **30 秒 pivot rule**（Phase 6 期間生效）：實作期間若選定模式跑 ≥30 秒不穩定（典型徵兆：抓不到 event / 座標飄 / state 不更新），**立即降回 default**，不需重 Phase 5.5 approve
- Phase 5.5 approval gate **只 lock user-facing outcome**（「點 X 可編輯 X」），**不 lock 實作模式**（modal vs popover / chart-level vs leaf-level）

⚠ 跳過此 stress test = Phase 6 高機率踩中 lib 版本 quirks / 互動模式錯配，迭代多輪仍卡。

[ ] **5.2.1 拖曳放置 (Drag & Drop)**：支援檔案配對 / 排序時，必須有明確 hover 與 drop-zone 視覺回饋。

[ ] **5.2.2 操作回饋 (Feedback Loop)**：每個操作必須有回饋。
   - 破壞性操作（刪除）必須有 Modal 確認
   - 一般操作完成必須有 Toast / Snackbar 提示
   - 處理時間 > 1 秒需 Loading / Skeleton 狀態
   - 進度改變必須即時反映在介面數值或 Progress Bar

[ ] **5.2.3 Interaction Guards (NEW — 實作 Phase 2.2.4 中 Interaction 層的清單)**：
   - **雙擊 / 重複送出**：對 Phase 2.2.4 標記的所有 mutation button 加 debounce (300ms) 或 disabled-while-pending；對網路 mutation 加 idempotency key（client-side UUID）
   - **Race condition**：對 Phase 2.2.4 標記的 mutation，pending 期間 disable 同一 form / lock 同一資源；用 AbortController 取消過時的 fetch
   - **Optimistic UI rollback**：對 Phase 2.2.4 標記的 optimistic action，failure path 必須 revert UI 狀態並 toast 錯誤訊息

### 5.3 動畫系統

[ ] **5.3.1 統一 Easing**：全局嚴格套用同一種貝茲曲線（如 `cubic-bezier(0.16, 1, 0.3, 1)`），嚴禁同一頁面混用 ease / linear / ease-in-out。

[ ] **5.3.2 時長控制**：Hover 類 100-150ms / 狀態切換 200ms / 面板展開收合 300-350ms。

[ ] **5.3.3 進出場動畫**：所有 Modal / Toast / Dropdown 必須有 Fade-Slide-in 進場（opacity 0→1, translateY 8px→0）。

### 5.4 Boundary Guards (NEW — 實作 Phase 2.2.4 中 Boundary 層的清單)

[ ] **5.4.1 Auth 邊界**：對 Phase 2.2.4 標記的受保護頁面 / API call：
   - 未登入 → 重導 login 或顯示 unauthorized 訊息
   - Token 過期 → silent refresh 或重導 login
   - 60 min sprint 預設 mock auth: 寫死一個 logged-in user，token 邏輯標 known limitation

[ ] **5.4.2 越權檢查**：對 Phase 2.2.4 標記的「資源型」API call（例：getUserOrder, updateProfile）：
   - 檢查 resource owner === current user
   - 越權嘗試 → 回傳 403 + UI 顯示 "你沒有權限存取此資源"

[ ] **5.4.3 Input 防護**：對 Phase 2.2.4 標記的 user input field：
   - Length cap：text input 上限（例：name ≤ 50, comment ≤ 500），UI 顯示字數計
   - 基本 XSS 防護：顯示 user-generated content 一律經 React 預設 escape（不用 `dangerouslySetInnerHTML`）
   - 數字 input：min / max + step（避免 NaN / Infinity 進入 state）

---

## 📍 Phase 5.5: Design Spec Document & Approval Gate

Agent 產出**兩份**設計交付文件，**STOP 等使用者 approve** 後才能開始 Phase 6 寫 code：

1. `{ProductName}_Design_Spec.md` — 完整設計規格（涵蓋 Phase 0-5，9 個 section，參考 `InstaVoxel_UI_Design_Specification.md`）
2. `{ProductName}_Wireframes.md` — ASCII / Box-drawing wireframes，每個主要 view / modal / state 一張

兩份文件並存，使用者通常先看 wireframes 確認視覺骨架，再看 Design Spec 確認規格細節。

### Wireframe 文件規格（必須遵守）

`{ProductName}_Wireframes.md` 應包含：

- **每個主要 page / view 一張 ASCII wireframe**
- **每個主要 modal / drawer / popover 一張**
- **三狀態（loading / empty / error）各一張**（若狀態差異明顯）
- 用 box-drawing 字元 `┌ ─ ┐ │ └ ┘ ├ ┤ ╔ ═ ╗`
- 標出主要元件位置 / 文字 / icon 標記
- 標出尺寸 hint（若關鍵）
- 標出 半透明 / shadow / hover 等視覺 hint（用括弧文字註）

範例格式：

```
#### M3.4.1 Modal 結構

┌──────────────────────── Bulk Modify Modal ────────────────────────┐
│ Bulk Modifying 4 parts                                          × │
├───────────────────────────────────────────────────────────────────┤
│ Quantity        │ Material               │ Finish                 │
│ [1]  [▲▼]      │ Aluminum 6061  [▼]    │ Standard       [▼]    │
├───────────────────────────────────────────────────────────────────┤
│ Inspection                                                        │
│ ● Standard Inspection                                             │
│   (description text...)                                           │
│ ○ Formal Inspection with Dimensional Report                      │
│   (description text...)                                           │
│ ○ CMM Inspection with Dimensional Report                         │
│   (description text...)                                           │
├───────────────────────────────────────────────────────────────────┤
│                          [Cancel]   [■ Apply to All]              │
└───────────────────────────────────────────────────────────────────┘
(半透明背景遮罩 #3B3B3BB2 + backdrop blur 3.5px)
```

[ ] **5.5.0 產出 `{ProductName}_Wireframes.md`**（給使用者 30 秒掃描視覺結構用）：
   - 主頁面 wireframe (1 張)
   - 每個 modal / drawer / popover (各 1 張)
   - 關鍵三狀態 (loading / empty / error, 視差異程度 1-3 張)
   - 格式遵照上方範例（box-drawing 字元）
   - **不需要彩色 / 真實 mockup，純 ASCII 即可**

[ ] **5.5.1 產出 `{ProductName}_Design_Spec.md`**，依序涵蓋：

   1. **產品定位 & 標竿**（Phase 0 + Phase 1.1）
      - One-liner 產品定義（from Spec）
      - UI 類型判斷（B2B / Productivity / Content / B2C / Dashboard）
      - 業界對標 2-3 個（含核心 UI 策略）

   2. **使用者研究**（Phase 0）
      - Persona 主 / 次（含環境 / 時間 / 認知 / 情緒 / 心智習慣）
      - 起始狀態 + JTBD + 常見錯誤
      - 推導使用流程 + 已對齊的 Demo Happy Path（含 error path 變體）
      - 細化後 AC（每 story 3-5 個）

   3. **功能清單樹**（Phase 1.2）
      - 資訊元素 / 操作元素 / 系統狀態元素 三表
      - 畫面三狀態 (loading / empty / error) 對每個 view 展開

   4. **資訊架構**（Phase 2.1）
      - OOUX 物件導向分析表（entity / 關係 / 屬性）
      - 導覽層級（Sitemap）+ 漸進式揭露策略

   5. **資料層**（Phase 2.2）
      - Data Schema 完整 TypeScript types（含 null/edge 行為宣告）
      - API Function Contracts（input / output / error signatures）
      - Mock Data Seeds（必要時）
      - **Edge Case Surface Map**：entity / interaction × edge category × 實作 phase 對照表

   6. **設計 Tokens**（Phase 3）
      - Brand Hue / 灰階 / 語義色 / 背景圖層
      - Radius / Shadow / Typography
      - 標註 Tailwind config 對應 token

   7. **元件與佈局**（Phase 4）
      - **Component Sourcing 決策表**（依 Phase 4.0 框架）：元件名稱 / 來源（shadcn / 自寫 / Recharts）/ 客製內容 / 理由
      - 元件清單（component inventory，含每個元件的尺寸 / 內容 / 狀態 / hover 行為）
      - 佈局類型（Dashboard / Split Screen / F-Pattern）
      - 對齊軸線設計
      - **註**：Wireframes 在另一份 `{ProductName}_Wireframes.md`，此處只敘述

   8. **互動設計**（Phase 5）
      - 元件 4 基礎狀態（Default / Hover / Active / Disabled）規格
      - 拖曳 / Modal / Toast / Dropdown 行為
      - 動畫 easing + duration 規格
      - **Interaction Guards**（debounce / race / optimistic rollback）逐項規格
      - **Boundary Guards**（auth / 越權 / input 防護）逐項規格

   9. **未決問題**（如有）
      - Agent 不確定的設計決策，標記等使用者裁決

[ ] **5.5.2 STOP — 等使用者 approve**
   - Agent 將兩份檔案路徑呈給使用者：先看 Wireframes（30 秒視覺掃描），再看 Design Spec（細節）
   - 使用者選項：
     - "approved" → 進 Phase 6 開始寫 code
     - "change A, B, C" → loop 回對應 Phase 修改，更新兩份檔案，再次 emit
     - "更新某條目" → 直接編輯對應段落並重 emit
   - **不准在使用者尚未 approve 前動 code**

[ ] **5.5.3 Lock 兩份 MD 為 build blueprint — 注意：只 lock user-facing outcome**
   - Approve 後兩份 MD 即為 Phase 6 的「唯一參考來源」
   - **Lock 的範圍**：user-facing outcome (e.g. 「點 X 可編輯 X」) / Schema / API contracts / Token system / BP-1 / Wireframe layout 骨架
   - **不 lock 的範圍**：實作模式（modal vs popover vs sheet）/ event 模式（chart-level vs leaf-level）/ lib 版本 → Phase 6 自由 pivot，無需重 approve
   - 任何 user-facing outcome 缺失 / drift → Agent 必須先停下來，更新對應 MD 並再次取得使用者 approve，才能繼續

---

## 📍 Phase 6: Build Implementation (NEW)

依 Phase 5.5 已 approved 的 Design Spec MD 寫 code。**設計決策不可在此 phase 自由變更**；遇到設計稿沒覆蓋的狀況必須回 Phase 5.5 補規格 + 重新 approve。

[ ] **6.0 Build-time Debug Discipline (NEW)**

每次跨 folder 同步 / 重大模組 swap (lib 升降版、interaction pattern pivot、大幅 refactor) 後，**強制跑 Signal Trace 4 步檢查**（≤ 1 min）：

1. **Disk-level grep**: 確認新 import / 新 render path 真的寫進對應檔案
2. **Build cache reset**: `rm -rf node_modules/.vite`（Vite 對 dep / config 變動的 cache 不一定 invalidate）
3. **Browser hard refresh**: `Ctrl+Shift+R` + DevTools Network → Disable cache 勾起
4. **若 user 回報「沒反應」**：用 Phase 7.0 Signal Trace 框架排查，**不要直接憑空猜 fix**

⚠ 違反此紀律 = 高機率「我以為改好了 / user 看到舊版」互信耗損。

[ ] **6.0.1 Change-Impact Analysis (NEW — 改動前必跑)**

任何 fix / refactor 開始 edit 前，先**列出影響範圍**（30 秒內完成）：

| 維度 | 該檢查 |
|---|---|
| **Function** | 改的 function 被誰呼叫？修改 signature 上游要不要跟著改？ |
| **Type** | 改的 interface / type 哪些檔案 import？多少使用點要同步更新？ |
| **State / Data shape** | state 加新欄位 / 改 shape，初始 state / reducer / selector 是否同步？舊 session HMR state 會 stale 嗎？ |
| **Component prop chain** | 改 component prop，父 / 兄弟 / 子是否要 propagate？ |
| **Side effect** | useEffect / event listener 依賴是否要更新？ |
| **External library** | 升降版 / 改 API 是否會 break tooltip / animation / event 鏈？ |
| **Build-time** | 改的檔案會被 oxc / esbuild / Vite plugin 處理嗎？編輯中間態會不會 parse fail 殺掉 dev server？ |

**例**：「加 `showTitle: boolean` 到 `ChartConfig`」=
- ✅ Type updated → `types.ts`
- ✅ Default state → `use-chart-state.ts` baseConfig
- ✅ UI toggle → `settings-panel.tsx` DISPLAY section
- ✅ 4 個 chart components 條件 render
- ⚠ 舊 HMR state 沒 `showTitle` → 觸發 controlled/uncontrolled warning → **告知 user 硬刷**

⚠ 跳過 impact analysis = 改完一個 file → 漏掉 3 個檔 → user 反映壞掉 → 反覆補洞。

[ ] **6.0.2 Fix-Verify Loop (NEW — 雙層升級式)**

**第一次 fix**（normal path）：

1. 完成 6.0.1 impact analysis
2. 改全部影響到的檔案（一次到位）
3. 跑 typecheck → pass (**僅 S0 訊號，禁止當 fix 完成證據**)
4. 告知 user **預期 S4 視覺/互動結果** + 請 user 硬刷驗證
5. 等 user 回報 S4 結果

**第二次起 fix**（user 回報 S4 失敗，e.g.「一樣」/「沒反應」/「壞掉」）→ **升級成 instrument-driven**：

1. **立刻停手**，不要再憑直覺改
2. 加 instrumentation `console.log` 在嫌疑信號層（見 Phase 7.0.4 模板）
3. 告知 user 預期看到什麼 console output / DOM signal
4. **收到 user 回報的實際 console output 後再判斷下一步**

⚠ 第一次 fix 走 normal path 是合理效率（多數 fix 一次成）；第二次起若還用直覺改 = 在 hypothesis space 隨機跳，**強制 instrument-first** 斷掉「修 → user 報沒改 → 再修」的浪費信任循環。

⚠ 同一 bug **換 ≥ 2 解法仍未通** = 鎖死 instrument-first 模式直到根因明確。

[ ] **6.1 Scaffold 起手**
   - Vite + React + TS 專案結構
   - 套用 `Tailwind_Design_Token_Setup.md` 的 `tailwind.config.ts` + `src/index.css`
   - 安裝 shadcn/ui + Lucide + 其他 Spec §2 列出的 dep
   - **Pin chart / data-grid / DnD 等 event-heavy lib 至 stable major（避免 latest 抓到剛 bump 的版本，事件 API 在 community 範例間不一致）**

[ ] **6.2 Implement components**（依 Design Spec §7 元件清單逐個）
   - 每個元件遵守 Phase 4.1 法則（borderless / hover-reveal / lightweight headers / dot indicators / etc.）
   - 4 基礎狀態完整（Phase 5.1.1）
   - 套用 Phase 3 design tokens（不可 arbitrary value）
   - 嚴守 BP-1（不卡片化）

[ ] **6.3 Implement layout & navigation**（依 Design Spec §7 佈局 + Phase 4.2）

[ ] **6.4 Implement three states**（loading / empty / error，依 Phase 1.2.4 + Design Spec §3）

[ ] **6.5 Implement interactions**（依 Phase 5.2 + Design Spec §8）
   - 拖曳 / Modal / Toast / Dropdown 行為
   - Fade-Slide-in 進場動畫
   - 統一 easing + duration

[ ] **6.6 Implement Interaction Guards**（依 Phase 5.2.3 + Design Spec §8）
   - 雙擊 debounce / disabled-while-pending
   - Race condition (AbortController)
   - Optimistic UI rollback

[ ] **6.7 Implement Boundary Guards**（依 Phase 5.4 + Design Spec §8）
   - Auth / 越權 / Input 防護

[ ] **6.8 Mock data injection**（依 Design Spec §5）
   - 載入 Mock Data Seeds，確保 demo 跑得起來

每完成 6.x 子步驟，TodoWrite 標 complete，Agent 主動向使用者 1 句 progress summary。

---

## 📍 Phase 7: 檢驗與最終驗證

### 7.0 Signal Trace 框架 (核心診斷工具)

**核心原則**：對任何 user 報告的「X 沒發生 / 不對 / 一樣」類 bug，**列出 user action → 預期結果的完整信號鏈**，每一環必須有可驗證的 proof signal，二分法砍掉未驗證的 hypothesis。**不要直接憑空猜**「應該是 cache / 應該是 lib / 應該是 …」。

---

#### 7.0.1 「對的訊號」階層 — 自我判斷正確性的依據

**這個階層每個 agent 必須記得**，避免「我 fix 了 / user 看到壞」的循環：

| Level | Signal | 可信度 | 何時使用 |
|---|---|---|---|
| S0 | typecheck pass / lint pass | ❌ **僅證明 syntax / types 對**，不代表 fix 正確。**禁止當 fix 完成訊號用** | 編譯前 sanity check |
| S1 | HMR update 沒報錯 | ❌ 只證明 Vite 接到新檔，不代表行為正確 | 確認 hot-reload 鏈接 |
| S2 | `console.log` 在預期位置印出預期值 | ✅ proof of execution path | L1-L3 信號層驗證 |
| S3 | DOM inspect 顯示預期元素 + 屬性 | ✅ proof of render | L4-L5 信號層驗證 |
| S4 | User 在 browser 確認視覺 / 互動正確 | ✅✅ **唯一可信的 final fix signal** | 終局驗證 |

**鐵則**：S0/S1 是「沒寫錯字」訊號，不是「fix 對」訊號。每次 fix 後，**主動 instrument S2/S3 並請 user 回報 S4**，否則就是 hypothesis。

---

#### 7.0.2 Interaction Signal Trace (click → visual update)

| L | 該發生 | Proof signal (cheapest first) |
|---|---|---|
| L0 | DOM 收到 click event | DevTools → Elements → 找對應 DOM node → Event Listeners 面板看 listener 真的綁上 |
| L1 | Lib / framework 攔截 event → call 我們的 handler | `console.log('[X handler] fired', payload)` 第一行 |
| L2 | Handler 抽出正確資料 | `console.log('[X handler] extracted idx=', i, 'value=', v)` |
| L3 | State 更新 | React DevTools → 該 component → state 變了 |
| L4 | Component re-render，目標 DOM 進場 | Inspect → 找預期的 DOM node (`[role="dialog"]`, `<aside>` etc.) |
| L5 | 視覺正確（z-index / position / opacity / display）| 看畫面 / DOM 樣式 |

**ruling-out 紀律**：
- **L1 不 fire** → 信號卡 L0-L1：lib event 攔截錯（lib major bump / Cell 級 deprecated / propagation 被中斷）→ 降版 / 改 leaf-event 模式
- **L1 fire 但 L3 state 沒更新** → React DevTools 確認 setState 真的呼叫 / 確認 component identity 沒換
- **L4 DOM 進來但看不到** → 查 z-index / overflow / opacity / pointer-events / portal target
- 每層 ruling out ≤ 15 秒，總共 1 分鐘內定位

---

#### 7.0.3 Rendering Signal Trace (預期視覺元素 X 沒出現 / 不對)

| L | 該發生 | Proof signal | F12 怎麼看 |
|---|---|---|---|
| L1 State | React state 正確 (e.g. `showCategoryLabels === true`) | React DevTools → component → State 面板 | F12 → Components → 找 component |
| L2 Props | 子元件收到正確 prop | React DevTools → Props 面板 / `console.log` in component body | F12 → Components → 找子元素 |
| L3 Render branch | conditional JSX 進對的分支 | `console.log('branch=', x)` in condition | console |
| L4 DOM 結構 | 預期 DOM node 存在於 DOM tree | DevTools Elements 搜尋 SVG class / selector | F12 → Ctrl+F |
| L5 DOM 內容 | 該 node 有 text / value / 子元素 | 看 innerHTML / element count | Elements → expand |
| L6 視覺 | 沒被 clip / opacity 0 / color = bg / off-screen | Computed style + Box model | Elements → Computed |
| L7 Export-only: lib 內部 animation / 延遲 render | 若是 chart lib，**動畫期間 path 退化**會讓 snapshot 抓到空殼 | DOM count rect/path 數量 | Elements / console.log |

---

#### 7.0.4 Instrumentation 模板 — 「沒反應 / 抓空白」標準 console.log 設計

每當 agent 要 debug bug，**先加這段 instrumentation 到嫌疑點，請 user reproduce 一次貼 console**，再做 fix：

**Interaction bug (click 沒反應)**：

```ts
const handleClick = (payload) => {
  console.log('[X.click] fired', { payload, hasCallback: !!onCallback });
  const idx = payload?.idx ?? payload?.payload?.idx;
  console.log('[X.click] resolved idx=', idx);
  if (typeof idx !== 'number') return;
  onCallback?.(idx);
  console.log('[X.click] callback invoked with', idx);
};
```

**Rendering bug (DOM / SVG 看不到)**：

```ts
// 在預期已 render 完成的時間點
const node = ref.current;
const childCount = node?.children.length;
const svg = node?.querySelector('svg');
const targetEls = node?.querySelectorAll('預期的 selector');
console.log('[X.render DIAG]', {
  wrapperW: node?.offsetWidth,
  wrapperH: node?.offsetHeight,
  childCount,
  svgExists: !!svg,
  svgWidth: svg?.getAttribute('width'),
  svgHeight: svg?.getAttribute('height'),
  innerSvgLen: svg?.innerHTML.length ?? 0,
  targetCount: targetEls?.length ?? 0,
  firstTargetFill: targetEls?.[0]?.getAttribute('fill') ?? '(none)',
});
```

**Export / snapshot bug (PNG 空白 / 內容缺)**：

```ts
// snapshot 前
console.log('[X.export DIAG]', {
  ...上方 render DIAG,
  targetDims: [w, h],
  background: bgValue,
});
const blob = await toPng(node, { ... });
console.log('[X.export DIAG] blob length=', blob?.length ?? 0);
```

**訊號判讀**：
- `wrapperW/H` 跟目標差很多 → flex / CSS 衝突 (L1-L2 失敗)
- `svgWidth/Height` 跟 wrapper 差很多 → ResponsiveContainer / lib 沒 redraw (L4 失敗)
- `targetCount === 1` (應該 ≥ N) → lib 內部 animation 中、path 退化 (L7 失敗) → disable animation / 等更久
- `firstTargetFill === "(none)"` 或 `transparent` → fill computation 失敗 / 被 opacity / clip-path 影響 (L6 失敗)
- `blob length` 很小 (< 5000) → html-to-image clone 完全失敗 (lib 問題)

---

#### 7.0.5 紀律總覽

⚠ 違反以下任一條 = 反覆「修 → user 報告沒改 → 再修」浪費信任：

1. **改動前**先做 Phase 6.0.1 Change-Impact Analysis（function caller / type usage / state shape / HMR state stale 等），**一次改齊所有受影響的檔**，避免漏改補洞
2. **第一次 fix** 走 normal path：一次到位 + 跟 user 講預期 S4 結果 + 等 user 驗證
3. **第二次起 fix**（user 回報 S4 失敗，e.g.「一樣」/「沒反應」）→ **立刻升級 instrument-driven**：加 console.log 印 S2/S3 訊號，等 user 回報實際 output 才判斷下一步
4. **typecheck pass / HMR ok 不可當 fix 訊號** — S0/S1 等於 0 證據
5. 同一 bug **換 ≥ 2 解法仍未通** = 在 hypothesis space 隨機跳 → **鎖死訊號驅動**直到根因明確
6. instrumentation 在 verify 完後**清理掉再 ship**（保留會污染 production console）

### 7.1 視覺品質自檢

[ ] **7.1.1 1px 審查與間距檢查**：全面掃描有無非 4px 倍數的數值？所有顏色是否均來自定義 Token（含 Hue-tinted grays）？

[ ] **7.1.2 視覺雜訊檢查**：再次質問每個邊框、陰影、長駐 Icon 是否必要？能移除就移除。

[ ] **7.1.3 互動驗證**：核心任務流程是否可全程點擊並獲得正確狀態回饋？鍵盤 Escape 是否能關閉 Modal？所有預期改變的數字 / 狀態是否已在 DOM 中正確更新？

[ ] **7.1.4 Design Spec 對照**：逐項對照 Phase 5.5 已 approved 的 Design Spec MD，標出 implementation drift 處（若有），明確標 known limitation 寫進 demo narrative。

### 7.2 Feature Logic / Edge Case 最終驗證

⚠ 此區是「驗證」不是「設計」。設計工作已在 Phase 2.2.4 完成、實作已在 Phase 6 完成。此處逐項勾選實作完整性。**未實作項目要明確標 known limitation 並寫進 demo narrative，不可隱瞞**。

[ ] **7.2.1 Data robustness 驗證**（對應 Phase 2.2.4 Data 層清單）：
   - Phase 2.2.4 標記的每個 null / undefined / empty / 巨型 / 邊界數字場景，UI 是否實際呈現合理
   - n = 0 list 是否有 empty state（first-time vs filtered 各自訊息）
   - 數字 NaN / Infinity 是否會出現在畫面（應該被 guard 掉）

[ ] **7.2.2 Interaction guard 驗證**（對應 Phase 5.2.3，實作於 Phase 6.6）：
   - Phase 2.2.4 標記的每個 mutation button 是否有 debounce / disabled-while-pending
   - 連點 5 次是否只送 1 次 request
   - 慢網路 (Chrome devtools throttle Fast 3G) 下能否 reproduce race-free

[ ] **7.2.3 Error handling 驗證**：
   - 所有 API call try-catch 是否完整（用 grep 找 await 看是否每個都被 try-catch 包）
   - Error 訊息三要素是否完整：(a) 發生什麼 (b) 為什麼 (c) 怎麼做
   - 至少 1 個 error path 可 demo（reproducible）

[ ] **7.2.4 Boundary 驗證**（對應 Phase 5.4，實作於 Phase 6.7）：
   - Phase 2.2.4 標記的 auth / 越權 / input 防護是否全數實作
   - 嘗試直接改 URL 跳到受保護頁面，是否會擋
   - Input 超過長度上限，是否有 UI 阻擋

[ ] **7.2.5 Demo readiness 驗證**：
   - Happy path 從 step 1 到結尾是否暢通（手動跑一次計時）
   - 至少 1 個 demo-able error path（不是 console.log 才看得到）
   - Mock data 是否 realistic（非 "Test 1" / "Lorem ipsum"）
   - 開 DevTools 看 console，無紅色 error（warning 可接受）

---

## ▶ BP-1: 嚴禁卡片式設計 (No Card-Based Design)

**問題分析**：卡片式設計（圓角容器 + 填色背景 + 可能的陰影）會造成視覺噪音、破壞資訊層級與設計專業度。

### 禁止的元素

- 圓角填色背景容器（border-radius + background-color 組合）
- 陰影浮起效果（box-shadow）— 除非為 modal / toast / dropdown 浮層必需
- 以背景色區分欄位
- 卡片式圓形 badge / 標記（如圓形編號容器）

### 替代設計技法

1. **垂直分欄線 (Column Divider)**：多欄版面用 1px 細線分隔，而非填色背景
   ```css
   width: 1px; background: var(--border); margin: 0 48px;
   ```

2. **水平分隔線 (Horizontal Rule)**：列表項目之間用 1px 底線分隔，建立結構感
   ```css
   border-bottom: 1px solid var(--border);
   ```

3. **縮排層級 (Indentation Hierarchy)**：以 padding-left 建立資訊層級，而非嵌套容器

4. **直接標記 (Direct Labeling)**：用粗體 / 變色文字直接標記重點，不需包裹容器

5. **扁平編號 (Flat Numbering)**：用 01/02/03 純文字編號 + 粗體強調，取代圓形 badge

6. **圖標 + 文字行 (Icon-Text Row)**：圖標直接與文字水平排列，無需卡片包裝

---

## 終止與回退策略 (60 min sprint)

若預算超過，按以下順序砍掉條目：

1. **先砍 Phase 7.1.2 polish 項**：視覺雜訊複查
2. **再砍 Phase 5.3.3 進出場動畫**：直接 show / hide 即可（同步從 Design Spec 移除）
3. **再砍 Phase 4.1.5 / 4.1.6 polish**：透明按鈕 / optical padding
4. **再砍 Phase 4.1.2 hover-reveal**：所有按鈕直接 visible
5. **再砍 Phase 5.4.2 / 5.4.3 boundary 細項**（保留 5.4.1 auth），砍掉的條目寫進 demo 的 known limitations
6. **再砍 Phase 5.2.3 race condition / optimistic rollback**（保留 debounce）
7. **再砍 Phase 7.2.1 / 7.2.2 / 7.2.3 / 7.2.4 驗證項**：只留 7.2.5 demo readiness（demo 跑不通就是 fail）
8. **緊急狀況**：Phase 5.5 簡化 — 只 emit 「精簡版 Design Spec」（One-liner + Happy Path + Data Schema + 元件清單），跳過完整詳述，但仍須使用者 approve

**不可砍（demo 必死保項）**：
- Phase 0.7（Happy path 對齊）
- Phase 2.1.1（OOUX）
- Phase 2.2.1（Data Schema）
- Phase 2.2.4（Edge Case Surface Map — 即使不全部實作也要列清單給 demo 用）
- Phase 3（Design tokens — 直接 copy 不花時間）
- Phase 1.2.4（畫面三狀態 — demo 必經）
- **Phase 5.5 approval gate**（不能省，使用者必須 approve）
- Phase 5.2.3 debounce（最常被 panel 故意連點測）
- Phase 7.2.5（demo readiness）

砍條目時，AI 必須：
1. 在 TodoWrite 標記「skipped: <條目> reason: 時間預算」
2. 同步在 Design Spec MD 對應段落標 ~~刪除線~~ 並註明「砍掉 / known limitation」
3. 在 demo narrative 主動提出，不可隱瞞
