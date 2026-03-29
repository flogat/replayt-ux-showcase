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

- **Keyboard / focus:** [`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md) — tab order, scrubber keys, roving composites, **Escape**.
- **Copy-paste examples:** [`docs/examples/PATTERNS.md`](../examples/PATTERNS.md) — **P-01**–**P-06** inventory and per-pattern acceptance criteria.
- **Loading / failure UX:** **P-04** [`embed-container-states.html`](../examples/embed-container-states.html) and [`PATTERNS.md` — P-04](../examples/PATTERNS.md#p-04-embed-container-states-empty-loading-failure-recovery).
- **Timeline scrubber:** **P-03** [`timeline-scrubber.html`](../examples/timeline-scrubber.html).
- **Pins and CDN:** [`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md), [`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).

## How to use in a handoff

1. Agree on **semantic tokens** from [`tokens.md`](tokens.md); map them in the integrator’s **Tailwind** theme or CSS variables once.
2. Walk **component anatomy** in [`component-anatomy.md`](component-anatomy.md) so DOM order, layering, and z-index match the **keyboard model** and pattern **P-02** / **P-03** / **P-04** precedents.
3. Run [`handoff-checklist.md`](handoff-checklist.md) (print or tick in review) before merge; file gaps as follow-ups with pattern IDs.

**Builder note:** Phase **3** may add contract tests for playbook files if the project adopts automated doc structure checks; until then, **spec gate** / review verifies completeness per [DESIGN_PRINCIPLES — backlog traceability](../DESIGN_PRINCIPLES.md#backlog-traceability-design-to-code-handoff-playbook-checklist--tokens).
