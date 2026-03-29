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

- CI automated tests: Demos render/load across supported replayt versions (smoke/integration via **pytest** + contract tests today; optional **Playwright** load smoke for **Shipped** vanilla **`docs/examples/*.html`** specified in **[`docs/DESIGN_PRINCIPLES.md` — Static HTML examples: browser smoke (Playwright)](DESIGN_PRINCIPLES.md#static-html-examples-browser-smoke-playwright)**); compatibility matrix green.
- Playbook: Handovers pass checklist (<1 dev-day) using **[`docs/playbook/README.md`](playbook/README.md)** (tokens, timeline/overlay anatomy, printable **[`handoff-checklist.md`](playbook/handoff-checklist.md)**), alongside **[`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md)** for keyboard/focus. **Figma**-side alignment, interim token export, shipped-example **`--rux-*`** wiring, and component inventory: **[`docs/design-kit/README.md`](design-kit/README.md)** (**F1–F8**, **BC1–BC4**).
- Player / timeline keyboard and focus: shared **[`docs/a11y/keyboard-model.md`](a11y/keyboard-model.md)** checklist (tab order, roving composites when applicable, scrubber keys, **Escape**), linked from **`docs/examples/`** patterns.
- Coverage: **5+** distinct UI patterns; tracked via **[`docs/examples/PATTERNS.md`](examples/PATTERNS.md)** (canonical inventory), **CHANGELOG**, and **[compat digest](compat.md#vanilla-ui-pattern-catalog)**.

### Pattern coverage tracking

**Source of truth:** [`docs/examples/PATTERNS.md`](examples/PATTERNS.md) — pattern IDs (**P-01**–**P-05**, **P-09**, and **P-10** vanilla **Shipped**; **P-06**–**P-08** framework rows, …), filenames, status (**Shipped** / **Spec only** / **Planned**), and per-pattern acceptance criteria.

| Metric | Target | Current (update when patterns ship) |
| ------ | ------ | ------------------------------------- |
| Distinct vanilla patterns in `docs/examples/` | ≥ 5 | **7** shipped (**P-01**–**P-05**, **P-09**, **P-10** — [`PATTERNS.md`](examples/PATTERNS.md)), including **`fixture-replay.html`** (**P-05**: deterministic offline fixture for reviewers / **LLM** harnesses), **`event-overlay.html`** [**P-09**](examples/PATTERNS.md#p-09--event-overlay-lane-scrub-hover-tooltips-keyboard) (event overlay lane + scrub-linked callouts), and **`click-heatmap-canvas.html`** [**P-10**](examples/PATTERNS.md#p-10--click-heatmap-on-static-canvas-session-click-coordinates) (binned **click** **`x`/`y`** heatmap on a viewport-sized canvas; distinct from **P-09**). |
| **React** framework example (`docs/examples/react/`) | **1** timeline player + **README** | **P-06** — [**Shipped**](examples/PATTERNS.md#p-06--react-timeline-player-basic-player--scrubber-parity): [`docs/examples/react/README.md`](examples/react/README.md), Vite + **`replayt.player.init`** + scrubber parity with **P-03**. |
| **Vue** framework example (`docs/examples/vue/`) | **1** minimal player + scrubber + **README** (parity with **P-06**) | **P-07** — [**Shipped**](examples/PATTERNS.md#p-07--vue-3-timeline-player-basic-player--scrubber-parity): [`docs/examples/vue/README.md`](examples/vue/README.md), Vite + **`replayt.player.init`** + scrubber parity with **P-03**. |
| **Svelte** framework example (`docs/examples/svelte/`) | **1** minimal player + scrubber + **README** (parity with **P-06**) | **P-08** — [**Shipped**](examples/PATTERNS.md#p-08--svelte-4-timeline-player-basic-player--scrubber-parity): [`docs/examples/svelte/README.md`](examples/svelte/README.md), same contract depth as **P-07** for **Svelte 4**. |

When a pattern moves to **Shipped**, update this table and the inventory in **`docs/examples/PATTERNS.md`** in the same change set as the new or updated **`*.html`** file and **CHANGELOG** **Unreleased**.
