# Design kit (Figma) — operator guide

**Audience:** Designers maintaining a **Figma** library aligned with this repository’s **`rux-*`** semantic tokens; integrators who need a machine-readable token snapshot when no public **Figma** URL exists yet.

**Canonical code/playbook tokens:** [`docs/playbook/tokens.md`](../playbook/tokens.md) — spacing, typography, and color tables; **T1–T5** acceptance there is enforced by **`tests/test_playbook_docs.py`**. This document adds **Figma**-side process, variable naming expectations, and **`design-tokens.json`** export rules. **`tests/test_design_kit_docs.py`** locks **F1–F8** structure, cross-links, and JSON shape in **CI**.

## Relationship to the playbook

- **Single semantic source for CSS / Tailwind:** [`tokens.md`](../playbook/tokens.md) remains authoritative for **`--rux-*`** names and suggested values.
- **This folder:** Documents how **Figma** variables (or styles) map **onto** those semantics, how to obtain or duplicate the library, and how to request changes.
- **Component regions:** Use [`component-anatomy.md`](../playbook/component-anatomy.md) for timeline/overlay structure; the design kit SHOULD use frame/layer naming that cross-references that doc where helpful.

## Shipped HTML examples and semantic CSS variables

Integrators copy from **`docs/examples/`**; the design kit MUST stay aligned with how those pages express **`--rux-*`** when they wire tokens.

| Pattern ID | Example (entry HTML) | Token story today |
| ---------- | -------------------- | ----------------- |
| **P-01** | [`basic-player.html`](../examples/basic-player.html) | **Canonical** `:root` map: **`--rux-space-{2,4,8}`**, **`--rux-font-sans`**, **`--rux-color-{surface,surface-muted,border,text,primary}`**, plus **`--replayt-primary: var(--rux-color-primary)`** for the embedded player theme. Matches the “Canonical **`--rux-*`** usage” table in [`tokens.md`](../playbook/tokens.md). |
| **P-02**–**P-10**, framework rows | Other shipped **`*.html`** / **`docs/examples/*/`** trees | **Not required** to duplicate the full **`--rux-*`** scale in the same change set as playbook updates ([`tokens.md`](../playbook/tokens.md) **T3**). When a pattern adopts semantic tokens, use **F3** names in **Figma** and the same **`semantic` / `cssVar` / `value`** triple you would emit in **`design-tokens.json`**. |

**Engineering mapping (design → code):** Designers pick **Figma** paths from **F3**; developers set CSS custom properties (or **Tailwind** `theme.extend` per **`tokens.md`**) to the resolved values in **`design-tokens.json`** **`value`** (and optional **`valueDark`**). The **P-01** snippet is the reference for “minimal player chrome” wiring.

## Component inventory (player chrome, timeline, event list)

Use this inventory to structure **Figma** pages/components so comps match the shared anatomy in [`component-anatomy.md`](../playbook/component-anatomy.md) and shipped patterns in [`PATTERNS.md`](../examples/PATTERNS.md).

| Design-kit component | What it covers | Playbook / anatomy anchor | Primary pattern references |
| -------------------- | -------------- | ------------------------- | -------------------------- |
| **Player chrome** | Surround for **`#player`**, instructions strip, borders/radii, primary surfaces | [`component-anatomy.md`](../playbook/component-anatomy.md) §3 (**P-01**, **P-02**, **P-04**) | **P-01** minimal shell, **P-02** metadata bar, **P-04** embed shell |
| **Timeline** | Scrubber track, thumb, time readout, context label | [`component-anatomy.md`](../playbook/component-anatomy.md) §1 (timeline / scrubber strip) + scrubber **states** table | **P-03** [`timeline-scrubber.html`](../examples/timeline-scrubber.html), **P-06**–**P-08** framework parity |
| **Event list / overlay lane** | Event rows, scrub-linked markers, callouts, optional roving focus | [`component-anatomy.md`](../playbook/component-anatomy.md) §2 (overlays, event callouts) | **P-09** [`event-overlay.html`](../examples/event-overlay.html) |

**Figma organization (recommended):** One page (or section) per row above; use slash-style component names that echo **F3** collections (**`RUX/…`**) for tokens applied to those frames. Do not invent parallel color/spacing names—extend **`tokens.md`** + **F3** + **`design-tokens.json`** in one maintainer change set when new semantics are needed.

## Backlog acceptance criteria (stub: tokens + component list)

These criteria make the backlog item **testable in review** alongside **F1–F8** (enforced in **CI** via **`tests/test_design_kit_docs.py`** where noted).

| # | Criterion | Verification |
| --- | --------- | ------------ |
| **BC1** | **Library or interim export** — Designers know how to get a **Figma** library **or**, when no public file exists, use **`design-tokens.json`** as the machine-readable source (**F1**, **F5**). | **F1** / **F5** prose + file present |
| **BC2** | **Full semantic coverage** — Every **`rux-*`** spacing, typography, and color semantic in [`tokens.md`](../playbook/tokens.md) appears in the **F3** table and in **`design-tokens.json`** **`tokens[]`**. | **`tests/test_design_kit_docs.py`** |
| **BC3** | **Component inventory** — This README names **player chrome**, **timeline**, and **event list / overlay lane** and ties each to **`component-anatomy.md`** + at least one **P-*** pattern (table above). | Doc review (**Spec gate**) |
| **BC4** | **Design → code path** — Describes mapping **Figma** variables → **`--rux-*`** (via **F3** + JSON) and points to **P-01** as the minimal CSS wiring example. | **F3**, **Shipped examples** section, **`tokens.md`** |

## Acceptance criteria (F1–F8)

| # | Criterion |
| --- | --------- |
| F1 | **Library access** — How integrators obtain the shared **Figma** file or duplicate it (public link, team invite, or “duplicate from template” with steps). If no link exists yet, state that explicitly and point to **F5** (interim JSON). |
| F2 | **Duplication / fork** — Short steps for creating a team-owned copy so downstream apps are not blocked on a single maintainer account. |
| F3 | **Variable → playbook mapping** — Table mapping **Figma** variable (or style) names to **[`tokens.md`](../playbook/tokens.md)** semantic rows (`rux-space-*`, `rux-text-*`, `rux-color-*`, `rux-font-*`). Every semantic token listed under **Spacing**, **Typography**, and **Color** in **`tokens.md`** appears at least once in the mapping, or is explicitly marked *N/A with rationale* if truly unused in UI chrome. |
| F4 | **Change requests** — Where to file issues or proposals (for example **GitHub** issues/discussions) and what to include (before/after, pattern **P-*** ID if UI-tied, screenshot). |
| F5 | **Interim JSON export** — When **no** stable public **Figma** URL exists, maintainers MUST check in **`design-tokens.json`** in **`docs/design-kit/`** as the interim machine-readable source of truth (see [JSON export schema](#json-export-schema-interim-source-of-truth)). When a public URL is published, keep the JSON **or** replace it only if **F3** mapping and **CHANGELOG** document the migration (avoid silent drift). |
| F6 | **Versioning** — Document **`schemaVersion`** / **`exportDate`** (or equivalent) in **`design-tokens.json`** so reviews can tell exports apart. |
| F7 | **Cross-links** — This README links **[`docs/playbook/README.md`](../playbook/README.md)** and **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** for handoff context (focus/contrast expectations tied to tokens). |
| F8 | **Upstream entry points** — Root **[`README.md`](../../README.md)** **Quick start** or **Project layout** mentions **`docs/design-kit/`** so designers find the kit from the repo home. |

## F1 — Library access

There is **no** published community or public **Figma** file URL for this design kit yet. Treat that as a temporary gap: use **[`design-tokens.json`](design-tokens.json)** (**F5**) for machine-readable values and the **F3** table below for **Figma** naming you can recreate in your own file.

When a stable public link exists, add it here (one line with the **Figma** URL or “duplicate” instructions), bump **`exportDate`** or **CHANGELOG** as needed, and keep **`design-tokens.json`** in sync or document a deliberate cutover in **CHANGELOG**.

**Privacy:** Do not embed **Figma** URLs or steps that depend on secret tokens, **API** keys, or private org-only embeds without maintainer approval.

## F2 — Duplication / fork

**After a public library URL ships:**

1. Open the linked **Figma** file while signed into an account that can view it.
2. Use **File → Save a copy…** (or **Duplicate** on community files) to create a team-owned copy in your workspace.
3. Rename the copy so downstream teams know it is theirs (for example **`RUX Showcase — Acme fork`**).
4. Re-publish variables from your copy if your workflow uses shared libraries; keep **F3** names aligned so **`design-tokens.json`** exports stay comparable.

**Until a public URL exists:** Duplicate the semantics by creating a **Figma** variables collection that follows the **F3** naming column, or branch this repository and extend **`design-tokens.json`** in git with a short note in **CHANGELOG** if you add tokens for a product fork.

## F3 — Figma variable → playbook mapping

Use one **Figma** collection (recommended name **`RUX`**) with slash-style variable paths. Map each path to the playbook semantic and CSS custom property from [`tokens.md`](../playbook/tokens.md).

| Figma variable (path) | Playbook semantic | Suggested CSS variable |
| --------------------- | ----------------- | ---------------------- |
| `RUX/Space/0` | `rux-space-0` | `--rux-space-0` |
| `RUX/Space/1` | `rux-space-1` | `--rux-space-1` |
| `RUX/Space/2` | `rux-space-2` | `--rux-space-2` |
| `RUX/Space/3` | `rux-space-3` | `--rux-space-3` |
| `RUX/Space/4` | `rux-space-4` | `--rux-space-4` |
| `RUX/Space/6` | `rux-space-6` | `--rux-space-6` |
| `RUX/Space/8` | `rux-space-8` | `--rux-space-8` |
| `RUX/Font/Family/Sans` | `rux-font-sans` | `--rux-font-sans` |
| `RUX/Font/Size/XS` | `rux-text-xs` | `--rux-text-xs` |
| `RUX/Font/Size/SM` | `rux-text-sm` | `--rux-text-sm` |
| `RUX/Font/Size/Base` | `rux-text-base` | `--rux-text-base` |
| `RUX/Font/Size/LG` | `rux-text-lg` | `--rux-text-lg` |
| `RUX/Font/Weight/Medium` | `rux-font-medium` | `--rux-font-medium` |
| `RUX/Font/Weight/Semibold` | `rux-font-semibold` | `--rux-font-semibold` |
| `RUX/Color/Surface` | `rux-color-surface` | `--rux-color-surface` |
| `RUX/Color/SurfaceMuted` | `rux-color-surface-muted` | `--rux-color-surface-muted` |
| `RUX/Color/Border` | `rux-color-border` | `--rux-color-border` |
| `RUX/Color/Text` | `rux-color-text` | `--rux-color-text` |
| `RUX/Color/TextMuted` | `rux-color-text-muted` | `--rux-color-text-muted` |
| `RUX/Color/Primary` | `rux-color-primary` | `--rux-color-primary` |
| `RUX/Color/Danger` | `rux-color-danger` | `--rux-color-danger` |
| `RUX/Color/FocusRing` | `rux-color-focus-ring` | `--rux-color-focus-ring` |

*No playbook spacing, type, or color semantic is marked N/A:* all rows from **Spacing scale**, **Typography**, and **Color (semantic)** in **`tokens.md`** appear above.

## F4 — Change requests

Open a **GitHub** issue in this repository (use the issue template if one exists, otherwise a blank issue is fine). Include:

- **Before / after** — prior token value or variable name and the proposed change.
- **Pattern ID** — if the change ties to a shipped example, reference **`docs/examples/PATTERNS.md`** (**P-01**, **P-02**, …).
- **Screenshot or frame link** — for color or spacing shifts, show the affected **Figma** frame or **HTML** example.

Maintainers update [`tokens.md`](../playbook/tokens.md), this mapping (**F3**), and **`design-tokens.json`** in one change set when a semantic rename or value change is accepted, and record it under **CHANGELOG** **Unreleased**.

## F5 — Interim JSON export

**File:** [`design-tokens.json`](design-tokens.json) (JSON, UTF-8), checked into **`docs/design-kit/`**.

Because **F1** has no public **Figma** URL yet, this file is the **interim** source of truth for tooling and reviews. Regenerate or hand-edit it when playbook values in **`tokens.md`** change; keep **`schemaVersion`** and **`exportDate`** honest per **F6**.

When a public **Figma** library ships, either keep exporting to this path or retire it with **CHANGELOG** and **F3** text that points integrators to the **Figma**-native source (avoid two diverging truths).

## F6 — Versioning

**`design-tokens.json`** must include:

- **`schemaVersion`** — semantic version of the JSON shape (for example **`"1.0.0"`**); bump when keys are renamed or required fields change.
- **`exportDate`** — ISO **8601** calendar date (**`YYYY-MM-DD`**) or full timestamp of the export.

Optional **`source`** describes origin (for example **`Figma variables — library draft`** or an exporter name).

## F7 — Cross-links

- **Playbook index (tokens, anatomy, checklist):** [`docs/playbook/README.md`](../playbook/README.md)
- **Keyboard and focus** (scrubber keys, **Escape**, focus ring visibility vs **`rux-color-focus-ring`**): [`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)

## F8 — Discoverability from the repo home

The root **[`README.md`](../../README.md)** **Quick start** paragraph links **`docs/design-kit/README.md`**, and the **Project layout** table lists **`docs/design-kit/README.md`** with a short description. That satisfies **F8**; keep those rows updated if this doc moves.

## JSON export schema (interim source of truth)

**File:** **`docs/design-kit/design-tokens.json`** (JSON, UTF-8).

**Minimal top-level shape** (extend with tool-specific fields if needed; preserve these keys for reviewers and future tooling):

| Field | Type | Purpose |
| ----- | ---- | ------- |
| `schemaVersion` | string | Semantic version of this JSON shape (for example **`"1.0.0"`**). Bump on breaking key renames. |
| `exportDate` | string | ISO **8601** date (**`YYYY-MM-DD`**) or full timestamp of export. |
| `source` | string | Human-readable note (for example **`Figma variables — library draft`**) or exporter tool name. |
| `tokens` | array | List of token records. |

Each element of **`tokens`** SHOULD include:

| Field | Type | Purpose |
| ----- | ---- | ------- |
| `semantic` | string | Playbook name, for example **`rux-space-4`**, **`rux-color-primary`**. MUST match a **`rux-*`** semantic defined in **`tokens.md`** (spacing, typography, or color sections). |
| `cssVar` | string | Suggested CSS custom property, for example **`--rux-space-4`**. |
| `value` | string | Resolved value for the default (light) theme, for example **`1rem`**, **`#111827`**. |
| `figmaName` | string (optional) | Variable or style path in **Figma** as designers see it (aligned with **F3**). |
| `valueDark` | string (optional) | Resolved value for dark theme when the design file defines one. |

**Dark / multi-theme:** Records may include **`valueDark`** where **`tokens.md`** documents paired dark values; otherwise omit **`valueDark`** and document dark pairs only in **Figma** until exported.
