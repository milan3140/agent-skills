# Tailwind Design Token Setup (vibe-coding starter)

對應 UIUX_Design_Check-list Phase 3（視覺基礎規範）。此檔提供 60-sec 可 copy-paste 的完整 Tailwind config + CSS variables，讓 60 min sprint 不用花時間設 design token。

---

## 一鍵安裝（< 2 min）

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm install -D tailwindcss postcss autoprefixer tailwindcss-animate
npx tailwindcss init -p
npm install lucide-react clsx tailwind-merge class-variance-authority
npm install recharts          # 或 lightweight-charts (K 線/股票圖)
npx shadcn@latest init        # 選: TypeScript / Tailwind / Default / src/index.css / @ alias
npm install react-hook-form zod @hookform/resolvers  # 表單需要才裝
```

接著用本檔下方的 `tailwind.config.ts` 與 `src/index.css` 覆寫掉 `shadcn init` 生出來的版本。

---

## `tailwind.config.ts`（完整 copy）

```typescript
import type { Config } from 'tailwindcss';
import animatePlugin from 'tailwindcss-animate';

export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      // ============================================================
      // 1. Brand & Surface Colors (UIUX 3.1.1 / 3.1.4)
      //    全部走 CSS variable，改色只動 :root
      // ============================================================
      colors: {
        brand: {
          DEFAULT: 'hsl(var(--brand) / <alpha-value>)',
          hover:   'hsl(var(--brand-hover) / <alpha-value>)',
          subtle:  'hsl(var(--brand-subtle) / <alpha-value>)',
          wash:    'hsl(var(--brand-wash) / <alpha-value>)',
          fg:      'hsl(var(--brand-fg) / <alpha-value>)',
        },
        gray: {
          50:  'hsl(var(--gray-50) / <alpha-value>)',
          100: 'hsl(var(--gray-100) / <alpha-value>)',
          200: 'hsl(var(--gray-200) / <alpha-value>)',
          300: 'hsl(var(--gray-300) / <alpha-value>)',
          400: 'hsl(var(--gray-400) / <alpha-value>)',
          500: 'hsl(var(--gray-500) / <alpha-value>)',
          600: 'hsl(var(--gray-600) / <alpha-value>)',
          700: 'hsl(var(--gray-700) / <alpha-value>)',
          800: 'hsl(var(--gray-800) / <alpha-value>)',
          900: 'hsl(var(--gray-900) / <alpha-value>)',
          950: 'hsl(var(--gray-950) / <alpha-value>)',
        },
        // Semantic (UIUX 3.1.3)
        success: {
          DEFAULT: 'hsl(var(--success) / <alpha-value>)',
          bg:      'hsl(var(--success-bg) / <alpha-value>)',
        },
        error: {
          DEFAULT: 'hsl(var(--error) / <alpha-value>)',
          bg:      'hsl(var(--error-bg) / <alpha-value>)',
        },
        warning: {
          DEFAULT: 'hsl(var(--warning) / <alpha-value>)',
          bg:      'hsl(var(--warning-bg) / <alpha-value>)',
        },
        info: {
          DEFAULT: 'hsl(var(--info) / <alpha-value>)',
          bg:      'hsl(var(--info-bg) / <alpha-value>)',
        },
        // Surface layers (UIUX 3.1.4)
        surface: {
          base:     'hsl(var(--surface-base) / <alpha-value>)',
          panel:    'hsl(var(--surface-panel) / <alpha-value>)',
          floating: 'hsl(var(--surface-floating) / <alpha-value>)',
        },
        // shadcn semantic 對映 (讓 shadcn 元件吃我們的 token)
        background:  'hsl(var(--surface-base) / <alpha-value>)',
        foreground:  'hsl(var(--gray-900) / <alpha-value>)',
        border:      'hsl(var(--gray-200) / <alpha-value>)',
        input:       'hsl(var(--gray-200) / <alpha-value>)',
        ring:        'hsl(var(--brand) / <alpha-value>)',
        primary:     'hsl(var(--brand) / <alpha-value>)',
        destructive: 'hsl(var(--error) / <alpha-value>)',
        muted:       'hsl(var(--gray-100) / <alpha-value>)',
        accent:      'hsl(var(--brand-wash) / <alpha-value>)',
      },

      // ============================================================
      // 2. Radius — 嚴格 3 級 (UIUX 3.3.1)
      // ============================================================
      borderRadius: {
        sm: '4px',
        md: '8px',
        lg: '12px',
        // 禁用 xl / 2xl / 3xl
      },

      // ============================================================
      // 3. Shadow — 嚴格 5 級，brand-tinted (UIUX 3.3.2)
      // ============================================================
      boxShadow: {
        xs: '0 1px 2px hsl(var(--shadow) / 0.05)',
        sm: '0 1px 3px hsl(var(--shadow) / 0.08), 0 1px 2px hsl(var(--shadow) / 0.04)',
        md: '0 4px 6px hsl(var(--shadow) / 0.06), 0 2px 4px hsl(var(--shadow) / 0.04)',
        lg: '0 10px 15px hsl(var(--shadow) / 0.08), 0 4px 6px hsl(var(--shadow) / 0.05)',
        xl: '0 20px 25px hsl(var(--shadow) / 0.10), 0 8px 10px hsl(var(--shadow) / 0.06)',
      },

      // ============================================================
      // 4. Typography — 5-級 type scale (UIUX 3.4)
      //    Tailwind 預設 text-xs/sm/base 已對齊；可額外加自訂
      // ============================================================
      fontFamily: {
        sans: ['Inter', 'SF Pro Text', 'Roboto', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'monospace'],
      },
      fontSize: {
        // 維持 Tailwind 預設 + 補幾個關鍵點
        micro:  ['11px', { lineHeight: '14px', letterSpacing: '0.05em' }],  // uppercase tags
        // text-xs (12px), text-sm (14px), text-base (16px), text-lg (18px) 都用預設
      },

      // ============================================================
      // 5. Animation (UIUX 5.3)
      // ============================================================
      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.16, 1, 0.3, 1)',  // 全局統一 easing
      },
      transitionDuration: {
        DEFAULT: '200ms',
      },
      keyframes: {
        'fade-slide-in': {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-out': {
          '0%':   { opacity: '1' },
          '100%': { opacity: '0' },
        },
      },
      animation: {
        'fade-slide-in': 'fade-slide-in 250ms cubic-bezier(0.16, 1, 0.3, 1)',
        'fade-out':      'fade-out 150ms cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [animatePlugin],
} satisfies Config;
```

---

## `src/index.css`（完整 copy）

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* ============================================================
       1. Brand Hue Control — 改一處，全部色彩跟著動
       ============================================================ */
    --hue: 260;        /* 0-360 degree. 260 = purple. 215 = blue. 145 = green. */
    --hue-sat: 80%;    /* brand saturation */

    /* ============================================================
       2. Brand Color Tokens (UIUX 3.1.1)
       ============================================================ */
    --brand:        var(--hue) var(--hue-sat) 55%;
    --brand-hover:  var(--hue) var(--hue-sat) 45%;
    --brand-subtle: var(--hue) 30%             92%;
    --brand-wash:   var(--hue) 30%             97%;
    --brand-fg:     0 0% 100%;

    /* ============================================================
       3. Tinted Grays (UIUX 3.1.2) — 嚴禁純灰
          Saturation 8-15% of brand hue
       ============================================================ */
    --gray-50:  var(--hue) 10% 98%;
    --gray-100: var(--hue) 10% 95%;
    --gray-200: var(--hue) 9%  90%;
    --gray-300: var(--hue) 8%  82%;
    --gray-400: var(--hue) 8%  68%;
    --gray-500: var(--hue) 8%  52%;
    --gray-600: var(--hue) 9%  40%;
    --gray-700: var(--hue) 10% 30%;
    --gray-800: var(--hue) 12% 20%;
    --gray-900: var(--hue) 14% 12%;
    --gray-950: var(--hue) 16% 6%;

    /* ============================================================
       4. Semantic Colors (UIUX 3.1.3) — 嚴禁純 RGB
          Hue 是調和過的，不是純 #FF0000 / #00FF00
       ============================================================ */
    --success:    145 65% 42%;
    --success-bg: 145 50% 95%;
    --error:      0   75% 55%;
    --error-bg:   0   70% 96%;
    --warning:    35  90% 50%;
    --warning-bg: 35  85% 95%;
    --info:       210 85% 55%;
    --info-bg:    210 80% 96%;

    /* ============================================================
       5. Surface Layers (UIUX 3.1.4)
          Level 0 = base / Level 1 = panel / Level 2 = floating
       ============================================================ */
    --surface-base:     0 0% 98%;    /* 整個 page 背景 */
    --surface-panel:    0 0% 100%;   /* 內容面板 */
    --surface-floating: 0 0% 100%;   /* modal / popover / tooltip */

    /* ============================================================
       6. Shadow Base — brand-tinted black, never pure black
       ============================================================ */
    --shadow: var(--hue) 30% 10%;

    /* ============================================================
       7. shadcn/ui Token 對映
       ============================================================ */
    --radius: 8px;
  }

  body {
    @apply bg-surface-base text-gray-900 antialiased;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-feature-settings: "ss01", "cv11";
  }

  /* (UIUX 3.4.3) Numbers must be tabular-aligned globally */
  :where(td, th) {
    font-variant-numeric: tabular-nums;
  }
  .num, [data-num] {
    font-variant-numeric: tabular-nums;
  }
}
```

---

## 用法 cheatsheet

### ✅ 正確用法

```tsx
// 用 design token 的 utility class
<div className="bg-surface-panel text-gray-700 rounded-md shadow-sm p-4 gap-2">
  <h2 className="text-lg text-gray-900 font-semibold">Title</h2>
  <p className="text-sm text-gray-600">Body content</p>
  <button className="bg-brand text-brand-fg hover:bg-brand-hover rounded-md px-4 py-2 transition">
    Action
  </button>
</div>

// Semantic state
<div className="bg-success-bg text-success border border-success/20 rounded-md p-3">
  Save offer applied
</div>

// Uppercase micro tag (UIUX 3.4.3)
<span className="text-micro uppercase text-gray-500 tracking-wider">
  Pro Plan
</span>

// Number aligned (UIUX 3.4.3)
<td className="num">NT$ 4,980</td>
```

### ❌ 禁止用法

```tsx
// 1. Arbitrary value — 破壞 4px grid / token 系統
<div className="p-[7px] gap-[5px] text-[#123456]">  ❌

// 2. 純灰 — 沒有 brand hue
<div className="bg-[#888] text-[#555]">  ❌

// 3. 超出 token 範圍
<div className="rounded-3xl shadow-2xl">  ❌

// 4. Tailwind 預設陰影但不帶 brand tint (透過 config 已修正，避免又自訂)
<div style={{boxShadow: '0 4px 6px rgba(0,0,0,0.1)'}}>  ❌

// 5. Mixed easing — 違反 UIUX 5.3.1
<div className="transition-all ease-in-out duration-500">  ❌ (用預設 cubic-bezier + 200ms)
```

---

## Spacing — 不用變數，直接用 Tailwind 預設

**Tailwind 預設 spacing 本來就是 4px grid**，不用再 token 化：

| Class | 值 |
|---|---|
| `p-0.5` / `gap-0.5` | 2px |
| `p-1` | 4px |
| `p-2` | 8px |
| `p-3` | 12px |
| `p-4` | 16px |
| `p-5` | 20px |
| `p-6` | 24px |
| `p-8` | 32px |
| `p-10` | 40px |
| `p-12` | 48px |

**規則**：
- 視覺群組內間距用 `p-1` ~ `p-2`（4-8px）
- 視覺群組外間距用 `p-6` ~ `p-8`（24-32px）
- 嚴禁 `p-[5px]` / `p-[15px]` 之類的 arbitrary value

---

## 改 hue / brand color 的方式

只動 `src/index.css` 的 `:root` 區塊兩個變數：

```css
:root {
  --hue: 215;       /* 從 260 (紫) 改成 215 (藍) */
  --hue-sat: 75%;   /* 微調飽和度 */
}
```

整個產品的所有色彩會跟著變，包括灰階、陰影、CSS variable 對映的 shadcn 元件。**這是「整套 design 美學系統」而不是「個別卡片修補」（呼應 UIUX 第 8 條原則）。**

---

## 60-sec 自檢 checklist（build 完跑一次）

- [ ] 所有 padding / margin / gap 都是 4px 倍數（無 arbitrary value）
- [ ] 沒有純灰色（#888 / #555 / gray-without-hue）
- [ ] 沒有純 #FF0000 / #00FF00（語義色全走 `--success / --error / --warning / --info`）
- [ ] 圓角只有 3 級（`rounded-sm / md / lg`），無 `xl / 2xl / 3xl`
- [ ] 陰影只有 5 級（`shadow-xs / sm / md / lg / xl`），全部 brand-tinted
- [ ] 字級維持 ≤5 級，相鄰至少差 2px
- [ ] 所有數字有 `font-variant-numeric: tabular-nums`（透過 `:where(td,th)` 已 global 處理）
- [ ] Modal / Toast / Dropdown 有 `animate-fade-slide-in`
- [ ] Transition 用預設 cubic-bezier + 200ms，無 mixed easing
