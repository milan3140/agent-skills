# Jira PM Ops — Onboarding（第一次使用必跑，約 15 分鐘）

> 目標：跑完本頁後，你的機器可以用程式讀單、查單、開單、傳附件——不用開瀏覽器。
> 適用：Acme 作者產品線 PM（PROJ／OPS／CSUCCESS／EDMIS 專案）。

## 1. 產生 Personal API Token

1. 用你的公司 Atlassian 帳號登入 https://id.atlassian.com/manage-profile/security/api-tokens
2. 「Create API token」→ 名稱建議 `pm-ops-cli`，效期選最長
3. 複製 token（只顯示一次）

## 2. 設環境變數（Windows）

```powershell
setx JIRA_SITE "https://your-org.atlassian.net"
setx JIRA_EMAIL "<你的公司信箱>"
setx JIRA_API_TOKEN "<剛複製的 token>"
```

⚠ **`setx` 只影響「之後新開」的終端機**——設完把 Claude Code／終端整個關掉重開，當前視窗讀不到新值。
⚠ Token 是機密：**不進 git、不貼對話、不寫進任何檔案**。只活在環境變數。

## 3. 驗證三連發（照順序跑，全過才算完成）

```bash
# ① 身分與 accountId（把回傳的 accountId 記下來，開單時「負責PM」「reporter」要用）
py scripts/jira_api.py whoami

# ② 專案權限（PROJ 要有 CREATE_ISSUES/EDIT_ISSUES；沒有=帳號層問題，找主管開權限，換工具沒用）
py scripts/jira_api.py myperms PROJ

# ③ 實際讀一張單（能看到標題與描述=通了）
py scripts/jira.py TICKET-1000
```

## 4. 常見錯誤對照

| 症狀 | 原因 | 解法 |
|---|---|---|
| HTTP 401 | token 錯/過期，或 setx 後沒重開終端 | 重產 token → setx → **重開終端** |
| HTTP 410 on `/search` | 舊版 search API 已汰換 | 用 `/rest/api/3/search/jql`（本 skill 的腳本都已用新版） |
| HTTP 403 / 開單失敗 | 專案權限不足 | 先跑 `myperms`，帳號層問題找主管，別換工具重試 |
| 建單 400 | 欄位格式錯（自訂欄位要 `{"id":"..."}`、多人欄位要陣列） | 照 `reference/field_registry.md` 的格式，或先撈同型舊單抄欄位 |
| 主控台中文變亂碼 | Windows 主控台編碼 | 指令前加 `PYTHONIOENCODING=utf-8`，或輸出重導向到檔案再讀 |
| curl 送中文 payload 變 400/500 | Windows curl 把中文編成 big5 | 一律用 Python（本 skill 腳本），別用 curl 送中文 |

## 5. 你需要知道的五個 Jira 專案

| 專案 | 用途 | 你會做什麼 |
|---|---|---|
| **PROJ** | 作者產品線開發單（bug／故事／任務／Stage-bug） | 最常用：開單、驗收、追蹤 |
| **OPS** | 通用工程＋QA Task | 送 QA 回歸測試、通用工程需求 |
| **CSUCCESS** | 客服單 | 讀客訴 → 轉開 PROJ 單 → 回寫進度 |
| **EDMIS** | Server／基建資源申請（表單自動開單） | 申請 DB／主機；查自己申請過什麼 |
| （看板） | VIP2 作者看板 board 2625 | 元件「VIP2作者(VIP2看板4)」＋Sprint 決定單子出現在哪 |

## 6. 下一步

讀 `SKILL.md`（任務索引：你想做的每件事對應哪支腳本哪份慣例），知識全貌看 `BLUEPRINT.md`。
