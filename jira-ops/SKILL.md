---
name: jira-pm-ops
description: Acme 作者產品線 PM 的 Jira 全流程 skill——程式化讀單/查單/開單/留言/附件/關聯(免開瀏覽器),加上從真單歸納的開單慣例(bug/故事三張/CS轉單/QA/PAGEs)與硬規範(五層閘門/免責句/語氣)。當使用者要「開單」「查單」「轉客服單」「送QA」「追進度」「寫驗收回饋」時使用。首次使用先跑 ONBOARDING.md。
---

# Jira PM Ops

> **第一次用？先跑 [ONBOARDING.md](ONBOARDING.md)**（token/環境變數/驗證三連發，15 分鐘）。
> 知識全貌與學習路徑見 [BLUEPRINT.md](BLUEPRINT.md)。

## 核心心法（三句話）

1. **一切走 API，不開瀏覽器**——讀單、開單、附件、關聯全部程式化，可重複、可稽核。
2. **慣例查真單，不憑印象**——開任何不熟的單型前，先撈一張同型舊單抄 parent/components/欄位格式（`--jql "summary ~ '關鍵字'"`）；上游對話的措辭≠產品事實。
3. **單子只放 RD 拿了就能做的內容**——待設計、待確認的東西留在草稿階段，別外包給 RD 盤查。

## 任務索引（想做什麼 → 用什麼）

| 任務 | 工具/慣例 |
|---|---|
| 讀一張單（含留言、附件） | `py scripts/jira.py TICKET-1000` |
| JQL 查單 | `py scripts/jira.py --jql "..." --max 20`（JQL 範例見 conventions §8） |
| 查自己身分/權限/版本/Sprint | `py scripts/jira_api.py whoami / myperms / versions / sprint` |
| 留言、建關聯、傳附件、轉單搬附件 | `py scripts/jira_api.py comment / link / attach / copyatt` |
| 開 bug 單 | 範本 `scripts/example_create_ticket.py`＋慣例 [conventions §1](reference/ticket_conventions.md) |
| 開雙平台故事（三張套裝） | 同上 §2（主單＋iOS＋Android＋議題分割；平台單＝完整複製） |
| 客服單轉開發單 | §3（處置四型→轉單→Relates→回寫【進度更新】範式） |
| 送 QA／追 QA 進度 | §4（QA Task 開 OPS；追進度＝QA Task 狀態＋Stage-bug 雙軌） |
| PAGEs 公版修正票 | §5（兩流派；影響版本掛公版版號） |
| 寫驗收回饋留言 | §7（三段格式／部分修復／雙平台各貼各單） |
| 欄位 id 對照 | [reference/field_registry.md](reference/field_registry.md)（先查這裡再寫 payload） |

## 硬規範（違反任一條＝這張單先別送）

1. **開單前五層閘門＋MVP 切分**（詳 conventions §0-1/2）——需求真偽、資料契約自查、邏輯定案、呈現三問（用戶看了能做什麼決策？答不出＝不顯示）、範圍沿用具體指認
2. **機器研判段加免責句**（固定句在 conventions §0-3）
3. **「要求別人做事/回覆」的內容未經 PM 允許不得發布**——先自問查不查得到，查得到自己查掉預填
4. **到期日必填**——沒給就開單前問一句
5. **語氣**：評估型寫商量感、驗收標準寫白話場景、不加親暱開場；已定案 bug 直述
6. **來源連結**：每張單描述必有一行「來源:＜可點連結或出處＞」
7. **附件**：bug 必附截圖/錄影；讀 CS 單必帶 attachment 欄位；轉單附件原檔搬運（copyatt）

## 檔案地圖

```
jira-pm-ops/
├── SKILL.md                    ← 本頁(任務索引+硬規範)
├── ONBOARDING.md               ← 首次設置(token/env/驗證/常見錯誤)
├── BLUEPRINT.md                ← 知識藍圖(六層地圖+學習路徑+來源出處)
├── reference/
│   ├── field_registry.md       ← 欄位真值總表(id/accountId/API端點)
│   └── ticket_conventions.md   ← 單型慣例+流程+語氣+JQL(全部真單歸納)
└── scripts/
    ├── jira.py                 ← 讀單/JQL(含附件顯示)
    ├── jira_api.py             ← whoami/權限/版本/sprint/留言/關聯/附件/搬附件
    └── example_create_ticket.py ← 開單範本(bug+三張套裝,ADF色塊)
```
