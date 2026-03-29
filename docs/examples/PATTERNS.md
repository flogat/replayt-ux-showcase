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
| **P-02** | [`player-session-metadata-bar.html`](player-session-metadata-bar.html) | **Shipped** | Session **metadata chrome**: compact bar **above** the player, same `sessionData` contract as P-01, plus loading / error / focus rules below. |
| **P-03** | [`timeline-scrubber.html`](timeline-scrubber.html) (planned) | **Spec only** | **Timeline scrubber strip**: seek/scrub UX driven by **replayt public JS** + `sessionData.events`, with documented ordering/throttling assumptions and CDN **limitations** note. |

**Mission trajectory:** **P-01** / **P-02** are shipped. **P-03** is specified here (**Spec only**) for the *Timeline scrubber strip example using replayt public events API* backlog; Builder implements `docs/examples/timeline-scrubber.html` (or an equivalent clearly separated section in an existing file—see [Delivery shape](#delivery-shape-normative)). Additional patterns toward **5+** stay **future** backlogs until registered in this table first.

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

**P-02** is **Shipped**; the original PR met the items below. Use the same bar when you change this pattern:

1. `docs/examples/player-session-metadata-bar.html` implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-02** as **Shipped** with the correct filename.
3. **CHANGELOG** **Unreleased** records notable example or contract changes; note pattern count / mission tracking when the inventory changes.
4. **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** reflects the shipped count.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`** (CDN pin vs **`pyproject.toml`**) and
**`tests/test_examples.py`** (example files on disk plus light **P-02** contract strings). Full browser automation remains
out of scope until the [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix) adds it.

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

---

## P-03 — Timeline scrubber strip (events-driven seek)

### User story

As an integrator, I want a **copy-paste vanilla** example that adds a **horizontal timeline scrubber** (slider / track)
below or above the player so operators can **seek** through the replay using **`sessionData.events`** and **replayt’s
published browser/JS API**, with **explicit assumptions** about event ordering and **input throttling** so my fork
behaves predictably across replayt minors inside the supported range.

### Relationship to P-01

[`basic-player.html`](basic-player.html) already mentions extending with a timeline via the replayt events API. **P-03**
is the **dedicated** pattern for that job: it **must not** silently redefine P-01’s init contract; it **layers** scrubber
UX and documented event handling on top of the same **`sessionData` root** (`events` + `metadata`) unless the Builder
documents a deliberate, additive extension in-snippet.

### Delivery shape (normative)

- **Preferred:** new file **`docs/examples/timeline-scrubber.html`**.
- **Allowed alternative:** extend **`basic-player.html`** only if the scrubber is a **clearly separated** section
  (distinct `<section>` or major comment banner + self-contained script block) and **P-03** acceptance criteria still
  read as a single pattern in review; if this path is chosen, update this inventory row to point at the anchor filename
  and **CHANGELOG** **Unreleased** in the same change set.

### `sessionData` and events (normative)

- **Root shape:** Same as P-01: `events` (array) and `metadata` (object). The scrubber **must** use **`events`** (not
  only empty placeholder arrays in the shipped snippet—include **synthetic or documented sample events** sufficient to
  demonstrate a non-trivial timeline, or document how to substitute real API payloads).
- **Documented ordering assumption:** The HTML/JS **must** include a short **comment block** (design-handoff style)
  stating what ordering integrators should assume for `events` (e.g. “replayt guarantees monotonic timestamps” vs
  “sort client-side by field X before mapping to the scrubber”). If the showcase cannot assert upstream guarantees,
  state **“integrators should verify against replayt release notes for their pin”** and implement **defensive ordering**
  (e.g. sort once before building the time range) **in the example** so the demo is stable.
- **Time range:** The snippet **must** document which **timestamp(s)** define scrubber min/max and playhead position
  (e.g. first/last event time, `metadata.startTs` + duration, or API described in comments). Ambiguous mapping is not
  acceptable for **Shipped**—pick one approach and document it.

### Scrub / seek interactions (normative)

- **Primary control:** A **range** or **single-thumb** slider (or equivalent ARIA **`slider`**) spanning the session
  timeline; dragging or keyboard adjustment **seeks** the replay.
- **Keyboard:** Slider (or focusable scrub control) **must** be reachable and adjustable without a pointer; document
  expected keys (native range behavior is enough if documented).
- **Published JS only:** All **replayt** calls **must** use **documented public** browser/JS entry points (same boundary
  as [Upstream boundary](../DESIGN_PRINCIPLES.md#one-way-to-do-it-canonical-patterns)—no minified private hooks). The file
  **must** list **exact symbols** used (e.g. `window.replayt.…`) in a header or comment block and tie them to **replayt**
  docs or release notes where possible.
- **Graceful degradation:** If init fails or `events` is empty, show a **user-visible** message (not only `console.error`).

### Throttling and coalescing (normative)

- **During scrub:** High-frequency input (pointer move, `input` events) **must** be **throttled or debounced** before
  calling seek APIs (e.g. `requestAnimationFrame`, debounced handler, or documented “at most N seeks per second”
  strategy). Document the chosen approach in comments so integrators can tune it.
- **End of gesture:** On **pointer up** / **change** (commit), **must** perform a **final** seek to the committed value
  so the player ends on the operator’s chosen frame.

### Limitations and CDN builds (normative)

- Include a visible **“Limitations”** short note (prose in the page or comment visible in “view source”) stating that
  **some CDN builds may omit or rename seek/event APIs**; integrators should **pin** a **replayt** version whose **JS**
  surface matches the snippet and **upgrade** if methods are missing. Align the **`<script src=…replayt@…>`** pin with
  [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).

### replayt pin and file placement

- **CDN / npm pin** in the shipped HTML **must** satisfy **`pyproject.toml`** **replayt** PEP 508 range (enforced by
  **`tests/test_docs_examples_replayt_pins.py`** once the file exists).

### Builder acceptance checklist (implementation)

**P-03** is **Spec only** until the items below are met; then mark **Shipped** in [Pattern inventory](#pattern-inventory)
and update **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** counts in the **same** change set as the HTML.

1. **`docs/examples/timeline-scrubber.html`** (or approved alternate per [Delivery shape](#delivery-shape-normative))
   implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-03** as **Shipped** with the correct filename.
3. **Extend** **`tests/test_examples.py`** with file presence and **light contract markers** aligned with this spec
   (ordering comment block, throttling note, limitations note, scrub control, **replayt** script pin)—mirror the **P-02**
   approach; full browser automation remains optional per [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
4. **CHANGELOG** **Unreleased** records the new example; note pattern count / mission tracking when status flips to **Shipped**.

**Automated checks today (when shipped):** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers as extended by Builder.

---

## Backlog traceability: Timeline scrubber strip example (replayt public events API)

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| New example or clearly separated section | [Delivery shape](#delivery-shape-normative) |
| Seek/scrub interactions | [Scrub / seek interactions](#scrub--seek-interactions-normative) |
| Documented event ordering assumptions | [`sessionData` and events](#sessiondata-and-events-normative) |
| Throttling / coalescing | [Throttling and coalescing](#throttling-and-coalescing-normative) |
| Published replayt JS surface only | [Scrub / seek interactions](#scrub--seek-interactions-normative) |
| Short limitations note if CDN lacks API | [Limitations and CDN builds](#limitations-and-cdn-builds-normative) |
| **replayt** pin in range | [replayt pin and file placement](#replayt-pin-and-file-placement) |
| Progress toward **5+** patterns | [Pattern inventory](#pattern-inventory), [Mission](../MISSION.md#pattern-coverage-tracking) |
