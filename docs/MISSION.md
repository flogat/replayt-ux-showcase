# Mission: Polished demos and UI patterns for replayt integrators with design-engineering handoff playbook

See [REPLAYT_ECOSYSTEM_IDEA.md](REPLAYT_ECOSYSTEM_IDEA.md) for positioning.

## Users / problem

Replayt integrators (frontend devs/teams embedding session replay in dashboards/apps). Pain removed: No polished, themeable UI patterns (timelines, overlays, players) or design-dev handoff playbook, forcing reinvention and pixel-misaligned handoffs.

## Replayt's role

Relies on replayt core primitives: session capture, event data, replay APIs/player. Consumer-side maintenance here: version pins, shims, CI integration tests (not in replayt core).

## Scope

Owns:
- Copy-pasteable demos/snippets: timeline players, event overlays (vanilla JS, React/Vue/Svelte).
- Design kits: Figma files/tokens.
- Playbook: checklists/tokens for design-to-code handoff.

Delegates upstream: core capture/replay logic.

## Success

- CI automated tests: Demos render/load across supported replayt versions (smoke/integration via pytest + browser automation); compatibility matrix green.
- Playbook: Handovers pass checklist (<1 dev-day).
- Coverage: **5+** distinct UI patterns; tracked via **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** (canonical inventory), **CHANGELOG**, and **[compat digest](compat.md#vanilla-ui-pattern-catalog)**.

### Pattern coverage tracking

**Source of truth:** [`docs/examples/PATTERNS.md`](examples/PATTERNS.md) — pattern IDs (**P-01**–**P-05**, …), filenames, status (**Shipped** / **Spec only** / **Planned**), and per-pattern acceptance criteria.

| Metric | Target | Current (update when patterns ship) |
| ------ | ------ | ------------------------------------- |
| Distinct vanilla patterns in `docs/examples/` | ≥ 5 | **5** shipped (**P-01**–**P-05** — [`PATTERNS.md`](examples/PATTERNS.md)), including **`fixture-replay.html`** (**P-05**: deterministic offline fixture for reviewers / **LLM** harnesses). |

When a pattern moves to **Shipped**, update this table and the inventory in **`docs/examples/PATTERNS.md`** in the same change set as the new or updated **`*.html`** file and **CHANGELOG** **Unreleased**.
