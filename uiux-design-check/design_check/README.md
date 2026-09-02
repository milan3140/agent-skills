# UIUX Design Check(通用端到端檢核 + 對標研究)

任何「設計/重設計/檢核 UI 介面」任務的標準流程:先用完整 Checklist 檢核本設計,再上網對標同類型頂尖範例,交叉比對得出 Best Practices,最後產出**專屬本設計的最佳設計規格文件**。2026-08-24 從 Project-instavoxel 的 Optimize_UIUX skill 收編為通用 toolkit。

## 三件套怎麼選(先分流再開工)

| 情境 | 用哪份 |
|---|---|
| **從零設計新產品/新頁面**,或**全面檢核既有設計** | 本資料夾 [UIUX_Design_Checklist_Full.md](UIUX_Design_Checklist_Full.md)(Phase 1-6 生成指南 + A-G 精修審計) |
| **在既有系統上增量加介面**(要繼承舊系統 DNA) | [../new_ui_spec_checklist.md](../new_ui_spec_checklist.md)(標明🟢繼承/🟡優化/🔴全新) |
| 要 **design token 起手包**(Tailwind、單 `--hue` 控全站)或 sprint 型 SOP | [../design_system/README.md](../design_system/README.md) |

## 標準流程(= skill `uiux-design-check` 的完整版)

1. **檢核本設計**:以 `UIUX_Design_Checklist_Full.md` 逐面向檢核——各部分**如何實作**、是為了達到**哪些設計目的**、**如何實現**該目的。不是打勾,是寫出因果。
2. **上網對標**:搜尋此類型網站/產品的頂尖範例,來源:
   - AWWWARDS.com
   - Dribbble.com
   - Mobbin.com
   - 其餘同類型平台或競爭者的類似功能頁面
3. **交叉檢核**:把各範例也用同一份 Checklist 檢核,互相比對,萃取**共通的 Best Practices**(共通=多個頂尖範例都這樣做,才算數;單一範例的特色只當選配)。
4. **ASCII Prototype 提案(強制閘門)**:佈局有 ≥2 種合理方案時,先用 ASCII 排 2~4 個候選給使用者挑,挑定前不寫規格不動工。規則+實戰範例見 [ascii_prototype.md](ascii_prototype.md)。
5. **產出規格文件**:統整所有項目、遵循 Checklist 的規格,制定**屬於本設計的最佳設計規格文件**(挑定的 ASCII 圖貼進去當佈局藍圖)。
6. **存放**:規格文件存到**當前工作專案的專屬設計資料夾**(使用者才看得到;絕不存回本 toolkit——toolkit 只放方法,產出跟著專案走)。

## Checklist 內容地圖(漸進式揭露:需要哪段讀哪段)

| 段落 | 用途 |
|---|---|
| 開頭鐵則 | 美學標竿(Linear/Stripe/Notion/Vercel)、禁 Emoji、**禁卡片式設計**、建系統不修補 |
| Phase 1-2 | 需求探索(UI 類型分流、功能清單樹、心智模型)、資訊架構(OOUX、≤3 點擊、漸進式揭露) |
| Phase 3 | **Design Tokens(品質的 80%)**:品牌色/含色相灰階/4px grid/3 級圓角/5 級陰影/5 級字階 |
| Phase 4-5 | 元件與佈局(視覺減法、borderless、hover-reveal)、互動與狀態(狀態完整性、回饋環、動畫系統) |
| Phase 6 + BP-1 | 驗收自檢、嚴禁卡片式設計的 6 種替代技法 |
| 精修規格書(元件級/頁面級) | 既有介面重構:元件三分類(導覽/總覽/高密度)、Max 6 Rule、Max 2 分區、CTA 嚴格控制 |
| 審計 A-G | 最後 10% 精緻度:視覺減法、間距節奏、**光學校正**、色彩精修、構圖、元件 polish、品牌一致性 |
| 附錄 | Apple/Material/Linear/Stripe 風格對標表 |

## 相關

- 全域 skill 入口:`~/.claude/skills/uiux-design-check/SKILL.md`(薄層,指回本資料夾)
- 記憶脊椎:MEMORY.md「UI/互動設計」類別
- 原始出處:`D:\AI_Agents_Projects\1_Google_Antigravity\Project-instavoxel\UI_Design\Global_Src_Skills\Skills\Optimize_UIUX\Optional\UIUX_Design_Check-list.md`(正本已收編至此;instavoxel 專案內修訂不會自動同步,重大更新請回抄)
