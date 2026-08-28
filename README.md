# Agent Skills

給 AI coding agent(Claude Code / Codex 等)用的一組工作流程 skill。
每個資料夾是一支 skill,核心是 `SKILL.md`——裡面是**流程與判準**,不是提示詞魔法:
它規定「做這類任務時,哪幾步不可跳過、什麼情況要停下來、產出要長什麼樣」。

## 安裝

Claude Code:

```bash
# 使用者層(所有專案都能用)
cp -r <skill 資料夾> ~/.claude/skills/

# 或專案層(只在這個 repo 生效)
cp -r <skill 資料夾> <你的專案>/.claude/skills/
```

Codex 走同樣的目錄式自動發現:

```bash
cp -r <skill 資料夾> ~/.codex/skills/
```

放好後開新 session 即可用 `/<skill-name>` 觸發,或讓 agent 依 description 自動載入。

## 內容

| Skill | 什麼時候用 | 它逼你做什麼 |
|---|---|---|
| **openspec** | 開始任何非瑣碎的改動之前 | 先把「要改什麼/為什麼/驗收條件」寫成版本化 Markdown 提案,同意後才實作,完成後 archive 併回主規格——下一輪 AI 從同一份真相源出發(CLI:`npm i -g @fission-ai/openspec`) |
| **spec-grade** | 寫完 PRD / 規格,想知道「工程與 QA 讀完能不能開工」 | 依 14 條必要元素逐項打分(範圍、Out of scope、狀態分支、設定參數、fallback、事件、平台、AC、已知缺口、導航、外部相依),未達標直接列出「請補什麼」;**只評分不改稿** |
| **jira-ops** | 用程式讀寫工單(查、開單、留言、改狀態) | 先讀欄位登錄表與慣例再動手;開單走 createmeta 必填欄位 + 抄同型單的合法格式;**留言要真 @mention 得用 ADF node**,純文字 @ 不會通知 |
| **uiux-design-check** | 設計/重設計任何介面 | ①Checklist 逐項檢核 ②**上網找 5 個真實範例並萃取 5 條 Best Practice** ③**為要做的視覺效果找業界最佳實作**(玻璃質感就去看 iOS 怎麼做) ④**給 2~4 個 ASCII 原型,每個代表不同使用者心智模型** ⑤挑定後才產規格;token 必須可由設定檔注入 |
| **presentation-builder** | 要把分析/進度做成給主管看的簡報 | 先回答「這份簡報要對方做什麼決定」;每頁標題是主張句;第一頁執行摘要含 insight/三數字/A-B 抉擇表/一個資源要求;每個數字要能自己說出母體與時間窗;產出 HTML→PDF 並逐頁自檢 |

## 建議的串接順序

```
需求 → openspec 提案 → spec-grade 打分(不足就補) → (含 UI 時)uiux-design-check
     → 實作 → openspec archive → 要報告時 presentation-builder
```

openspec **產生並管理**規格,spec-grade **檢驗**規格夠不夠完整——兩者互補不重疊。

## 這些 skill 的共同設計原則

1. **流程有閘門**:某些步驟不可跳過(例:UIUX 沒找範例不准畫、簡報答不出「要對方做什麼決定」就不要做)。
2. **產出可驗收**:每支都定義了「怎樣算做完」,不是靠感覺。
3. **誠實優先**:資料不足就標「需要補什麼」,不編造(spec-grade 找不到即 0 分、簡報數字必附母體)。
4. **失敗模式表**:每支都帶一張「常見症狀 → 根因 → 解法」,那是實戰累積出來的,比正向規則更省時間。

## 授權

MIT
