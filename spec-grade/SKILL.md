---
name: spec-grade
description: PM 生完 PRD 後跑一次打分，檢查是否包含 QA 測試需要的所有元素（範圍、RC 參數、ELK 事件、平台特定行為、AC 例外、後端相依交付與驗收環境等 14 條）。未達 22/28 通過閾值 → 直接在對話裡列出未達項目與補件建議，PM 補完 spec 重跑 → 直到通過才進下一步。當用戶為 PM 想檢查自己寫的 PRD 是否 QA-ready、或 QA 想反向 audit 現有 PRD 缺什麼時觸發。
version: 1.0.0
disable-model-invocation: false
argument-hint: [PRD 來源（gitlab URL / 本地檔絕對路徑 / --paste 直接貼內容）]
---

## 任務資訊

用戶提供的 PRD 來源：$ARGUMENTS

從上述參數中解析 PRD 來源。**單一來源**：gitlab MR URL、gitlab file URL、本地 .md 絕對路徑，或以 `--paste` 開頭表示接下來使用者會貼入內容。

---

# PRD 打分協議

## 一、協議目的

本協議定義 `spec-grade` skill 主控（以下稱「主控」）執行「PRD 打分 → 補件清單 → 迭代」流程時必須遵守的規範，確保：

1. 每條必要元素依 `reference/spec_required_elements.md` **統一評分**，PM 與 QA 認知一致
2. 打分結果**具體可行動**——不是「這裡不夠好」，而是「請補 §X 加入 XXX」
3. 支援**多輪迭代**（v1、v2、v3...）：PM 補件重跑，可比對前後版本進步
4. **不擋 spec、不改 spec**——本 skill 只**評分**與**產出補件清單**，spec 的實際修改由 PM 自己在 gitlab 完成

---

## 二、啟動前準備

### 2.0 開場告知

【必須】skill 一開始執行就向使用者輸出：

> 📋 開始 PRD 打分。我會依 `reference/spec_required_elements.md` 的 **14 條必要元素**逐項評分（滿分 28、通過線 22/28；Android-only 或 iOS-only 時基準降為 26、通過線 21；Web-only 時基準降為 24、通過線 20），輸出分數 + 補件清單。**未達 2 分的每一項**都會**直接印在對話裡告訴你要補什麼**（不用另開 md 檔）；同時也會落檔 `grading_v{N}.md` 供事後回顧。這個 skill **不改你的 spec、不 push gitlab**，只評分；你補完 spec 重跑 `/spec-grade <URL>` 就是 v2。

### 2.1 解析啟動參數

【必須】從 `$ARGUMENTS` 判定來源類型：

| 形態 | 判定 | 處理方式 |
|-----|-----|---------|
| **gitlab URL**（`http://gitlab...` / `https://gitlab...`）| URL 開頭 | 用 `curl` 或 `gh api` 抓 raw content（見 §三 G1.2）|
| **本地檔**（絕對路徑、`.md` 副檔名）| 檔案存在 | Read tool 讀入 |
| **`--paste`**（互動模式）| 開頭 `--paste` | 在 §三 G1 停下請使用者貼入 spec 內容 |

【禁止】自己判斷 spec 內容形態或改寫（那不是本 skill 的職責）。

### 2.2 偵測既有未完成打分／建立工作目錄

【必須】：

1. 掃 `.tmp/spec-grade/` 下所有子目錄，若有 `phase_status.report` 非 `done` 的，列給使用者「續跑 or 新開？」
2. 新開時：以當前時間戳建 `.tmp/spec-grade/{YYYY-MM-DD_HHmm}/`
3. 該目錄下建 `revisions/v1/` 子目錄（若使用者以既有 timestamp 為基底重跑，則版本 +1）

### 2.3 初始化 progress.json

【必須】在 `.tmp/spec-grade/{timestamp}/revisions/v{N}/progress.json` 寫入：

```json
{
  "timestamp": "2026-07-30_1400",
  "revision": "v1",
  "based_on": {
    "prd_source": "<原始 URL 或檔案路徑>",
    "previous_grading": "<若為 v{N>1} 則指向前一版 grading_v{N-1}.md，否則空>"
  },
  "phase_status": {
    "G1_load_prd": "not_started",
    "G2_grade": "not_started",
    "G3_report": "not_started"
  },
  "last_updated": "<ISO 8601>"
}
```

【必須】每 phase 狀態變更（`not_started` → `in_progress` → `done`）都更新此檔。

---

## 三、Phase G1：載入 PRD

【必須】更新 `phase_status.G1_load_prd = "in_progress"`。

### G1.1 gitlab URL 抓取

若來源是 gitlab URL：

1. 判定是 **MR URL**（`.../merge_requests/N`）還是 **file URL**（`.../blob/branch/path.md` 或 `.../raw/branch/path.md`）
2. **File URL**：直接 `curl` raw content（gitlab 支援 `/raw/` 路徑）
3. **MR URL**：抓 MR description + 讀 changed files 中的 `*.md` / `*.txt` 檔（PM 的 PRD 通常在 MR description 或以 markdown 檔提交）
4. gitlab 若需認證：檢查是否有 `GITLAB_TOKEN` env var；沒有則提示使用者「請設 GITLAB_TOKEN 或改給本地檔路徑」，不 fail-loud 但 skill 中止

【必須】把抓到的 PRD 原文落檔到 `{revision_dir}/prd_source.md`。

### G1.2 本地檔讀取

若來源是本地檔絕對路徑：

1. Read tool 讀入
2. 複製一份到 `{revision_dir}/prd_source.md`（原檔保留不動）

### G1.3 `--paste` 互動模式

若來源為 `--paste`：

1. 停下告訴使用者「請把 PRD 內容貼在下一則訊息」
2. 使用者貼完後，把內容存到 `{revision_dir}/prd_source.md`
3. 使用者可用多則訊息貼分段，最後說「貼完了」

【必須】更新 `phase_status.G1_load_prd = "done"`。

---

## 四、Phase G2：逐項評分

【必須】更新 `phase_status.G2_grade = "in_progress"`。

### G2.1 載入評分依據

【必須】Read `reference/spec_required_elements.md` 完整內容，確認 14 條元素的**定義**與**評分規則**（缺 0 / 部分 1 / 完整 2）都在 context 中。

### G2.2 平台範圍判定（決定 N/A 條目）

【必須】讀 `prd_source.md`，掃描平台範圍聲明：
- 若 spec 明確寫「本次 Android only」／「iOS 不涵蓋」 → 第 10 條 iOS 平台特定行為標 **N/A**
- 若 spec 明確寫「本次 iOS only」／「Android 不涵蓋」 → 第 9 條 Android 平台特定行為標 **N/A**
- 若 spec 明確寫「本次 Web only」／未涵蓋任何 mobile 平台 → 第 9、10 條**皆**標 **N/A**
- 若跨平台 或 未明確聲明 → 依 spec 實際涵蓋平台判定

N/A 條目**不計分、不列入總分基準**：
- Android-only 或 iOS-only：總分基準降為 **26** 分、通過線 ⌈26×0.8⌉ = **21**
- Web-only：總分基準降為 **24** 分、通過線 ⌈24×0.8⌉ = **20**

### G2.3 逐項評分

【必須】對 14 條元素逐一評分：

1. 對每條元素，在 `prd_source.md` 中**搜尋對應章節或內容**
2. 依 `spec_required_elements.md` 的**完整(2) / 部分(1) / 缺(0)** 規則判定
3. 記錄：
   - 分數（0/1/2/N/A）
   - **依據**（引用 spec 中的段落／章節；若缺項則說「未找到相關章節」）
   - **具體補件建議**（若分數 <2，給「請補：XXX」；例：「請補 §5 加入 Firebase RC 設定範例，含 key 名 / JSON 值 / 值的來源」）

【禁止】自己腦補 spec 沒寫的東西當作「有寫」；找不到即為 0 分。

【禁止】對「文字寫得好不好」打主觀分——評分只看**必要資訊有無**，不看文筆／排版／篇幅。

### G2.4 統計

【必須】計算：
- **總分**：所有非 N/A 條目的實際得分總和
- **總分基準**：所有非 N/A 條目滿分總和（有 N/A 則基準降低）
- **通過線**：`ceil(總分基準 × 0.8)`
- **狀態**：
  - `總分 >= 通過線` → 🟢 通過
  - `總分 = 通過線 - 1` 或 `通過線 - 2` → 🟡 邊緣通過（建議補件再送）
  - `總分 < 通過線 - 2` → 🔴 未達通過閾值

【必須】更新 `phase_status.G2_grade = "done"`，把評分結果存到 `{revision_dir}/scoring.json`。

---

## 五、Phase G3：產出報告

【必須】更新 `phase_status.G3_report = "in_progress"`。

### G3.1 補件優先建議

【必須】依「缺件嚴重度」排序未達 2 分的條目：

**優先度排序規則**：
1. **[高優] 完全缺（0 分）**：這些是硬缺、測試員完全開不了工，PM 必補
2. **[中優] 部分（1 分）**：資訊不完整，測試員能開工但會踩坑，PM 應補
3. **[低優] N/A** 或已 2 分：不列入補件

同層級內按 A-G 章節順序排列。

### G3.2 產出 grading_v{N}.md

【必須】在 `{revision_dir}/grading_v{N}.md` 寫入報告，格式如下：

```markdown
# PRD 打分報告 — v{N}

**打分時間**：{timestamp}
**PRD 來源**：{source_url_or_path}
**基底版本**：{previous_grading 或「首版」}

---

## 📊 評分結果

**總分**：{score} / {base} ({percentage}%)
**通過線**：{pass_line}（滿分 {base} × 80%）
**狀態**：{🟢 通過 / 🟡 邊緣通過 / 🔴 未達通過閾值}

{若 v2+：附「與上一版對比」，例如 v1 20/28 → v2 26/28 (+6)}

---

## 📋 逐項評分

### A. 範圍界定 ({A_score}/{A_base})

| # | 項目 | 分數 | 依據 / 建議 |
|---|-----|-----|-----------|
| 1 | 變更範圍與改動類型 | {icon} {n}/2 | {evidence 或 建議} |
| 2 | 不做的事（Out of scope）| {icon} {n}/2 | {...} |
| 3 | 相依既有功能與回歸範圍 | {icon} {n}/2 | {...} |

### B. 前置條件與帳號 ({B_score}/4)

（同格式）

### C. 設定參數 ({C_score}/4)
### D. 埋點與觀察 ({D_score}/4)
### E. 平台環境 ({E_score}/{4 或 2 依 N/A})
### F. 驗收與例外 ({F_score}/4)
### G. 導航 ({G_score}/2)
### H. 後端相依 ({H_score}/2)

（每段同 A 段格式：一列一項、含 icon / 分數 / evidence 或建議）

---

## 🔧 補件優先建議

### [高優] 完全缺 — PM 必補

1. **§{n} {項目名稱}**（0/2）
   - 目前狀態：{原因}
   - 請補：{具體要補什麼、含建議範例}

（依此列出所有 0 分項）

### [中優] 部分 — 資訊不足，PM 應補

（依此列出所有 1 分項）

---

## ✅ 已通過項目

（列出所有 2 分項，只列項目名稱與一句話依據，不佔篇幅）

---

## 🔄 迭代建議

- 補完上述「高優」項目後預估分數：{new_score_estimate}
- 若同時補完「中優」項目：{new_score_estimate_full}
- 補完後重跑：`/spec-grade {source_url}` → 產出 v{N+1}
```

### G3.3 完成回報（直接印在對話裡）

【必須】更新 `phase_status.G3_report = "done"`。向使用者回報時**必須把關鍵內容直接印在對話裡**（使用者才不用另開 md 檔）：

**1. 狀態一句話**（永遠印）：
- `🟢 通過`：`{score}/{base}（{percentage}%）— 通過`
- `🟡 邊緣通過`：`{score}/{base}（{percentage}%）— 邊緣通過（{score} 剛好等於或接近通過線 {pass_line}）`
- `🔴 未達通過閾值`：`{score}/{base}（{percentage}%）— 未達通過閾值 {pass_line}（差 X 分）`

**2. 逐項評分表**（永遠印，14 項每項一列，含「沒過原因」）：

```
| # | 項目 | 分數 | 狀態 / 沒過原因 |
|---|-----|-----|--------------|
| 1 | 變更範圍與改動類型 | 2/2 | ✅ 通過 |
| 2 | 不做的事（Out of scope）| 1/2 | ⚠️ 沒過：{一句話原因，例：3 條散在文中無專屬 Out of Scope 章節（L5、L130、L157）} |
| 3 | 相依既有功能 | 2/2 | ✅ 通過 |
| 4 | 使用者狀態與帳號 tier | 2/2 | ✅ 通過 |
| 5 | Remote Config 參數 | 1/2 | ⚠️ 沒過：{一句話原因，例：缺 JSON 範例 / 值來源 / A/B experiment 說明} |
| 6 | 前端 fallback | 2/2 | ✅ 通過 |
| 7 | ELK 事件 | 1/2 | ⚠️ 沒過：{一句話原因，例：只有描述性名稱、無具體 UPA_* 事件名} |
| 8 | UI 可觀察行為 | 1/2 | ⚠️ 沒過：{一句話原因，例：混雜「排入排程」等內部狀態，前端 QA 觀察不到} |
| 9 | Android 平台特定行為 | 2/2 | ✅ 通過 |
| 10 | iOS 平台特定行為 | N/A | ⚪ 不計分（本 spec Android-only）|
| 11 | AC 驗收條件（Scenario）| 2/2 | ✅ 通過 |
| 12 | 已知缺口 / AC 例外 | 2/2 | ✅ 通過 |
| 13 | 新增 UI 導航路徑 | 2/2 | ✅ 通過 |
| 14 | 後端相依交付項與驗收環境 | 1/2 | ⚠️ 沒過：{一句話原因，例：有列後端依賴欄位但未標正式機/測試機交付狀態、也沒指定驗收環境} |
```

**核心要求**：
- **每一項都列**（不只章節加總）—— 使用者一眼看完 14 項哪些過、哪些沒過
- **未達 2 分項目**在「狀態 / 沒過原因」欄位**當場寫一句話原因**（不要只寫 ⚠️ 沒過、要接原因）
- N/A 項目明示原因（例：本 spec Android-only）
- 通過項目寫 ✅ 通過 即可，不用附長篇解釋

**3. 未達 2 分項目的詳細診斷**（若有）——【必須】**逐條印出「spec 原文 + 沒過原因 + 補件建議」三段**：

```
⚠️ §N 項目名稱 (1/2)  或  ❌ §N 項目名稱 (0/2)

【spec 原文】
> L{行號}: 「{直接複製 spec 該行 / 該段的實際文字}」
> L{行號}: 「{...}」
（若整段缺，寫：「未找到相關章節或內容」）

【沒過原因】
{一句話說明為何未達 2 分：例「三條散在文中無彙整，QA 翻閱易漏」/ 「有 key 名但缺 JSON 範例、值來源、experiment 說明」}

【請補】
{具體建議，可以子彈點列出多項}
```

**核心原則**：
- **有寫但寫得不對** → 引用 spec 該段原文 + 一句話說出「哪裡不對」 + 補件建議
- **完全沒寫** → 【spec 原文】欄寫「未找到相關章節或內容」 + 補件建議直接說「請新增一節 XXX 描述 YYY」
- **引用行號**：讓 PM 一鍵定位到 spec 對應位置去改（尤其 gitlab 有 L{N} 錨點連結時最方便）
- **原文複製要一字不差**：不要摘要／改寫 spec 內容——PM 要看到自己實際寫了什麼

**4. 迭代預估**（若非 🟢）——印一到兩行：
   - 補完所有未達項目後預估分數
   - 提示補完後重跑指令：`/spec-grade <原始 source>` → 產出 v{N+1}

**5. 若過**：印一句「✅ 可進下一步」加上一行「full report 落檔：`{grading_v{N}.md 絕對路徑}`」（供事後回顧或存檔用，但**主要內容已在對話裡了**）

【禁止】只印「請看 `grading_v{N}.md`」把責任丟給使用者去開檔——**未達項目與補件建議必須直接印在對話裡**（這是本 skill 的核心 UX，md 檔是備份不是主要輸出）。

【必須】本 skill **產出報告即止**，不 handoff、不改 spec、不 push gitlab。

---

## 六、多版本迭代

### 6.1 版本偵測

【必須】skill 啟動時，若使用者以「同一 PRD 來源」重跑（判定方式：`$ARGUMENTS` 與既有某 v{N} 的 `based_on.prd_source` 相同），則自動：
1. 沿用該 timestamp 目錄
2. 建立 `revisions/v{N+1}/`
3. `progress.json.based_on.previous_grading` 指向前一版報告

### 6.2 對比前後版本

【必須】v{N>1} 的報告中包含「與上一版對比」段落：
- 總分變化（+X 或 -X）
- 每項分數變化（哪些條目補齊了、哪些新崩了）

---

## 七、禁止行為

- ❌ 自己改 spec 或 push gitlab（本 skill 只評分，不動 spec）
- ❌ 對文筆／排版／篇幅打分（只看必要資訊有無）
- ❌ 腦補 spec 沒寫的東西當「有寫」（找不到即 0 分）
- ❌ 因 spec 缺 A 就對 B 也扣分（每條獨立評分）
- ❌ 自動 handoff 到別的 skill（產出即止）
- ❌ 未跑完 14 條就早停（除非 §八 極端狀況）

---

## 八、極端狀況

**Q1：PRD 太短，沒有章節結構怎麼辦？**
A：仍逐項評分。多數條目會落 0 分——這反映 spec 真的缺內容，屬預期行為，不是 skill 誤判。

**Q2：spec 混雜多個 feature 一起寫，一份 spec 涵蓋 3 個變更怎麼算？**
A：以整份 spec 為單位打分。若某條元素「只寫了 feature A 沒寫 feature B」，該條算部分(1)。

**Q3：gitlab URL 抓不到（權限問題 / 401）**
A：告知使用者「gitlab 抓取失敗，請設 `GITLAB_TOKEN` env var 或改給本地檔路徑」，中止 skill、不繼續評分。

**Q4：PRD 為圖為主、文字少（如全部靠 Figma link）**
A：本 skill 只評文字內容；圖片不解析。若 spec 主要靠圖，多數條目會 0 分——**建議 PM 至少把 RC 參數 / ELK 事件 / AC 這類結構化資訊落文字**，才能被評分（也才能被 QA 讀懂）。

**Q5：spec 用英文寫**
A：仍可評分；評分邏輯不依賴中文關鍵字，看內容有無而非語言。

---

## 九、自我檢查

### 9.1 啟動前
- □ `$ARGUMENTS` 已解析出來源
- □ 已檢查 `.tmp/spec-grade/` 未完成打分
- □ 已建工作目錄並初始化 `progress.json`

### 9.2 G1
- □ PRD 已載入並落檔到 `{revision_dir}/prd_source.md`

### 9.3 G2
- □ 已 Read `reference/spec_required_elements.md`
- □ 已判定平台範圍決定 N/A 條目
- □ 14 條全部評分完成、無跳過
- □ 每個 <2 分項都有「請補：XXX」具體建議

### 9.4 G3
- □ `grading_v{N}.md` 已產出、包含所有必要段落
- □ 已回報使用者：狀態一句話 + 報告路徑 + 主要缺件摘要
- □ **未** handoff、**未** 動 spec

---

## 十、常見問題

**Q1：分數多少算 PM 可以進下一步？**
A：**≥ 22/28（≈79%）**為通過線。22-23 分算邊緣通過（🟡），建議還是補完再進下一步。Android-only 或 iOS-only 時基準降為 26、通過線為 21；Web-only 時基準降為 24、通過線為 20（同樣約 80%）。

**Q2：某條元素我沒實際要做（如 iOS 這次不涵蓋、或本產品純 Web），要扣分嗎？**
A：不會。skill 會偵測「本次 Android only / iOS only / Web only」聲明，自動把不涵蓋的平台條目標 N/A、不計分。

**Q3：跑完後補 spec 重跑，會累積版本嗎？**
A：會。同一 PRD 來源重跑會自動建 v2、v3...，且新版報告會附「與上一版對比」。

**Q4：這個 skill 會幫我改 spec 嗎？**
A：**不會**。本 skill 只評分與產出補件清單；spec 的實際修改請 PM 自己在 gitlab 完成。

**Q5：QA 也可以用這個 skill 反向 audit PM 寫好的 spec 嗎？**
A：可以。用法一樣：`/spec-grade <URL>`。QA 拿到報告後可以：
- 若過了 → 可進入下一步的測試計畫設計 / 測試準備
- 若沒過 → 把補件清單丟給 PM 補，補完再跑 → 過了才進測試準備階段
