---
name: openspec
description: |
  Spec-driven development(規格先行)工作流:用 OpenSpec CLI 把「要改什麼」先寫成版本化的 Markdown 規格提案(change proposal),取得同意後才實作,完成後 archive 回主規格。適用「新功能、跨檔案重構、行為變更、多輪迭代且需要對齊」的任務。
  觸發:「用 openspec」「先寫規格再做」「這個要先提案」「spec-driven」「把需求變成 spec」「archive 這個 change」。
  與 spec-grade 的分工:**openspec 產生並管理規格**(流程與檔案結構),**spec-grade 檢驗規格夠不夠完整**(14 條必要元素打分)。兩支搭配使用:openspec propose → spec-grade 打分 → 補件 → 實作 → archive。
version: 1.0.0
---

# OpenSpec — 規格先行的開發流程

> 官方:https://github.com/Fission-AI/OpenSpec ｜ https://openspec.dev/
> 本 skill 是「怎麼在日常工作中用它」的操作指南,不是它的複製品;CLI 行為以官方為準。

## 為什麼用它

AI agent 最大的浪費是**「做完才發現方向錯」**。OpenSpec 的解法是把規格變成 repo 裡**版本化的 Markdown**:

- 每次改動先產生一份 **change proposal**(要改什麼、為什麼、驗收條件)
- 人看過同意後才進實作
- 完成後 `archive`,規格差異併回主規格 → **下一次 AI 執行從同一份真相源出發**

沒有 API key、不需要 MCP,產物就是純文字檔,可 review、可 diff、可回溯。

## 安裝(一次)

```bash
npm install -g @fission-ai/openspec@latest   # 需要 Node.js 20.19+
openspec --version
```

在專案根目錄初始化:

```bash
cd <你的專案>
openspec init          # 建立 openspec/ 目錄與 agent 指令檔
openspec update        # 之後升級 CLI 時,把指令檔同步到新版
```

`init` 會依你用的工具寫入對應的 agent 指令(支援 Claude Code、Codex、Cursor、Copilot 等 20+ 客戶端)。

## 日常流程(五個動作)

| 動作 | 指令 | 什麼時候 |
|---|---|---|
| **提案** | 在 AI 助理裡下 `/opsx:propose <要做什麼>` | 開始任何非瑣碎的改動之前 |
| **看清單** | `openspec list` / `openspec list --specs` | 想知道現在有哪些提案/規格 |
| **檢視** | `openspec view` | 互動式看規格與提案全貌 |
| **管理提案** | `openspec change` | 修改、拆分、關閉提案 |
| **歸檔** | `openspec archive <change-name>` | 實作完成且驗收通過後,把 delta 併回主規格 |

## 在本工作流中的用法(與其他 skill 的接法)

```
需求進來
   │
   ├─ openspec propose            ← 產生 change proposal(要改什麼/為什麼/AC)
   │
   ├─ /spec-grade <proposal 路徑>  ← 打分:14 條必要元素夠不夠(範圍/Out of scope/
   │                                 狀態分支/設定/事件/AC/已知缺口/外部相依)
   │      └─ 未達 22/28 → 依補件清單補 proposal → 重跑
   │
   ├─ (若含 UI)/uiux-design-check  ← 對標 → Best Practice → ASCII 原型 → 設計規格
   │
   ├─ 實作
   │
   └─ openspec archive <change>    ← 規格併回主線,下一輪從新真相源開始
```

## 使用守則(實務上會踩的)

1. **提案要小到能一次驗收**。一份 proposal 對應一個可獨立驗收的行為變更;跨三個子系統的大改請拆成多份。
2. **AC 寫成 Given/When/Then**,而且要能對應到「使用者看得到的東西」或可觀察事件——這也是 spec-grade 第 11 條的判準。
3. **不要在 proposal 裡寫實作細節**(用什麼函式、哪個檔案);那屬於實作階段,寫進去會讓規格很快過期。
4. **archive 前先確認驗收真的過了**。archive 會改寫主規格,等於宣告「這就是現在的行為」——沒驗收就 archive,規格會開始說謊。
5. **規格與程式碼同一個 PR**。分開送會出現「規格說 A、程式碼做 B」的漂移。
6. **既有專案(brownfield)先跑一次 `openspec init` 再逐步補**:不要試圖一次把現有系統全寫成規格,從「接下來要改的那塊」開始長。

## 什麼時候**不要**用

- 一行修正、typo、純重新命名 → 直接做,寫提案的成本高於價值
- 探索性 spike(還不知道要做什麼)→ 先做原型,確定方向後才回來寫提案
- 別人的 repo、你只是送個小 PR → 依對方流程走
