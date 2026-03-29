# Design-to-code handoff playbook

**Audience:** Designers handing UI to frontend integrators, and integrators embedding **replayt** players, timelines, and overlays in host apps.

**Mission alignment:** [MISSION.md — Success](../MISSION.md#success) expects handovers to complete a shared checklist in **under one dev-day**. This playbook is the **canonical** place for that checklist, **semantic → implementation** token mapping, and **component anatomy** for the surfaces this repo’s examples cover.

## Contents

| Doc | Purpose |
| --- | ------- |
| **[`tokens.md`](tokens.md)** | Spacing, typography, and color tokens with suggested **CSS custom properties** and **Tailwind**-friendly names (`theme.extend`). |
| **[`component-anatomy.md`](component-anatomy.md)** | Named regions and responsibilities for **timeline / scrubber** strips and **overlay** UI (dialogs, popovers, event callouts). |
| **[`handoff-checklist.md`](handoff-checklist.md)** | **Printable** checklist: accessibility, loading, and error states (cross-links to normative examples). |

## Normative companions (do not duplicate)

- **Figma design kit / variable → `rux-*` mapping / interim JSON export:** [`docs/design-kit/README.md`](../design-kit/README.md) — **F1–F8** operator sections and **`design-tokens.json`** schema (Builder); aligns with [`tokens.md`](tokens.md).
- **Keyboard / focus:** [`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md) — tab order, scrubber keys, roving composites, **Escape**.
- **Copy-paste examples:** [`docs/examples/PATTERNS.md`](../examples/PATTERNS.md) — **P-01**–**P-06** inventory and per-pattern acceptance criteria.
- **Loading / failure UX:** **P-04** [`embed-container-states.html`](../examples/embed-container-states.html) and [`PATTERNS.md` — P-04](../examples/PATTERNS.md#p-04-embed-container-states-empty-loading-failure-recovery).
- **Timeline scrubber:** **P-03** [`timeline-scrubber.html`](../examples/timeline-scrubber.html).
- **Pins and CDN:** [`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md), [`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).

## How to use in a handoff

1. Agree on **semantic tokens** from [`tokens.md`](tokens.md); map them in the integrator’s **Tailwind** theme or CSS variables once.
2. Walk **component anatomy** in [`component-anatomy.md`](component-anatomy.md) so DOM order, layering, and z-index match the **keyboard model** and pattern **P-02** / **P-03** / **P-04** precedents.
3. Run [`handoff-checklist.md`](handoff-checklist.md) (print or tick in review) before merge; file gaps as follow-ups with pattern IDs.

**CI:** `tests/test_playbook_docs.py` keeps the four playbook files, acceptance row markers (**T1–T3**, **A1–A3**, **H1–H3**), and integrator entry-point links aligned with [DESIGN_PRINCIPLES — traceability to automated checks](../DESIGN_PRINCIPLES.md#traceability-to-automated-checks). `tests/test_design_kit_docs.py` covers **[`docs/design-kit/`](../design-kit/README.md)** (**F1–F8**, interim **`design-tokens.json`**).
