# Design tokens → CSS variables → Tailwind-friendly names

**Goal:** One table designers and developers can share so spacing, type, and color stay aligned when moving from Figma (or similar) into **Tailwind**-based apps **without** hard-coding one-off pixel values in JSX.

**Convention:**

- **CSS custom properties** use the prefix **`--rux-`** (**r**eplayt **ux** showcase handoff) to avoid clashing with host apps or **replayt**’s own theme vars (e.g. `--replayt-primary` in **P-01**).
- **Tailwind** mappings assume **`tailwind.config.js`** (or **`tailwind.config.ts`**) **`theme.extend`** — integrators copy the **suggested keys**; this repo’s vanilla **HTML** examples may stay plain CSS until a pattern explicitly ships Tailwind.

---

## Spacing scale

| Semantic token | Meaning (design) | Suggested CSS variable | Example value | Tailwind `theme.extend.spacing` key | Usage |
| -------------- | ---------------- | ---------------------- | ------------- | ------------------------------------- | ----- |
| `rux-space-0` | None / collapse | `--rux-space-0` | `0` | `'rux-0': 'var(--rux-space-0)'` | Tight stacks, divider-only gaps |
| `rux-space-1` | Tight inline gap | `--rux-space-1` | `0.25rem` (4px) | `'rux-1': 'var(--rux-space-1)'` | Icon ↔ label, chip padding |
| `rux-space-2` | Default inline / stack | `--rux-space-2` | `0.5rem` (8px) | `'rux-2': 'var(--rux-space-2)'` | Form fields, toolbar groups |
| `rux-space-3` | Comfortable block gap | `--rux-space-3` | `0.75rem` (12px) | `'rux-3': 'var(--rux-space-3)'` | Card internal sections |
| `rux-space-4` | Section rhythm | `--rux-space-4` | `1rem` (16px) | `'rux-4': 'var(--rux-space-4)'` | Player chrome margins |
| `rux-space-6` | Major section break | `--rux-space-6` | `1.5rem` (24px) | `'rux-6': 'var(--rux-space-6)'` | Above/below player block |
| `rux-space-8` | Page-level gutter | `--rux-space-8` | `2rem` (32px) | `'rux-8': 'var(--rux-space-8)'` | Outer page padding (see **P-01** `body` padding) |

**Tailwind usage (after extend):** `p-rux-4`, `gap-rux-2`, `mt-rux-6`.

**Arbitrary fallback (no config change):** `p-[var(--rux-space-4)]`, `gap-[var(--rux-space-2)]`.

---

## Typography

| Semantic token | Meaning (design) | Suggested CSS variable | Example stack / size | Tailwind `theme.extend` | Notes |
| -------------- | ---------------- | ---------------------- | -------------------- | ------------------------- | ----- |
| `rux-font-sans` | UI body | `--rux-font-sans` | `system-ui, sans-serif` | `fontFamily: { rux: ['var(--rux-font-sans)'] }` | Match **P-01** `body` |
| `rux-text-xs` | Captions, meta | `--rux-text-xs` | `0.75rem` / `1rem` line-height | `fontSize: { 'rux-xs': ['var(--rux-text-xs)', { lineHeight: '1rem' }] }` | Metadata bar (**P-02**) |
| `rux-text-sm` | Secondary body | `--rux-text-sm` | `0.875rem` / `1.25rem` | `fontSize: { 'rux-sm': ['var(--rux-text-sm)', { lineHeight: '1.25rem' }] }` | Instructions, errors |
| `rux-text-base` | Primary body | `--rux-text-base` | `1rem` / `1.5rem` | `fontSize: { 'rux-base': ['var(--rux-text-base)', { lineHeight: '1.5rem' }] }` | Default reading text |
| `rux-text-lg` | Section titles | `--rux-text-lg` | `1.125rem` / `1.75rem` | `fontSize: { 'rux-lg': ['var(--rux-text-lg)', { lineHeight: '1.75rem' }] }` | Page `<h1>` scale |
| `rux-font-medium` | Emphasis | `--rux-font-medium` | `500` | `fontWeight: { ruxmedium: 'var(--rux-font-medium)' }` | Labels, button text |
| `rux-font-semibold` | Strong emphasis | `--rux-font-semibold` | `600` | `fontWeight: { ruxsemibold: 'var(--rux-font-semibold)' }` | Headings |

**Tailwind usage:** `font-rux`, `text-rux-sm`, `font-ruxmedium` (exact class names depend on how you name the extend keys; prefer short stable tokens agreed in design).

---

## Color (semantic)

| Semantic token | Meaning (design) | Suggested CSS variable | Example (light UI) | Tailwind `theme.extend.colors` | Notes |
| -------------- | ---------------- | ---------------------- | ------------------ | -------------------------------- | ----- |
| `rux-color-surface` | Page / panel background | `--rux-color-surface` | `#ffffff` | `rux: { surface: 'var(--rux-color-surface)' }` | Player surround |
| `rux-color-surface-muted` | Instructions strip | `--rux-color-surface-muted` | `#f8f9fa` | `rux: { 'surface-muted': 'var(--rux-color-surface-muted)' }` | **P-01** `.instructions` |
| `rux-color-border` | Default hairline | `--rux-color-border` | `#e0e0e0` | `rux: { border: 'var(--rux-color-border)' }` | **P-01** `#player` border |
| `rux-color-text` | Primary text | `--rux-color-text` | `#111827` | `rux: { text: 'var(--rux-color-text)' }` | Body copy |
| `rux-color-text-muted` | Secondary text | `--rux-color-text-muted` | `#6b7280` | `rux: { 'text-muted': 'var(--rux-color-text-muted)' }` | Hints, timestamps |
| `rux-color-primary` | Brand / link / focus ring | `--rux-color-primary` | `#007bff` | `rux: { primary: 'var(--rux-color-primary)' }` | Align with **P-01** `--replayt-primary` if desired |
| `rux-color-danger` | Error text / border | `--rux-color-danger` | `#b91c1c` | `rux: { danger: 'var(--rux-color-danger)' }` | **P-04** failure copy |
| `rux-color-focus-ring` | Focus visible ring | `--rux-color-focus-ring` | `var(--rux-color-primary)` | `rux: { 'focus-ring': 'var(--rux-color-focus-ring)' }` | Match [`keyboard-model.md`](../a11y/keyboard-model.md) visibility expectations |

**Tailwind usage:** `bg-rux-surface-muted`, `border-rux-border`, `text-rux-danger`.

**Dark theme:** Document paired values in the design file; swap variables at `:root` / `.dark` without renaming semantic tokens.

---

## Acceptance (Builder / spec gate)

| # | Criterion |
| --- | --------- |
| T1 | This file lists **spacing**, **typography**, and **color** tables, each with **semantic name**, **CSS variable**, and **Tailwind extend** mapping. |
| T2 | Naming is **stable** (`rux-*`); breaking renames require **CHANGELOG** and a short migration note in [`README.md`](../../README.md) or this playbook. |
| T3 | Examples in **`docs/examples/`** are **not** required to adopt these variables in the same change set as this spec; when a pattern is updated for tokens, mention the pattern ID in **CHANGELOG**. |
