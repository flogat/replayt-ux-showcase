# Examples — UI pattern catalog

This file is the **canonical inventory** for distinct, copy-paste integrator examples under `docs/examples/`: **vanilla
HTML/JS** files (default path) and **registered framework subtrees** (**React** — **P-06**; **Vue** — **P-07**; **Svelte**
— **P-08**). **P-09** is the **vanilla** teaching example for **event overlays** (**Shipped** as **`event-overlay.html`**).
**P-10** is the **vanilla** pattern for **click heatmap / density on a static viewport-sized stage** (**Shipped** as
**[`click-heatmap-canvas.html`](click-heatmap-canvas.html)** — see [P-10 — Click heatmap on static canvas](#p-10--click-heatmap-on-static-canvas-session-click-coordinates)). It supports the mission
success criterion “**5+**” **vanilla** patterns and gives **Spec gate** / **Builder** a single place to check
**what counts as a pattern**, **what ships where**, and **acceptance criteria** before code lands.

**Related:** [Mission — Success](../MISSION.md#pattern-coverage-tracking), [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix), [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins), [**Session fixture schema (canonical)**](SESSION_SCHEMA.md) (`SAMPLE_SESSION_DATA` / **P-01** alignment), [Keyboard and focus model](../a11y/keyboard-model.md) (shared a11y checklist for player / timeline embeds), [Design-to-code playbook](../playbook/README.md) (tokens, component anatomy, printable handoff checklist), [Optional local bundler recipe](build.md) (maintainer **npm** + **Vite** / **esbuild** — not a UI pattern ID), [Changelog, semver, and release notes](../DESIGN_PRINCIPLES.md#changelog-semver-and-release-notes) (**`CHANGELOG.md`** **Unreleased** bullets when **Shipped** patterns or mission counts move). **P-10** extends integrator **analytics-style** overlays without replacing **P-09**’s scrub-linked callout lane.

**Release notes:** When a row here moves to **Shipped** (or you add a new **P-xx** consumers will track), update **`CHANGELOG.md`** **`[Unreleased]`** in the **same change set** as this file, **`docs/MISSION.md`** (pattern table), and **`docs/compat.md`** (vanilla catalog) when that digest lists the pattern—see [Unreleased: pattern coverage and mission tracking](../DESIGN_PRINCIPLES.md#unreleased-pattern-coverage-and-mission-tracking).

## Pattern inventory

A **pattern** is a **standalone** integrator-facing example with its own **primary user job** (not a one-line tweak of
another file). Filename changes follow [Deprecation and removal](../DESIGN_PRINCIPLES.md#deprecation-and-removal).

| ID | Artifact | Status | Summary |
| -- | -------- | ------ | ------- |
| **P-01** | [`basic-player.html`](basic-player.html) | **Shipped** | Minimal embedded player: container, §1 JSON fixture (**`rux-showcase-session-fixture`**), adapter before **`replayt.player.init`**, theme note — see [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md). |
| **P-02** | [`player-session-metadata-bar.html`](player-session-metadata-bar.html) | **Shipped** | Session **metadata chrome**: compact bar **above** the player, same `sessionData` contract as P-01, plus loading / error / focus rules below. |
| **P-03** | [`timeline-scrubber.html`](timeline-scrubber.html) | **Shipped** | **Timeline scrubber strip**: seek/scrub UX driven by **replayt public JS** + `sessionData.events`, with documented ordering/throttling assumptions and CDN **limitations** note. |
| **P-04** | [`embed-container-states.html`](embed-container-states.html) | **Shipped** | **Embed container** lifecycle: skeleton while **loading**, user-visible **failure** + **retry**, **`aria-live`** / **`role="status"`** status for operators and **automation agents**; **published** replayt JS only. |
| **P-05** | [`fixture-replay.html`](fixture-replay.html) | **Shipped** | **Offline fixture** for **reviewers** and **LLM** harnesses: **inlined** synthetic **`sessionData`**, **no** runtime session fetch, **no** secrets, **no** live/stochastic model calls; pinned **replayt** player script only. |
| **P-06** | [`react/`](react/) ([`README.md`](react/README.md), [`src/App.jsx`](react/src/App.jsx)) | **Shipped** | **React 18** timeline player: same **`sessionData`** / **`replayt.player.init`** contract as **P-01**, timeline scrub UX aligned with **P-03**; **Vite**-first (or **esbuild** notes); **not** an npm-published package. |
| **P-07** | [`vue/`](vue/) ([`README.md`](vue/README.md), [`src/App.vue`](vue/src/App.vue)) | **Shipped** | **Vue 3** minimal timeline player: same **replayt-facing** data and init contract as **P-01**, scrubber parity with **P-03** / **P-06**; **static-build**-friendly (**`npm run build`**); **not** an npm-published package from this repo. |
| **P-08** | [`svelte/`](svelte/) ([`README.md`](svelte/README.md), [`src/App.svelte`](svelte/src/App.svelte)) | **Shipped** | **Svelte 4** minimal timeline player: same contracts as **P-07** (mirror **P-06** intent for the **Svelte** stack). |
| **P-09** | [`event-overlay.html`](event-overlay.html) | **Shipped** | **Event overlay lane**: scrub-linked playhead, **hover** (pointer) **tooltips** / callouts on events, **keyboard**-reachable focus and **Escape** for dismissible layers; **offline** / **LLM**-safe **`sessionData`** story per normative section below. |
| **P-10** | [`click-heatmap-canvas.html`](click-heatmap-canvas.html) | **Shipped** | **Click heatmap on static canvas (or SVG)**: map **`click`** events’ **`x`/`y`** onto a **viewport-sized** stage; **density** / aggregation visualization; **`SAMPLE_SESSION_DATA`**-aligned **§1** literal (with extra **click** samples for visible hotspots); **accessible** name + focus order per normative section below — **distinct** from **P-09** (no requirement to duplicate scrub-linked callout lane as the primary teaching goal). |

**Mission trajectory:** **P-01** through **P-05**, **P-09**, and **P-10** are shipped (**7** distinct **vanilla** patterns), satisfying the mission **5+** target for HTML examples. **P-06** through **P-08** are **shipped** **framework** subtrees (**React**, **Vue**, **Svelte**). Framework examples do not change the vanilla count. **P-09** extends teaching coverage for **overlay** UX described in the playbook—**[component anatomy §2](../playbook/component-anatomy.md#2-overlays-dialogs-popovers-event-callouts)**. **P-10** is **Shipped** as **`click-heatmap-canvas.html`** (**Playwright** inventory + **`tests/test_examples.py`** markers ship with the file). Additional patterns stay **future** backlogs until registered in this table first.

---

## Canonical session fixture (cross-surface)

**Normative doc:** [`docs/examples/SESSION_SCHEMA.md`](SESSION_SCHEMA.md).

- **§1 Showcase session fixture** is the **same** object family as **`replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`** and
  the **`SAMPLE_SESSION_DATA`** block in **[`docs/demo.md`](../demo.md)** (**`start_ts`**, **`viewport.w` / `h`**, **`duration`**,
  **`events[].ts`** in **seconds**).
- **§2 `replayt.player.init` wire shape** covers **camelCase** / **ms** fields where the browser API differs; use a **pure
  adapter** (see **`docs/examples/react/README.md`**) instead of inventing a third naming scheme.
- **§3** maps **P-01** / **P-02** to §1 vs §2; **§4–§5** are backlog acceptance and the **`pytest`** guard
  (**`tests/test_session_schema_examples.py`**).

When **P-01**/**P-02**/**P-03** prose says “same `sessionData` as **P-01**,” distinguish **fixture canonical** (§1) from
**init wire** (§2) if both appear in one file.

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
- **Showcase fixture baseline** (cross-surface with **`SAMPLE_SESSION_DATA`**): see [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1
  — **`metadata.start_ts`**, **`metadata.viewport.w` / `h`**, **`metadata.duration`**, **`events[].ts`** (seconds).
  **P-01** ships that shape in **`basic-player.html`**. **P-02** keeps **`startTs`**, **`durationMs`**, and similar fields in the
  mocked async payload for the chrome bar (**init**-style); **viewport** accepts **`w` / `h`** first with **`width` / `height`**
  fallback (see **`player-session-metadata-bar.html`** and **SESSION_SCHEMA** §3).
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
| Viewport | **`metadata.viewport.w` × `metadata.viewport.h`** (canonical per [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1), or legacy **`width` × `height`** until removed | **Required** after load. If missing, show **error state** (not an empty bar pretending success). |
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

Shared checklist: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** (tab order, **Escape** for dismissible UI, focus visibility). The bullets below are **P-02**-specific.

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
  (e.g. first/last event time, **`metadata.start_ts`** + **`metadata.duration`** in seconds for fixture parity, or **ms**
  **`metadata.startTs`** + **`metadata.durationMs`** after adapter — see [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md)). Ambiguous mapping is not
  acceptable for **Shipped**—pick one approach and document it.

### Scrub / seek interactions (normative)

- **Primary control:** A **range** or **single-thumb** slider (or equivalent ARIA **`slider`**) spanning the session
  timeline; dragging or keyboard adjustment **seeks** the replay.
- **Keyboard:** Slider (or focusable scrub control) **must** be reachable and adjustable without a pointer; document
  expected keys (native range behavior is enough if documented). Full scrubber / **Escape** guidance: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** (sections 3–4).
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

**P-03** is **Shipped**; the original delivery met the items below. Use the same markers when you change this pattern:

1. **`docs/examples/timeline-scrubber.html`** (or approved alternate per [Delivery shape](#delivery-shape-normative))
   implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-03** as **Shipped** with the correct filename.
3. **`tests/test_examples.py`** includes file presence and **light contract markers** aligned with this spec
   (ordering comment block, throttling note, limitations note, scrub control, **replayt** script pin)—mirror the **P-02**
   approach; full browser automation remains optional per [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
4. **CHANGELOG** **Unreleased** records notable example or contract changes; note pattern count / mission tracking when the inventory changes.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-03**.

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

---

## P-04 Embed container states (empty, loading, failure, recovery)

### User story

As an **operator** or **integrator**, I want the **replay player embed container** (the DOM subtree passed to
`replayt.player.init` as `container`, per **P-01**) to have **predictable UX** while `sessionData` is **not yet**
available, when **fetch fails**, and when **init or data** fails after load— including **skeleton** affordances,
**retry**, and **accessible status announcements**—without relying on **undocumented** replayt internals.

### Relationship to P-01 and P-02

- **P-01** ([`basic-player.html`](basic-player.html)) shows a minimal init with inline `sessionData`. It does **not**
  yet normatively define loading/error/retry for the **embed container** itself; **P-04** is the dedicated contract for
  that job.
- **P-02** defines loading/error for the **metadata bar** and “at least one of bar or player must make loading obvious.”
  **P-04** tightens the **player/embed** side: even when no metadata bar exists, the **container** must communicate
  **loading**, **failure**, and **recovery** per below.
- **P-04** may ship as **`docs/examples/embed-container-states.html`** or as a **clearly delimited** section inside
  **`basic-player.html`** (same rules as **P-03** [Delivery shape](#delivery-shape-normative): if merged into **P-01**,
  update this inventory row to point at the anchor file and keep acceptance criteria in one place).

### P-04 async sessionData acquisition (normative)

- The example **must** model **async** acquisition of `sessionData` (e.g. `fetch` to a placeholder URL or a **documented**
  `setTimeout` fake loader)—**no** suggestion that operators should call private replayt HTTP helpers not described in
  **published** replayt docs.
- **Empty vs not-yet-loaded:** Before the async source resolves, the UI **must not** look like a **successful** session
  with zero events unless the snippet explicitly demonstrates **“loaded empty”** as a **distinct** labeled state from
  **“still loading.”**
- **On success:** Pass the resolved object to **`replayt.player.init`** (or the **documented** equivalent public entry
  for the pinned version) using only **published** JS symbols; list those symbols in a header or comment block (same
  boundary as **P-03**).

### P-04 embed skeleton and loading (normative)

- While `sessionData` is **in flight**, the **embed container** (or a dedicated child **wrapper** that fills the same
  visual box as the player) **must** show **skeleton UI**: non-empty placeholder **structure** (e.g. muted blocks,
  shimmer optional) and **visible text** such as “Loading replay…”—not a blank white box.
- **Automation / design handoff:** Include a short comment that **operators** and **automation agents** should treat the
  loading placeholder as **non-final** UI (stable **hook** optional: e.g. `data-demo-state="loading"` on the wrapper—
  not required unless the Builder documents it as the scrape contract).

### P-04 embed failure surface (normative)

- If **fetch** fails (network / non-OK HTTP) or **`replayt.player.init`** throws / rejects per the snippet’s error
  handling, the embed region **must** show a **user-visible** error message (not only `console.error`).
- The copy **must** distinguish **network/load failure** from **invalid payload** when both are demonstrated (can be
  two separate demo buttons or commented alternate code paths).

### P-04 retry affordance (normative)

- After a **recoverable** failure (at minimum: **failed fetch**), the snippet **must** expose a **keyboard-focusable**
  control (e.g. `<button type="button">`) labeled for **retry** (e.g. “Retry”) that **re-runs** the load path.
- **Tab order:** Retry control **must** appear in **logical** order (typically **before** any secondary chrome that is
  disabled while broken)—document intent in a comment block for handoff.
- Broader **keyboard / focus** checklist (toolbar vs player, **Escape**): **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**.

### P-04 status live region (normative)

- The snippet **must** include an element with **`role="status"`** (preferred) or equivalent **`aria-live="polite"`**
  region dedicated to **high-level phase changes**: at least **loading**, **ready** (or **playing** / **initialized**),
  and **failed** (exact strings are implementation-defined but **must** be listed in-snippet as the **announcement
  contract**).
- **Polite** by default; use **`assertive`** only if the snippet documents **why** (e.g. synchronous fatal error)—avoid
  noisy announcements on every micro-interaction.
- **Audience — automation agents ([`DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#audience)):** Document that LLM/CI
  scrapers may rely on **this live region’s text** (or the optional `data-demo-state` hook) **only** as described in
  the file’s comment block—do not invent parallel hidden channels.

### P-04 replayt pin and file placement

- Planned primary file: **`docs/examples/embed-container-states.html`**. **replayt** script URL **must** satisfy
  [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins).
- **No private APIs:** All replayt usage **must** match **published** player/init docs for the pinned version; if the
  snippet checks for optional APIs, document **graceful** fallback (message + retry or doc link)—not deep object
  probing of minified internals.

### Builder acceptance checklist (implementation)

**P-04** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin tests aligned when this pattern changes.

1. **`docs/examples/embed-container-states.html`** implements the normative sections above (new file per [Relationship to P-01 and P-02](#relationship-to-p-01-and-p-02)).
2. [Pattern inventory](#pattern-inventory) lists **P-04** as **Shipped** with the correct filename.
3. **[`docs/demo.md`](../demo.md#cross-surface-operator-story-console-demo-and-web-embed)** stays aligned with the
   shipped **operator story** table (same vocabulary: loading / failure / retry / ready).
4. **CHANGELOG** **Unreleased** records the example; **`docs/MISSION.md`** pattern count includes **P-04** as a **fourth**
   shipped vanilla file.
5. **`tests/test_docs_examples_replayt_pins.py`** scans the new **`*.html`**. **`tests/test_examples.py`** includes file presence and light contract markers (loading copy, live region, **Retry**, tab-order comment, **replayt** script pin).

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-04**.

---

## Backlog traceability: Empty, loading, and failure states for the embed container

| Backlog acceptance criterion | Where specified |
| ---------------------------- | --------------- |
| Skeleton / loading UX for embed container | [P-04 embed skeleton and loading](#p-04-embed-skeleton-and-loading-normative) |
| User-visible failure + distinguish load vs validation where applicable | [P-04 embed failure surface](#p-04-embed-failure-surface-normative) |
| Retry affordance (focusable) | [P-04 retry affordance](#p-04-retry-affordance-normative) |
| Accessible announcements (`role="status"` / `aria-live`) | [P-04 status live region](#p-04-status-live-region-normative) |
| **Automation agents** + operators: documented scrape/announcement contract | [P-04 status live region](#p-04-status-live-region-normative), [P-04 embed skeleton and loading](#p-04-embed-skeleton-and-loading-normative) |
| **Published** replayt JS only | [P-04 async sessionData acquisition](#p-04-async-sessiondata-acquisition-normative), [P-04 replayt pin and file placement](#p-04-replayt-pin-and-file-placement) |
| Same operator story as **console** demo doc | **[`docs/demo.md`](../demo.md#cross-surface-operator-story-console-demo-and-web-embed)** |
| Pattern inventory + mission trajectory | [Pattern inventory](#pattern-inventory), [Mission](../MISSION.md#pattern-coverage-tracking) |

---

## P-05 Offline deterministic fixture page for LLM and reviewer workflows

### User story

As a **reviewer** or **automation agent**, I want a **single vanilla HTML** file that renders a replay using **only**
inlined, synthetic **`sessionData`** (no API or `fetch` for the session payload), aligned with
**[LLM boundaries](../DESIGN_PRINCIPLES.md#llm-boundaries)**, so local opens and harness runs are **predictable** and
**secret-free**.

### Relationship to P-01 and P-04

- **P-01** ([`basic-player.html`](basic-player.html)) may mention fetching real **`sessionData`** from a backend. **P-05**
  is the **dedicated** pattern for the **opposite** job: **fixture** data lives **entirely in the document** (or in
  **static** literals the script assigns without I/O).
- **P-04** models **async** acquisition (including simulated `fetch`). **P-05** **must not** use that acquisition story
  for **`sessionData`**—no staged “loading” that resolves from the network for the payload. A **minimal** “ready” UI is
  allowed once **`sessionData`** is a constant and **`replayt.player.init`** (or equivalent public API) has run.

### P-05 sessionData and offline boundary (normative)

- **`sessionData` source:** The object passed to **`replayt.player.init`** (or the **documented** public equivalent for
  the pinned **replayt** JS version) **must** originate from an **inline** JavaScript literal or **static** assignment in
  the same file (or a **non-network** embedding pattern documented in-snippet, e.g. a `const` assembled only from fixed
  primitives—**not** loaded from another URL).
- **Forbidden for session payloads:** `fetch`, **`XMLHttpRequest`**, **`WebSocket`**, **`EventSource`**, **`import()`** to
  remote modules, or any other runtime I/O whose purpose is to obtain or mutate **`sessionData`** from a **network** or
  **environment-specific** source.
- **Allowed:** One **pinned** **replayt** browser bundle via **`<script src="…">`** (same **CDN** / semver story as
  **P-01**–**P-04** and [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins)). That script load is **not** a **session** fetch; it is the **player** dependency. Optional future work (separate backlog) may vendor the bundle for air-gapped workflows; this spec does **not** require it for **Shipped**.

### P-05 forbidden behaviors (normative)

- **No secrets:** No API keys, bearer tokens, signed URLs with secrets, private hostnames tied to credentials, or
  **`import.meta.env`** / **`process.env`**-style reads that could pull real credentials into the page.
- **No live model calls:** No `fetch` or SDK calls to hosted **LLM** / inference endpoints, telemetry that sends session
  content off-device, or **replayt** workflow runners that invoke non-deterministic models **from this file**.
- **No non-reproducible model paths:** Do not embed or call helpers whose **default** behavior is stochastic or
  time-dependent **model** output (contrast with fixed **`MockLLMClient`** narratives elsewhere—**P-05** stays **static
  replay** only unless this spec is revised).

### P-05 determinism (normative)

- **`sessionData`:** Use **fixed** timestamps, ids, and event payloads (e.g. numeric literals, fixed strings). **Do not**
  use `Date.now()`, `new Date()`, `Math.random()`, or environment-derived values **inside `sessionData`** or in
  **harness-scraped** visible strings that are meant to be stable across runs.
- **Comments:** The file **must** include a short **header comment** stating that the page is a **deterministic fixture**
  for reviewers and agents and that **`sessionData`** is **synthetic** and **stable**.

### P-05 replayt pin and open instructions (normative)

- **Primary path:** **`docs/examples/fixture-replay.html`**. If renamed, update this inventory row, **CHANGELOG**
  **Unreleased**, and cross-links in **`README.md`** / **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** in the same change set.
- **Pin:** **`<script src=…>`** **must** satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`** once the file exists).
- **Local open (documentation, not code):** **`README.md`** and **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** **must** tell reviewers
  and harness authors to open the page via a **local static server** rooted sensibly (e.g. from the repo: `cd docs/examples`
  then `python -m http.server`, then browse to `/fixture-replay.html`) so the **CDN** **replayt** script can load under
  typical browser **mixed-content / file URL** rules. **Optional:** note that **`file://`** may fail to load **CDN**
  scripts in some browsers—do not claim **fully air-gapped** behavior unless a **vendored** script path is also shipped
  (future backlog).

### Builder acceptance checklist (implementation)

**P-05** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin tests aligned when this pattern changes.

1. **`docs/examples/fixture-replay.html`** implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-05** as **Shipped** with the correct filename.
3. **`README.md`** and **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** include **local open** instructions (static server under **`docs/examples/`**).
4. **CHANGELOG** **Unreleased** records the example; **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)**
   pattern table reflects **5** shipped vanilla patterns.
5. **`tests/test_docs_examples_replayt_pins.py`** scans the **`*.html`**. **`tests/test_examples.py`** includes file presence and light **P-05** contract markers (determinism header, no session **`fetch(`**, **replayt** script pin).

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-05**.

---

## Backlog traceability: Offline deterministic fixture page for LLM and reviewer workflows

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Inlined synthetic **`sessionData`**, no session over the wire | [P-05 sessionData and offline boundary](#p-05-sessiondata-and-offline-boundary-normative) |
| **No secrets**; **no** live / stochastic model usage in this path | [P-05 forbidden behaviors](#p-05-forbidden-behaviors-normative), [LLM boundaries](../DESIGN_PRINCIPLES.md#llm-boundaries) |
| **Deterministic** fixture | [P-05 determinism](#p-05-determinism-normative) |
| **replayt** pin + local open docs | [P-05 replayt pin and open instructions](#p-05-replayt-pin-and-open-instructions-normative), **`README.md`**, **`docs/REPLAYT_ECOSYSTEM_IDEA.md`** |
| Traceability in design principles | [Offline deterministic fixture page](../DESIGN_PRINCIPLES.md#offline-deterministic-fixture-page-for-llm-and-reviewer-workflows) |
---

## P-06 — React timeline player (basic-player + scrubber parity)

### User story

As a **React** integrator, I want a **self-contained** example under **`docs/examples/react/`** that embeds the replayt
player with a **timeline scrubber**, using the **same** `sessionData` root shape and **published** **`window.replayt`**
consumer APIs as **[`basic-player.html`](basic-player.html)**, with **copy-paste**-friendly layout, **pin** guidance for
**replayt** (npm and/or CDN), and optional **local preview** notes (**Vite** preferred; **esbuild** alternative prose
allowed) — **without** implying this repository publishes a **React** or **showcase** package to npm.

### Relationship to P-01 and P-03

- **P-01** defines the **minimal** embed: `sessionData` with `events` + `metadata`, `replayt.player.init({ container, data, theme })`, theme note, and links to the shared a11y checklist. **P-06** **must** keep that **init** contract and data root; React-specific wiring (e.g. `useRef` for `container`) is an implementation detail.
- **P-03** defines **timeline** behavior: scrub control, defensive ordering of `events`, **throttling** / final seek on commit, **limitations** note for CDN builds, and **tab order** (scrub before player when both are focusable). **P-06** **must** meet the same **normative intent** in React (hooks/effects/components), citing **P-03** in comments where behavior is mirrored.

### `sessionData` and event shapes (normative)

- **Root shape:** Same as **P-01**: an object with **`events`** (array) and **`metadata`** (object). **Fixture field names**
  for parity with **`SAMPLE_SESSION_DATA`** **must** follow [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1 (**`start_ts`**,
  **`viewport.w` / `h`**, **`duration`**, **`events[].ts`**). The object passed to **`replayt.player.init`** may use the
  **init wire** shape (§2) after a **pure** adapter — same pattern as shipped **`adaptConsoleSessionToReplaytMs`**; do **not**
  invent a third parallel schema.
- **Event payloads:** Event objects should be **compatible** with the **schema-level** story in **[`docs/demo.md`](../demo.md#replayt-primitives-usage)** and **replayt** docs for the pinned version (types such as `click`, `scroll`, `keypress`, etc.). The shipped snippet should include **enough non-empty `events`** to exercise the scrubber (not an empty array as the only shipped state).
- **Synthetic vs live:** A **static** literal in source (recommended for copy-paste stability) or a clearly marked placeholder for `fetch` is acceptable; if the snippet uses **`fetch`**, it **must** remain a **documented** public HTTP pattern (no private replayt endpoints), consistent with **P-04** spirit for errors (user-visible failure path documented in README or in-app).
- **P-06 console parity (optional checked-in shape):** The **React** tree may keep a literal matching **`replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`** (**`events[].ts`** in seconds, **`metadata.duration`**, **`metadata.viewport.w` / `h`**, **`metadata.start_ts`**). **`replayt.player.init`** still expects **P-01**-style ms fields; document a **pure** adapter and any wall-clock anchor in **`docs/examples/react/README.md`**. Normative detail: [P-06 — Console sample parity (SAMPLE_SESSION_DATA)](#p-06--console-sample-parity-sample_session_data).

### P-06 — Console sample parity (SAMPLE_SESSION_DATA)

- **Purpose:** One offline session string for **`python -m replayt_ux_showcase.demo`** and the **P-06** **React** sample so operators can diff behavior across surfaces without network or LLM on the default **`npm run dev`** path.
- **Source of truth:** **`replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`** in **`src/replayt_ux_showcase/demo.py`**.
- **Checked-in wiring:** **`docs/examples/react/src/App.jsx`** defines the same **event** list and **metadata** numbers; **`adaptConsoleSessionToReplaytMs`** (or equivalent) maps to **P-01** ms (**`timestamp`**, **`metadata.startTs`**, **`metadata.durationMs`**, **`metadata.viewport.width` / `height`**) before **`init`** and scrub math.
- **Tests:** **`tests/test_examples.py`** should keep **P-06** markers and a check that **React** literals stay aligned with the **Python** module when **`SAMPLE_SESSION_DATA`** changes.

### replayt JavaScript surface (normative)

- **Published consumer API only:** All replayt calls **must** use **documented public** browser entry points — same boundary as **P-03** (e.g. `window.replayt.player.init`, optional seek helpers such as `seekToMs` / `goto` on the object returned from `init` if present). List **exact symbols** used in a file header or top-of-module comment block.
- **No Python / no showcase package imports:** The example is **front-end** only; it does **not** import `replayt_ux_showcase` or assume this repo is installed as a **Python** package for the snippet to run.

### React and tooling (normative)

- **React:** Target **React 18** (`react` / `react-dom` ^18) — aligns with [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
- **Bundler:** **Preferred** delivery: **Vite** (`npm create vite@latest` style) with a short README path: install, `npm run dev`, expected URL. **Allowed:** a concise **esbuild** (or similar) subsection in **`docs/examples/react/README.md`** for integrators who skip Vite.
- **Script loading:** Either (a) **pinned** **CDN** `<script>` in **`index.html`** that loads **`replayt`**’s browser bundle before the app bundle, or (b) **npm** dependency on **`replayt`** and import from the package path documented by **replayt** for the pinned version. Any **explicit** **replayt** version in **`docs/examples/react/*.{html,md}`** must satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`**).
- **Repository boundary:** Files live only under **`docs/examples/react/`** (plus cross-links from **README** / this catalog). Do **not** add a second canonical snippet tree at the repo root; optional root **`package.json`** remains the **maintainer** bundler recipe per **[`build.md`](build.md)**, not a substitute for **`react/`**.

### P-06 README and folder layout (normative)

- **`docs/examples/react/README.md`** (**Shipped** **P-06** must include):
  - **Copy-paste** orientation: what to copy into an existing app vs run as a standalone mini-project.
  - **Version pins:** **replayt** semver (npm and/or CDN) **inside** the PEP 508 band in **`pyproject.toml`**; **React 18** range; link to **[`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md)** for CDN vs bundled tradeoffs.
  - **Runbook:** `npm install`, `npm run dev` (or equivalent), and any prerequisite (**Node** version) in one place.
  - **Non-goal:** State explicitly that this folder is **not** a published npm package from this repository.
- **Source files:** At minimum, one **React** module (or **JSX**/**TSX** if the Builder chooses TypeScript) that mounts the player and implements the timeline; **`index.html`** + small entry (**`main.jsx`**) acceptable. Exact filenames are a **Builder** choice; update the [Pattern inventory](#pattern-inventory) row if the primary entry differs from “see README.”

### Accessibility and keyboard (normative)

- Follow **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** — scrubber keys, focus visibility, **Escape** where overlays exist, tab order consistent with **P-03** (scrub control before player focusables when both exist).
- Include a short **handoff comment** (JSX comment or README bullet) describing **tab order** intent.

### Limitations note (normative)

- Include the same **class** of **CDN / build limitations** callout as **P-03** (visible copy or view-source comment): some builds may omit or rename seek APIs; integrators should **pin** a **replayt** version whose JS matches the snippet.

### Builder acceptance checklist (implementation)

**P-06** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, pin tests, and **`tests/test_examples.py`** aligned when this pattern changes.

1. **`docs/examples/react/`** exists with **`README.md`** meeting [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative).
2. React source implements **`sessionData`** + **`replayt.player.init`** per [Relationship to P-01 and P-03](#relationship-to-p-01-and-p-03) and timeline behavior per **P-03** intent.
3. [Pattern inventory](#pattern-inventory) lists **P-06** as **Shipped** with the correct paths.
4. **`tests/test_docs_examples_replayt_pins.py`** scans **`*.html`**, **`*.md`** under **`docs/examples/react/`**; **`tests/test_examples.py`** includes file-presence and light **P-06** contract markers.
5. **CHANGELOG** **Unreleased** records the example; **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** framework row is **Shipped**.
6. **[`README.md`](../../README.md)** project layout mentions **`docs/examples/react/`** as **Shipped**.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-06**.

---

## Backlog traceability: Ship React timeline player snippet under docs/examples/react/

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Self-contained **React** example under **`docs/examples/react/`** | [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative), [React and tooling](#react-and-tooling-normative) |
| **Vite** or **esbuild** notes | [React and tooling](#react-and-tooling-normative) |
| Mirrors **basic-player** `sessionData` + **`replayt.player.init`** | [Relationship to P-01 and P-03](#relationship-to-p-01-and-p-03), [`sessionData` and event shapes](#sessiondata-and-event-shapes-normative) |
| Timeline / scrub UX aligned with **P-03** | [Relationship to P-01 and P-03](#relationship-to-p-01-and-p-03), [Limitations note](#limitations-note-normative) |
| **Published** replayt JS only | [replayt JavaScript surface](#replayt-javascript-surface-normative) |
| README: copy-paste + **version pin** guidance | [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative) |
| **Not** an npm-published showcase package | [React and tooling](#react-and-tooling-normative) |
| Shared **keyboard / focus** checklist | [Accessibility and keyboard](#accessibility-and-keyboard-normative) |
| Traceability in design principles | [Backlog traceability: Ship React timeline player snippet](../DESIGN_PRINCIPLES.md#backlog-traceability-ship-react-timeline-player-snippet) |

---

## P-07 — Vue 3 timeline player (basic-player + scrubber parity)

### User story

As a **Vue** integrator, I want a **self-contained** example under **`docs/examples/vue/`** that embeds the replayt
player with a **timeline scrubber**, using the **same** `sessionData` root shape and **published** **`window.replayt`**
consumer APIs as **[`basic-player.html`](basic-player.html)**, with **scrubber behavior** matching the normative intent
of **P-03** and the shipped **P-06** React sample — **copy-paste**-friendly layout, **pin** guidance for **replayt**
(npm and/or CDN), **Vite**-based **static production build** (`npm run build`), and explicit **non-goal** language that
this repository does **not** publish a **Vue** or **showcase** package to npm.

### Relationship to P-01, P-03, and P-06

- **P-01** defines the **minimal** embed contract. **P-07** **must** keep **`sessionData`** (`events` + `metadata`),
  **`replayt.player.init({ container, data, theme })`**, and **published** JS entry points only.
- **P-03** / **P-06** define **timeline** behavior (scrub control, defensive **`events`** ordering, **throttling** /
  final seek on commit, **limitations** note, **tab order** when scrubber and player are both focusable). **P-07** **must**
  meet the same **normative intent** in **Vue 3** (Composition API preferred; Options API allowed if documented).
- **P-06** is the **reference shape** for “framework subtree + README + Vite”: **P-07** should mirror **folder
  responsibilities** (README sections, pin table, runbook, **not an npm package** disclaimer) even if filenames differ.

### P-07 sessionData and event shapes (normative)

Same requirements as **P-06** [`sessionData` and event shapes](#sessiondata-and-event-shapes-normative): **P-01** root
shape, sample **non-empty** `events` for the scrubber, synthetic literal or documented **`fetch`** pattern, **no**
`replayt_ux_showcase` / Python imports.

### P-07 replayt JavaScript surface (normative)

Same as **P-06** [replayt JavaScript surface](#replayt-javascript-surface-normative): **documented** **`window.replayt`**
symbols only; list them in a **file header** or top-of-SFC comment block.

### P-07 Vue and tooling (normative)

- **Vue:** Target **Vue 3** (`vue` **^3.4** or compatible **^3** range) — aligns with [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
- **Bundler:** **Vite** with **`@vitejs/plugin-vue`** as the **default** documented path: `npm install`, `npm run dev`,
  `npm run build` / `npm run preview` (or equivalent static preview) called out in **`docs/examples/vue/README.md`**.
  **Allowed:** a short **esbuild** (or **Rollup**) subsection in the README for integrators who skip Vite, consistent
  with **P-06** esbuild notes (CDN **`script`** before app bundle).
- **Script loading:** Same options as **P-06** — pinned **CDN** `<script>` in **`index.html`** before the app bundle,
  **or** **npm** `replayt` import per upstream docs for the pinned version. Any **explicit** **replayt** version in
  **`docs/examples/vue/*.{html,md,vue}`** inside demonstrator snippets must satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`**).
- **DOM container:** The element passed as **`container`** to **`replayt.player.init`** **must** be a **real** DOM node
  (e.g. Vue **`ref`** to a mount-target **`div`**, **`onMounted`** / **`watch`** lifecycle for init and teardown
  documented in README or comments).
- **Repository boundary:** Files live only under **`docs/examples/vue/`** (plus cross-links). **Do not** imply a
  published package scope such as **`@replayt-ux-showcase/*`** or a **non-`private`** **`package.json`** without a
  maintainer decision and **CHANGELOG** entry.

### P-07 README and folder layout (normative)

- **`docs/examples/vue/README.md`** (**Shipped** **P-07** must include): same **class** of sections as **P-06**
  [P-06 README and folder layout](#p-06-readme-and-folder-layout-normative) — copy-paste vs standalone, **version pins**
  table (**replayt**, **Vue**), link to **[`docs/FRONTEND_SUPPLY_CHAIN.md`](../FRONTEND_SUPPLY_CHAIN.md)**, **runbook**
  (**Node** prerequisite, `npm install`, dev + production-shaped preview), **non-goal** (not a published npm product
  from this repo).
- **Source files:** At minimum, one **`.vue`** SFC (or small composition split) that mounts the player and implements the
  timeline; **`index.html`** + **`main.js`**/**`main.ts`** entry acceptable. **`package.json`** in this subtree **must**
  include **`"private": true`** when shipped.

### P-07 Accessibility and keyboard (normative)

Same as **P-06** [Accessibility and keyboard](#accessibility-and-keyboard-normative): **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**,
tab order consistent with **P-03**, short handoff comment on **tab order** intent.

### P-07 Limitations note (normative)

Same as **P-06** [Limitations note](#limitations-note-normative): **CDN / build** caveats for seek APIs; **pin** a
matching **replayt** JS version.

### P-07 Builder acceptance checklist (implementation)

**P-07** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, pin tests, and **`tests/test_examples.py`** aligned when this pattern changes.

1. **`docs/examples/vue/`** exists with **`README.md`** meeting [P-07 README and folder layout](#p-07-readme-and-folder-layout-normative).
2. Vue source implements **`sessionData`** + **`replayt.player.init`** and **P-03**-aligned scrubber behavior per [Relationship to P-01, P-03, and P-06](#relationship-to-p-01-p-03-and-p-06).
3. [Pattern inventory](#pattern-inventory) lists **P-07** as **Shipped** with correct paths.
4. **`tests/test_docs_examples_replayt_pins.py`** scans **`*.html`**, **`*.md`**, and **`*.vue`** under **`docs/examples/`**; **`tests/test_examples.py`** includes file-presence and light **P-07** contract markers (mirror **P-06**).
5. **CHANGELOG** **Unreleased** records the example; **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)**
   framework row for **Vue** is **Shipped**.
6. **[`README.md`](../../README.md)** project layout mentions **`docs/examples/vue/`** as **Shipped**.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-07**.

---

## Backlog traceability: Vue minimal player under docs/examples/vue/

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| **`docs/examples/vue/`** self-contained tree | [P-07 README and folder layout](#p-07-readme-and-folder-layout-normative), [P-07 Vue and tooling](#p-07-vue-and-tooling-normative) |
| Same **`sessionData`** + **`replayt.player.init`** as **P-01** | [Relationship to P-01, P-03, and P-06](#relationship-to-p-01-p-03-and-p-06), [P-07 sessionData and event shapes](#p-07-sessiondata-and-event-shapes-normative) |
| Scrubber UX aligned with **P-03** / **P-06** | [Relationship to P-01, P-03, and P-06](#relationship-to-p-01-p-03-and-p-06), [P-07 Limitations note](#p-07-limitations-note-normative) |
| **Vite** + **static** `build` path documented | [P-07 Vue and tooling](#p-07-vue-and-tooling-normative) |
| **Published** replayt JS only | [P-07 replayt JavaScript surface](#p-07-replayt-javascript-surface-normative) |
| **Not** a published npm package; **`private`** package.json | [P-07 Vue and tooling](#p-07-vue-and-tooling-normative), [P-07 README and folder layout](#p-07-readme-and-folder-layout-normative) |
| Shared **keyboard / focus** checklist | [P-07 Accessibility and keyboard](#p-07-accessibility-and-keyboard-normative) |
| Traceability in design principles | [Backlog traceability: Vue and Svelte minimal player examples](../DESIGN_PRINCIPLES.md#backlog-traceability-vue-and-svelte-minimal-player-examples) |

---

## P-08 — Svelte 4 timeline player (basic-player + scrubber parity)

### User story

As a **Svelte** integrator, I want a **self-contained** example under **`docs/examples/svelte/`** that matches **P-07**
feature and contract depth for the **Svelte** stack: **P-01** **`sessionData`** / **`replayt.player.init`**, **P-03**
scrubber intent, **Vite** + **`@sveltejs/vite-plugin-svelte`**, **static-build**-friendly output, and clear **non-goal**
language that this folder is **documentation**, not a published npm product from this repository.

### Relationship to P-01, P-03, P-06, and P-07

Same logical relationships as [P-07 — Relationship to P-01, P-03, and P-06](#relationship-to-p-01-p-03-and-p-06), with
**Svelte** components (**.svelte** files) and **Svelte** reactivity / lifecycle (`onMount`, `$effect` where appropriate)
instead of Vue. **P-07** and **P-08** should be **parallel** in scope (no requirement that one ships before the other,
but both should stay **consistent** if one gains a normative tweak — update both sections in one change set when
possible).

### P-08 sessionData, replayt surface, a11y, limitations (normative)

By reference: apply the same normative bullets as **P-07** [P-07 sessionData and event shapes](#p-07-sessiondata-and-event-shapes-normative),
[P-07 replayt JavaScript surface](#p-07-replayt-javascript-surface-normative), [P-07 Accessibility and keyboard](#p-07-accessibility-and-keyboard-normative),
and [P-07 Limitations note](#p-07-limitations-note-normative), substituting **Svelte** idioms for **Vue**.

### P-08 Svelte and tooling (normative)

- **Svelte:** Target **Svelte 4** (`svelte` **^4**) — aligns with [Showcase stack matrix](../DESIGN_PRINCIPLES.md#showcase-stack-matrix).
  If the Builder ships on **Svelte 5**, update this row, the **Showcase stack matrix**, and **README** pin tables in the
  **same** change set.
- **Bundler:** **Vite** with **`@sveltejs/vite-plugin-svelte`** as the **default** documented path; **`npm run build`**
  produces integrator-inspectable static assets. **Allowed:** esbuild / Rollup prose mirroring **P-07**.
- **Script loading**, **repository boundary**, **`private` `package.json`:** Same intent as **P-07** [P-07 Vue and tooling](#p-07-vue-and-tooling-normative)
  (paths under **`docs/examples/svelte/`** only).

### P-08 README and folder layout (normative)

- **`docs/examples/svelte/README.md`**: mirror **P-07** [P-07 README and folder layout](#p-07-readme-and-folder-layout-normative)
  (sections, pins table, runbook, non-goal).
- **Source files:** At least one **`.svelte`** component + **`index.html`** + small JS entry; exact names are a **Builder**
  choice; update the [Pattern inventory](#pattern-inventory) row if the primary entry differs from “see README.”

### P-08 Builder acceptance checklist (implementation)

**P-08** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, pin tests, and **`tests/test_examples.py`** aligned when this pattern changes.

1. **`docs/examples/svelte/`** + **`README.md`** per [P-08 README and folder layout](#p-08-readme-and-folder-layout-normative).
2. Svelte source meets **P-01** / **P-03** / **P-06** intent per [Relationship to P-01, P-03, P-06, and P-07](#relationship-to-p-01-p-03-p-06-and-p-07).
3. [Pattern inventory](#pattern-inventory) lists **P-08** as **Shipped** with correct paths.
4. **`tests/test_docs_examples_replayt_pins.py`** scans **`*.svelte`** with **`*.html`** / **`*.md`** where applicable; **`tests/test_examples.py`** includes **P-08** file-presence and contract markers.
5. **CHANGELOG** **Unreleased** + **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** (**Svelte** row **Shipped**).
6. **[`README.md`](../../README.md)** project layout row for **`docs/examples/svelte/`** as **Shipped**.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-08**.

---

## Backlog traceability: Svelte minimal player under docs/examples/svelte/

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| **`docs/examples/svelte/`** self-contained tree | [P-08 README and folder layout](#p-08-readme-and-folder-layout-normative), [P-08 Svelte and tooling](#p-08-svelte-and-tooling-normative) |
| Same **`sessionData`** + **`replayt.player.init`** as **P-01** | [Relationship to P-01, P-03, P-06, and P-07](#relationship-to-p-01-p-03-p-06-and-p-07) |
| Scrubber UX aligned with **P-03** / **P-06** | Same section |
| **Vite** + **static** `build` | [P-08 Svelte and tooling](#p-08-svelte-and-tooling-normative) |
| **Published** replayt JS only | [P-08 sessionData, replayt surface, a11y, limitations](#p-08-sessiondata-replayt-surface-a11y-limitations-normative) |
| **Not** a published npm package | [P-08 Svelte and tooling](#p-08-svelte-and-tooling-normative) |
| **Keyboard / focus** | [P-08 sessionData, replayt surface, a11y, limitations](#p-08-sessiondata-replayt-surface-a11y-limitations-normative) |
| Traceability in design principles | [Backlog traceability: Vue and Svelte minimal player examples](../DESIGN_PRINCIPLES.md#backlog-traceability-vue-and-svelte-minimal-player-examples) |

---

## P-09 — Event overlay lane (scrub, hover tooltips, keyboard)

### User story

As an integrator, I want a **copy-paste vanilla** page that shows an **event overlay** pattern: a **timeline scrubber**
(or equivalent seek control) **linked** to **per-event callouts** (labels, tooltips, or a small inspector strip) so
operators see **which event** corresponds to the current scrub position, with **pointer hover** affordances **and**
**keyboard** access—using only **published** **`replayt`** browser APIs and a **`sessionData`** story safe for **reviewers**
and **automation agents** per **[LLM boundaries](../DESIGN_PRINCIPLES.md#llm-boundaries)**.

### Relationship to existing patterns and playbook

- **P-01** / **P-03**: Reuse the **same** **`sessionData` root** (`events` + `metadata`) and **P-03**-style **scrub /
  seek** behavior (throttling, final seek on commit, documented event ordering). **P-09** **layers overlay / callout
  UI** on top; it **must not** redefine the init contract.
- **P-05**: For **determinism** and **LLM** / harness friendliness, the **preferred** delivery uses **inlined synthetic
  `sessionData`** (fixed timestamps, ids, strings)—same spirit as **P-05**—so the page is **teachable** without network
  session fetch. An **alternate** subsection that uses **async** acquisition **must** follow **P-04** norms (skeleton,
  error, retry, live region) and **must** remain **secret-free**; do **not** combine non-deterministic model output with
  the primary teaching path unless clearly labeled **out of scope** for default CI scrapers.
- **Playbook:** Overlay **regions**, **z-index**, and **modal vs non-modal** vocabulary **must** align with
  **[`docs/playbook/component-anatomy.md`](../playbook/component-anatomy.md#2-overlays-dialogs-popovers-event-callouts)**.
- **A11y:** Shared checklist **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)** — tab order, scrubber keys,
  **Escape**, optional **roving** list for many focusable event rows (see **§2** there).

### P-09 Overlay UX (normative)

- **Scrub-linked highlight:** Moving the scrubber / playhead **must** update which event (or time bucket) is treated as
  **current**—visually distinct **selected** or **active** state on the corresponding **marker** or **row** in the overlay
  lane (not only a static list).
- **Hover tooltips (pointer):** **At least one** non-empty **tooltip, popover, or title-like callout** **must** appear on
  **hover** (or **pointer over**) for an event marker **or** list row, showing **human-readable** event summary (e.g. type
  + time). **Must not** rely on hover **alone** for the only copy of critical safety text—keep a **visible** label or
  **focus-visible** path (see below).
- **Keyboard / focus:** Operators **must** be able to **tab** to **interactive** overlay controls (markers, list rows, or
  a single composite with **roving** focus). **Focus** on an event **must** surface the **same class of information** as
  hover (e.g. show callout on **`focus`**, not only on **`mouseenter`**). **Escape** **must** dismiss **dismissible**
  layers (popover / non-modal inspector) per **[keyboard-model §4](../a11y/keyboard-model.md#4-escape)**; document
  **focus return** to the **activator** in-snippet.
- **Tab order (handoff):** Include a short **“Tab order (handoff):”** comment block: recommended default **scrubber →
  overlay lane / event list → player container** (adjust only with documented rationale, consistent with
  **[keyboard-model §1](../a11y/keyboard-model.md#1-tab-order-default-dom-order)**).

### P-09 Data and offline / LLM boundary (normative)

- **Primary path (preferred for Ship):** **`sessionData`** from an **inline** literal or **static** assignment in the
  same file—**no** `fetch` / **XHR** / **WebSocket** / **EventSource** for the **session payload** (same forbidden list as
  **P-05** [sessionData and offline boundary](#p-05-sessiondata-and-offline-boundary-normative) for **session** I/O).
- **Determinism:** No `Date.now()`, `new Date()`, `Math.random()`, or environment-derived values **inside `sessionData`**
  or in **harness-scraped** visible strings meant to be stable across runs (mirror **P-05** [Determinism](#p-05-determinism-normative)).
- **Forbidden:** Secrets, live **LLM** calls, or non-reproducible **model** paths in the **default** teaching surface
  (**P-05** [Forbidden behaviors](#p-05-forbidden-behaviors-normative) by reference).
- **Minimum events:** Include **enough** non-trivial **`events`** (suggest **≥ 5**) so scrubbing visibly changes the
  active callout (empty-only demos are **not** **Shipped** for **P-09**).

### P-09 replayt JS surface and pin (normative)

- **Published API only:** **`replayt.player.init`** (or documented equivalent for the pinned version) plus any **seek**
  helpers **listed explicitly** in a header or comment block—same boundary as **P-03**.
- **CDN pin:** **`<script src=…>`** **must** satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`** once the file exists).
- **Primary filename:** **`docs/examples/event-overlay.html`** unless a naming collision forces a rename; if renamed,
  update this inventory row, **CHANGELOG** **Unreleased**, and cross-links in the same change set.

### Optional demo.py console hook (normative intent, optional deliverable)

Cross-surface vocabulary lives in **[`docs/demo.md`](../demo.md#cross-surface-operator-story-console-demo-and-web-embed)**.
When the Builder implements this backlog **and** chooses the optional hook:

- **`demo.py`** remains **stdlib-only** and **offline** (no **replayt** import, no network, no **LLM** calls)—existing
  **[`docs/demo.md`](../demo.md)** acceptance table is unchanged unless extended **additively**.
- **Allowed:** Extra **`[replayt-demo]`** log lines or ASCII annotations that **name** overlay concepts (**active event**,
  **tooltip** / **callout**, **scrub alignment**) using **`SAMPLE_SESSION_DATA`**—**deterministic** ordering only.
- **Verification:** Extend **`docs/demo.md`** test-plan rows **in the same change set** as code; **pytest** updates are
  **Builder** / **Tester** scope (phase **3** / **4**), not this spec.

### P-09 Builder acceptance checklist (implementation)

**P-09** is **Shipped**; delivery met the items below. Keep **PATTERNS.md**, **MISSION**, **CHANGELOG**, and pin tests aligned when this pattern changes.

1. **`docs/examples/event-overlay.html`** implements the normative sections above.
2. [Pattern inventory](#pattern-inventory) lists **P-09** as **Shipped** with the correct filename.
3. **CHANGELOG** **Unreleased** records the example; **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)**
   vanilla count is **6** shipped (**P-01**–**P-05**, **P-09**).
4. **`tests/test_docs_examples_replayt_pins.py`** scans the **`*.html`**; **`tests/test_examples.py`** includes file-presence
   and **light contract markers**—scrub + overlay tab-order comment, determinism / no session **`fetch(`** on the primary path,
   **Limitations** note aligned with **P-03**, **replayt** symbol list.
5. **[`README.md`](../../README.md)** project layout row for **`event-overlay.html`** is **Shipped**.
6. **[`docs/compat.md`](../compat.md#vanilla-ui-pattern-catalog)** digest mentions **P-09** as **Shipped**.

**Automated checks today:** **`tests/test_docs_examples_replayt_pins.py`**; **`tests/test_examples.py`** markers for **P-09**.

---

## Backlog traceability: Event overlay vanilla example + optional demo.py hook

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Registered **vanilla** pattern **P-09** + planned filename | [Pattern inventory](#pattern-inventory), [P-09 replayt JS surface and pin](#p-09-replayt-js-surface-and-pin-normative) |
| Scrub-linked overlay / callout behavior | [P-09 Overlay UX](#p-09-overlay-ux-normative) |
| Hover **and** keyboard-equivalent disclosure | [P-09 Overlay UX](#p-09-overlay-ux-normative) |
| **Escape** + focus return for dismissible layers | [P-09 Overlay UX](#p-09-overlay-ux-normative), [`keyboard-model.md` §4](../a11y/keyboard-model.md#4-escape) |
| **LLM** / offline **`sessionData`** (preferred inline fixture) | [P-09 Data and offline / LLM boundary](#p-09-data-and-offline--llm-boundary-normative), [LLM boundaries](../DESIGN_PRINCIPLES.md#llm-boundaries) |
| **Published** replayt JS only + PEP 508 **CDN** pin | [P-09 replayt JS surface and pin](#p-09-replayt-js-surface-and-pin-normative) |
| Optional **`demo.py`** narrative hook | [Optional demo.py console hook](#optional-demopy-console-hook-normative-intent-optional-deliverable), [`docs/demo.md`](../demo.md#cross-surface-operator-story-console-demo-and-web-embed) |
| **MISSION** / **compat** / **README** when **Shipped** | [P-09 Builder acceptance checklist](#p-09-builder-acceptance-checklist-implementation) |

---

## P-10 — Click heatmap on static canvas (session click coordinates)

### User story

As an integrator, I want a **copy-paste vanilla** page that draws a **viewport-sized “stage”** (static **`<canvas>`** 2D,
**SVG**, or equivalent) showing **where users clicked** during a session by plotting **`click`** event coordinates from
**`sessionData.events`**, with a **clear accessible name**, **visible summary text** for operators, and a **documented
tab / focus order**—using **offline** fixture data aligned with **`SAMPLE_SESSION_DATA`** / [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1,
without conflating this **spatial analytics** view with **P-09**’s **timeline + scrub-linked callouts** pattern.

### Relationship to P-01, P-05, P-09, and SESSION_SCHEMA

- **P-01** / [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md): **`sessionData`** uses **`events`** + **`metadata`**. **Click** events
  carry **`x`**, **`y`** in **viewport pixel space** relative to the recorded session viewport (**`metadata.viewport.w` /
  `h`**). **P-10** **must** document how **`x`/`y`** map to the **CSS size** of the drawing surface (scale, letterboxing,
  or 1:1 when the stage’s **intrinsic** dimensions match **`metadata.viewport`**).
- **P-05** / **P-09**: **Preferred** teaching path uses **inlined** synthetic **`sessionData`** — **no** `fetch` / **XHR** /
  **WebSocket** / **EventSource** for the **session payload** (same forbidden list as **P-05** [sessionData and offline boundary](#p-05-sessiondata-and-offline-boundary-normative)).
  **Determinism** and **LLM**-safe rules mirror **P-05** ([Determinism](#p-05-determinism-normative), [Forbidden behaviors](#p-05-forbidden-behaviors-normative) by reference).
- **P-09**: **P-09** is normatively about **scrub-linked** event **callouts** and **hover**/**keyboard** disclosure along a
  **timeline lane**. **P-10** is normatively about **aggregated spatial** visualization (**heatmap**, **bins**, **stacked
  alpha circles**, or similar) on a **single** stage. A **Shipped** **P-10** file **may** live alongside a minimal player
  **only** if the **primary** integrator job remains obvious in page structure and comments; **must not** replace **P-09**
  or copy its acceptance checklist wholesale.

### P-10 Event selection and data (normative)

- **Filter:** Use events with **`type === 'click'`** (string) and numeric **`x`**, **`y`**. Other event types **may** be
  ignored for the heatmap layer; **must** be stated in a short **header comment**.
- **Fixture:** **Preferred:** literal derived from **`replayt_ux_showcase.demo.SAMPLE_SESSION_DATA`** (full or **trimmed**
  subset) so operators can diff against **`python -m replayt_ux_showcase.demo`** and **P-01**. **Trimmed** literals **must**
  stay **§1**-compatible for all included events and **metadata** keys they rely on (see [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1).
- **Minimum clicks:** Include **enough** **`click`** events (suggest **≥ 4** with **overlapping** or **nearby** coordinates)
  so **density** or **stacking** is visible; an **empty** or **single-point-only** demo is **not** **Shipped** for **P-10**
  unless the snippet explicitly demonstrates **degenerate** data as a **separate** labeled subsection (still with **user-visible**
  explanation).

### P-10 Stage and visualization (normative)

- **Viewport-sized stage:** The drawing surface **must** represent the session viewport **semantically**: either **CSS**
  dimensions match **`metadata.viewport.w` × `h`** (with documented scaling), or the snippet **documents** a **scale factor**
  from viewport pixels to canvas pixels. **Letterboxing** is allowed if **documented** and **consistent** with **`x`/`y`** mapping.
- **Heatmap / aggregation:** **Must** produce a **visual aggregation** (e.g. **2D histogram** / **binned** heatmap, **Gaussian**
  blur of click points, **additive alpha** splats). A **scatter** of raw points **without** any **density** cue is **not**
  sufficient for **Shipped** **P-10** unless paired with **binning** or **alpha** overlap that makes **hot regions** obvious —
  document the chosen algorithm in-snippet for **design–engineering handoff**.
- **Implementation:** **`<canvas>`** (2D context) **or** **SVG** — **Builder** choice; **must** state **why** if one is chosen
  (e.g. performance vs inspectable DOM).

### P-10 Accessibility and keyboard (normative)

Shared checklist: **[`docs/a11y/keyboard-model.md`](../a11y/keyboard-model.md)**.

- **Programmatic name:** If the heatmap uses **`<canvas>`**, it **must** expose an accessible name via **`role="img"`** and
  **`aria-label`**, or **`aria-labelledby`** pointing at a visible **heading** / **caption** element that describes the
  visualization (e.g. “Click density heatmap for session viewport”).
- **Visible text:** **Must** include a **short** visible description (paragraph or **`<figcaption>`**-style) summarizing what
  the heatmap encodes (e.g. “Darker regions = more recorded clicks in that area of the viewport”) — **not** only tooltip copy.
- **Focus order:** **Must** include a **“Tab order (handoff):”** comment listing focusable controls in **DOM order** (e.g.
  page **Skip** link if present → **legend** / **controls** → **optional** player chrome). **If** the page ships **only**
  non-focusable static output besides global navigation, **must** document that choice and still provide **focusable**
  **skip** or **“About this demo”** disclosure control **or** link **before** any **optional** embedded player trap — pick
  one **keyboard** path that does not **strand** screen-reader users with **no** focusable landmark in the pattern’s **main**
  section.
- **Optional controls:** Toggles (**density vs points**, **reset**, **opacity**) **must** be **real** **focusable** controls
  with **visible** **`:focus`** / **`focus-visible`** styling when present.

### P-10 replayt JavaScript dependency (normative)

- **Optional player embed:** **P-10** **does not** require **`replayt.player.init`** for **Shipped** if the page’s **sole**
  teaching goal is **static** visualization from **`sessionData`**. If a **Builder** adds a **player**, all **replayt** usage
  **must** follow **published** browser APIs only (**same** boundary as **P-03** / **P-09**); list **symbols** in a header
  comment.
- **CDN pin:** If **any** **`<script src=…replayt…>`** is present, it **must** satisfy [Vanilla examples: integrator-facing replayt pins](../DESIGN_PRINCIPLES.md#vanilla-examples-integrator-facing-replayt-pins) (**`tests/test_docs_examples_replayt_pins.py`** when **Shipped**).

### P-10 File placement (normative)

- **Planned primary file:** **`docs/examples/click-heatmap-canvas.html`**. Renames **must** update this inventory row,
  **`CHANGELOG`**, **`README.md`** layout, **Playwright** shipped list (when applicable), and **[`docs/compat.md`](../compat.md#vanilla-ui-pattern-catalog)** in the **same** change set.

### P-10 Verification intent (Builder / Tester — not phase 2)

- **Static HTML:** When **Shipped**, extend **`tests/test_examples.py`** with **light** contract markers (viewport / heatmap
  comment, **`Tab order (handoff):`**, no session **`fetch(`** on the primary path, **`aria-label`** / **`aria-labelledby`** or
  equivalent caption pattern). Add **`tests/test_docs_examples_replayt_pins.py`** coverage when a **replayt** script tag exists.
- **Playwright:** When **Shipped** as a **root** **`docs/examples/*.html`**, add the file to the **Shipped** inventory consumed
  by **`tests/playwright/test_static_html_examples_load.py`** (no **console** errors on load) — **same** policy as other **Shipped**
  vanilla examples ([Static HTML examples: browser smoke (Playwright)](../DESIGN_PRINCIPLES.md#static-html-examples-browser-smoke-playwright)).
- **Optional snapshots:** Visual regression (**Playwright** screenshots) is **optional** backlog unless **mission** / **CI**
  policy changes; **smoke** load remains the **default** gate.
- **Python:** If **non-demo** Python helpers are added under **`src/replayt_ux_showcase/`**, extend **`pytest`** / **coverage**
  per [Demo module testing and replayt integration boundaries](../DESIGN_PRINCIPLES.md#demo-module-testing-and-replayt-integration-boundaries); **heatmap math** should stay **in-page** unless there is an explicit maintainer reason.

### P-10 Builder acceptance checklist (implementation)

**P-10** is **Shipped** as **`docs/examples/click-heatmap-canvas.html`**; keep the items below aligned when this pattern changes:

1. Normative sections above implemented in the **HTML/JS** (or **SVG**) snippet.
2. [Pattern inventory](#pattern-inventory) row **P-10** stays **Shipped** with the correct filename.
3. **[`docs/MISSION.md`](../MISSION.md#pattern-coverage-tracking)** vanilla count remains **7**; **[`docs/compat.md`](../compat.md#vanilla-ui-pattern-catalog)** digest lists **P-10** as **Shipped**.
4. **`CHANGELOG`** **Unreleased** records notable example or contract changes.
5. **`tests/test_examples.py`** markers; **`tests/test_docs_examples_replayt_pins.py`** when a **replayt** **`<script>`** is added; **Playwright** **Shipped** root **`*.html`** inventory updated together with any new root **`*.html`**.

---

## Backlog traceability: Click heatmap on static canvas (vanilla **P-10**)

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| **Distinct** from **P-09** (spatial density vs scrub-linked callouts) | [Relationship to P-01, P-05, P-09, and SESSION_SCHEMA](#relationship-to-p-01-p-05-p-09-and-session_schema) |
| **`click`** **`x`/`y`** + viewport mapping | [P-10 Event selection and data](#p-10-event-selection-and-data-normative), [P-10 Stage and visualization](#p-10-stage-and-visualization-normative) |
| **`SAMPLE_SESSION_DATA`** / **§1**-compatible fixture | [P-10 Event selection and data](#p-10-event-selection-and-data-normative), [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1 |
| Offline / deterministic / **LLM**-safe primary path | [Relationship to P-01, P-05, P-09, and SESSION_SCHEMA](#relationship-to-p-01-p-05-p-09-and-session_schema) |
| Accessible name + visible summary + **Tab order (handoff)** | [P-10 Accessibility and keyboard](#p-10-accessibility-and-keyboard-normative), [`keyboard-model.md`](../a11y/keyboard-model.md) |
| **replayt** pin when script present; optional player | [P-10 replayt JavaScript dependency](#p-10-replayt-javascript-dependency-normative) |
| **pytest** / **Playwright** when **Shipped** | [P-10 Verification intent](#p-10-verification-intent-builder--tester--not-phase-2) |

---

## Backlog traceability: Normalize session schema examples (Python demo ↔ **P-01**)

| Backlog acceptance criterion | Where specified |
| ---------------------------- | ---------------- |
| Canonical JSON / field names for **`SAMPLE_SESSION_DATA`** parity | [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §1–§2, [Canonical session fixture](#canonical-session-fixture-cross-surface) |
| **`basic-player.html`** placeholder + comments align with §1 | [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §3–§4 |
| **pytest** drift guard vs Python fixture | [`SESSION_SCHEMA.md`](SESSION_SCHEMA.md) §5 |
| **P-02** / **P-03** / **P-06** cross-links | [P-02 `sessionData` contract](#sessiondata-contract-compatibility-with-p-01), [P-03 time range](#sessiondata-and-events-normative), [P-06 `sessionData` and event shapes](#sessiondata-and-event-shapes-normative) |
| Design principles + **compat** digest | [`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#backlog-traceability-normalize-session-schema-examples-python-demo-and-basic-playerhtml), [`docs/compat.md`](../compat.md#vanilla-ui-pattern-catalog) |
