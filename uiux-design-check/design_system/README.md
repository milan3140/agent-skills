# Design System(前端設計起手包)

做任何前端 UI(vibe-coding sprint、原型、產品頁)時用的一套通用設計方法論 + token 起手包。不綁特定專案。2026-06-21 從 ChartForge 抽出。

> 分流:要「**通用端到端檢核+上網對標產規格**」→ [../design_check/README.md](../design_check/README.md)(skill=`uiux-design-check`);「**既有系統增量加介面**」→ [../new_ui_spec_checklist.md](../new_ui_spec_checklist.md);本資料夾=token 起手包+sprint SOP。

## 你要做什麼 → 用哪個

| 情境 | 檔案 |
|---|---|
| 跑整個 UIUX 設計流程(從 spec 到成品) | [UIUX_Design_Checklist.md](UIUX_Design_Checklist.md) |
| Phase 3 設 design token(直接 copy) | [Tailwind_Design_Token_Setup.md](Tailwind_Design_Token_Setup.md) |
| 開工前收集需求的 spec 模板 | [Spec_Prompt_Template.md](Spec_Prompt_Template.md) |

## 怎麼搭配

1. **Spec_Prompt_Template** 先把使用者需求問清楚。
2. **UIUX_Design_Checklist**(給 AI agent 執行的 SOP)把「spec → 成品」拆成 ~50min sprint 的 phase:研究對標 → IA/資料層 → design token → 元件佈局 → 互動/guard → 設計稿審核 gate → 實作 → 驗證。含 debug 鐵則(instrument-first、同 bug 換 ≥2 解法就鎖死加 log)、多 agent 對標框架、禁卡片式設計。
3. 走到 Phase 3 時直接 copy **Tailwind_Design_Token_Setup**:單一 `--hue` 控制全站色彩(brand/灰階/語義色/陰影都從 hue 推導)+ 用法 cheatsheet + 60 秒自檢。

## Worked example

`2_Toolkit/Output/2D/Charts/ChartForge/` 就是用這套 token 系統做的(主題色墨綠,改 `index.css` 一處 `--hue` 即換色)。要看「token 系統長在真實 app 裡」的樣子,讀它的 `app/src/index.css`。
