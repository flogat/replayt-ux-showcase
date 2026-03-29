# Vanilla examples — UI pattern catalog

This file is the **canonical inventory** for distinct, copy-paste **vanilla HTML/JS** patterns under
`docs/examples/`. It supports the mission success criterion “**5+ patterns**” and gives **Spec gate** / **Builder**
a single place to check **what counts as a pattern**, **what ships where**, and **acceptance criteria** before code
lands.

**Related:** [Mission — Success](../MISSION.md#pattern-coverage-tracking), [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix), [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).

## Pattern inventory

A **pattern** is a **standalone** integrator-facing example with its own **primary user job** (not a one-line tweak of
another file). Filename changes follow [Deprecation and removal](../DESIGN_PRINCIPLES.md#deprecation-and-removal).

| ID | Artifact | Status | Summary |
| -- | -------- | ------ | ------- |
| **P-01** | [`basic-player.html`](basic-player.html) | **Shipped** | Minimal embedded player: container, `sessionData`, `replayt.player.init`, theme note. |
| **P-02** | `player-session-metadata-bar.html` (planned) | **Spec only** — implement in Builder phase | Session **metadata chrome**: compact bar **above** the player, same `sessionData` contract as P-01, plus loading / error / focus rules below. |

**Mission trajectory:** P-01 is the first shipped pattern. This backlog (**P-02**) moves the repo toward **5+** distinct
patterns; additional rows (timeline chrome, error boundary, framework variants, etc.) are **future** backlogs unless
explicitly added here first.

---

## P-02 — Session metadata chrome (viewport, duration, session id)

### User story

As an integrator, I want a **second vanilla snippet** that layers a **compact metadata bar** above the replay player
so operators see **session id**, **viewport**, and **duration** without opening devtools, using the same data object I
already pass to the player as in **P-01**.

### `sessionData` contract (compatibility with P-01)

- **Same root shape** as [`basic-player.html`](basic-player.html): an object with at least:
  - **`events`** — array (may be empty in the snippet; real apps pass replayt event arrays).
  - **`metadata`** — object.
- **P-01 baseline keys** inside `metadata` (from `basic-player.html`): `startTs`, `viewport` (`width`, `height`).
- **Extensions for P-02** (additive; must not break P-01 copies):
  - **`metadata.sessionId`** — string, human-readable stable id for the session row in the chrome.
  - **`metadata.durationMs`** — non-negative number, **session duration in milliseconds**, shown in the bar (preferred;
    avoids guessing from empty `events` in static demos).

Integrators may omit `sessionId` or `durationMs` only where the **error / empty-state rules** below still produce a
clear UX (see **Required chrome inputs**).

### Layout and visual intent

- **Metadata bar** sits **immediately above** the player container (same horizontal width as the player or its wrapper).
- **Compact**: one row (wrapping allowed on small widths), typographic hierarchy secondary to the player.
- **Themeable** via the same CSS-variable story as P-01 where practical (e.g. bar border/background uses neutral
  surfaces; document any vars the snippet introduces).

### Required chrome inputs (normative)

After the integrator has finished loading (not during the loading placeholder), the bar **must** be able to show:

| Field | Source | Rule |
| ----- | ------ | ---- |
| Viewport | `metadata.viewport.width` × `metadata.viewport.height` | **Required** after load. If missing, show **error state** (not an empty bar pretending success). |
| Session id | `metadata.sessionId` | **Required** after load for this pattern. If missing, show **error state** (integrators must supply for this demo’s contract). |
| Duration | `metadata.durationMs` | **Required** after load. If missing, show **error state**. Format for display: human-readable (e.g. `m:ss` or `H:MM:SS` for long sessions) — exact formatting is implementation detail as long as it is consistent and documented in the snippet comments. |

**Rationale:** P-02 is explicitly about **viewport, duration, session id**; treating them as required after load keeps
the pattern testable and aligned with the backlog title.

### Loading state (normative)

- Before `sessionData` is available (e.g. async fetch), the metadata bar region **must** show **visible placeholder
  text** (e.g. “Loading session…”), not a blank strip.
- The player area may use an equivalent placeholder or stay empty until init — **document in-snippet** which approach
  is used; at least one of bar or player must make the loading phase obvious.

### Error state (normative)

- If, after load, **any required chrome input** is missing or invalid (e.g. `durationMs` negative, `viewport` without
  numeric width/height), the snippet **must** show a **user-visible error message** in or above the bar (not only a
  `console.error`).
- Errors **must not** silently fall back to an “empty” bar that looks like a successful zeroed session.

### Keyboard focus and accessibility (normative)

- **Tab order:** Elements in the **metadata bar** that are **focusable** (links, buttons, inputs) **must** appear **before**
  the player’s focusable controls in **DOM order** (bar first, then player). If the bar has no focusable controls, the
  first focusable control **inside** the player container follows naturally — do not trap focus in the player before
  the bar when the bar contains interactive elements.
- **Focus visibility:** Focusable controls **must** keep a visible focus ring (browser default or snippet CSS).
- **Copy-paste comment:** The HTML/JS **must** include a short comment block summarizing tab order intent for
  design-engineering handoff.

### replayt pin and file placement

- New file lives under **`docs/examples/`** with the **planned name** `player-session-metadata-bar.html` (adjust only
  if a naming collision requires it; if renamed, update this catalog and **CHANGELOG** in the same change set).
- **replayt** script URL **must** satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (same PEP 508 range as `pyproject.toml`).

### Builder acceptance checklist (implementation)

When **P-02** ships, the PR **must**:

1. Add `docs/examples/player-session-metadata-bar.html` implementing the rules above.
2. Register **P-02** as **Shipped** in the [Pattern inventory](#pattern-inventory) table (this file).
3. Add **CHANGELOG** **Unreleased** bullets under **Added** (new example) and note pattern count / mission tracking if
   appropriate.
4. Mention the new file in **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** so the shipped count stays
   accurate.

**Out of scope for this backlog (spec only here):** new pytest/browser automation — optional follow-up when the repo
adopts automated checks for static examples (see [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix)).

---

## Backlog traceability: Ship session metadata chrome pattern

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Second vanilla snippet, metadata bar above player | [P-02 — Session metadata chrome](#p-02--session-metadata-chrome-viewport-duration-session-id) |
| Same `sessionData` shape as `basic-player.html` (additive metadata) | [`sessionData` contract](#sessiondata-contract-compatibility-with-p-01) |
| Loading placeholder text | [Loading state](#loading-state-normative) |
| Error when metadata missing / invalid | [Error state](#error-state-normative) |
| Keyboard-focus order | [Keyboard focus and accessibility](#keyboard-focus-and-accessibility-normative) |
| Progress toward **5+** patterns | [Pattern inventory](#pattern-inventory), [Mission](../MISSION.md#pattern-coverage-tracking) |
| **CHANGELOG** / mission tracking | [Builder acceptance checklist](#builder-acceptance-checklist-implementation), [Mission](../MISSION.md#pattern-coverage-tracking) |
