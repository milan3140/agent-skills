🚀 增量設計專用：新增介面 AI 規格產出 Check List (Agent 建造指南版)
此 Check list 是為 AI Agent 最佳化的「生成與建造指南」，專用於在既有系統上新增介面或功能。它明確定義了哪些應「繼承」原系統以保證一致性，哪些應「植入現代化法則」以拉升產品整體的專業美學與操作體驗。

*遵循 Apple HIG 設計原則、 Material Design 與 Minimalist style，但以 Linear / Stripe / Notion / Vercel 等現代精緻 SaaS 為美學標竿
*清晰直觀，明確引導使用者使用並符合其視覺與操作習慣，最大程度降低使用負擔為最高原則
*Symbol 或 Icon 一律使用 SVG 或 Lucide (備用 Heroicon / Phosphor Icons / Material Icons)，嚴禁使用 Emoji。
*嚴禁使用卡片式設計（含圓角填色背景容器、陰影浮起容器等 UI 卡片風格元素）
*原則：增量不是「複製貼上舊缺點」，而是要在保持品牌一致性的前提下，建立高通透性、低認知負荷的統一設計美學邏輯系統。
*風格保持嚴謹專業

以本 Check list 檢核新增介面設計在這些面向上如何實作、各部分是為了達到哪些設計目的、各部分如何實現此設計目的。

分析完本設計後，上網搜尋此類型網站的範例
(可參考 1. AWWWARDS.com / 2. Dribble.com / 3. Mobbin.com / 4. 競爭者類似功能 / 5. 跨產業解決方案)
搜查分析設計重點與 Best practices ，比對得出共通之最佳設計，並遵循本 Check list 的嚴格規格，制定出屬於本新增介面的最佳設計規格文件 (附上使用者原始輸入以利後續 Agent 製作)，存放於 Project-instavoxel/UI_Design 中。

📍 Phase 1: 新需求探索與邊界定義 (Scope Definition)
確立新功能在既有系統中的定位與目標。

[ ] 🟢 1.1.1 [直接繼承] 產品 UI 介面種類 (UI Types): 從原規格讀取並鎖定產品類型（如：B2B 工業級應用），新介面必須嚴格遵守該類型的核心設計準則（如防呆、高資訊密度），不可偏離原產品調性。
[ ] 🔴 1.2.1 [全新定義] 新介面目標與痛點: 根據輸入的新需求，確立「這個新介面」要解決的特定痛點與核心任務（Core Task）是什麼？
[ ] 🔴 1.2.2 [全新定義] 影響範圍評估 (Impact Radius): 列出這個新功能會牽動到系統中哪些「既有物件或資料」（例如：新增「快速報價」會牽動「訂單」與「客戶名單」）。

📍 Phase 2: 資訊架構整合與動線 (IA Integration & Flow)
將新功能無縫接軌到原有的地圖中。

[ ] 🟡 2.1.1 [混合擴充] 局部關聯 Sitemap 與層級控制:
- 保留與標記: 讀取原 Sitemap，明確標示出相關的「既有父節點」與「相鄰節點」。
- 插入新節點: 規劃準確位置。
- 層級限制: 從首頁到達新功能的核心操作區域，最大點擊次數不得超過 3 次。
[ ] 🔴 2.1.2 [全新定義] 定義入口與出口 (Entry & Exit Points):
- 入口: 使用者從「哪裡」、「點擊什麼」進入？
- 出口: 任務完成後導向何處？（上一頁/成功畫面/其他模組）
[ ] 🔴 2.2.1 [全新定義] 新任務流程 (Task Flow): 畫出線性最短操作路徑。跨步驟時，必須攜帶前綴上下文，避免使用者依靠記憶操作 (符合 Miller's Law)。

📍 Phase 3: 視覺基礎規範嫁接 (Design Tokens Integration)
這裡是既有品牌 DNA 與現代化美學法則交匯的關鍵。即使舊系統有設計缺陷，新介面的區塊也必須遵守以下嚴格規格進行升級。

[ ] 🟡 3.1.1 [優化繼承] 色彩系統 (Color System) - 告別純灰與死板色:
- 繼承主色: 提取原系統品牌主色 Hue (如 Purple 260°)。
- 建立品牌灰階 (Tinted Grays): 新介面中**絕對禁止使用純灰 (#888, #555)**。所有文字、邊框與背景灰，都必須帶有品牌 Hue (Saturation 8-15%)。這會讓新區塊瞬間變高級。
- 背景層次: 使用 3 層洗色 — Level 0 (基底 #FAFAFA), Level 1 (內容區 #FFFFFF), Level 2 (浮層 #FFFFFF + 微陰影)，取代舊系統可能的厚重背景。
[ ] 🟡 3.2.1 [嚴格規範] 間距與尺寸系統 (Spacing) - 嚴格 4px Grid:
- 即使舊系統間距隨意，新介面區塊的 Padding/Margin/Gap **必須嚴格遵守 4px 的整數倍** (4, 8, 12, 16, 20, 24, 32, 40, 48px)。嚴禁 5px, 10px, 15px。
[ ] 🟡 3.3.1 [嚴格規範] 視覺風格與形狀 (Shape & Elevation):
- 圓角系統 (Radius): 繼承原風格大方向，但限制在 3 級內 (如: 按鈕 4-6px, 模塊 8px, 容器 12-16px)。
- 陰影系統 (Shadows): 新介面所有浮層必須使用「帶品牌色的近黑 rgba(...)」，嚴禁原系統可能使用的濃重純黑死硬陰影。
[ ] 🟡 3.4.1 [優化繼承] 排版字體 (Typography) - 微排版精修:
- 繼承原字族。但新版塊中的行高必須舒適 (內文 1.5-1.6)。
- 全大寫標籤 (Uppercase tags) 必須增加 letter-spacing (0.05em)。
- 數值欄位強制套用 `font-variant-numeric: tabular-nums` 進行對齊。

📍 Phase 4: 介面元件與新佈局設計 (UI Components & Layout)
運用現代化的視覺減法，組裝新任務佈局。

[ ] 🟡 4.1.1 [混合擴充] 全域框架與新局部佈局:
- 繼承全域導覽 (Navbar & Sidebar)。
- 新內容區佈局: 選擇最適合新任務的模式 (Split Screen, Dashboard Grid, Single Column)。確保元素左邊界對齊 2-3 條剛性的隱形垂線。
[ ] 🔴 4.2.1 [嚴格規範] ▶ BP-1: 嚴禁卡片式設計與邊框干擾 (No Card-Based Design):
新介面的內容區塊嚴禁被包裹在「圓角填色背景容器」或「陰影浮起容器」中。
替代設計技法:
(1) 垂直分欄線: 多欄版面使用 1px 細線分隔 (`width: 1px; background: var(--border);`)。
(2) 水平分隔線 / 留白: 列表項目之間使用 1px 底線或純粹加大 Row Gap 分隔。
(3) 輕量化標題 (Lightweight Headers): 面板標題不要用厚重的深色背景 Bar。改用透明背景 + 小標籤文字 (`11px/600/uppercase/gray-500`) 並加 1px 淺色底線。
[ ] 🔴 4.3.1 [全新定義] 高密度與複雜元件的細節處理:
- Hover-reveal: 列表中的次要操作按鈕（刪除、編輯）預設 `opacity: 0`，hover 時才出現，降低靜態視覺密度。
- 扁平識別: 使用「01/02 純文字編號 + 粗體強調」或「6px 色點 (Dot Indicators)」取代圓形 badge 與繁複 Icon 狀態標記。
- 融入感按鈕: 若按鈕需放在深色 Header 上，改用 `rgba(255,255,255, 0.15)` 半透明樣式取代實心填色。

📍 Phase 5: 狀態管理與業務邏輯 (State Management & Business Logic)
外觀雖然繼承，但內在的「條件判斷」與「回饋流」必須全面現代化。

[ ] 🔴 5.1.1 [全新定義] 專屬業務邏輯狀態 (Business Logic States) 與防呆:
- 定義核心操作元件的觸發條件。什麼情況下按鈕會 Disabled？(必須防範錯誤送出，並清楚提示原因)。
[ ] 🔴 5.2.1 [嚴格規範] 元件狀態與回饋完整性 (Component State & Feedback Loop):
- 所有新加入的可互動元件必須明確包含 4 種狀態: Default, Hover (背景變色/不透明度改變), Active/Pressed (微縮放或加深), Disabled。
- 破壞性操作 (刪除) 必須有 Modal 確認。
- 一般操作成功/失敗必須有 Toast / Snackbar 提示。若載入 > 1 秒需有 Loading 狀態。
[ ] 🟡 5.3.1 [優化繼承] 動畫系統 (Motion):
- 即使舊系統缺乏規範，新介面的所有動效必須統一！全局嚴格套用同一種貝茲曲線 (如 `cubic-bezier(0.16, 1, 0.3, 1)`)。
- 所有新增的 Modal, Toast, Dropdown 都必須要求配置 Fade-Slide-in 進場動畫 (opacity 0->1, translateY 8px->0，時長 200-300ms)。

📍 Phase 6: 整合檢驗與規格輸出 (Integration Validation & Handoff)

[ ] 🔴 6.1.1 [全新定義] 解析度與視覺噪音自檢 (1px Polish & Noise Check):
- 新介面的所有數值是否完全符合 4px Grid？各種灰色是否都有帶品牌 Hue？
- 是否確實消滅了所有的卡片式設計與非必要的邊框？次要按鈕是否做到了 Hover-reveal？
[ ] 🔴 6.2.1 [全新定義] 增量規格文件輸出 (Delta Spec Generation):
- 產出最終文件時，只需輸出針對此「新介面」的規格。
- 文件起頭必須明確聲明：「本介面之色彩、字體、基礎框架繼承【原系統設計規範】，本文件詳述基於現代化 Minimalist SaaS 美學所定義之新版塊佈局、4px 網格系統、帶彩色相灰階與互動回饋邏輯。」