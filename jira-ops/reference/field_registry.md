# 欄位真值總表（開單/改單照抄；來源＝真單實測，非文件推測）

> 鐵律：**寫死的 id 會過期（Sprint／版本每期變）**——標「動態查」的一定當場查，其餘 id 變動率低可直接用。
> 建單 400 的九成原因＝欄位格式錯：自訂欄位傳 `{"id":"..."}`、多人欄位傳陣列、下拉選項傳 `{"value":"..."}`。拿不準就先撈一張同型舊單，抄它的欄位格式。

## 專案與單型（issuetype）

| 專案 | 單型 | id |
|---|---|---|
| PROJ | 故事（需求/新功能） | 10010 |
| PROJ | 漏洞（bug） | 10015 |
| PROJ | 任務（小任務/優化/UI） | 10013 |
| PROJ | 大型工作（Epic） | 10000 |
| PROJ | Stage-bug（QA 回歸產物） | 10071 |
| OPS | QA Task | 10054 |
| OPS | 任務 | 10013 |

## PROJ 元件（components）

| 名稱 | id | 何時掛 |
|---|---|---|
| iOS_RD | 10062 | iOS 平台單 |
| Android_RD | 10061 | Android 平台單 |
| UI | 10059 | UI 設計單 |
| VIP2作者(VIP2看板4) | 12559 | 看板歸屬（Product A/Product B/Product C/Product D共用）——**掛了才會進看板** |

## 作者 Epic（parent）

| 作者 | Epic |
|---|---|
| Product A（定存股） | TICKET-1000 |
| Product B（型態學） | TICKET-1000 |
| Product C（動能選股） | TICKET-1000 |
| Product D（放風箏） | TICKET-1000 |

## 常用 accountId

| 角色 | 人 | accountId |
|---|---|---|
| iOS 主力（四作者共用） | 吳尚容 RD-iOS | `ACCOUNT_ID_PLACEHOLDER` |
| Android 主力（Product A/Product C） | 鄭宇婷 RD-Android | `630f08214fbe9c4bd0edb348` |
| Android 主力（Product D）＋後端 crash | 黃建榮 RD-Mobile | `ACCOUNT_ID_PLACEHOLDER` |
| UI 設計 | 陳宣諠 kana_chen | `ACCOUNT_ID_PLACEHOLDER` |
| QA | 蔣明廷 Ming_Chiang | `63f08ae6333d0e2ec17048f3` |
| **你自己**（負責PM/reporter） | — | 跑 `py scripts/jira_api.py whoami` 查 |

派工原則：衍生 bug／修正單**優先指派原修復者**（修復連續性）；判不出就留空＋草稿註明「派工待定」，別硬派。

## 自訂欄位（customfield）

| 欄位 | key | 格式 |
|---|---|---|
| 負責 PM | customfield_10059 | **陣列** `[{"accountId":"..."}]` |
| Sprint | customfield_10020 | 數字 id（**動態查**：`jira_api.py sprint <同看板任一單>`；VIP2 看板 board 2625，目前 active＝15429「永久」sprint） |
| Bug 來源 | customfield_10169 | `{"id":"..."}`：使用者回報 10375／QA 測試 10376／RD或PM內部通報 10377／作者回報 10441 |
| 影響版本 | versions | 陣列 `[{"id":"..."}]`（**動態查**：`jira_api.py versions "<作者>" --ios`；慣例掛該 App＋平台**最大版**；修在 PAGEs 公版就掛 `PAGEs_iOS_x.y.z` 版號） |
| 到期日 | duedate | `"YYYY-MM-DD"`——**開單必填，使用者沒給就先問一句再送** |

## Bug 五評估欄位（開單時初估，不確定標「估·待驗」請 PM 確認）

| 欄位 | key | 選項 id |
|---|---|---|
| 發生頻率 | customfield_10069 | 1(<2%)=10134／2(2-5%)=10135／3(5-10%)=10136／4(>10%)=10137 |
| 影響用戶數 | customfield_10070 | 1未知=10138／2百人=10139／3千人=10140／4萬人=10141 |
| 影響權益 | customfield_10071 | 1=10142／2低=10143／3中=10144／4高=10145 |
| 能否重現 | customfield_10072 | 1不可=10146／3可提供重現=10147 |
| 當天修復 | customfield_10073 | 0不用=10148／4要=10149 |

1-3 分鐘估法：可重現看有無影片/步驟（有=3）；影響權益看核心價值＋有無變通（整功能死無解=4、有變通=3、小功能=2）；當天修復＝阻斷付費/登入/交易且無變通才 4；用戶數/頻率沒真數就標估·待驗。

## 關聯（issueLink type）

| type name | 用途 |
|---|---|
| 議題分割 | 故事主單→平台單（inward=主單, outward=平台單） |
| Relates | CS 單↔開發單、衍生單↔原單（**轉單必掛，只在描述引文字不算**） |
| Blocks | QA 單 blocks 需求單（QA 過才能關需求） |
| Cloners | Stage-bug 轉正式 bug 單 |

## OPS 專案必填（通用工程/QA）

- 一般任務三必填：customfield_10053 需求發起單位（**陣列** `[{"value":"營運部"}]`）／10054 需求分類（`{"value":"維運"}`）／10061 需求執行單位（**陣列** `[{"value":"通用工程"}]`）
- QA Task：customfield_10053 用 `[{"id":"10179"}]`＝金融事業群-共用；duedate 必填；描述用 markdown（非 ADF）

## API 端點速查

- 查詢：`/rest/api/3/search/jql`（游標分頁 nextPageToken；**舊 `/search` 已 410 汰換**）
- 建單/改單：`POST|PUT /rest/api/3/issue`；留言 `/issue/{key}/comment`；關聯 `/issueLink`
- 附件：上傳 `POST /issue/{key}/attachments`（multipart＋`X-Atlassian-Token: no-check`）；下載 `GET /attachment/content/{id}`
- 讀單**記得帶 `attachment` 欄位**——漏帶會誤判「無附件」（CS 單常有用戶錄影）
- **建版本**：PM 帳號通常**沒有** ADMINISTER_PROJECTS（Jira API `POST /version` 會 404「no permission」）——**走 PM 夥伴工具庫自助**：`POST http://192.168.105.175:8899/api/jira-create-version`，body `{"name":"<完整版本名>","description":"..."}`（需 VPN；版本名照該 App 既有格式抄，如 `Product D-放風箏選股_iOS_2.5.3`；回 `{ok,id,name}`）。建完把 id 掛回單的 versions 欄（改單權限 PM 有）。實例：TICKET-1000 目標版 2.5.3（id 23913）
