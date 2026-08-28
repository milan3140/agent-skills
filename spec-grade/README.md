# /spec-grade — PRD 打分 skill

> **給誰用**：PM（主要）／ QA（反向 audit 用）
> **什麼時候用**：PM 生完 PRD、準備 handoff 給 RD/QA 前跑一次；未達通過線就補件重跑
> **產出什麼**：分數 + 未達項目與補件建議**直接印在對話裡**（不用另開檔）；同時落檔 `grading_v{N}.md` 供事後回顧

---

## 為什麼要這個 skill

PRD 常常寫得看起來很完整，但**測試員實際開跑時才發現**：
- 前置條件寫「一般帳號」——實際上要區分試用中／已購買／訪客等 tier，模糊詞會導致測試根本觸發不了目標行為
- RC 章節只寫「透過 Remote Config 控制」——**沒給 key 名、沒給 JSON 範例、沒說值的來源**，測試員拿到 spec 也建不起環境
- 沒提**平台 quirk**——Android VIP 內購測試要上 Play Store Beta；
- 沒標**已知缺口／AC 例外**——QA 遇到會全部當 new bug 開單

這個 skill 把 QA 的痛點整理成 **14 條必要元素**，PM 跑完就知道自己哪裡漏寫。

---

## 快速使用

```bash
# 從 gitlab MR 打分
/spec-grade https://gitlab.acme.tw/team/project/-/merge_requests/510

# 從 gitlab 檔案 URL 打分
/spec-grade https://gitlab.acme.tw/team/project/-/blob/main/prd.md

# 從本地 markdown 檔打分
/spec-grade C:/Users/user1/Documents/AutoTesting/.tmp/mkt-11748-spec/prd_android_v2.5.md

# 直接貼內容進來（互動模式）
/spec-grade --paste
```

---

## 你會拿到什麼

**直接印在對話裡**（你不用開檔就看得到），長這樣：

```
🟢 22/26（84.6%）— 剛好過線
（本 spec 為 Android-only，iOS 條目 N/A，基準降為 26、通過線 21）

| # | 項目 | 分數 | 狀態 / 沒過原因 |
|---|-----|-----|--------------|
| 1 | 變更範圍與改動類型 | 2/2 | ✅ 通過 |
| 2 | 不做的事（Out of scope）| 1/2 | ⚠️ 沒過：3 條「不做」散在文中，無專屬章節（L5、L130、L157）|
| 3 | 相依既有功能 | 2/2 | ✅ 通過 |
| 4 | 使用者狀態與帳號 tier | 2/2 | ✅ 通過 |
| 5 | Remote Config 參數 | 1/2 | ⚠️ 沒過：缺 JSON 範例、值來源、A/B experiment 說明 |
| 6 | 前端 fallback | 2/2 | ✅ 通過 |
| 7 | ELK 事件 | 1/2 | ⚠️ 沒過：只有描述性名稱、無具體 UPA_* 事件名 |
| 8 | UI 可觀察行為 | 1/2 | ⚠️ 沒過：混雜「排入排程」等內部狀態、QA 觀察不到 |
| 9 | Android 平台特定行為 | 2/2 | ✅ 通過 |
| 10 | iOS 平台特定行為 | N/A | ⚪ 不計分（本 spec Android-only）|
| 11 | AC 驗收條件 | 2/2 | ✅ 通過 |
| 12 | 已知缺口 / AC 例外 | 2/2 | ✅ 通過 |
| 13 | 新增 UI 導航路徑 | 2/2 | ✅ 通過 |
| 14 | 後端相依交付項與驗收環境 | 2/2 | ✅ 通過 |

未達 2 分項目的詳細診斷（含 spec 原文引用）：

⚠️ §2 不做的事（Out of scope）(1/2)

【spec 原文】
> L5: 「本 capability 不改動該頁任何既有行為，僅新增一個進入來源與一個曝光埋點」
> L130: 「MUST NOT 新增任何對外連結入口，亦 MUST NOT 修改既有的連結分派元件（deep link 分派、推播轉導、FCM 服務）」
> L157: 「MUST NOT 新增或修改任何 DeepLinkPage route，MUST NOT 改動 RedirectActivity / DeepLinkUtils / ChipKFcmListenerService」

【沒過原因】
3 條「不做的事」散落在 spec 不同位置，QA 翻閱時容易漏看；規範要求集中在專屬 Out of Scope 章節。

【請補】
新增一節「## Out of Scope」，把上述 3 條集中條列，避免 QA 誤把相鄰議題當本次驗收範圍。

---

⚠️ §5 Remote Config 參數 (1/2)

【spec 原文】
> L161: 「提醒清單 MUST 讀自既有 Remote Config key `newUserGainVipPlan2025` 的**頂層** `trialReminderNotification`（與 `planType` / `planInfo` 同層），型別為**清單**，每筆含 `minutesBefore` / `title` / `message`」

【沒過原因】
有 key 名（`newUserGainVipPlan2025`）與 schema，但**缺 3 樣**：
1. 沒給 baseline JSON 範例（三則 1440/720/60 各自的實際 title/message）
2. 沒說值的來源（PM 自填 / 從既有配置抄 / 需 RD 提供）
3. 沒提 A/B experiment 干擾說明（該 key 有 running experiment 會擋住測試帳號）

【請補】
在 RC 章節加：
- Baseline JSON 範例（含三則各自 title/message）
- 標注值的來源
- 明說「本次驗證期間該 key 無 running experiment」或「需暫停 experiment X」

---

⚠️ §7 ELK 事件 (1/2)

【spec 原文】
> L246-253:
> | 事件 | 觸發點 | 參數 |
> | 提醒排程建立 | 成功排入一則提醒 | 來源 ＋ 剩餘分鐘數 |
> | 提醒顯示 | 通知**實際貼出** | 來源 ＋ 剩餘分鐘數 |
> | 提醒點擊 | 使用者點擊通知 | 來源 ＋ 剩餘分鐘數 |

【沒過原因】
事件表用中文描述性名稱（「提醒排程建立」），沒有 QA 到 ELK 查詢時用的實際 event name（如 `UPA_TrialReminder_scheduled`）。

【請補】
事件表補上具體 `UPA_*` 事件名稱：
- `UPA_TrialReminder_scheduled`（排程建立）
- `UPA_TrialReminder_showed`（顯示）
- `UPA_TrialReminder_clicked`（點擊）
- `UPA_TrialReminder_viewed`（落地頁觀看）

或明確指向 `prd.md` v2.5 §埋點章節（若那邊已列出）。

---

⚠️ §8 UI 可觀察行為 (1/2)

【spec 原文】
> L79-81: 「App MUST 在**每次啟動時**重算並重建提醒排程」
> L83: 「**重算 MUST 是原子操作**：『算出應有時點』與『讓實際排程收斂到該結果』MUST 在同一個互斥區間內完成」
> L87-89: 「**已到期、尚未送達的排程 MUST NOT 被重算撤除**」

【沒過原因】
主要驗收行為（收通知、點通知、開頁面）是 UI 可觀察的，但混雜大量「排入排程／撤除排程」等內部狀態要求——前端 QA 只能觀察「有沒有發通知」，看不到 JobScheduler 內部物件變化，需 dumpsys 或 RD 交付才能驗。

【請補】
把「排程物件級變化」類條目改為 UI 可觀察表達：
- 用「三個時點下拉通知欄各看到一則」代替「排入 3 筆」
- 用「重開機後 App 開啟仍能收到後續預定通知」代替「排程物件級重建幂等」
- 或明確標「本項屬 RD/自動化交付驗證，前端 QA 手動可跳過」

🔄 補完 §5/§7 兩項即可 26/26 滿分
📄 完整報告：.tmp/spec-grade/{timestamp}/revisions/v1/grading_v1.md
```

**重點**：
- **14 項每項一列**——一眼看完哪些過、哪些沒過
- **沒過的每一項** = spec 原文（複製貼過來的實際文字 + 行號）+ 沒過原因 + 補件建議
- PM 打開對話就看到自己 spec 哪句寫得不對，一鍵改
- md 檔仍會落檔備份（**不是主要輸出**）

---

## 14 條必要元素（滿分 28、通過線 22）

| 章節 | 條數 | 分數 |
|-----|-----|-----|
| **A. 範圍界定** | 3 | 6 |
| A1 變更範圍與改動類型 | 2 |
| A2 不做的事（Out of scope）| 2 |
| A3 相依既有功能與回歸範圍 | 2 |
| **B. 前置條件** | 1 | 2 |
| B4 使用者狀態與帳號 tier | 2 |
| **C. 設定參數** | 2 | 4 |
| C5 Remote Config（含 A/B experiment 干擾說明）| 2 |
| C6 前端內建預設與 fallback | 2 |
| **D. 埋點與觀察** | 2 | 4 |
| D7 ELK 事件（名/時機/屬性）| 2 |
| D8 UI 可觀察行為 | 2 |
| **E. 平台特定行為** | 2 | 4 |
| E9 Android 版本相依 + Play Store Beta（若涉內購）| 2 |
| E10 iOS 版本相依 + APN | 2 |
| **F. 驗收與例外** | 2 | 4 |
| F11 AC 驗收條件（Scenario 結構）| 2 |
| F12 已知缺口 / AC 例外 | 2 |
| **G. 導航** | 1 | 2 |
| G13 新增 UI 導航路徑 | 2 |
| **H. 後端相依** | 1 | 2 |
| H14 後端相依交付項與驗收環境 | 2 |

**完整定義**：`reference/spec_required_elements.md`（skill 目錄內）

**N/A 規則**：
- Android-only（spec 明確聲明「本次 Android only」）→ iOS 條目 N/A、基準降為 26、通過線 21
- iOS-only → Android 條目 N/A、基準降為 26、通過線 21
- Web-only（未涵蓋任何 mobile 平台）→ Android/iOS 皆 N/A、基準降為 24、通過線 20

**團隊分工前提**（本 skill 預設以 App QA / 前端 QA 團隊為主要對象；其他部門若團隊組成不同——例如全端 QA、純 Web 團隊——可 fork `reference/spec_required_elements.md` 改對應的豁免規則）：
- 註冊流程 / 帳號建立步驟（假設 QA 有既存 helper 腳本）
- 後端 API 細節（假設本團隊只驗前端；全端 QA 團隊可自行加碼要求）
- RC 生效方式 / debug 工具 UI 入口 / Build 類型（QA 操作 SOP）
- AC 中的實作語言類名（Kotlin / Swift / TypeScript 等，AC 給 RD 看的實作契約）

---

## FAQ

### Q: 我 spec 沒寫 iOS，會被扣分嗎？
A: 不會。只要在 spec 明確寫「本次 Android only」，iOS 條目自動 N/A、不計分、基準降為 26（通過線 21）。反之亦然。Web-only（未涵蓋任何 mobile 平台）→ 基準降為 24、通過線 20。

### Q: 分數多少算過？
A: **≥ 22/28（≈79%）** 為通過。22-23 分算邊緣通過（🟡），建議還是補完再進下一步。Android-only 或 iOS-only 時基準降為 26、通過線為 21；Web-only 時基準降為 24、通過線為 20（同樣約 80%）。

### Q: 結果不用開 md 檔就看得到嗎？
A: 對。所有未達項目與補件建議會**直接印在對話裡**，你就地讀就好。md 檔（`grading_v{N}.md`）仍會落檔在 `.tmp/spec-grade/{timestamp}/revisions/v{N}/` 供事後回顧或存檔用，但**不是主要輸出**。

### Q: 補完 spec 重跑會怎樣？
A: 同一 PRD 來源重跑會自動建 v2、v3...；新版報告會附「與上一版對比」（總分變化、哪些條目補齊了）。

### Q: 這 skill 會改我的 spec 嗎？
A: **不會**。只評分、只產報告。spec 的實際修改請你自己在 gitlab 完成。

### Q: gitlab 抓不到怎麼辦？
A: gitlab 若需認證：檢查是否有 `GITLAB_TOKEN` env var；沒有的話改給本地檔路徑就好。

### Q: 為什麼把 RC 的 A/B experiment 干擾也列必要元素？
A: 實務常見坑——PM 把 RC 值改對了，但目標 key 剛好有一個 running experiment，測試帳號被分到 variant 而拿不到 PM 設的值。QA 會誤判「PM 沒改到值 / bug」，其實是 experiment 擋著。所以 spec 要明說「本次驗證需先暫停 experiment X」或「該 key 目前無 experiment」。

### Q: QA 也可以用這個 skill 嗎？
A: 可以。QA 拿到 PM 的 PRD 後跑一次做反向 audit：
- 過了 → 可進入下一步的測試計畫設計 / 測試準備
- 沒過 → 把補件清單丟給 PM 補、補完再跑 → 過了才進測試準備階段

---

## 詳細協議與規則

見同目錄 `SKILL.md`。README 只給概念與用法；`SKILL.md` 是主控協議（適合 debug 或深入了解 skill 行為時參考）。

---

## Changelog

- **2026-07-30 v2**：依團隊分工調整——移除「帳號準備方式」（QA 自有 helper）、「後端 API 影響」（只測前端）；「Android 準備」簡化為只驗版本相依 + Play Store Beta；AC 移除 Kotlin 術語扣分；UI 導航移除 DebugSetting 入口要求。總分 30→**26**、通過線 24→**21**（Android/iOS-only 時 24→**20**）。輸出改為**直接印在對話裡**（md 檔仍落檔備份）。
- **2026-07-30 v1**：首版 skill，15 條必要元素、30 分制、通過線 24/30；來源支援 gitlab URL / 本地 .md / `--paste` 互動模式
