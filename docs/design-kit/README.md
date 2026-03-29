# Design kit (Figma) — spec and operator guide

**Audience:** Designers maintaining a **Figma** library aligned with this repository’s **`rux-*`** semantic tokens; integrators who need a machine-readable token snapshot when no public **Figma** URL exists yet.

**Canonical code/playbook tokens:** [`docs/playbook/tokens.md`](../playbook/tokens.md) — spacing, typography, and color tables; **T1–T3** acceptance there is enforced by **`tests/test_playbook_docs.py`**. This document adds **Figma**-side process, variable naming expectations, and optional **`design-tokens.json`** export rules.

## Relationship to the playbook

- **Single semantic source for CSS / Tailwind:** [`tokens.md`](../playbook/tokens.md) remains authoritative for **`--rux-*`** names and suggested values.
- **This folder:** Documents how **Figma** variables (or styles) map **onto** those semantics, how to obtain or duplicate the library, and how to request changes.
- **Component regions:** Use [`component-anatomy.md`](../playbook/component-anatomy.md) for timeline/overlay structure; the design kit SHOULD use frame/layer naming that cross-references that doc where helpful.

## Required operator-facing sections (Builder deliverable)

When the **Figma design kit stub** backlog is **done**, this `README.md` MUST satisfy **F1–F8**:

| # | Criterion |
| --- | --------- |
| F1 | **Library access** — How integrators obtain the shared **Figma** file or duplicate it (public link, team invite, or “duplicate from template” with steps). If no link exists yet, state that explicitly and point to **F5** (interim JSON). |
| F2 | **Duplication / fork** — Short steps for creating a team-owned copy so downstream apps are not blocked on a single maintainer account. |
| F3 | **Variable → playbook mapping** — Table (or link to a **Figma** page that acts as the table) mapping **Figma** variable (or style) names to **[`tokens.md`](../playbook/tokens.md)** semantic rows (`rux-space-*`, `rux-text-*`, `rux-color-*`, `rux-font-*`). Every semantic token listed under **Spacing**, **Typography**, and **Color** in **`tokens.md`** MUST appear at least once in the mapping, or be explicitly marked *N/A with rationale* if truly unused in UI chrome. |
| F4 | **Change requests** — Where to file issues or proposals (for example **GitHub** issues/discussions) and what to include (before/after, pattern **P-*** ID if UI-tied, screenshot). |
| F5 | **Interim JSON export** — When **no** stable public **Figma** URL exists, maintainers MUST check in **`design-tokens.json`** in **`docs/design-kit/`** as the interim machine-readable source of truth (see [JSON export schema](#json-export-schema-interim-source-of-truth)). When a public URL is published, keep the JSON **or** replace it only if **F3** mapping and **CHANGELOG** document the migration (avoid silent drift). |
| F6 | **Versioning** — Document **`schemaVersion`** / **`exportDate`** (or equivalent) in **`design-tokens.json`** so reviews can tell exports apart. |
| F7 | **Cross-links** — This README links **[`docs/playbook/README.md`](../playbook/README.md)** and **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** for handoff context (focus/contrast expectations tied to tokens). |
| F8 | **Upstream entry points** — Root **[`README.md`](../../README.md)** **Quick start** or **Project layout** mentions **`docs/design-kit/`** so designers find the kit from the repo home. |

**CI / automation:** **Not** enforced in **CI** today. A follow-up **Builder** change set MAY add **`tests/test_design_kit_docs.py`** (similar to **`test_playbook_docs.py`**) to lock **F1–F8** markers and links; until then, **Spec gate** / human review applies.

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
| `figmaName` | string (optional) | Variable or style name in **Figma** as designers see it. |

**Dark / multi-theme:** Use additional fields (for example **`valueDark`**) or separate records with a **`theme`** key — document the chosen convention in prose in this README when **Builder** ships JSON.

**Privacy:** Do not embed **Figma** URLs or instructions that rely on secret tokens, **API** keys, or private org-only embeds without maintainer approval; prefer public/community links or omit the URL until it is public (per **F5**).

## Builder checklist (phase 3)

1. Implement narrative sections **F1–F8** in this README; add **`design-tokens.json`** when **F5** applies.
2. Link from **[`docs/playbook/README.md`](../playbook/README.md)** and root **[`README.md`](../../README.md)** per **F7** / **F8** (playbook index may be satisfied by the existing row in **Normative companions** once the design-kit link is added there).
3. Add **CHANGELOG** **Unreleased** when the kit or JSON first ships or when the **Figma** URL / token set materially changes.
4. Optional: add **`tests/test_design_kit_docs.py`** and a row under **[`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#traceability-to-automated-checks)** in the same change set.

## Status (phase 2 spec)

This revision defines the **contract** for the **Figma design kit stub: tokens export + link from docs** backlog. Populated **F1–F8** prose and **`design-tokens.json`** are **Builder** (phase **3**) deliverables.
