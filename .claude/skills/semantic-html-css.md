---
name: semantic-html-css
description: Use when building web pages, writing HTML/CSS, creating UI components, styling elements, or setting up a new frontend project. Covers CSS custom properties, semantic markup, wrapper patterns, and reusable layouts.
---

# Semantic HTML & CSS

## Overview

Write maintainable, semantic web pages by enforcing five rules: centralized design tokens with color pairing, semantic markup, proper content wrapping, and reusable layout patterns.

## When to Use

- Building any web page or UI component
- Writing or reviewing HTML/CSS
- Setting up a new frontend project's stylesheet
- Refactoring existing markup or styles

## Rules

### 1. CSS Custom Properties for All Values

Every color, size, spacing, and font value MUST be defined as a custom property under `:root`. No raw values in selectors.

```css
/* ✅ Correct */
:root {
  --gap-sm: 4px;
  --gap-md: 8px;
  --font-base: 1rem;
}

p {
  margin-bottom: var(--gap-sm);
}

/* ❌ Wrong — raw values in selectors */
p {
  margin-bottom: 4px;
}
```

**No `opacity` or `rgba()` alpha for color variants.** Define separate tokens instead. `opacity` hides contrast ratios from code review — readability can only be verified by opening a browser. The only acceptable use of `rgba()` is for non-text effects like `box-shadow` or overlay backdrops.

### 2. Color Pairs

Every background color MUST have a matching `on-` foreground token. Name the foreground token after the background it sits on — never use a color on the wrong surface.

```css
/* ✅ Correct — colors defined as pairs */
:root {
  --color-bg: #fafafa;
  --color-on-bg: #2c2c3a;
  --color-on-bg-muted: #6b6b80;

  --color-bg-dark: #1a1a2e;
  --color-on-bg-dark: #ffffff;
  --color-on-bg-dark-muted: #a0a0b8;

  --color-surface: #ffffff;
  --color-on-surface: #2c2c3a;
  --color-on-surface-muted: #6b6b80;

  --color-primary: #4f46e5;
  --color-on-primary: #ffffff;

  --color-accent: #e94560;
  --color-on-accent: #ffffff;
}

/* ✅ Correct — pair matches the background */
header { background: var(--color-bg-dark); }
header h1 { color: var(--color-on-bg-dark); }

.card { background: var(--color-surface); }
.card p { color: var(--color-on-surface-muted); }

button { background: var(--color-primary); color: var(--color-on-primary); }

/* ❌ Wrong — mismatch: on-bg-muted text on a surface background */
.card { background: var(--color-surface); }
.card p { color: var(--color-on-bg-muted); }

/* ❌ Wrong — opacity hack instead of a proper muted token */
footer p { color: var(--color-on-bg-dark); opacity: 0.7; }
```

**Key principle:** The token name tells you where it belongs. `--color-on-surface` can ONLY appear on `--color-surface`. If you need a dimmer variant, create a `-muted` token.

**`opacity` is banned for color/text dimming.** When you use `opacity`, the contrast ratio becomes invisible in code — someone has to open a browser to verify readability. With a named `-muted` token, the contrast is decided once at definition time and guaranteed everywhere it's used.

### 3. Semantic HTML Elements

Use elements for their meaning, not their appearance. Every element should render correctly with zero classes.

```html
<!-- ✅ Correct -->
<button>Save</button>
<nav>...</nav>
<article>...</article>

<!-- ❌ Wrong — an anchor is not a button -->
<a class="button">Save</a>
<div class="nav">...</div>
<div class="article">...</div>
```

**Key principle:** A `<button>` with no classes must still look and behave like a button. Style the element, not the class.

```css
/* ✅ Correct — style the element */
button {
  padding: var(--gap-sm) var(--gap-md);
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

/* ❌ Wrong — element needs a class to look right */
.btn {
  padding: 4px 8px;
}
```

### 4. Wrapper Pattern

Page content MUST be wrapped. The wrapper goes INSIDE semantic elements, not outside them.

```html
<!-- ✅ Correct — wrapper inside each section -->
<header>
  <div class="wrapper">...</div>
</header>
<main>
  <div class="wrapper">...</div>
</main>
<footer>
  <div class="wrapper">...</div>
</footer>

<!-- ❌ Wrong — wrapper wraps semantic elements -->
<div class="wrapper">
  <header>...</header>
</div>
```

**Why:** Semantic elements often need full-width backgrounds or borders. When the wrapper is outside, you lose that ability.

### 5. Reusable Layout Patterns

Repeating layout structures must be abstracted into reusable classes. Name by structure, not by page.

```html
<!-- ✅ Correct — layout is reusable -->
<div class="layout-sidebar">
  <aside class="side-panel">...</aside>
  <div class="content">...</div>
</div>

<!-- ❌ Wrong — layout tied to a specific page -->
<div class="profile-page-left-panel">...</div>
<div class="profile-page-content">...</div>
```

### 6. Scope Semantic Element Selectors

Semantic elements like `<footer>`, `<header>`, `<nav>`, `<section>`, `<article>` can appear in multiple contexts — a `<footer>` can be the site footer AND a card's action bar. Never style them with unscoped selectors.

```css
/* ✅ Correct — scoped to context */
body > footer { padding: var(--space-24) 0; }
.story-card footer { padding: var(--space-8); }

/* ❌ Wrong — hits every footer on the page */
footer { padding: var(--space-24) 0; }
footer:last-of-type { text-align: center; }
```

**Why:** HTML spec allows `<footer>` inside `<article>`, `<section>`, and `<body>`. An unscoped `footer` selector will bleed into card footers, section footers, etc. Same applies to `<header>`, `<nav>`, and other semantic elements that nest.

### 7. No Dead CSS

Every token in `:root` and every CSS rule must be actively used. When HTML elements are added or removed, the corresponding CSS must be updated in the same change.

- **No unused tokens** — if no selector references `--gap-2xl`, delete it from `:root`
- **No orphaned rules** — if `.post-image` is removed from HTML, its CSS rule must go too
- **Check both directions** — adding HTML? Add CSS. Removing HTML? Remove CSS. Renaming a class? Update both.

```css
/* ❌ Wrong — token defined but never used */
:root {
  --color-warning: #f59e0b;
  --color-on-warning: #ffffff;
}

/* ❌ Wrong — rule targets an element that no longer exists in HTML */
.old-sidebar {
  width: 300px;
}
```

## Quick Reference

| Rule | Do | Don't |
|------|-----|-------|
| Values | `var(--gap-sm)` | `4px` |
| Colors | `--color-on-surface` on `--color-surface` | `--color-on-bg` on `--color-surface` |
| Muted text | `--color-on-bg-dark-muted` | `opacity: 0.7` |
| Elements | `<button>` | `<a class="button">` |
| Styling | `button { ... }` | `.btn { ... }` |
| Wrapper | Inside `<header>` | Outside `<header>` |
| Layouts | `.layout-sidebar` | `.profile-page-left` |
| Scoping | `body > footer`, `.card footer` | `footer { }` |
| Dead CSS | Remove unused tokens and rules | Leave orphaned CSS "just in case" |

## Common Mistakes

- **Forgetting `:root` tokens for one-off values** — even a single `border-radius: 4px` should use a variable
- **Mismatched color pairs** — using `--color-on-bg` text on a `--color-surface` background. Token name must match its surface
- **Using `opacity` or `rgba()` alpha for text/color dimming** — banned. Create a `-muted` token. Opacity hides contrast from code review
- **Using `<div>` for everything** — check if `<section>`, `<article>`, `<nav>`, `<aside>`, `<header>`, `<footer>` fits
- **Wrapper outside semantic elements** — always wrapper INSIDE
- **Page-specific layout classes** — if two pages share a layout, abstract it
- **Unscoped semantic element selectors** — `header`, `footer`, `nav`, `section` can nest inside other elements. `footer { }` will hit both the site footer and a card's footer. Always scope with parent: `body > footer`, `.card footer`
- **Leaving dead CSS after HTML changes** — unused tokens and orphaned rules accumulate silently. Clean up in the same commit

## Tooling

A Stylelint plugin (`stylelint-plugin-semantic.js`) enforces rules 1, 2, 3, and 6 automatically. Copy it into your project alongside `.stylelintrc.json`.

**Setup:**

```bash
npm install --save-dev stylelint
```

**Four rules enforced:**

| Stylelint Rule | Skill Rule | What it catches |
|---|---|---|
| `semantic/no-raw-values` | 1. Custom Properties | Raw `#hex`, `px`, `rem` values outside `:root` |
| `semantic/no-opacity-dimming` | 3. No Opacity | `opacity` property and `rgba()`/`hsla()` alpha in color declarations |
| `semantic/no-unused-tokens` | 6. No Dead CSS | Custom properties defined in `:root` but never referenced |
| `semantic/color-pair-match` | 2. Color Pairs | `color` token that doesn't match the `background` token in the same rule |

**Run:**

```bash
npx stylelint "**/*.css"
```

**Not enforced by tooling** (requires manual review):
- Semantic HTML element choices (rule 3)
- Wrapper placement inside vs outside semantic elements (rule 4)
- Layout class reusability and naming (rule 5)
